-- Tabela de Peças do PC Gamer
CREATE TABLE IF NOT EXISTS pc_pecas (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    especificacoes TEXT,
    imagem_url TEXT,
    preco_referencia NUMERIC(10, 2) NOT NULL,
    preco_alvo NUMERIC(10, 2),
    ordem INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de Ofertas Atuais por Loja
CREATE TABLE IF NOT EXISTS pc_ofertas (
    id SERIAL PRIMARY KEY,
    peca_id TEXT REFERENCES pc_pecas(id) ON DELETE CASCADE,
    loja TEXT NOT NULL,
    titulo_anuncio TEXT,
    preco_pix NUMERIC(10, 2) NOT NULL,
    preco_parcelado NUMERIC(10, 2),
    disponivel BOOLEAN DEFAULT TRUE,
    url_produto TEXT NOT NULL,
    ultima_checagem TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(peca_id, loja)
);

-- Tabela de Histórico de Preços para Gráficos
CREATE TABLE IF NOT EXISTS pc_historico_precos (
    id SERIAL PRIMARY KEY,
    peca_id TEXT REFERENCES pc_pecas(id) ON DELETE CASCADE,
    loja TEXT NOT NULL,
    preco_pix NUMERIC(10, 2) NOT NULL,
    data_hora TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar RLS e permitir leitura pública anon
ALTER TABLE pc_pecas ENABLE ROW LEVEL SECURITY;
ALTER TABLE pc_ofertas ENABLE ROW LEVEL SECURITY;
ALTER TABLE pc_historico_precos ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Public read pc_pecas" ON pc_pecas;
CREATE POLICY "Public read pc_pecas" ON pc_pecas FOR SELECT USING (true);

DROP POLICY IF EXISTS "Public read pc_ofertas" ON pc_ofertas;
CREATE POLICY "Public read pc_ofertas" ON pc_ofertas FOR SELECT USING (true);

DROP POLICY IF EXISTS "Public read pc_historico_precos" ON pc_historico_precos;
CREATE POLICY "Public read pc_historico_precos" ON pc_historico_precos FOR SELECT USING (true);

-- Permissão total para service_role
DROP POLICY IF EXISTS "Service role all pc_pecas" ON pc_pecas;
CREATE POLICY "Service role all pc_pecas" ON pc_pecas FOR ALL USING (true);

DROP POLICY IF EXISTS "Service role all pc_ofertas" ON pc_ofertas;
CREATE POLICY "Service role all pc_ofertas" ON pc_ofertas FOR ALL USING (true);

DROP POLICY IF EXISTS "Service role all pc_historico_precos" ON pc_historico_precos;
CREATE POLICY "Service role all pc_historico_precos" ON pc_historico_precos FOR ALL USING (true);
