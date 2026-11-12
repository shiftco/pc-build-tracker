import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
            ]
        )
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            viewport={'width': 1366, 'height': 768},
            locale='pt-BR',
            timezone_id='America/Sao_Paulo'
        )
        page = await context.new_page()
        url = 'https://www.pichau.com.br/monitor-gamer-asus-tuf-gaming-27-pol-fast-ips-qhd-0-3ms-255hz-elmb-sync-hdmi-dp-vg27aqme5f'
        print(f"Navegando para: {url}")
        
        try:
            await page.goto(url, wait_until='domcontentloaded', timeout=25000)
            await page.wait_for_timeout(3000)
            title = await page.title()
            print(f"Title: {title}")
            
            # Pegar texto da página
            content = await page.content()
            
            # Procurar preços no texto visível
            body_text = await page.inner_text('body')
            prices = re.findall(r'R\$\s*[\d\.]+(?:,\d{2})?', body_text)
            print(f"Preços no body: {prices[:10]}")
            
            # Procurar seletores de preço específicos da Pichau
            for sel in ['[class*="price"]', '[class*="preco"]', '[data-price]', 'div:has-text("à vista")', 'div:has-text("no PIX")']:
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
