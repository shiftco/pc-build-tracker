import os
import re
import sys
import json
import asyncio
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
from bot.telegram_bot import TelegramAlertBot

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

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

# Regras de Validação Anti-Redirect, Anti-Esgotado, Teto de Sanidade e Auto-Substituição
CATALOG_RULES = {
    "cpu-ryzen-7800x3d": {
        "must_match": ["7800x3d"],
        "must_not_match": ["5800x3d", "9800x3d", "kit upgrade", "pc gamer", "computador"],
        "min_price": 1200,
        "max_price": 3200,
        "query": "Ryzen 7 7800X3D",
        "kabum_slug": "processador-amd-ryzen-7-7800x3d",
    },
    "gpu-rtx-5070": {
        "must_match": ["5070", "gigabyte"],
        "must_not_match": ["5070 ti", "5070ti", "notebook", "pc gamer", "computador", "open box", "cadeira", "gabinete"],
        "min_price": 4200,
        "max_price": 7500,
        "query": "RTX 5070 Gigabyte",
        "kabum_slug": "rtx-5070-gigabyte",
    },
    "placa-mae-b650em": {
        "must_match": ["asus", "tuf", "b650"],
        "must_not_match": ["kit upgrade", "pc gamer", "computador", "b550", "open box"],
        "min_price": 900,
        "max_price": 2400,
        "query": "Asus TUF B650EM-Plus",
        "kabum_slug": "placa-mae-asus-tuf-b650",
    },
    "ram-corsair-vengeance-32gb": {
        "must_match": ["corsair", "vengeance", "rgb", "32gb", "6000"],
        "must_not_match": ["1x16gb", "16gb (1x16gb)", "ddr4", "notebook"],
        "min_price": 1000,
        "max_price": 5800,
        "query": "CMH32GX5M2D6000Z38",
        "kabum_slug": "cmh32gx5m2d6000z38",
    },
    "ram-corsair-vengeance-32gb-sem-rgb": {
        "must_match": ["corsair", "vengeance", "32gb", "6000"],
        "must_not_match": ["rgb", "1x16gb", "16gb (1x16gb)", "ddr4", "notebook"],
        "min_price": 1000,
        "max_price": 5800,
        "query": "CMK32GX5M2D6000Z38",
        "kabum_slug": "cmk32gx5m2d6000z38",
    },
    "ram-corsair-vengeance-rgb-16gb": {
        "must_match": ["corsair", "vengeance", "rgb", "16gb", "6000"],
        "must_not_match": ["32gb", "2x16gb", "ddr4", "notebook"],
        "min_price": 600,
        "max_price": 3400,
        "query": "CMH16GX5M1D6000Z38",
        "kabum_slug": "cmh16gx5m1d6000z38",
    },
    "ssd-lexar-nm790-1tb": {
        "must_match": ["nvme"],
        "must_not_match": ["250gb", "256gb", "480gb", "500gb", "512gb", "sata", "externo", "cartao"],
        "min_price": 450,
        "max_price": 1900,
        "query": "SSD 1TB NVMe PCIe 4.0",
        "kabum_slug": "ssd-kingston-nv3-1tb",
    },
    "fonte-msi-mag-850w": {
        "must_match": ["msi", "850w"],
        "must_not_match": ["550w", "600w", "650w", "750w"],
        "min_price": 400,
        "max_price": 1200,
        "query": "MSI MAG A850GL",
        "kabum_slug": "fonte-msi-mag-a850gl-850w",
    },
    "cooler-corsair-nautilus-360": {
        "must_match": ["corsair", "nautilus", "360"],
        "must_not_match": ["240mm", "120mm"],
        "min_price": 300,
        "max_price": 1100,
        "query": "Corsair Nautilus 360",
        "kabum_slug": "water-cooler-corsair-nautilus-360",
    },
    "monitor-asus-tuf-27": {
        "must_match": ["asus", "tuf", "27"],
        "must_not_match": ["24 pol", "23.8", "suporte"],
        "min_price": 900,
        "max_price": 2200,
        "query": "VG27AQME5F",
        "kabum_slug": "vg27aqme5f",
    },
}


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


