import urllib.request
import urllib.parse
import json

def search_mercadolivre(query, limit=5):
    encoded = urllib.parse.quote(query)
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={encoded}&limit={limit}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = []
            for item in data.get("results", []):
                results.append({
                    "titulo": item.get("title"),
                    "preco": item.get("price"),
                    "link": item.get("permalink"),
                    "disponivel": item.get("available_quantity", 0) > 0,
                    "vendedor": item.get("seller", {}).get("nickname", "Desconhecido")
                })
            return results
    except Exception as e:
        print(f"[MercadoLivre] Erro ao buscar '{query}': {e}")
        return []

if __name__ == "__main__":
    items = search_mercadolivre("Corsair Vengeance RGB 32GB DDR5 6000MHz", limit=3)
    print(f"Encontrados no Mercado Livre: {len(items)}")
    for it in items:
        print(f"-> {it['titulo']} | R$ {it['preco']} | {it['link']}")
