import asyncio
from playwright.async_api import async_playwright
import re

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled', '--no-sandbox'])
        context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        page = await context.new_page()
        
        urls = [
            ("gpu", "https://www.terabyteshop.com.br/produto/34407/placa-de-video-gigabyte-nvidia-geforce-rtx-5070-gaming-oc-12gb-gddr7-dlss-ray-tracing-gv-n5070gaming-oc-12gd"),
            ("mobo", "https://www.terabyteshop.com.br/produto/23471/placa-mae-asus-tuf-gaming-b650m-plus-wifi-chipset-b650-amd-am5-matx-ddr5-90mb1lu0-m0eay0"),
            ("ssd", "https://www.pichau.com.br/ssd-lexar-nm790-1tb-m-2-2280-pcie-nvme-leitura-7400mb-s-gravacao-6500mb-s-lnm790x001t-rnnng")
        ]
        
        for name, url in urls:
            try:
                await page.goto(url, wait_until='domcontentloaded', timeout=25000)
                await page.wait_for_timeout(3000)
                title = await page.title()
                body = await page.inner_text('body')
                prices = re.findall(r'R\$\s*[\d\.]+(?:,\d{2})?', body)
                print(f"[{name}] Title: {title[:60]}")
                print(f"[{name}] Prices in body: {prices[:6]}")
            except Exception as e:
                print(f"[{name}] Erro: {e}")
        await browser.close()

asyncio.run(check())
