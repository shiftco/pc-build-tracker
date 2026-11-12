import os
import urllib.request
import json

SUPABASE_TOKEN = os.environ.get("SUPABASE_ACCESS_TOKEN", "")
PROJECT_REF = os.environ.get("SUPABASE_PROJECT_REF", "zwfecsnodhxbzbagdxng")

def query_supabase(sql):
    req = urllib.request.Request(
        f'https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query',
        headers={'Authorization': f'Bearer {SUPABASE_TOKEN}', 'Content-Type': 'application/json'},
        data=json.dumps({'query': sql}).encode('utf-8')
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

# Atualizar imagens nas peças
query_supabase("""
UPDATE pc_pecas SET imagem_url = '/images/cpu.jpg?v=2' WHERE id = 'cpu-ryzen-7800x3d';
UPDATE pc_pecas SET imagem_url = '/images/gpu.jpg?v=2' WHERE id = 'gpu-rtx-5070';
UPDATE pc_pecas SET imagem_url = '/images/motherboard.jpg?v=2' WHERE id = 'placa-mae-b650em';
UPDATE pc_pecas SET imagem_url = '/images/ram.jpg?v=2', especificacoes = 'Kit 32GB (2x16GB) • DDR5 6000MHz • AMD EXPO & Intel XMP • CMH32GX5M2D6000Z38 • Estoque Oficial Confirmado', preco_referencia = 4598.99 WHERE id = 'ram-corsair-vengeance-32gb';
UPDATE pc_pecas SET imagem_url = '/images/ssd.jpg?v=2' WHERE id = 'ssd-lexar-nm790-1tb';
UPDATE pc_pecas SET imagem_url = '/images/psu.jpg?v=2' WHERE id = 'fonte-msi-mag-850w';
UPDATE pc_pecas SET imagem_url = '/images/cooler.jpg?v=2' WHERE id = 'cooler-corsair-nautilus-360';
UPDATE pc_pecas SET imagem_url = '/images/monitor.jpg?v=2' WHERE id = 'monitor-asus-tuf-27';
""")

# Atualizar links exatos diretos das ofertas (100% em estoque)
query_supabase("""
-- CPU
UPDATE pc_ofertas SET url_produto = 'https://www.kabum.com.br/produto/426262/processador-amd-ryzen-7-7800x3d-4-2ghz-5-0ghz-max-turbo-cache-104mb-8-nucleos-16-threads-am5-com-video-integrado-100-100000910wof' WHERE peca_id = 'cpu-ryzen-7800x3d' AND loja = 'Kabum';
UPDATE pc_ofertas SET url_produto = 'https://www.terabyteshop.com.br/produto/24856/processador-amd-ryzen-7-7800x3d-42ghz-50ghz-turbo-8-cores-16-threads-am5-sem-cooler-100-100000910wof' WHERE peca_id = 'cpu-ryzen-7800x3d' AND loja = 'Terabyte';
UPDATE pc_ofertas SET url_produto = 'https://www.pichau.com.br/processador-amd-ryzen-7-7800x3d-8-core-16-threads-4-2ghz-5-0ghz-turbo-cache-104mb-am5-100-100000910wof' WHERE peca_id = 'cpu-ryzen-7800x3d' AND loja = 'Pichau';

-- GPU
UPDATE pc_ofertas SET url_produto = 'https://www.terabyteshop.com.br/produto/34407/placa-de-video-gigabyte-nvidia-geforce-rtx-5070-gaming-oc-12gb-gddr7-dlss-ray-tracing-gv-n5070gaming-oc-12gd' WHERE peca_id = 'gpu-rtx-5070' AND loja = 'Terabyte';
UPDATE pc_ofertas SET url_produto = 'https://www.kabum.com.br/produto/754152/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192-bits-gv-n5070gaming-oc-12gd' WHERE peca_id = 'gpu-rtx-5070' AND loja = 'Kabum';
UPDATE pc_ofertas SET url_produto = 'https://www.pichau.com.br/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192-bit-gv-n5070gaming-oc-12gd' WHERE peca_id = 'gpu-rtx-5070' AND loja = 'Pichau';

-- PLACA-MÃE
UPDATE pc_ofertas SET url_produto = 'https://www.terabyteshop.com.br/produto/23471/placa-mae-asus-tuf-gaming-b650m-plus-wifi-chipset-b650-amd-am5-matx-ddr5-90mb1lu0-m0eay0' WHERE peca_id = 'placa-mae-b650em' AND loja = 'Terabyte';
UPDATE pc_ofertas SET url_produto = 'https://www.kabum.com.br/produto/871302/placa-mae-asus-tuf-b650em-plus-amd-am5-m-atx-ddr5-wifi-6e-bluetooth-preto-90mb1lu0' WHERE peca_id = 'placa-mae-b650em' AND loja = 'Kabum';
UPDATE pc_ofertas SET url_produto = 'https://www.pichau.com.br/placa-mae-asus-tuf-gaming-b650m-plus-wifi-ddr5-socket-am5-m-atx-chipset-amd-b650-tuf-gaming-b650m-plus-wifi' WHERE peca_id = 'placa-mae-b650em' AND loja = 'Pichau';

-- RAM (Código 1074524 em estoque na KaBuM!)
DELETE FROM pc_ofertas WHERE peca_id = 'ram-corsair-vengeance-32gb';
INSERT INTO pc_ofertas (peca_id, loja, preco_pix, preco_parcelado, disponivel, url_produto) VALUES
('ram-corsair-vengeance-32gb', 'KaBuM! (Estoque Ativo)', 4599.99, 5111.10, true, 'https://www.kabum.com.br/produto/1074524/memoria-ram-corsair-vengeance-rgb-32gb-2x16gb-6000mhz-ddr5-cl38-cinza-cmh32gx5m2d6000z38'),
('ram-corsair-vengeance-32gb', 'Mercado Livre (Print do Primo)', 4598.99, 4598.99, true, 'https://lista.mercadolivre.com.br/corsair-vengeance-rgb-ddr5-32gb-6000mhz');

-- SSD (Pichau 119 em estoque + KaBuM Kingston NV3 621162 em estoque)
DELETE FROM pc_ofertas WHERE peca_id = 'ssd-lexar-nm790-1tb';
INSERT INTO pc_ofertas (peca_id, loja, preco_pix, preco_parcelado, disponivel, url_produto) VALUES
('ssd-lexar-nm790-1tb', 'Pichau (119 em Estoque)', 1299.99, 1529.40, true, 'https://www.pichau.com.br/ssd-lexar-nm790-1tb-m-2-2280-pcie-nvme-leitura-7400mb-s-gravacao-6500mb-s-lnm790x001t-rnnng'),
('ssd-lexar-nm790-1tb', 'KaBuM! (Kingston NV3 1TB Gen4)', 1299.99, 1529.40, true, 'https://www.kabum.com.br/produto/621162/ssd-kingston-nv3-1-tb-m-2-2280-pcie-4-0-x4-nvme-leitura-6000-mb-s-gravacao-4000-mb-s-azul-snv3s-1000g');

-- FONTE (Código 592338 em estoque na KaBuM!)
DELETE FROM pc_ofertas WHERE peca_id = 'fonte-msi-mag-850w';
INSERT INTO pc_ofertas (peca_id, loja, preco_pix, preco_parcelado, disponivel, url_produto) VALUES
('fonte-msi-mag-850w', 'KaBuM! (Em Estoque)', 608.79, 691.80, true, 'https://www.kabum.com.br/produto/592338/fonte-msi-mag-a850gl-pcie5-850w-80-plus-gold-modular-pfc-ativo-preto'),
('fonte-msi-mag-850w', 'Terabyte', 679.90, 799.88, true, 'https://www.terabyteshop.com.br/produto/25338/fonte-msi-mag-a850gl-850w-80-plus-gold-modular-pfc-ativo-com-cabo-preto');

-- COOLER
UPDATE pc_ofertas SET url_produto = 'https://www.kabum.com.br/produto/998245/water-cooler-corsair-nautilus-360-argb-360mm-amd-e-intel-preto-cw-9060093-ww' WHERE peca_id = 'cooler-corsair-nautilus-360' AND loja = 'Kabum';

-- MONITOR
UPDATE pc_ofertas SET url_produto = 'https://www.kabum.com.br/produto/1017203/monitor-gamer-asus-tuf-27-qhd-255hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aqme5f' WHERE peca_id = 'monitor-asus-tuf-27' AND loja = 'Kabum';
""")

print("SUPABASE ATUALIZADO COM OS LINKS EXATOS E IMAGENS LOCAIS!")
