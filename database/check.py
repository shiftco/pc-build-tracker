import os
import urllib.request
import json

SUPABASE_TOKEN = os.environ.get("SUPABASE_ACCESS_TOKEN", "")
PROJECT_REF = os.environ.get("SUPABASE_PROJECT_REF", "zwfecsnodhxbzbagdxng")

def run_query(sql):
    req = urllib.request.Request(
        f'https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query',
        headers={'Authorization': f'Bearer {SUPABASE_TOKEN}', 'Content-Type': 'application/json'},
        data=json.dumps({'query': sql}).encode('utf-8')
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

# Reload postgrest
run_query("NOTIFY pgrst, 'reload schema';")
res = run_query("SELECT id, nome, preco_referencia FROM pc_pecas ORDER BY ordem;")
print(f"Total de pecas gravadas: {len(res)}")
for r in res:
    print(f"- {r['nome']}: R$ {r['preco_referencia']}")