def matches_rule(title: str, rule: dict) -> bool:
    if not title or not rule:
        return False
    low = title.lower()
    for kw in rule["must_match"]:
        if kw.lower() not in low:
            return False
    for bad in rule["must_not_match"]:
        if bad.lower() in low:
            return False
    return True


def is_broken_redirect(final_url: str) -> bool:
    u = (final_url or "").lower()
    return any(
        bad in u
        for bad in ["/open-box", "/kit-upgrade", "/busca", "404"]
    ) or u.rstrip("/") in (
        "https://www.kabum.com.br",
        "https://www.pichau.com.br",
        "https://www.terabyteshop.com.br",
    )


async def auto_heal_store_offer(browser, peca_id: str, loja: str, rule: dict):
    """Procura automaticamente um novo link ativo na mesma loja caso o link anterior tenha quebrado ou esgotado."""
    ctx = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 900},
        locale="pt-BR",
    )
    page = await ctx.new_page()
    await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    try:
        loja_low = loja.lower()
        if "kabum" in loja_low:
            url = f"https://www.kabum.com.br/busca/{urllib.parse.quote(rule['kabum_slug'])}"
            await page.goto(url, wait_until="domcontentloaded", timeout=25000)
            html = await page.content()
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
            if m:
                raw = json.loads(m.group(1)).get("props", {}).get("pageProps", {}).get("data", {})
                d2 = json.loads(raw) if isinstance(raw, str) else raw
                items = d2.get("catalogServer", {}).get("data", [])
                valid = [
                    it for it in items
                    if it.get("available")
                    and matches_rule(it.get("name", ""), rule)
                    and rule["min_price"] <= float(it.get("priceWithDiscount") or it.get("price") or 0) <= rule["max_price"]
                ]
                valid.sort(key=lambda x: float(x.get("priceWithDiscount") or x.get("price")))
                if valid:
                    best = valid[0]
                    slug = best.get("friendlyName") or str(best["code"])
                    return (
                        float(best.get("priceWithDiscount") or best.get("price")),
                        float(best.get("price") or best.get("priceWithDiscount")),
                        True,
                        f"https://www.kabum.com.br/produto/{best['code']}/{slug}",
                    )
        elif "terabyte" in loja_low:
            url = f"https://www.terabyteshop.com.br/busca?str={urllib.parse.quote(rule['query'])}"
            await page.goto(url, wait_until="domcontentloaded", timeout=25000)
            await page.wait_for_timeout(3500)
            items = await page.evaluate("""() => {
                return Array.from(document.querySelectorAll('.product-item, .pbox')).map(c => ({
                    name: c.querySelector('.product-item__name, h2, a.prod-name')?.innerText?.trim() || '',
                    price: c.querySelector('.product-item__new-price, .prod-new-price')?.innerText?.trim() || '',
                    href: c.querySelector('a')?.href || '',
                    esgotado: /esgotado|indispon/i.test(c.innerText)
                })).filter(x => x.name && x.href && !x.esgotado);
            }""")
            candidates = []
            for it in items:
                m_pr = re.search(r"([\d\.]+,\d{2})", it["price"])
                if not m_pr:
                    continue
                pix = parse_brl_number(m_pr.group(1))
                if matches_rule(it["name"], rule) and rule["min_price"] <= pix <= rule["max_price"]:
                    candidates.append((pix, round(pix / 0.85, 2), True, it["href"]))
            candidates.sort(key=lambda x: x[0])
            if candidates:
                return candidates[0]
    except Exception as e:
        print(f"  [Auto-Heal] Erro ao buscar substituto para {peca_id} em {loja}: {e}")
    finally:
        await ctx.close()
    return None


