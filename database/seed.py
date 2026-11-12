import os
import urllib.request
import json

SUPABASE_TOKEN = os.environ.get("SUPABASE_ACCESS_TOKEN", "")
PROJECT_REF = os.environ.get("SUPABASE_PROJECT_REF", "zwfecsnodhxbzbagdxng")

pecas = [
    {
        "id": "cpu-ryzen-7800x3d",
        "nome": "AMD Ryzen 7 7800X3D (8 Núcleos / 16 Threads, AM5)",
        "categoria": "Processador",
        "especificacoes": "4.2GHz (5.0GHz Max Turbo), Cache 104MB, AM5, c/ Vídeo Integrado (100-100000910WOF)",
        "imagem_url": "https://images.kabum.com.br/produtos/fotos/426262/processador-amd-ryzen-7-7800x3d-5-0ghz-max-turbo-cache-104mb-am5-8-nucleos-16-threads-video-integrado-100-100000910wof_1680695027_g.jpg",
        "preco_referencia": 1769.99,
        "preco_alvo": 1650.00,
        "ordem": 1
    },
    {
        "id": "gpu-rtx-5070",
        "nome": "Gigabyte GeForce RTX 5070 Gaming OC 12GB GDDR7",
        "categoria": "Placa de Vídeo",
        "especificacoes": "12GB GDDR7, 192-bit, DLSS 4, Ray Tracing, Triplo Fan (GV-N5070GAMING-OC-12GD)",
        "imagem_url": "https://www.terabyteshop.com.br/img/produtos/g/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192bit-gv-n5070gaming-oc-12gd_200424.jpg",
        "preco_referencia": 5899.99,
        "preco_alvo": 5500.00,
        "ordem": 2
    },
    {
        "id": "placa-mae-b650em",
        "nome": "Asus TUF Gaming B650EM-Plus WIFI (AM5, mATX, DDR5)",
        "categoria": "Placa-Mãe",
        "especificacoes": "Chipset B650, Socket AMD AM5, Formato Micro-ATX, Suporte DDR5, Wi-Fi 6 (90MB1LU0-M0EAY0)",
        "imagem_url": "https://www.terabyteshop.com.br/img/produtos/g/placa-mae-asus-tuf-gaming-b650m-plus-wifi-chipset-b650-amd-am5-matx-ddr5-90mb1lu0-m0eay0_183577.jpg",
        "preco_referencia": 1449.99,
        "preco_alvo": 1350.00,
        "ordem": 3
    },
    {
        "id": "ram-corsair-vengeance-32gb",
        "nome": "Corsair Vengeance RGB 32GB (2x16GB) DDR5 6000MHz",
        "categoria": "Memória RAM",
        "especificacoes": "Kit Dual Channel 32GB (2x16GB), DDR5 6000MHz, RGB dinâmico, Perfil AMD EXPO / XMP",
        "imagem_url": "https://m.media-amazon.com/images/I/61k1qH9VlPL._AC_SL1500_.jpg",
        "preco_referencia": 1199.90,
        "preco_alvo": 1050.00,
        "ordem": 4
    },
    {
        "id": "ssd-lexar-nm790-1tb",
        "nome": "Lexar NM790 1TB M.2 NVMe PCIe 4.0 (7400MB/s)",
        "categoria": "SSD / Armazenamento",
        "especificacoes": "M.2 2280, PCIe Gen4x4 NVMe, Leitura 7400MB/s, Gravação 6500MB/s (LNM790X001T-RNNNG)",
        "imagem_url": "https://media.pichau.com.br/media/catalog/product/l/n/lnm790x001t-rnnng.jpg",
        "preco_referencia": 689.90,
        "preco_alvo": 620.00,
        "ordem": 5
    },
    {
        "id": "fonte-msi-mag-850w",
        "nome": "MSI MAG A850GL 850W 80 Plus Gold Modular (PCIe 5.0)",
        "categoria": "Fonte de Alimentação",
        "especificacoes": "850W, Certificação 80 Plus Gold, Full Modular, PFC Ativo, Suporte nativo PCIe 5.0 (12V-2x6)",
        "imagem_url": "https://images.kabum.com.br/produtos/fotos/476317/fonte-msi-mag-a850gl-pcie5-850w-80-plus-gold-modular-pfc-ativo-com-cabo-preto-306-7zp8b11-ce0_1692285196_g.jpg",
        "preco_referencia": 649.90,
        "preco_alvo": 599.00,
        "ordem": 6
    },
    {
        "id": "cooler-corsair-nautilus-360",
        "nome": "Water Cooler Corsair Nautilus RS ARGB 360mm",
        "categoria": "Refrigeração",
        "especificacoes": "Radiador 360mm, 3x Fans RS120 ARGB PWM, Bomba c/ iluminação ARGB, AM5/Intel (CW-9060093-WW)",
        "imagem_url": "https://images.kabum.com.br/produtos/fotos/998245/water-cooler-corsair-nautilus-rs-argb-360mm-pwm-intel-amd-preto-cw-9060093-ww_1715783305_g.jpg",
        "preco_referencia": 495.88,
        "preco_alvo": 450.00,
        "ordem": 7
    },
    {
        "id": "monitor-asus-tuf-27",
        "nome": "Monitor Gamer Asus TUF Gaming VG27AQME5F 27\" QHD 255Hz",
        "categoria": "Monitor Gamer",
        "especificacoes": "27 Polegadas, Quad HD (2560x1440), 255Hz, Fast IPS, 0.3ms MPRT, G-Sync / FreeSync, HDMI/DP",
        "imagem_url": "https://m.media-amazon.com/images/I/81xU9E6-a2L._AC_SL1500_.jpg",
        "preco_referencia": 1297.89,
        "preco_alvo": 1250.00,
        "ordem": 8
    }
]

