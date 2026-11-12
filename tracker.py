import os
import json
import urllib.request
from datetime import datetime
from bot.telegram_bot import TelegramAlertBot

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

def update_offer(peca_id, loja, novo_preco_pix, novo_preco_parcelado=None, url=None):
    """
    Atualiza o preço de uma oferta, verifica se houve queda e dispara alerta no Telegram se aplicável.
    """
    telegram = TelegramAlertBot()

    # Busca a peça e a oferta anterior
    peca_data = query_supabase(f"SELECT nome, preco_alvo, imagem_url FROM pc_pecas WHERE id = '{peca_id}';")
    if not peca_data:
        print(f"Peça {peca_id} não encontrada!")
        return

    peca = peca_data[0]
    oferta_anterior = query_supabase(f"SELECT preco_pix, url_produto FROM pc_ofertas WHERE peca_id = '{peca_id}' AND loja = '{loja}';")

    preco_antigo = float(oferta_anterior[0]['preco_pix']) if oferta_anterior else None
    url_final = url or (oferta_anterior[0]['url_produto'] if oferta_anterior else "")

    # Salva no histórico de preços
    query_supabase(f"""
        INSERT INTO pc_historico_precos (peca_id, loja, preco_pix, data_hora)
        VALUES ('{peca_id}', '{loja}', {novo_preco_pix}, NOW());
    """)

    # Atualiza oferta atual
    if oferta_anterior:
        query_supabase(f"""
            UPDATE pc_ofertas
            SET preco_pix = {novo_preco_pix},
                preco_parcelado = {novo_preco_parcelado if novo_preco_parcelado else 'preco_parcelado'},
                ultima_checagem = NOW()
            WHERE peca_id = '{peca_id}' AND loja = '{loja}';
        """)
    else:
        query_supabase(f"""
            INSERT INTO pc_ofertas (peca_id, loja, preco_pix, preco_parcelado, disponivel, url_produto)
            VALUES ('{peca_id}', '{loja}', {novo_preco_pix}, {novo_preco_parcelado or novo_preco_pix}, TRUE, '{url_final}');
        """)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] {peca['nome']} na {loja}: R$ {novo_preco_pix:.2f}")

    # Verifica se houve queda significativa
    if preco_antigo and novo_preco_pix < preco_antigo:
        print(f"🔥 QUEDA DETECTADA! De R$ {preco_antigo:.2f} para R$ {novo_preco_pix:.2f}")
        telegram.send_price_drop_alert(
            peca_nome=peca['nome'],
            loja=loja,
            preco_antigo=preco_antigo,
            preco_novo=novo_preco_pix,
            url_produto=url_final,
            imagem_url=peca.get('imagem_url')
        )
    elif peca.get('preco_alvo') and novo_preco_pix <= float(peca['preco_alvo']):
        print(f"🎯 META DE PREÇO ATINGIDA! Preço atual R$ {novo_preco_pix:.2f} <= Alvo R$ {peca['preco_alvo']}")

def run_tracker_cycle():
    print(f"\n==========================================")
    print(f"🚀 INICIANDO CICLO DE MONITORAMENTO - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"==========================================")
    
    pecas = query_supabase("SELECT id, nome, preco_referencia FROM pc_pecas ORDER BY ordem;")
    print(f"Peças ativas no radar: {len(pecas)}")

    # Simulação de verificação / coleta
    for p in pecas:
        print(f"-> Monitorando: {p['nome']} (Ref: R$ {p['preco_referencia']})")

    print("\n✅ Ciclo concluído com sucesso.")

if __name__ == "__main__":
    run_tracker_cycle()
