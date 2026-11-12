import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9',
}

kabum_products = {
    'cpu-ryzen-7800x3d': 426262,
    'gpu-rtx-5070': 754152,
    'placa-mae-b650em': 871302,
    'ram-corsair-vengeance-32gb': 1074524,
    'ssd-kingston-nv3': 621162,
    'fonte-msi-mag-850w': 592338,
    'cooler-corsair-nautilus-360': 998245,
    'monitor-asus-tuf-27': 1017203,
}

print("=== AUDITANDO PREÇOS REAIS AO VIVO NA KABUM ===")
for pid, code in kabum_products.items():
    url = f"https://www.kabum.com.br/produto/{code}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
            if m:
                data = json.loads(m.group(1))
                prod = data.get('props', {}).get('pageProps', {}).get('product', {})
                title = prod.get('title')
                available = prod.get('available')
                prices = prod.get('prices', {})
                pix = prices.get('priceWithDiscount')
                parcelado = prices.get('price')
                print(f"[{pid}] (Código {code})")
                print(f"  Nome: {title}")
                print(f"  Disponível: {available}")
                print(f"  Preço PIX: R$ {pix}")
                print(f"  Preço Parcelado: R$ {parcelado}")
            else:
                print(f"[{pid}] NEXT_DATA não encontrado")
    except Exception as e:
        print(f"[{pid}] Erro: {e}")
