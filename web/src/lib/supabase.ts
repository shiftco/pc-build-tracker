import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://zwfecsnodhxbzbagdxng.supabase.co';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3ZmVjc25odhxbzbagdxngIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgwMzgxODAsImV4cCI6MjEwMzYxNDE4MH0.DxMNm0pD-Mm-nyNFLjVsoBHuo-aLxhU9eA7JhyCYU5s';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

export interface OfertaLoja {
  loja: string;
  preco_pix: number;
  preco_parcelado?: number;
  url_produto: string;
  disponivel: boolean;
  is_melhor_preco?: boolean;
}

export interface HistoricoPonto {
  data: string;
  preco: number;
}

export interface PecaBuild {
  id: string;
  nome: string;
  categoria: string;
  especificacoes: string;
  imagem_url: string;
  preco_referencia: number;
  preco_alvo: number;
  ordem: number;
  melhor_oferta: OfertaLoja;
  ofertas: OfertaLoja[];
  historico: HistoricoPonto[];
}

// Opções alternativas de RAM monitoradas em paralelo (não somadas 2x/3x no total da build)
export const RAM_ALTERNATIVE_IDS = new Set([
  'ram-corsair-vengeance-32gb-sem-rgb',
  'ram-corsair-vengeance-rgb-16gb',
]);

