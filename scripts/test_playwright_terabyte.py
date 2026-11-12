import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
        )
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            viewport={'width': 1366, 'height': 768},
            locale='pt-BR'
        )
        page = await context.new_page()
        url = 'https://www.terabyteshop.com.br/produto/42016/monitor-gamer-asus-tuf-gaming-vg27aqme5f-27-pol-quad-hd-255hz-fast-ips-03ms-g-syncfreesync-hdmidp'
        print(f"Navegando para Terabyte: {url}")
        
        try:
            await page.goto(url, wait_until='domcontentloaded', timeout=25000)
            await page.wait_for_timeout(3000)
            title = await page.title()
            print(f"Title: {title}")
            
            body_text = await page.inner_text('body')
            prices = re.findall(r'R\$\s*[\d\.]+(?:,\d{2})?', body_text)
            print(f"Preços no body Terabyte: {prices[:10]}")
            
            for sel in ['#val-prod', '.val-prod', '[class*="price"]', '[class*="preco"]']:
                els = await page.query_selector_all(sel)
                for el in els[:3]:
                    txt = (await el.inner_text()).strip().replace('\n', ' ')
                    if 'R$' in txt:
                        print(f"  Selector {sel}: {txt[:100]}")
                        
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            await browser.close()

asyncio.run(main())
