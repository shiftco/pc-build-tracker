import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9',
}

url = 'https://www.kabum.com.br/produto/1017203/monitor-gamer-asus-tuf-27-qhd-255hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aqme5f'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    if m:
        data = json.loads(m.group(1))
        prod = data.get('props', {}).get('pageProps', {}).get('product', {})
        print("Product Title:", prod.get('title'))
        print("Product Available:", prod.get('available'))
        print("Product Price Details:")
        for k, v in prod.items():
            if 'price' in k.lower() or 'valor' in k.lower() or 'offer' in k.lower():
                print(f"  {k}: {v}")