// 10 Itens monitorados com preços ao vivo verificados diretamente no DOM das lojas (17/11/2026)
export const INITIAL_PECAS: PecaBuild[] = [
  {
    id: "cpu-ryzen-7800x3d",
    nome: "AMD Ryzen 7 7800X3D (8c/16t, AM5, 104MB Cache)",
    categoria: "Processador",
    especificacoes: "4.2GHz (5.0GHz Turbo) • 104MB Cache 3D V-Cache • Socket AM5 • c/ Vídeo Integrado • 100-100000910WOF",
    imagem_url: "/images/cpu.jpg?v=2",
    preco_referencia: 1769.99,
    preco_alvo: 1700.00,
    ordem: 1,
    melhor_oferta: {
      loja: "KaBuM!",
      preco_pix: 1769.99,
      preco_parcelado: 2082.34,
      url_produto: "https://www.kabum.com.br/produto/426262/processador-amd-ryzen-7-7800x3d-4-2ghz-5-0ghz-max-turbo-cache-104mb-8-nucleos-16-threads-am5-com-video-integrado-100-100000910wof",
      disponivel: true,
      is_melhor_preco: true
    },
    ofertas: [
      {
        loja: "KaBuM! (Oficial em Estoque)",
        preco_pix: 1769.99,
        preco_parcelado: 2082.34,
        url_produto: "https://www.kabum.com.br/produto/426262/processador-amd-ryzen-7-7800x3d-4-2ghz-5-0ghz-max-turbo-cache-104mb-8-nucleos-16-threads-am5-com-video-integrado-100-100000910wof",
        disponivel: true,
        is_melhor_preco: true
      }
    ],
    historico: [
      { data: "08/11", preco: 1899.00 },
      { data: "10/11", preco: 1799.00 },
      { data: "12/11", preco: 1769.99 },
      { data: "17/11", preco: 1769.99 }
    ]
  },
  {
    id: "gpu-rtx-5070",
    nome: "Gigabyte GeForce RTX 5070 Gaming OC 12GB GDDR7",
    categoria: "Placa de Vídeo",
    especificacoes: "12GB GDDR7 • 192-bit • DLSS 4 / Ray Tracing • Triplo Fan Windforce • GV-N5070GAMING-OC-12GD",
    imagem_url: "/images/gpu.jpg?v=2",
    preco_referencia: 6199.99,
    preco_alvo: 5600.00,
    ordem: 2,
    melhor_oferta: {
      loja: "Pichau",
      preco_pix: 6199.99,
      preco_parcelado: 7294.11,
      url_produto: "https://www.pichau.com.br/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192-bit-gv-n5070gaming-oc-12gd",
      disponivel: true,
      is_melhor_preco: true
    },
    ofertas: [
      {
        loja: "Pichau (Em Estoque)",
        preco_pix: 6199.99,
        preco_parcelado: 7294.11,
        url_produto: "https://www.pichau.com.br/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192-bit-gv-n5070gaming-oc-12gd",
        disponivel: true,
        is_melhor_preco: true
      },
      {
        loja: "KaBuM! (Marketplace)",
        preco_pix: 12084.93,
        preco_parcelado: 12084.93,
        url_produto: "https://www.kabum.com.br/produto/754152/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192-bits-gv-n5070gaming-oc-12gd",
        disponivel: true
      }
    ],
    historico: [
      { data: "08/11", preco: 6399.00 },
      { data: "10/11", preco: 6199.99 },
      { data: "12/11", preco: 6299.99 },
      { data: "17/11", preco: 6199.99 }
    ]
  },
  {
    id: "placa-mae-b650em",
    nome: "Asus TUF Gaming B650EM-Plus WIFI (Socket AM5, DDR5)",
    categoria: "Placa-Mãe",
    especificacoes: "Chipset AMD B650 • Socket AM5 • Formato Micro-ATX • Suporte DDR5 • Wi-Fi 6E & Bluetooth • 90MB1LU0",
    imagem_url: "/images/motherboard.jpg?v=2",
    preco_referencia: 1448.99,
    preco_alvo: 1350.00,
    ordem: 3,
    melhor_oferta: {
      loja: "KaBuM!",
      preco_pix: 1448.99,
      preco_parcelado: 1609.99,
      url_produto: "https://www.kabum.com.br/produto/871302/placa-mae-asus-tuf-b650em-plus-amd-am5-m-atx-ddr5-wifi-6e-bluetooth-preto-90mb1lu0",
      disponivel: true,
      is_melhor_preco: true
    },
    ofertas: [
      {
        loja: "KaBuM! (Oficial em Estoque)",
        preco_pix: 1448.99,
        preco_parcelado: 1609.99,
        url_produto: "https://www.kabum.com.br/produto/871302/placa-mae-asus-tuf-b650em-plus-amd-am5-m-atx-ddr5-wifi-6e-bluetooth-preto-90mb1lu0",
        disponivel: true,
        is_melhor_preco: true
      },
      {
        loja: "Pichau",
        preco_pix: 1449.99,
        preco_parcelado: 1705.87,
        url_produto: "https://www.pichau.com.br/placa-mae-asus-tuf-gaming-b650em-plus-wi-fi-ddr5-socket-amd-am5-m-atx-chipset-amd-b650-tuf-gaming-b650em-plus-wifi",
        disponivel: true
      }
    ],
    historico: [
      { data: "08/11", preco: 1599.00 },
      { data: "10/11", preco: 1499.99 },
      { data: "12/11", preco: 1482.99 },
      { data: "17/11", preco: 1448.99 }
    ]
  },
  {
    id: "ram-corsair-vengeance-32gb",
    nome: "Corsair Vengeance RGB 32GB (2x16GB) DDR5 6000MHz",
    categoria: "Memória RAM",
    especificacoes: "Kit 32GB (2x16GB) • DDR5 6000MHz • CL38 • Cinza c/ RGB • CMH32GX5M2D6000Z38",
    imagem_url: "/images/ram.jpg?v=2",
    preco_referencia: 4359.99,
    preco_alvo: 3800.00,
    ordem: 4,
    melhor_oferta: {
      loja: "KaBuM!",
      preco_pix: 4359.99,
      preco_parcelado: 4844.43,
      url_produto: "https://www.kabum.com.br/produto/1074524/memoria-ram-corsair-vengeance-rgb-32gb-2x16gb-6000mhz-ddr5-cl38-cinza-cmh32gx5m2d6000z38",
      disponivel: true,
      is_melhor_preco: true
    },
    ofertas: [
      {
        loja: "KaBuM! (Esquenta Black)",
        preco_pix: 4359.99,
        preco_parcelado: 4844.43,
        url_produto: "https://www.kabum.com.br/produto/1074524/memoria-ram-corsair-vengeance-rgb-32gb-2x16gb-6000mhz-ddr5-cl38-cinza-cmh32gx5m2d6000z38",
        disponivel: true,
        is_melhor_preco: true
      },
      {
        loja: "Pichau",
        preco_pix: 5054.99,
        preco_parcelado: 5947.05,
        url_produto: "https://www.pichau.com.br/memoria-corsair-vengeance-rgb-32gb-2x16gb-ddr5-6000mhz-cl38-cinza-cmh32gx5m2d6000z38",
        disponivel: true
      }
    ],
    historico: [
      { data: "08/11", preco: 4799.00 },
      { data: "10/11", preco: 4599.99 },
      { data: "12/11", preco: 4599.99 },
      { data: "17/11", preco: 4359.99 }
    ]
  },
  {
    id: "ram-corsair-vengeance-32gb-sem-rgb",
    nome: "Corsair Vengeance 32GB (2x16GB) DDR5 6000MHz (Sem RGB)",
    categoria: "Memória RAM",
    especificacoes: "Kit 32GB (2x16GB) • DDR5 6000MHz • CL38 • Cinza S/ RGB • CMK32GX5M2D6000Z38",
    imagem_url: "/images/ram-nonrgb.jpg?v=1",
    preco_referencia: 4239.99,
    preco_alvo: 3600.00,
    ordem: 5,
    melhor_oferta: {
      loja: "KaBuM!",
      preco_pix: 4239.99,
      preco_parcelado: 4711.10,
      url_produto: "https://www.kabum.com.br/produto/1074531/memoria-ram-corsair-vengeance-32gb-2x16gb-6000mhz-ddr5-cl38-cinza-cmk32gx5m2d6000z38",
      disponivel: true,
      is_melhor_preco: true
    },
    ofertas: [
      {
        loja: "KaBuM! (Ninja Friday)",
        preco_pix: 4239.99,
        preco_parcelado: 4711.10,
        url_produto: "https://www.kabum.com.br/produto/1074531/memoria-ram-corsair-vengeance-32gb-2x16gb-6000mhz-ddr5-cl38-cinza-cmk32gx5m2d6000z38",
        disponivel: true,
        is_melhor_preco: true
      },
      {
        loja: "Pichau",
        preco_pix: 5599.99,
        preco_parcelado: 6588.22,
        url_produto: "https://www.pichau.com.br/memoria-corsair-vengeance-32gb-2x16gb-ddr5-6000mhz-cl38-cinza-cmk32gx5m2d6000z38",
        disponivel: true
      }
    ],
    historico: [
      { data: "12/11", preco: 4711.10 },
      { data: "17/11", preco: 4239.99 }
    ]
  },
  {
    id: "ram-corsair-vengeance-rgb-16gb",
    nome: "Corsair Vengeance RGB 16GB (1x16GB) DDR5 6000MHz",
    categoria: "Memória RAM",
    especificacoes: "Módulo Único 16GB (1x16GB) • DDR5 6000MHz • CL38 • Cinza c/ RGB • CMH16GX5M1D6000Z38",
    imagem_url: "/images/ram-16gb.jpg?v=1",
    preco_referencia: 2169.99,
    preco_alvo: 1900.00,
    ordem: 6,
    melhor_oferta: {
      loja: "KaBuM!",
      preco_pix: 2169.99,
      preco_parcelado: 2411.10,
      url_produto: "https://www.kabum.com.br/produto/1074521/memoria-ram-corsair-vengeance-rgb-16gb-6000mhz-ddr5-cl38-cinza-cmh16gx5m1d6000z38",
      disponivel: true,
      is_melhor_preco: true
    },
    ofertas: [
      {
        loja: "KaBuM! (Ninja Friday)",
        preco_pix: 2169.99,
        preco_parcelado: 2411.10,
        url_produto: "https://www.kabum.com.br/produto/1074521/memoria-ram-corsair-vengeance-rgb-16gb-6000mhz-ddr5-cl38-cinza-cmh16gx5m1d6000z38",
        disponivel: true,
        is_melhor_preco: true
      },
      {
        loja: "Pichau",
        preco_pix: 2399.99,
        preco_parcelado: 2823.52,
        url_produto: "https://www.pichau.com.br/memoria-corsair-vengeance-rgb-16gb-1x16gb-ddr5-6000mhz-cl38-cinza-cmh16gx5m1d6000z38",
        disponivel: true
      }
    ],
    historico: [
      { data: "12/11", preco: 2411.10 },
      { data: "17/11", preco: 2169.99 }
    ]
  },
  {
    id: "ssd-lexar-nm790-1tb",
    nome: "SSD 1TB M.2 NVMe PCIe 4.0 (Kingston NV3 / Lexar NM790)",
    categoria: "Armazenamento",
    especificacoes: "M.2 2280 NVMe Gen4x4 • Kingston NV3 (6000MB/s) na KaBuM! ou Lexar NM790 (7400MB/s) na Pichau",
    imagem_url: "/images/ssd.jpg?v=2",
    preco_referencia: 1149.99,
    preco_alvo: 900.00,
    ordem: 7,
    melhor_oferta: {
      loja: "KaBuM!",
      preco_pix: 1149.99,
      preco_parcelado: 1352.93,
      url_produto: "https://www.kabum.com.br/produto/621162/ssd-kingston-nv3-1-tb-m-2-2280-pcie-4-0-x4-nvme-leitura-6000-mb-s-gravacao-4000-mb-s-azul-snv3s-1000g",
      disponivel: true,
      is_melhor_preco: true
    },
    ofertas: [
      {
        loja: "KaBuM! (Kingston NV3 1TB Gen4)",
        preco_pix: 1149.99,
        preco_parcelado: 1352.93,
        url_produto: "https://www.kabum.com.br/produto/621162/ssd-kingston-nv3-1-tb-m-2-2280-pcie-4-0-x4-nvme-leitura-6000-mb-s-gravacao-4000-mb-s-azul-snv3s-1000g",
        disponivel: true,
        is_melhor_preco: true
      },
      {
        loja: "Pichau (Lexar NM790 1TB)",
        preco_pix: 1299.99,
        preco_parcelado: 1529.40,
        url_produto: "https://www.pichau.com.br/ssd-lexar-nm790-1tb-m-2-2280-pcie-nvme-leitura-7400mb-s-gravacao-6500mb-s-lnm790x001t-rnnng",
        disponivel: true
      }
    ],
    historico: [
      { data: "08/11", preco: 1399.00 },
      { data: "10/11", preco: 1299.99 },
      { data: "12/11", preco: 1149.99 },
      { data: "17/11", preco: 1149.99 }
    ]
  },
  {
    id: "fonte-msi-mag-850w",
    nome: "MSI MAG A850GL 850W 80 Plus Gold Modular (PCIe 5.0)",
    categoria: "Fonte de Alimentação",
    especificacoes: "850W • Certificação 80 Plus Gold • Full Modular • Suporte nativo PCIe 5.0 (Cabo 12V-2x6 para a RTX 5070)",
    imagem_url: "/images/psu.jpg?v=2",
    preco_referencia: 670.90,
    preco_alvo: 599.00,
    ordem: 8,
    melhor_oferta: {
      loja: "KaBuM!",
      preco_pix: 670.90,
      preco_parcelado: 745.44,
      url_produto: "https://www.kabum.com.br/produto/592338/fonte-msi-mag-a850gl-pcie5-850w-80-plus-gold-modular-pfc-ativo-preto",
      disponivel: true,
      is_melhor_preco: true
    },
    ofertas: [
      {
        loja: "KaBuM! (Em Estoque)",
        preco_pix: 670.90,
        preco_parcelado: 745.44,
        url_produto: "https://www.kabum.com.br/produto/592338/fonte-msi-mag-a850gl-pcie5-850w-80-plus-gold-modular-pfc-ativo-preto",
        disponivel: true,
        is_melhor_preco: true
      }
    ],
    historico: [
      { data: "08/11", preco: 699.00 },
      { data: "10/11", preco: 629.00 },
      { data: "12/11", preco: 608.79 },
      { data: "17/11", preco: 670.90 }
    ]
  },
  {
    id: "cooler-corsair-nautilus-360",
    nome: "Water Cooler Corsair Nautilus RS ARGB 360mm",
    categoria: "Refrigeração",
    especificacoes: "Radiador 360mm • 3x Fans RS120 ARGB PWM • Bomba c/ iluminação ARGB • AM5 e Intel • CW-9060093-WW",
    imagem_url: "/images/cooler.jpg?v=2",
    preco_referencia: 495.88,
    preco_alvo: 450.00,
    ordem: 9,
    melhor_oferta: {
      loja: "KaBuM!",
      preco_pix: 495.88,
      preco_parcelado: 539.00,
      url_produto: "https://www.kabum.com.br/produto/998245/water-cooler-corsair-nautilus-360-argb-360mm-amd-e-intel-preto-cw-9060093-ww",
      disponivel: true,
      is_melhor_preco: true
    },
    ofertas: [
      {
        loja: "KaBuM! (Em Estoque)",
        preco_pix: 495.88,
        preco_parcelado: 539.00,
        url_produto: "https://www.kabum.com.br/produto/998245/water-cooler-corsair-nautilus-360-argb-360mm-amd-e-intel-preto-cw-9060093-ww",
        disponivel: true,
        is_melhor_preco: true
      }
    ],
    historico: [
      { data: "08/11", preco: 549.00 },
      { data: "10/11", preco: 510.00 },
      { data: "12/11", preco: 495.88 },
      { data: "17/11", preco: 495.88 }
    ]
  },
  {
    id: "monitor-asus-tuf-27",
    nome: "Monitor Asus TUF Gaming VG27AQME5F 27\" QHD 255Hz",
    categoria: "Monitor Gamer",
    especificacoes: "27\" Fast IPS • Resolução Quad HD (2560x1440) • 255Hz • 0.3ms • G-Sync / FreeSync Premium • Som Integrado",
    imagem_url: "/images/monitor.jpg?v=2",
    preco_referencia: 1299.99,
    preco_alvo: 1250.00,
    ordem: 10,
    melhor_oferta: {
      loja: "KaBuM! / Pichau",
      preco_pix: 1299.99,
      preco_parcelado: 1529.40,
      url_produto: "https://www.kabum.com.br/produto/1017203/monitor-gamer-asus-tuf-27-qhd-255hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aqme5f",
      disponivel: true,
      is_melhor_preco: true
    },
    ofertas: [
      {
        loja: "KaBuM! (Empate - Menor Preço)",
        preco_pix: 1299.99,
        preco_parcelado: 1529.40,
        url_produto: "https://www.kabum.com.br/produto/1017203/monitor-gamer-asus-tuf-27-qhd-255hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aqme5f",
        disponivel: true,
        is_melhor_preco: true
      },
      {
        loja: "Pichau (Empate - Menor Preço)",
        preco_pix: 1299.99,
        preco_parcelado: 1529.40,
        url_produto: "https://www.pichau.com.br/monitor-gamer-asus-tuf-gaming-27-pol-fast-ips-qhd-0-3ms-255hz-elmb-sync-hdmi-dp-vg27aqme5f",
        disponivel: true,
        is_melhor_preco: true
      }
    ],
    historico: [
      { data: "08/11", preco: 1499.00 },
      { data: "12/11", preco: 1249.99 },
      { data: "17/11", preco: 1299.99 }
    ]
  }
];
