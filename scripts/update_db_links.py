import os
import urllib.request
import json
from pathlib import Path

# Carregar .env do workspace se existir
env_path = Path(r"c:\Users\Felipe Oliveira\.octobrain\.env")
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

SUPABASE_TOKEN = os.environ.get("SUPABASE_ACCESS_TOKEN", "")
PROJECT_REF = os.environ.get("SUPABASE_PROJECT_REF", "zwfecsnodhxbzbagdxng")

def query_supabase(sql):
    req = urllib.request.Request(
        f'https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query',
        headers={
            'Authorization': f'Bearer {SUPABASE_TOKEN}',
            'Content-Type': 'application/json',
            'User-Agent': 'curl/8.0'
        },
        data=json.dumps({'query': sql}).encode('utf-8')
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode('utf-8'))

# 1. Upsert todas as 10 peças
query_supabase("""
INSERT INTO pc_pecas (id, nome, categoria, especificacoes, imagem_url, preco_referencia, preco_alvo, ordem) VALUES
('cpu-ryzen-7800x3d', 'AMD Ryzen 7 7800X3D (8c/16t, AM5, 104MB Cache)', 'Processador', '4.2GHz (5.0GHz Turbo) • 104MB Cache 3D V-Cache • Socket AM5 • c/ Vídeo Integrado • 100-100000910WOF', '/images/cpu.jpg?v=2', 1769.99, 1700.00, 1),
('gpu-rtx-5070', 'Gigabyte GeForce RTX 5070 12GB GDDR7 (Windforce / Gaming OC)', 'Placa de Vídeo', '12GB GDDR7 • 192-bit • DLSS 4 / Ray Tracing • Triplo Fan • GV-N5070WF3OC-12GD / GV-N5070GAMING-OC-12GD', '/images/gpu.jpg?v=2', 5999.99, 5600.00, 2),
('placa-mae-b650em', 'Asus TUF Gaming B650EM-Plus WIFI (Socket AM5, DDR5)', 'Placa-Mãe', 'Chipset AMD B650 • Socket AM5 • Formato Micro-ATX • Suporte DDR5 • Wi-Fi 6E & Bluetooth • 90MB1LU0', '/images/motherboard.jpg?v=2', 1448.99, 1350.00, 3),
('ram-corsair-vengeance-32gb', 'Corsair Vengeance RGB 32GB (2x16GB) DDR5 6000MHz', 'Memória RAM', 'Kit 32GB (2x16GB) • DDR5 6000MHz • CL38 • Cinza c/ RGB • CMH32GX5M2D6000Z38', '/images/ram.jpg?v=2', 4359.99, 3800.00, 4),
('ram-corsair-vengeance-32gb-sem-rgb', 'Corsair Vengeance 32GB (2x16GB) DDR5 6000MHz (Sem RGB)', 'Memória RAM', 'Kit 32GB (2x16GB) • DDR5 6000MHz • CL38 • Cinza S/ RGB • CMK32GX5M2D6000Z38', '/images/ram-nonrgb.jpg?v=1', 4239.99, 3600.00, 5),
('ram-corsair-vengeance-rgb-16gb', 'Corsair Vengeance RGB 16GB (1x16GB) DDR5 6000MHz', 'Memória RAM', 'Módulo Único 16GB (1x16GB) • DDR5 6000MHz • CL38 • Cinza c/ RGB • CMH16GX5M1D6000Z38', '/images/ram-16gb.jpg?v=1', 2169.99, 1900.00, 6),
('ssd-lexar-nm790-1tb', 'SSD 1TB M.2 NVMe PCIe 4.0 (Kingston NV3 / Lexar NM790)', 'Armazenamento', 'M.2 2280 NVMe Gen4x4 • Kingston NV3 (6000MB/s) na KaBuM! ou Lexar NM790 (7400MB/s) na Pichau', '/images/ssd.jpg?v=2', 1149.99, 900.00, 7),
('fonte-msi-mag-850w', 'MSI MAG A850GL 850W 80 Plus Gold Modular (PCIe 5.0)', 'Fonte de Alimentação', '850W • Certificação 80 Plus Gold • Full Modular • Suporte nativo PCIe 5.0 (Cabo 12V-2x6 para a RTX 5070)', '/images/psu.jpg?v=2', 670.90, 599.00, 8),
('cooler-corsair-nautilus-360', 'Water Cooler Corsair Nautilus RS ARGB 360mm', 'Refrigeração', 'Radiador 360mm • 3x Fans RS120 ARGB PWM • Bomba c/ iluminação ARGB • AM5 e Intel • CW-9060093-WW', '/images/cooler.jpg?v=2', 495.88, 450.00, 9),
('monitor-asus-tuf-27', 'Monitor Asus TUF Gaming VG27AQME5F 27" QHD 255Hz', 'Monitor Gamer', '27" Fast IPS • Resolução Quad HD (2560x1440) • 255Hz • 0.3ms • G-Sync / FreeSync Premium • Som Integrado', '/images/monitor.jpg?v=2', 1249.99, 1250.00, 10)
ON CONFLICT (id) DO UPDATE SET
  nome = EXCLUDED.nome,
  categoria = EXCLUDED.categoria,
  especificacoes = EXCLUDED.especificacoes,
  imagem_url = EXCLUDED.imagem_url,
  preco_referencia = EXCLUDED.preco_referencia,
  preco_alvo = EXCLUDED.preco_alvo,
  ordem = EXCLUDED.ordem;
""")

