import asyncio
import os
import re
import json
from pathlib import Path
from playwright.async_api import async_playwright
import urllib.request

# Carregar env
env_path = Path(r"c:\Users\Felipe Oliveira\.octobrain\.env")
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

SUPABASE_TOKEN = os.environ.get("SUPABASE_ACCESS_TOKEN", "")
PROJECT_REF = os.environ.get("SUPABASE_PROJECT_REF", "zwfecsnodhxbzbagdxng")

def query_supabase(sql):
    req = urllib.request.Request(
        f'https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query',
        headers={'Authorization': f'Bearer {SUPABASE_TOKEN}', 'Content-Type': 'application/json'},
        data=json.dumps({'query': sql}).encode('utf-8')
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

async def scrape_url(page, url):
    """Extrai preço PIX e parcelado da URL real"""
    print(f"\n[Scraping] {url[:80]}...")
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=25000)
        await page.wait_for_timeout(2500)
        
        # Se for KaBuM, tenta pegar o __NEXT_DATA__ primeiro
        content = await page.content()
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', content)
        if m:
            data = json.loads(m.group(1))
            prod = data.get('props', {}).get('pageProps', {}).get('product', {})
            prices = prod.get('prices', {})
            pix = prices.get('priceWithDiscount')
            parc = prices.get('price')
            if pix:
                return float(pix), float(parc or pix), prod.get('available', True)
        
        # Se for Pichau
        if 'pichau.com.br' in url:
            # Seletores específicos da Pichau
            price_el = await page.query_selector('[class*="price"]')
            body_text = await page.inner_text('body')
            # Procurar padrão de preço à vista
            # Ex: R$ 1.249,99 à vista
            m_pix = re.search(r'R\$\s*([\d\.]+,\d{2})\s*(?:à vista|no PIX)', body_text, re.IGNORECASE)
            if not m_pix:
                # busca geral
                matches = re.findall(r'R\$\s*([\d\.]+,\d{2})', body_text)
                if len(matches) >= 2:
                    val_str = matches[1].replace('.', '').replace(',', '.')
                    return float(val_str), float(val_str), True
            else:
                val_str = m_pix.group(1).replace('.', '').replace(',', '.')
                return float(val_str), float(val_str), True

        # Se for Terabyte
        if 'terabyteshop.com.br' in url:
            val_el = await page.query_selector('.val-prod, #val-prod')
            if val_el:
                txt = await val_el.inner_text()
                m_val = re.search(r'([\d\.]+,\d{2})', txt)
                if m_val:
                    val_str = m_val.group(1).replace('.', '').replace(',', '.')
                    return float(val_str), float(val_str), True

        # Fallback genérico de preços
        body_text = await page.inner_text('body')
        matches = re.findall(r'R\$\s*([\d\.]+,\d{2})', body_text)
        if matches:
            val_str = matches[0].replace('.', '').replace(',', '.')
            return float(val_str), float(val_str), True

    except Exception as e:
        print(f"  Erro ao raspar {url}: {e}")
    return None, None, False

async def main():
    print("=== INICIANDO AUDITORIA COM NAVEGADOR REAL (PLAYWRIGHT) ===")
    
    # 1. Monitor
    urls_to_test = [
        ("monitor-asus-tuf-27", "Pichau", "https://www.pichau.com.br/monitor-gamer-asus-tuf-gaming-27-pol-fast-ips-qhd-0-3ms-255hz-elmb-sync-hdmi-dp-vg27aqme5f"),
        ("monitor-asus-tuf-27", "Terabyte", "https://www.terabyteshop.com.br/produto/42016/monitor-gamer-asus-tuf-gaming-vg27aqme5f-27-pol-quad-hd-255hz-fast-ips-03ms-g-syncfreesync-hdmidp"),
        ("monitor-asus-tuf-27", "KaBuM!", "https://www.kabum.com.br/produto/1017203/monitor-gamer-asus-tuf-27-qhd-255hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aqme5f"),
        ("gpu-rtx-5070", "Terabyte", "https://www.terabyteshop.com.br/produto/34407/placa-de-video-gigabyte-nvidia-geforce-rtx-5070-gaming-oc-12gb-gddr7-dlss-ray-tracing-gv-n5070gaming-oc-12gd"),
        ("placa-mae-b650em", "Terabyte", "https://www.terabyteshop.com.br/produto/23471/placa-mae-asus-tuf-gaming-b650m-plus-wifi-chipset-b650-amd-am5-matx-ddr5-90mb1lu0-m0eay0"),
        ("ssd-lexar-nm790-1tb", "Pichau", "https://www.pichau.com.br/ssd-lexar-nm790-1tb-m-2-2280-pcie-nvme-leitura-7400mb-s-gravacao-6500mb-s-lnm790x001t-rnnng"),
        ("cpu-ryzen-7800x3d", "KaBuM!", "https://www.kabum.com.br/produto/426262/processador-amd-ryzen-7-7800x3d-4-2ghz-5-0ghz-max-turbo-cache-104mb-8-nucleos-16-threads-am5-com-video-integrado-100-100000910wof"),
        ("fonte-msi-mag-850w", "KaBuM!", "https://www.kabum.com.br/produto/592338/fonte-msi-mag-a850gl-pcie5-850w-80-plus-gold-modular-pfc-ativo-preto"),
        ("cooler-corsair-nautilus-360", "KaBuM!", "https://www.kabum.com.br/produto/998245/water-cooler-corsair-nautilus-360-argb-360mm-amd-e-intel-preto-cw-9060093-ww"),
        ("ram-corsair-vengeance-32gb", "KaBuM!", "https://www.kabum.com.br/produto/1074524/memoria-ram-corsair-vengeance-rgb-32gb-2x16gb-6000mhz-ddr5-cl38-cinza-cmh32gx5m2d6000z38"),
    ]
    
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled', '--no-sandbox'])
        context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', locale='pt-BR')
        page = await context.new_page()
        
        for peca_id, loja, url in urls_to_test:
            pix, parc, avail = await scrape_url(page, url)
            print(f"-> {peca_id} na {loja}: PIX = R$ {pix} | Parcelado = R$ {parc} | Disp = {avail}")
            results.append((peca_id, loja, pix, parc, avail, url))
            
        await browser.close()
        
    print("\n=== RESUMO COMPLETO DOS PREÇOS REAIS EXTRAÍDOS DA PÁGINA ===")
    for r in results:
        print(r)

if __name__ == '__main__':
    asyncio.run(main())
