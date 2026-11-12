import urllib.request
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

dest_dir = r'c:\Users\Felipe Oliveira\.octobrain\pc-tracker\web\public\images'
os.makedirs(dest_dir, exist_ok=True)

images = {
    "cpu.jpg": "https://images.kabum.com.br/produtos/fotos/426262/processador-amd-ryzen-7-7800x3d-5-0ghz-max-turbo-cache-104mb-am5-8-nucleos-16-threads-video-integrado-100-100000910wof_1680695027_g.jpg",
    "gpu.jpg": "https://images.kabum.com.br/produtos/fotos/754152/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192-bits-gv-n5070gaming-oc-12gd_1736270518_g.jpg",
    "motherboard.jpg": "https://images.kabum.com.br/produtos/fotos/871302/placa-mae-asus-tuf-b650em-plus-amd-am5-m-atx-ddr5-wifi-6e-bluetooth-preto-90mb1lu0_1712239474_g.jpg",
    "ram.jpg": "https://images.kabum.com.br/produtos/fotos/1086379/memoria-ram-corsair-vengeance-rgb-ddr5-32gb-2x16gb-6000mhz-cmh32gx5m2b6000c30-preto-cl30-intel-xmp-amd-expo-heatsink-desktop-gamer_1729004077_g.jpg",
    "ssd.jpg": "https://images.kabum.com.br/produtos/fotos/597845/ssd-lexar-nm790-1tb-m-2-2280-pcie-nvme-leitura-7400-mb-s-gravacao-6500-mb-s-preto-e-cinza-lnm790x001t-rnnng_1721757833_g.jpg",
    "psu.jpg": "https://images.kabum.com.br/produtos/fotos/462816/fonte-msi-mag-a850gl-850w-80-plus-gold-modular-pfc-ativo-com-cabo-preto_1688062837_g.jpg",
    "cooler.jpg": "https://images.kabum.com.br/produtos/fotos/998245/water-cooler-corsair-nautilus-360-argb-360mm-amd-e-intel-preto-cw-9060093-ww_1715783305_g.jpg",
    "monitor.jpg": "https://images.kabum.com.br/produtos/fotos/1017203/monitor-gamer-asus-tuf-27-qhd-255hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aqme5f_1719253457_g.jpg"
}

for fname, url in images.items():
    dest = os.path.join(dest_dir, fname)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp, open(dest, 'wb') as out:
            out.write(resp.read())
        print(f"OK: {fname} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"FALLBACK for {fname}: {e}")
        # Se kabum der erro, busca na terabyte ou fallback
