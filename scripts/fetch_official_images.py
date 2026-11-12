import urllib.request
import json
import os
from bs4 import BeautifulSoup

dest_dir = r'c:\Users\Felipe Oliveira\.octobrain\pc-tracker\web\public\images'
os.makedirs(dest_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

kabum_pages = {
    'cpu': 'https://www.kabum.com.br/produto/426262/processador-amd-ryzen-7-7800x3d-4-2ghz-5-0ghz-max-turbo-cache-104mb-8-nucleos-16-threads-am5-com-video-integrado-100-100000910wof',
    'gpu': 'https://www.kabum.com.br/produto/754152/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192-bits-gv-n5070gaming-oc-12gd',
    'motherboard': 'https://www.kabum.com.br/produto/871302/placa-mae-asus-tuf-b650em-plus-amd-am5-m-atx-ddr5-wifi-6e-bluetooth-preto-90mb1lu0',
    'ram': 'https://www.kabum.com.br/produto/1074524/memoria-ram-corsair-vengeance-rgb-32gb-2x16gb-6000mhz-ddr5-cl38-cinza-cmh32gx5m2d6000z38',
    'ssd': 'https://www.kabum.com.br/produto/597845/ssd-lexar-nm790-1tb-m-2-2280-pcie-nvme-leitura-7400-mb-s-gravacao-6500-mb-s-preto-e-cinza-lnm790x001t-rnnng',
    'psu': 'https://www.kabum.com.br/produto/592338/fonte-msi-mag-a850gl-pcie5-850w-80-plus-gold-modular-pfc-ativo-preto',
    'cooler': 'https://www.kabum.com.br/produto/998245/water-cooler-corsair-nautilus-360-argb-360mm-amd-e-intel-preto-cw-9060093-ww',
    'monitor': 'https://www.kabum.com.br/produto/1017203/monitor-gamer-asus-tuf-27-qhd-255hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aqme5f'
}

for key, page_url in kabum_pages.items():
    try:
        req = urllib.request.Request(page_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            # Tenta pegar og:image ou __NEXT_DATA__
            og_img = soup.find('meta', property='og:image')
            img_url = og_img['content'] if og_img and og_img.get('content') else None
            
            if not img_url:
                script = soup.find('script', id='__NEXT_DATA__')
                if script:
                    data = json.loads(script.string)
                    # Procura recursivamente por urls de fotos
                    text_data = json.dumps(data)
                    import re
                    matches = re.findall(r'https://images\d*\.kabum\.com\.br/produtos/fotos/[^\"]+_(?:gg|g|original)\.jpg', text_data)
                    if matches:
                        img_url = matches[0]

            print(f"{key}: img_url = {img_url}")
            if img_url:
                img_req = urllib.request.Request(img_url, headers=headers)
                raw_path = os.path.join(dest_dir, f"{key}_raw.jpg")
                with urllib.request.urlopen(img_req, timeout=15) as ir, open(raw_path, 'wb') as out:
                    out.write(ir.read())
                print(f"   -> Baixado {raw_path} ({os.path.getsize(raw_path)} bytes)")
    except Exception as e:
        print(f"Erro em {key}: {e}")