ofertas = [
    # CPU
    {"peca_id": "cpu-ryzen-7800x3d", "loja": "Kabum", "titulo": "Processador AMD Ryzen 7 7800X3D", "preco_pix": 1769.99, "preco_parcelado": 2082.30, "url": "https://www.kabum.com.br/produto/426262/processador-amd-ryzen-7-7800x3d"},
    {"peca_id": "cpu-ryzen-7800x3d", "loja": "Terabyte", "titulo": "Processador AMD Ryzen 7 7800X3D", "preco_pix": 1829.00, "preco_parcelado": 2151.76, "url": "https://www.terabyteshop.com.br/busca?str=Ryzen+7+7800X3D"},
    {"peca_id": "cpu-ryzen-7800x3d", "loja": "Pichau", "titulo": "Processador AMD Ryzen 7 7800X3D", "preco_pix": 1849.99, "preco_parcelado": 2176.46, "url": "https://www.pichau.com.br/search?q=Ryzen%207%207800X3D"},

    # GPU
    {"peca_id": "gpu-rtx-5070", "loja": "Terabyte", "titulo": "Placa de Vídeo Gigabyte RTX 5070 Gaming OC 12GB", "preco_pix": 5899.99, "preco_parcelado": 6941.16, "url": "https://www.terabyteshop.com.br/produto/34407/placa-de-video-gigabyte-nvidia-geforce-rtx-5070-gaming-oc-12gb-gddr7-dlss-ray-tracing-gv-n5070gaming-oc-12gd"},
    {"peca_id": "gpu-rtx-5070", "loja": "Pichau", "titulo": "Placa de Vídeo Gigabyte RTX 5070 Gaming OC 12GB", "preco_pix": 6199.99, "preco_parcelado": 7294.11, "url": "https://www.pichau.com.br/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192-bit-gv-n5070gaming-oc-12gd"},
    {"peca_id": "gpu-rtx-5070", "loja": "Kabum", "titulo": "Placa de Vídeo Gigabyte RTX 5070 Gaming OC 12GB", "preco_pix": 6099.90, "preco_parcelado": 7176.35, "url": "https://www.kabum.com.br/busca?q=RTX+5070+Gigabyte+Gaming+OC"},

    # Placa-mãe
    {"peca_id": "placa-mae-b650em", "loja": "Terabyte", "titulo": "Placa Mãe Asus TUF Gaming B650EM-Plus WIFI", "preco_pix": 1449.99, "preco_parcelado": 1705.87, "url": "https://www.terabyteshop.com.br/produto/23471/placa-mae-asus-tuf-gaming-b650m-plus-wifi-chipset-b650-amd-am5-matx-ddr5-90mb1lu0-m0eay0"},
    {"peca_id": "placa-mae-b650em", "loja": "Kabum", "titulo": "Placa Mãe Asus TUF Gaming B650M-Plus WIFI", "preco_pix": 1499.99, "preco_parcelado": 1764.70, "url": "https://www.kabum.com.br/busca?q=Asus+TUF+B650M+Plus+WIFI"},

    # RAM
    {"peca_id": "ram-corsair-vengeance-32gb", "loja": "Kabum", "titulo": "Memória Corsair Vengeance RGB 32GB (2x16GB) DDR5 6000MHz", "preco_pix": 1199.90, "preco_parcelado": 1411.65, "url": "https://www.kabum.com.br/busca?q=Corsair+Vengeance+RGB+32GB+DDR5+6000"},
    {"peca_id": "ram-corsair-vengeance-32gb", "loja": "Terabyte", "titulo": "Memória Corsair Vengeance RGB 32GB (2x16GB) DDR5 6000MHz", "preco_pix": 1249.00, "preco_parcelado": 1469.41, "url": "https://www.terabyteshop.com.br/busca?str=Corsair+Vengeance+RGB+32GB+6000MHz"},

    # SSD
    {"peca_id": "ssd-lexar-nm790-1tb", "loja": "Kabum", "titulo": "SSD Lexar NM790 1TB M.2 NVMe PCIe 4.0", "preco_pix": 689.90, "preco_parcelado": 811.65, "url": "https://www.kabum.com.br/busca?q=Lexar+NM790+1TB"},
    {"peca_id": "ssd-lexar-nm790-1tb", "loja": "Pichau", "titulo": "SSD Lexar NM790 1TB M.2 NVMe PCIe 4.0", "preco_pix": 1299.99, "preco_parcelado": 1529.40, "url": "https://www.pichau.com.br/ssd-lexar-nm790-1tb-m-2-2280-pcie-nvme-leitura-7400mb-s-gravacao-6500mb-s-lnm790x001t-rnnng"},

    # Fonte
    {"peca_id": "fonte-msi-mag-850w", "loja": "Kabum", "titulo": "Fonte MSI MAG A850GL 850W 80 Plus Gold Modular", "preco_pix": 649.90, "preco_parcelado": 676.90, "url": "https://www.kabum.com.br/busca?q=MSI+MAG+A850GL"},
    {"peca_id": "fonte-msi-mag-850w", "loja": "Terabyte", "titulo": "Fonte MSI MAG A850GL 850W 80 Plus Gold Modular", "preco_pix": 679.90, "preco_parcelado": 799.88, "url": "https://www.terabyteshop.com.br/busca?str=MSI+MAG+A850GL"},

    # Cooler
    {"peca_id": "cooler-corsair-nautilus-360", "loja": "Kabum", "titulo": "Water Cooler Corsair Nautilus RS ARGB 360mm", "preco_pix": 495.88, "preco_parcelado": 539.00, "url": "https://www.kabum.com.br/produto/998245/water-cooler-corsair-nautilus-rs-argb-360mm-pwm-intel-amd-preto-cw-9060093-ww"},

    # Monitor
    {"peca_id": "monitor-asus-tuf-27", "loja": "Shopee", "titulo": "Monitor Gamer Asus TUF Gaming VG27AQME5F 27 QHD 255Hz", "preco_pix": 1297.89, "preco_parcelado": 1494.99, "url": "https://shopee.com.br/search?keyword=VG27AQME5F"},
    {"peca_id": "monitor-asus-tuf-27", "loja": "Kabum", "titulo": "Monitor Gamer Asus TUF Gaming 27 QHD", "preco_pix": 1499.00, "preco_parcelado": 1763.53, "url": "https://www.kabum.com.br/busca?q=Monitor+Asus+TUF+27+QHD"}
]

