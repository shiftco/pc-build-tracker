import os
import re
import sys
import json
import asyncio
import urllib.request
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
from bot.telegram_bot import TelegramAlertBot

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Carrega variáveis do .env do workspace (se disponível)
for env_candidate in [
    Path(__file__).parent / ".env",
    Path(r"c:\Users\Felipe Oliveira\.octobrain\.env"),
]:
    if env_candidate.exists():
        for line in env_candidate.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

SUPABASE_TOKEN = os.environ.get("SUPABASE_ACCESS_TOKEN", "")
PROJECT_REF = os.environ.get("SUPABASE_PROJECT_REF", "zwfecsnodhxbzbagdxng")


def query_supabase(sql: str):
    if not SUPABASE_TOKEN:
        raise RuntimeError("SUPABASE_ACCESS_TOKEN não configurado no ambiente.")
    req = urllib.request.Request(
        f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query",
        headers={
            "Authorization": f"Bearer {SUPABASE_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "curl/8.0",
        },
        data=json.dumps({"query": sql}).encode("utf-8"),
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_brl_number(raw: str) -> float:
    return float(raw.replace(".", "").replace(",", "."))


async def scrape_offer_live(browser, peca_id: str, loja: str, url: str):
    """
    Raspa preço PIX, parcelado e disponibilidade diretamente do DOM / __NEXT_DATA__ da loja.
    Usa contexto isolado por loja para evitar bloqueios em sequência.
    """
    ctx = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 900},
        locale="pt-BR",
    )
    page = await ctx.new_page()
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3500)
        title = (await page.title()).strip()
        html = await page.content()

        if "kabum.com.br" in url:
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
            if not m:
                return None, None, None
            prod = json.loads(m.group(1)).get("props", {}).get("pageProps", {}).get("product", {})
            prices = prod.get("prices", {})
            pix = prices.get("priceWithDiscount") or prices.get("price")
            parc = prices.get("price") or pix
            avail = bool(prod.get("available", False))
            if pix:
                return float(pix), float(parc), avail

        elif "pichau.com.br" in url:
            if "404" in title or "manuten" in title.lower() or "moment" in title.lower():
                await page.wait_for_timeout(3000)
                title = (await page.title()).strip()
                if "404" in title or "manuten" in title.lower() or "moment" in title.lower():
                    return None, None, None
            body = await page.inner_text("body")
            esgotado = any(w in body.upper() for w in ["PRODUTO INDISPON", "ESGOTADO", "AVISE-ME"])
            m_pix = re.search(r"à vista\s*R\$\s*([\d\.]+,\d{2})|de\s*R\$\s*[\d\.]+,\d{2}\s*por:\s*à vista\s*R\$\s*([\d\.]+,\d{2})", body, re.I)
            all_prices = re.findall(r"R\$\s*([\d\.]+,\d{2})", body)
            if esgotado:
                return None, None, False
            if m_pix:
                pix_str = m_pix.group(1) or m_pix.group(2)
                pix = parse_brl_number(pix_str)
                # Procura valor parcelado logo após
                m_parc = re.search(r"R\$\s*([\d\.]+,\d{2})\s*em até", body, re.I)
                parc = parse_brl_number(m_parc.group(1)) if m_parc else pix
                return pix, parc, True
            elif len(all_prices) >= 2:
                # Pichau geralmente lista [preco_de, preco_pix, preco_parcelado, valor_parcela]
                pix = parse_brl_number(all_prices[1])
                parc = parse_brl_number(all_prices[2]) if len(all_prices) >= 3 else pix
                return pix, parc, True

    except Exception as e:
        print(f"  [Scraper] Erro em {peca_id} ({loja}): {e}")
    finally:
        await ctx.close()

    return None, None, None


def sql_escape(val: str) -> str:
    return val.replace("'", "''")


def update_offer(peca: dict, oferta_antiga: dict, novo_preco_pix: float, novo_preco_parcelado: float, disponivel: bool, telegram: TelegramAlertBot):
    """Atualiza oferta no Supabase, registra histórico e dispara Telegram em queda real."""
    peca_id = sql_escape(peca["id"])
    loja = sql_escape(oferta_antiga["loja"])
    url_final = oferta_antiga["url_produto"]
    preco_antigo = float(oferta_antiga["preco_pix"]) if oferta_antiga.get("preco_pix") is not None else None

    query_supabase(f"""
        INSERT INTO pc_historico_precos (peca_id, loja, preco_pix, data_hora)
        VALUES ('{peca_id}', '{loja}', {novo_preco_pix}, NOW());
    """)

    query_supabase(f"""
        UPDATE pc_ofertas
        SET preco_pix = {novo_preco_pix},
            preco_parcelado = {novo_preco_parcelado},
            disponivel = {'TRUE' if disponivel else 'FALSE'},
            ultima_checagem = NOW()
        WHERE peca_id = '{peca_id}' AND loja = '{loja}';
    """)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] {peca['nome']} | {oferta_antiga['loja']}: R$ {novo_preco_pix:.2f} (Disp={disponivel})")

    if disponivel and preco_antigo and novo_preco_pix < preco_antigo - 0.5:
        print(f"  🔥 QUEDA DETECTADA! De R$ {preco_antigo:.2f} -> R$ {novo_preco_pix:.2f}")
        telegram.send_price_drop_alert(
            peca_nome=peca["nome"],
            loja=oferta_antiga["loja"],
            preco_antigo=preco_antigo,
            preco_novo=novo_preco_pix,
            url_produto=url_final,
        )
    elif disponivel and peca.get("preco_alvo") and novo_preco_pix <= float(peca["preco_alvo"]):
        print(f"  🎯 META ATINGIDA! R$ {novo_preco_pix:.2f} <= Alvo R$ {peca['preco_alvo']}")


async def run_tracker_cycle():
    print("\n==========================================")
    print(f"🚀 INICIANDO CICLO REAL DE MONITORAMENTO - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("==========================================")

    pecas = query_supabase("SELECT id, nome, preco_referencia, preco_alvo FROM pc_pecas ORDER BY ordem;")
    ofertas = query_supabase("SELECT peca_id, loja, preco_pix, preco_parcelado, disponivel, url_produto FROM pc_ofertas ORDER BY peca_id, preco_pix;")
    peca_map = {p["id"]: p for p in pecas}
    telegram = TelegramAlertBot()

    print(f"Peças ativas no radar: {len(pecas)} | Ofertas monitoradas: {len(ofertas)}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
        )
        for of in ofertas:
            peca = peca_map.get(of["peca_id"])
            if not peca:
                continue
            pix, parc, avail = await scrape_offer_live(browser, of["peca_id"], of["loja"], of["url_produto"])
            if pix is not None and avail is not None:
                update_offer(peca, of, pix, parc or pix, avail, telegram)
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Mantendo último valor em cache para {of['peca_id']} | {of['loja']} (indisponível/anti-bot no momento)")
        await browser.close()

    # Recalcula menor preço disponível por peça e atualiza pc_pecas.preco_referencia
    query_supabase("""
        UPDATE pc_pecas p
        SET preco_referencia = COALESCE((
            SELECT MIN(o.preco_pix)
            FROM pc_ofertas o
            WHERE o.peca_id = p.id AND o.disponivel = TRUE
        ), p.preco_referencia);
    """)

    print("\n✅ Ciclo concluído e sincronizado com o Supabase!")


if __name__ == "__main__":
    asyncio.run(run_tracker_cycle())
