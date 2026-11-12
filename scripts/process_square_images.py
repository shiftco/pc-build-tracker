import urllib.request
import os
from PIL import Image, ImageChops

dest_dir = r'c:\Users\Felipe Oliveira\.octobrain\pc-tracker\web\public\images'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

high_res_urls = {
    'cpu': [
        'https://images.kabum.com.br/produtos/fotos/426262/processador-amd-ryzen-7-7800x3d-5-0ghz-max-turbo-cache-104mb-am5-8-nucleos-video-integrado-100-100000910wof_1680784502_gg.jpg',
        'https://images.kabum.com.br/produtos/fotos/426262/processador-amd-ryzen-7-7800x3d-5-0ghz-max-turbo-cache-104mb-am5-8-nucleos-video-integrado-100-100000910wof_1680784502_g.jpg',
    ],
    'gpu': [
        'https://images.kabum.com.br/produtos/fotos/sync_mirakl/754152/xlarge/Placa-De-Video-Gigabyte-Geforce-RTX-5070-Gaming-Oc-12gb-Gddr7-192-Bits-Gv-n5070gaming-Oc-12gd_1794488022.png',
        'https://images.kabum.com.br/produtos/fotos/sync_mirakl/754152/large/Placa-De-Video-Gigabyte-Geforce-RTX-5070-Gaming-Oc-12gb-Gddr7-192-Bits-Gv-n5070gaming-Oc-12gd_1794488022.png',
    ],
    'motherboard': [
        'https://images.kabum.com.br/produtos/fotos/871302/placa-mae-asus-tuf-b650em-plus-amd-am5-m-atx-ddr5-wi-fi-7-bluetooth-preto-90mb1lu0_1751987131_gg.jpg',
        'https://images.kabum.com.br/produtos/fotos/871302/placa-mae-asus-tuf-b650em-plus-amd-am5-m-atx-ddr5-wi-fi-7-bluetooth-preto-90mb1lu0_1751987131_g.jpg',
    ],
    'ram': [
        'https://images.kabum.com.br/produtos/fotos/1074524/memoria-ram-corsair-vengeance-rgb-32gb-2x16gb-6000mhz-ddr5-cl38-cinza-cmh32gx5m2d6000z38_1793901091_gg.jpg',
        'https://images.kabum.com.br/produtos/fotos/1074524/memoria-ram-corsair-vengeance-rgb-32gb-2x16gb-6000mhz-ddr5-cl38-cinza-cmh32gx5m2d6000z38_1793901091_g.jpg',
    ],
    'ssd': [
        'https://images.kabum.com.br/produtos/fotos/597845/ssd-lexar-1tb-nm790-m-2-2280-pcie-nvme-leitura-7400-mb-s-gravacao-6500-mb-s-lnm790x001t-rnnnu_1730143249_gg.jpg',
        'https://images.kabum.com.br/produtos/fotos/597845/ssd-lexar-1tb-nm790-m-2-2280-pcie-nvme-leitura-7400-mb-s-gravacao-6500-mb-s-lnm790x001t-rnnnu_1730143249_g.jpg',
    ],
    'psu': [
        'https://images.kabum.com.br/produtos/fotos/sync_mirakl/592338/xlarge/Fonte-Msi-Mag-A850gl-PCie5-850w-80-Plus-Gold-Modular-Pfc-Ativo-Preto_1791401021.jpg',
        'https://images.kabum.com.br/produtos/fotos/sync_mirakl/592338/large/Fonte-Msi-Mag-A850gl-PCie5-850w-80-Plus-Gold-Modular-Pfc-Ativo-Preto_1791401021.jpg',
    ],
    'cooler': [
        'https://images.kabum.com.br/produtos/fotos/sync_mirakl/998245/xlarge/Water-Cooler-Corsair-Nautilus-Rs-ARGB-360mm-Pwm-Intel-amd-Preto-Cw-9060093-ww_1790621314.jpg',
        'https://images.kabum.com.br/produtos/fotos/sync_mirakl/998245/large/Water-Cooler-Corsair-Nautilus-Rs-ARGB-360mm-Pwm-Intel-amd-Preto-Cw-9060093-ww_1790621314.jpg',
    ],
    'monitor': [
        'https://images.kabum.com.br/produtos/fotos/1017203/monitor-gamer-asus-tuf-27-qhd-255hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aqme5f_1789393722_gg.jpg',
        'https://images.kabum.com.br/produtos/fotos/1017203/monitor-gamer-asus-tuf-27-qhd-255hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aqme5f_1789393722_g.jpg',
    ]
}

def trim_white_and_square(im_path, out_path, target_size=600, padding=36):
    im = Image.open(im_path)
    # Se tiver transparência (PNG), converte para fundo branco primeiro
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        bg = Image.new('RGB', im.size, (255, 255, 255))
        im_rgba = im.convert('RGBA')
        bg.paste(im_rgba, mask=im_rgba.split()[3])
        im = bg
    else:
        im = im.convert('RGB')

    # Faz auto-crop de bordas brancas excessivas para que o produto ocupe exatamente a mesma proporção em todos os cards!
    bg = Image.new('RGB', im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -20)
    bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)

    # Redimensiona mantendo proporção para caber dentro de (target_size - 2*padding)
    inner_size = target_size - (padding * 2)
    im.thumbnail((inner_size, inner_size), Image.Resampling.LANCZOS)

    # Cria canvas quadrado 600x600 branco puro e centraliza perfeitamente o produto
    square = Image.new('RGB', (target_size, target_size), (255, 255, 255))
    offset_x = (target_size - im.width) // 2
    offset_y = (target_size - im.height) // 2
    square.paste(im, (offset_x, offset_y))
    square.save(out_path, 'JPEG', quality=95)
    print(f"   -> Padronizado 1:1 (600x600): {out_path} ({os.path.getsize(out_path)} bytes)")

for key, urls in high_res_urls.items():
    raw_file = os.path.join(dest_dir, f"{key}_hd.jpg")
    downloaded = False
    for u in urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r, open(raw_file, 'wb') as out:
                out.write(r.read())
            downloaded = True
            print(f"[OK] {key} HD baixado de {u}")
            break
        except Exception as e:
            print(f"[Tentativa] {key}: {e}")
    
    if not downloaded:
        raw_file = os.path.join(dest_dir, f"{key}_raw.jpg")
    
    final_file = os.path.join(dest_dir, f"{key}.jpg")
    trim_white_and_square(raw_file, final_file)

# Remove arquivos temporários _raw e _hd
for f in os.listdir(dest_dir):
    if '_raw' in f or '_hd' in f or 'thumb' in f:
        try:
            os.remove(os.path.join(dest_dir, f))
        except:
            pass
