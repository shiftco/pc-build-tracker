import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9',
}

urls = {
    'monitor_kabum': 'https://www.kabum.com.br/produto/1017203/monitor-gamer-asus-tuf-27-qhd-255hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aqme5f',
    'cpu_kabum': 'https://www.kabum.com.br/produto/426262/processador-amd-ryzen-7-7800x3d-4-2ghz-5-0ghz-max-turbo-cache-104mb-8-nucleos-16-threads-am5-com-video-integrado-100-100000910wof',
    'gpu_terabyte': 'https://www.terabyteshop.com.br/produto/34407/placa-de-video-gigabyte-nvidia-geforce-rtx-5070-gaming-oc-12gb-gddr7-dlss-ray-tracing-gv-n5070gaming-oc-12gd',
    'gpu_kabum': 'https://www.kabum.com.br/produto/754152/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192-bits-gv-n5070gaming-oc-12gd',
    'ram_kabum': 'https://www.kabum.com.br/produto/1074524/memoria-ram-corsair-vengeance-rgb-32gb-2x16gb-6000mhz-ddr5-cl38-cinza-cmh32gx5m2d6000z38',
    'psu_kabum': 'https://www.kabum.com.br/produto/592338/fonte-msi-mag-a850gl-pcie5-850w-80-plus-gold-modular-pfc-ativo-preto',
    'cooler_kabum': 'https://www.kabum.com.br/produto/998245/water-cooler-corsair-nautilus-360-argb-360mm-amd-e-intel-preto-cw-9060093-ww',
    'mobo_terabyte': 'https://www.terabyteshop.com.br/produto/23471/placa-mae-asus-tuf-gaming-b650m-plus-wifi-chipset-b650-amd-am5-matx-ddr5-90mb1lu0-m0eay0',
    'mobo_kabum': 'https://www.kabum.com.br/produto/871302/placa-mae-asus-tuf-b650em-plus-amd-am5-m-atx-ddr5-wifi-6e-bluetooth-preto-90mb1lu0',
}

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
            if m:
                data = json.loads(m.group(1))
                page_props = data.get('props', {}).get('pageProps', {})
                product_data = page_props.get('productData', {}) or page_props.get('initialData', {}).get('product', {})
                print(f"=== {name} (KABUM NEXT_DATA) ===")
                print(f"  Title: {product_data.get('name')}")
                print(f"  Price: {product_data.get('price')}")
                print(f"  PriceWithDiscount: {product_data.get('priceWithDiscount')}")
                print(f"  RegularPrice: {product_data.get('regularPrice')}")
                print(f"  Discount: {product_data.get('discount')}")
                print(f"  Available: {product_data.get('available')}")
                offers = product_data.get('offer', {}) or product_data.get('offers', {})
                if offers:
                    print(f"  Offer details: {offers}")
            else:
                # Terabyte or other
                prices = re.findall(r'R\$\s*[\d\.]+(?:,\d{2})?', html)
                print(f"=== {name} (HTML) ===")
                print(f"  Prices found: {prices[:6]}")
    except Exception as e:
        print(f"=== {name} === ERROR: {e}")
