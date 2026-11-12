import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9',
}

pichau_urls = {
    'ssd': 'https://www.pichau.com.br/ssd-lexar-nm790-1tb-m-2-2280-pcie-nvme-leitura-7400mb-s-gravacao-6500mb-s-lnm790x001t-rnnng',
    'gpu': 'https://www.pichau.com.br/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192-bit-gv-n5070gaming-oc-12gd',
    'cpu': 'https://www.pichau.com.br/processador-amd-ryzen-7-7800x3d-8-core-16-threads-4-2ghz-5-0ghz-turbo-cache-104mb-am5-100-100000910wof',
    'mobo': 'https://www.pichau.com.br/placa-mae-asus-tuf-gaming-b650m-plus-wifi-ddr5-socket-am5-m-atx-chipset-amd-b650-tuf-gaming-b650m-plus-wifi'
}

for name, url in pichau_urls.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
            if m:
                data = json.loads(m.group(1))
                pp = data.get('props', {}).get('pageProps', {})
                print(f"[Pichau {name}] NEXT_DATA keys: {list(pp.keys())}")
                # check for product / initialData
                prod = pp.get('product') or pp.get('initialData', {}).get('product') or {}
                if prod:
                    print(f"  Name: {prod.get('name') or prod.get('title')}")
                    print(f"  Price info: {prod.get('price') or prod.get('prices') or prod.get('final_price')}")
            else:
                prices = re.findall(r'R\$\s*[\d\.]+(?:,\d{2})?', html)
                print(f"[Pichau {name}] Prices in HTML: {prices[:4]}")
    except Exception as e:
        print(f"[Pichau {name}] Erro: {e}")
