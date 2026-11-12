import urllib.request
import json
from bs4 import BeautifulSoup

url = 'https://www.kabum.com.br/busca/kingston-fury-beast-ddr5-32gb'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as r:
    soup = BeautifulSoup(r.read().decode('utf-8', errors='ignore'), 'html.parser')
    data = json.loads(soup.find('script', id='__NEXT_DATA__').string)
    catalog = data['props']['pageProps']['data']['catalogServer']
    prods = catalog.get('data', [])
    for p in prods[:10]:
        code = p.get('code')
        name = p.get('name')
        price = p.get('priceWithDiscount')
        available = p.get('available')
        seller = p.get('sellerName')
        slug = p.get('friendlyName', '')
        print(f"[{code}] R$ {price:.2f} | Disp: {available} | {seller} | {name}")
        print(f"   Link: https://www.kabum.com.br/produto/{code}/{slug}")