async def scrape_and_validate_offer(browser, peca_id: str, loja: str, url: str):
    """
    Valida se o link não redirecionou, se o título confere com a peça, se há estoque
    e se o preço está dentro do teto de sanidade. Caso contrário, aciona Auto-Heal.
    """
    rule = CATALOG_RULES.get(peca_id)
    ctx = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 900},
        locale="pt-BR",
    )
    page = await ctx.new_page()
    await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3200)
        final_url = page.url
        title = (await page.title()).strip()
        html = await page.content()

        # Trava 1: Anti-Redirect
        if is_broken_redirect(final_url):
            print(f"  ⚠️ [Redirect Detectado] {peca_id} ({loja}) redirecionou para {final_url}. Buscando novo link ativo...")
            if rule:
                healed = await auto_heal_store_offer(browser, peca_id, loja, rule)
                if healed:
                    return healed
            return None, None, False, url

        if "kabum.com.br" in url:
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
            if m:
                prod = json.loads(m.group(1)).get("props", {}).get("pageProps", {}).get("product", {})
                prod_title = prod.get("title") or title
                prices = prod.get("prices", {})
                pix = float(prices.get("priceWithDiscount") or prices.get("price") or 0)
                parc = float(prices.get("price") or pix)
                avail = bool(prod.get("available", False))

                if not avail or (rule and (not matches_rule(prod_title, rule) or not (rule["min_price"] <= pix <= rule["max_price"]))):
                    print(f"  ⚠️ [Link Inválido/Esgotado/Ágio] {peca_id} ({loja}): avail={avail}, pix={pix}. Acionando Auto-Heal...")
                    if rule:
                        healed = await auto_heal_store_offer(browser, peca_id, loja, rule)
                        if healed:
                            return healed
                    return None, None, False, url
                return pix, parc, True, final_url

        elif "pichau.com.br" in url:
            if "404" in title:
                return None, None, False, url
            if "manuten" in title.lower() or "moment" in title.lower():
                return None, None, None, url
            body = await page.inner_text("body")
            esgotado = any(w in body.upper() for w in ["PRODUTO INDISPON", "ESGOTADO", "AVISE-ME"])
            if esgotado or (rule and not matches_rule(title, rule)):
                return None, None, False, url
            all_prices = re.findall(r"R\$\s*([\d\.]+,\d{2})", body)
            if len(all_prices) >= 2:
                pix = parse_brl_number(all_prices[1])
                parc = parse_brl_number(all_prices[2]) if len(all_prices) >= 3 else pix
                if rule and not (rule["min_price"] <= pix <= rule["max_price"]):
                    return None, None, False, url
                return pix, parc, True, final_url

        elif "terabyteshop.com.br" in url:
            if "moment" in title.lower():
                return None, None, None, url
            body = await page.inner_text("body")
            esgotado = any(w in body.upper() for w in ["PRODUTO INDISPON", "ESGOTADO", "AVISE-ME"])
            val_el = await page.query_selector(".val-prod, #val-prod")
            val_txt = (await val_el.inner_text()).strip() if val_el else ""
            m_val = re.search(r"([\d\.]+,\d{2})", val_txt)
            if esgotado or not m_val or (rule and not matches_rule(title, rule)):
                if rule:
                    healed = await auto_heal_store_offer(browser, peca_id, loja, rule)
                    if healed:
                        return healed
                return None, None, False, url
            pix = parse_brl_number(m_val.group(1))
            all_prices = re.findall(r"R\$\s*([\d\.]+,\d{2})", body)
            parc = parse_brl_number(all_prices[4]) if len(all_prices) >= 5 else round(pix / 0.85, 2)
            if rule and not (rule["min_price"] <= pix <= rule["max_price"]):
                return None, None, False, url
            return pix, parc, True, final_url

    except Exception as e:
        print(f"  [Scraper] Erro em {peca_id} ({loja}): {e}")
    finally:
        await ctx.close()

    return None, None, None, url