# 2. Atualizar ofertas 100% ativas, em estoque e validadas contra redirecionamentos (17/11/2026)
query_supabase("""
DELETE FROM pc_ofertas;
INSERT INTO pc_ofertas (peca_id, loja, preco_pix, preco_parcelado, disponivel, url_produto, ultima_checagem) VALUES
-- CPU (KaBuM 426262 ativo em estoque)
('cpu-ryzen-7800x3d', 'KaBuM! (Em Estoque)', 1769.99, 2082.34, true, 'https://www.kabum.com.br/produto/426262/processador-amd-ryzen-7-7800x3d-4-2ghz-5-0ghz-max-turbo-cache-104mb-8-nucleos-16-threads-am5-com-video-integrado-100-100000910wof', NOW()),

-- GPU (Terabyte ID ativo 35379 Windforce OC R$ 5.999,99 + Pichau Gaming OC R$ 6.199,99 + KaBuM ID ativo 714570 Aero 12G R$ 6.999,99)
('gpu-rtx-5070', 'Terabyte (Windforce OC 12GB)', 5999.99, 7058.81, true, 'https://www.terabyteshop.com.br/produto/35379/placa-de-video-gigabyte-nvidia-geforce-rtx-5070-windforce-oc-sff-12gb-gddr7-dlss-ray-tracing-gv-n5070wf3oc-12gd', NOW()),
('gpu-rtx-5070', 'Pichau (Gaming OC 12GB)', 6199.99, 7294.11, true, 'https://www.pichau.com.br/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192-bit-gv-n5070gaming-oc-12gd', NOW()),
('gpu-rtx-5070', 'KaBuM! (Em Estoque)', 6999.99, 8045.96, true, 'https://www.kabum.com.br/produto/714570/placa-de-video-gigabyte-rtx-5070-aero-12g-nvidia-geforce-12gb-gddr7-192bits-rgb-dlss-ray-tracing-9vn5070ao-00-g10', NOW()),

-- PLACA-MÃE (KaBuM 871302 R$ 1.448,99 + Pichau R$ 1.449,99 + Terabyte ID ativo 38004 R$ 1.449,99)
('placa-mae-b650em', 'KaBuM! (Em Estoque)', 1448.99, 1609.99, true, 'https://www.kabum.com.br/produto/871302/placa-mae-asus-tuf-b650em-plus-amd-am5-m-atx-ddr5-wifi-6e-bluetooth-preto-90mb1lu0', NOW()),
('placa-mae-b650em', 'Pichau', 1449.99, 1705.87, true, 'https://www.pichau.com.br/placa-mae-asus-tuf-gaming-b650em-plus-wi-fi-ddr5-socket-amd-am5-m-atx-chipset-amd-b650-tuf-gaming-b650em-plus-wifi', NOW()),
('placa-mae-b650em', 'Terabyte', 1449.99, 1705.87, true, 'https://www.terabyteshop.com.br/produto/38004/placa-mae-asus-tuf-gaming-b650em-plus-wifi-chipset-b650-amd-am5-matx-ddr5-90mb1lu0-m0eay0', NOW()),

-- RAM 1: Corsair Vengeance RGB 32GB (2x16GB) 6000MHz Cinza (1074524)
('ram-corsair-vengeance-32gb', 'KaBuM! (Esquenta Black)', 4359.99, 4844.43, true, 'https://www.kabum.com.br/produto/1074524/memoria-ram-corsair-vengeance-rgb-32gb-2x16gb-6000mhz-ddr5-cl38-cinza-cmh32gx5m2d6000z38', NOW()),
('ram-corsair-vengeance-32gb', 'Pichau', 5054.99, 5947.05, true, 'https://www.pichau.com.br/memoria-corsair-vengeance-rgb-32gb-2x16gb-ddr5-6000mhz-cl38-cinza-cmh32gx5m2d6000z38', NOW()),

-- RAM 2: Corsair Vengeance 32GB (2x16GB) 6000MHz Sem RGB Cinza (1074531)
('ram-corsair-vengeance-32gb-sem-rgb', 'KaBuM! (Ninja Friday)', 4239.99, 4711.10, true, 'https://www.kabum.com.br/produto/1074531/memoria-ram-corsair-vengeance-32gb-2x16gb-6000mhz-ddr5-cl38-cinza-cmk32gx5m2d6000z38', NOW()),
('ram-corsair-vengeance-32gb-sem-rgb', 'Pichau', 5599.99, 6588.22, true, 'https://www.pichau.com.br/memoria-corsair-vengeance-32gb-2x16gb-ddr5-6000mhz-cl38-cinza-cmk32gx5m2d6000z38', NOW()),

-- RAM 3: Corsair Vengeance RGB 16GB (1x16GB) 6000MHz Cinza (1074521)
('ram-corsair-vengeance-rgb-16gb', 'KaBuM! (Ninja Friday)', 2169.99, 2411.10, true, 'https://www.kabum.com.br/produto/1074521/memoria-ram-corsair-vengeance-rgb-16gb-6000mhz-ddr5-cl38-cinza-cmh16gx5m1d6000z38', NOW()),
('ram-corsair-vengeance-rgb-16gb', 'Pichau', 2399.99, 2823.52, true, 'https://www.pichau.com.br/memoria-corsair-vengeance-rgb-16gb-1x16gb-ddr5-6000mhz-cl38-cinza-cmh16gx5m1d6000z38', NOW()),

-- SSD (KaBuM Kingston NV3 621162 + Pichau Lexar NM790)
('ssd-lexar-nm790-1tb', 'KaBuM! (Kingston NV3 1TB Gen4)', 1149.99, 1352.93, true, 'https://www.kabum.com.br/produto/621162/ssd-kingston-nv3-1-tb-m-2-2280-pcie-4-0-x4-nvme-leitura-6000-mb-s-gravacao-4000-mb-s-azul-snv3s-1000g', NOW()),
('ssd-lexar-nm790-1tb', 'Pichau (Lexar NM790 1TB)', 1299.99, 1529.40, true, 'https://www.pichau.com.br/ssd-lexar-nm790-1tb-m-2-2280-pcie-nvme-leitura-7400mb-s-gravacao-6500mb-s-lnm790x001t-rnnng', NOW()),

-- FONTE (KaBuM 592338 R$ 670,90 + Terabyte ID ativo 29394 R$ 699,99)
('fonte-msi-mag-850w', 'KaBuM! (Em Estoque)', 670.90, 745.44, true, 'https://www.kabum.com.br/produto/592338/fonte-msi-mag-a850gl-pcie5-850w-80-plus-gold-modular-pfc-ativo-preto', NOW()),
('fonte-msi-mag-850w', 'Terabyte', 699.99, 823.52, true, 'https://www.terabyteshop.com.br/produto/29394/fonte-msi-mag-a850gl-pcie5-850w-80-plus-gold-pfc-ativo-full-modular-preto-mag-a850gl-pcie5', NOW()),

-- COOLER (KaBuM 998245 R$ 495,88 + Terabyte ID ativo 40029 R$ 589,99)
('cooler-corsair-nautilus-360', 'KaBuM! (Em Estoque)', 495.88, 539.00, true, 'https://www.kabum.com.br/produto/998245/water-cooler-corsair-nautilus-360-argb-360mm-amd-e-intel-preto-cw-9060093-ww', NOW()),
('cooler-corsair-nautilus-360', 'Terabyte', 589.99, 694.11, true, 'https://www.terabyteshop.com.br/produto/40029/water-cooler-corsair-nautilus-rs-argb-360mm-pwm-intel-amd-preto-cw-9060093-ww', NOW()),

-- MONITOR (Terabyte ID ativo 42016 R$ 1.249,99 + KaBuM 1017203 R$ 1.299,99 + Pichau R$ 1.299,99)
('monitor-asus-tuf-27', 'Terabyte (Menor Preço)', 1249.99, 1470.58, true, 'https://www.terabyteshop.com.br/produto/42016/monitor-gamer-asus-tuf-gaming-vg27aqme5f-27-pol-quad-hd-255hz-fast-ips-03ms-g-syncfreesync-hdmidp', NOW()),
('monitor-asus-tuf-27', 'KaBuM!', 1299.99, 1529.40, true, 'https://www.kabum.com.br/produto/1017203/monitor-gamer-asus-tuf-27-qhd-255hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aqme5f', NOW()),
('monitor-asus-tuf-27', 'Pichau', 1299.99, 1529.40, true, 'https://www.pichau.com.br/monitor-gamer-asus-tuf-gaming-27-pol-fast-ips-qhd-0-3ms-255hz-elmb-sync-hdmi-dp-vg27aqme5f', NOW());
""")