sql_statements = []

for p in pecas:
    sql = f"""
    INSERT INTO pc_pecas (id, nome, categoria, especificacoes, imagem_url, preco_referencia, preco_alvo, ordem)
    VALUES ('{p['id']}', '{p['nome'].replace("'", "''")}', '{p['categoria']}', '{p['especificacoes'].replace("'", "''")}', '{p['imagem_url']}', {p['preco_referencia']}, {p['preco_alvo']}, {p['ordem']})
    ON CONFLICT (id) DO UPDATE SET
        nome = EXCLUDED.nome,
        categoria = EXCLUDED.categoria,
        especificacoes = EXCLUDED.especificacoes,
        imagem_url = EXCLUDED.imagem_url,
        preco_referencia = EXCLUDED.preco_referencia,
        preco_alvo = EXCLUDED.preco_alvo,
        ordem = EXCLUDED.ordem;
    """
    sql_statements.append(sql)

for o in ofertas:
    sql = f"""
    INSERT INTO pc_ofertas (peca_id, loja, titulo_anuncio, preco_pix, preco_parcelado, disponivel, url_produto)
    VALUES ('{o['peca_id']}', '{o['loja']}', '{o['titulo'].replace("'", "''")}', {o['preco_pix']}, {o['preco_parcelado']}, TRUE, '{o['url']}')
    ON CONFLICT (peca_id, loja) DO UPDATE SET
        titulo_anuncio = EXCLUDED.titulo_anuncio,
        preco_pix = EXCLUDED.preco_pix,
        preco_parcelado = EXCLUDED.preco_parcelado,
        url_produto = EXCLUDED.url_produto,
        ultima_checagem = NOW();
    
    INSERT INTO pc_historico_precos (peca_id, loja, preco_pix, data_hora)
    VALUES ('{o['peca_id']}', '{o['loja']}', {o['preco_pix']}, NOW() - INTERVAL '1 day');
    INSERT INTO pc_historico_precos (peca_id, loja, preco_pix, data_hora)
    VALUES ('{o['peca_id']}', '{o['loja']}', {o['preco_pix']}, NOW());
    """
    sql_statements.append(sql)

full_sql = "\n".join(sql_statements)

req = urllib.request.Request(
    f'https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query',
    headers={'Authorization': f'Bearer {SUPABASE_TOKEN}', 'Content-Type': 'application/json'},
    data=json.dumps({'query': full_sql}).encode('utf-8')
)

try:
    with urllib.request.urlopen(req) as resp:
        print("SEEDING COMPLETE!")
except Exception as e:
    print("SEEDING FAILED:", e)