def sql_escape(val: str) -> str:
    return (val or "").replace("'", "''")


def update_offer(peca: dict, oferta_antiga: dict, novo_preco_pix: float, novo_preco_parcelado: float, disponivel: bool, nova_url: str, telegram: TelegramAlertBot):
    peca_id = sql_escape(peca["id"])
    loja = sql_escape(oferta_antiga["loja"])
    url_escaped = sql_escape(nova_url or oferta_antiga["url_produto"])

    if not disponivel:
        query_supabase(f"""
            UPDATE pc_ofertas
            SET disponivel = FALSE, ultima_checagem = NOW()
            WHERE peca_id = '{peca_id}' AND loja = '{loja}';
        """)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ {peca['nome']} | {oferta_antiga['loja']} marcado como INDISPONÍVEL e ocultado do dashboard.")
        return

    preco_antigo = float(oferta_antiga["preco_pix"]) if oferta_antiga.get("preco_pix") is not None else None

    query_supabase(f"""
        INSERT INTO pc_historico_precos (peca_id, loja, preco_pix, data_hora)
        VALUES ('{peca_id}', '{loja}', {novo_preco_pix}, NOW());
    """)

    query_supabase(f"""
        UPDATE pc_ofertas
        SET preco_pix = {novo_preco_pix},
            preco_parcelado = {novo_preco_parcelado},
            url_produto = '{url_escaped}',
            disponivel = TRUE,
            ultima_checagem = NOW()
        WHERE peca_id = '{peca_id}' AND loja = '{loja}';
    """)

    healed_tag = " [LINK AUTO-CORRIGIDO]" if nova_url != oferta_antiga["url_produto"] else ""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ {peca['nome']} | {oferta_antiga['loja']}: R$ {novo_preco_pix:.2f}{healed_tag}")

    if preco_antigo and novo_preco_pix < preco_antigo - 0.5:
        print(f"  🔥 QUEDA DETECTADA! De R$ {preco_antigo:.2f} -> R$ {novo_preco_pix:.2f}")
        telegram.send_price_drop_alert(
            peca_nome=peca["nome"],
            loja=oferta_antiga["loja"],
            preco_antigo=preco_antigo,
            preco_novo=novo_preco_pix,
            url_produto=nova_url,
        )


async def run_tracker_cycle():
    print("\n==========================================")
    print(f"🚀 INICIANDO CICLO REAL DE MONITORAMENTO & AUTO-HEAL - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("==========================================")

    pecas = query_supabase("SELECT id, nome, preco_referencia, preco_alvo FROM pc_pecas ORDER BY ordem;")
    ofertas = query_supabase("SELECT peca_id, loja, preco_pix, preco_parcelado, disponivel, url_produto FROM pc_ofertas ORDER BY peca_id, preco_pix;")
    peca_map = {p["id"]: p for p in pecas}
    telegram = TelegramAlertBot()

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    launch_kwargs = {
        "headless": True,
        "args": ["--disable-blink-features=AutomationControlled", "--no-sandbox"],
    }
    if os.path.exists(chrome_path):
        launch_kwargs["executable_path"] = chrome_path

    async with async_playwright() as p:
        browser = await p.chromium.launch(**launch_kwargs)
        for of in ofertas:
            peca = peca_map.get(of["peca_id"])
            if not peca:
                continue
            pix, parc, avail, final_url = await scrape_and_validate_offer(
                browser, of["peca_id"], of["loja"], of["url_produto"]
            )
            if avail is False:
                update_offer(peca, of, float(of["preco_pix"]), float(of["preco_parcelado"] or of["preco_pix"]), False, final_url, telegram)
            elif pix is not None and avail is True:
                update_offer(peca, of, pix, parc or pix, True, final_url, telegram)
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Mantendo último valor validado para {of['peca_id']} | {of['loja']}")
        await browser.close()

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
