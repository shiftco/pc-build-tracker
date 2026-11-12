import urllib.request
import json
from bs4 import BeautifulSoup

url = 'https://www.kabum.com.br/hardware/memoria-ram/ddr-5/6000mhz'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as r:
    soup = BeautifulSoup(r.read().decode('utf-8', errors='ignore'), 'html.parser')
    data = json.loads(soup.find('script', id='__NEXT_DATA__').string)
    parsed = json.loads(data['props']['pageProps']['data'])
    prods = parsed['catalogServer'].get('data', [])
    print(f"Total produtos catalogados: {len(prods)}")
    
    in_stock_32gb = []
    for p in prods:
        code = p.get('code')
        name = p.get('name', '')
        price = p.get('priceWithDiscount', 0)
        available = p.get('available', False)
        seller = p.get('sellerName', '')
        slug = p.get('friendlyName', '')
        link = f"https://www.kabum.com.br/produto/{code}/{slug}"
        
        if available and '32gb' in name.lower():
            in_stock_32gb.append({
                'code': code,
                'name': name,
                'price': price,
                'seller': seller,
                'link': link
            })

    print(f"\nENCONTRADOS {len(in_stock_32gb)} KITS 32GB DDR5 6000MHz EM ESTOQUE:")
    for it in in_stock_32gb:
        print(f"\n[Código {it['code']}] R$ {it['price']:.2f} (Loja: {it['seller']})")
        print(f"-> Nome: {it['name']}")
        print(f"-> Link Direto: {it['link']}")