# 3. Histórico limpo até 17/11/2026
query_supabase("""
DELETE FROM pc_historico_precos;
INSERT INTO pc_historico_precos (peca_id, loja, preco_pix, data_hora) VALUES
('cpu-ryzen-7800x3d', 'KaBuM!', 1899.00, '2026-11-08T15:00:00Z'),
('cpu-ryzen-7800x3d', 'KaBuM!', 1799.00, '2026-11-10T15:00:00Z'),
('cpu-ryzen-7800x3d', 'KaBuM!', 1769.99, '2026-11-12T15:00:00Z'),
('cpu-ryzen-7800x3d', 'KaBuM!', 1769.99, '2026-11-17T15:00:00Z'),

('gpu-rtx-5070', 'Pichau', 6399.00, '2026-11-08T15:00:00Z'),
('gpu-rtx-5070', 'Pichau', 6299.99, '2026-11-10T15:00:00Z'),
('gpu-rtx-5070', 'Pichau', 6199.99, '2026-11-12T15:00:00Z'),
('gpu-rtx-5070', 'Terabyte', 5999.99, '2026-11-17T15:00:00Z'),

('placa-mae-b650em', 'KaBuM!', 1599.00, '2026-11-08T15:00:00Z'),
('placa-mae-b650em', 'KaBuM!', 1499.99, '2026-11-10T15:00:00Z'),
('placa-mae-b650em', 'KaBuM!', 1482.99, '2026-11-12T15:00:00Z'),
('placa-mae-b650em', 'KaBuM!', 1448.99, '2026-11-17T15:00:00Z'),

('ram-corsair-vengeance-32gb', 'KaBuM!', 4799.00, '2026-11-08T15:00:00Z'),
('ram-corsair-vengeance-32gb', 'KaBuM!', 4599.99, '2026-11-10T15:00:00Z'),
('ram-corsair-vengeance-32gb', 'KaBuM!', 4599.99, '2026-11-12T15:00:00Z'),
('ram-corsair-vengeance-32gb', 'KaBuM!', 4359.99, '2026-11-17T15:00:00Z'),

('ram-corsair-vengeance-32gb-sem-rgb', 'KaBuM!', 4711.10, '2026-11-12T15:00:00Z'),
('ram-corsair-vengeance-32gb-sem-rgb', 'KaBuM!', 4239.99, '2026-11-17T15:00:00Z'),

('ram-corsair-vengeance-rgb-16gb', 'KaBuM!', 2411.10, '2026-11-12T15:00:00Z'),
('ram-corsair-vengeance-rgb-16gb', 'KaBuM!', 2169.99, '2026-11-17T15:00:00Z'),

('ssd-lexar-nm790-1tb', 'KaBuM!', 1399.00, '2026-11-08T15:00:00Z'),
('ssd-lexar-nm790-1tb', 'KaBuM!', 1299.99, '2026-11-10T15:00:00Z'),
('ssd-lexar-nm790-1tb', 'KaBuM!', 1149.99, '2026-11-12T15:00:00Z'),
('ssd-lexar-nm790-1tb', 'KaBuM!', 1149.99, '2026-11-17T15:00:00Z'),

('fonte-msi-mag-850w', 'KaBuM!', 699.00, '2026-11-08T15:00:00Z'),
('fonte-msi-mag-850w', 'KaBuM!', 629.00, '2026-11-10T15:00:00Z'),
('fonte-msi-mag-850w', 'KaBuM!', 608.79, '2026-11-12T15:00:00Z'),
('fonte-msi-mag-850w', 'KaBuM!', 670.90, '2026-11-17T15:00:00Z'),

('cooler-corsair-nautilus-360', 'KaBuM!', 549.00, '2026-11-08T15:00:00Z'),
('cooler-corsair-nautilus-360', 'KaBuM!', 510.00, '2026-11-10T15:00:00Z'),
('cooler-corsair-nautilus-360', 'KaBuM!', 495.88, '2026-11-12T15:00:00Z'),
('cooler-corsair-nautilus-360', 'KaBuM!', 495.88, '2026-11-17T15:00:00Z'),

('monitor-asus-tuf-27', 'Pichau', 1499.00, '2026-11-08T15:00:00Z'),
('monitor-asus-tuf-27', 'KaBuM!', 1299.99, '2026-11-12T15:00:00Z'),
('monitor-asus-tuf-27', 'Terabyte', 1249.99, '2026-11-17T15:00:00Z');
""")

print("SUPABASE SINCRONIZADO COM OS LINKS AUTO-CORRIGIDOS (TERABYTE, PICHAU E KABUM)!")
