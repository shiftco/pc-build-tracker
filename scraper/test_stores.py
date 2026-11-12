import httpx
from bs4 import BeautifulSoup
import json
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}

client = httpx.Client(headers=headers, follow_redirects=True, timeout=15.0)

def test_mercadolivre():
    print("\n--- TESTANDO MERCADO LIVRE ---")
    url = "https://lista.mercadolivre.com.br/corsair-vengeance-rgb-ddr5-32gb-6000mhz"
    try:
        r = client.get(url)
        print(f"ML Status: {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select(".ui-search-layout__item")
        print(f"ML Itens encontrados: {len(items)}")
        for it in items[:3]:
            title_el = it.select_one(".poly-component__title, .ui-search-item__title")
            price_int = it.select_one(".andes-money-amount__fraction")
            link_el = it.select_one("a.poly-component__title, a.ui-search-link")
            title = title_el.text.strip() if title_el else "N/A"
            price = price_int.text.strip() if price_int else "N/A"
            link = link_el["href"] if link_el and "href" in link_el.attrs else "N/A"
            print(f"  * {title[:60]}... -> R$ {price} ({link[:50]}...)")
    except Exception as e:
        print("ML Error:", e)

def test_kabum():
    print("\n--- TESTANDO KABUM (API DE BUSCA) ---")
    # API interna usada pelo frontend da Kabum
    url = "https://servicespub.kabum.com.br/produtos/v4/produtos"
    params = {
        "query": "Ryzen 7 7800X3D",
        "page_number": "1",
        "page_size": "3",
        "facet_filters": "",
        "sort": "most_searched"
    }
    kabum_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.kabum.com.br",
        "Referer": "https://www.kabum.com.br/"
    }
    try:
        r = httpx.get(url, params=params, headers=kabum_headers, timeout=15.0)
        print(f"Kabum Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            prods = data.get("data", [])
            print(f"Kabum Produtos retornados: {len(prods)}")
            for p in prods[:3]:
                attrs = p.get("attributes", {})
                title = attrs.get("title")
                price = attrs.get("price")
                price_pix = attrs.get("price_details", {}).get("discount_price", price)
                code = p.get("id")
                print(f"  * [{code}] {title[:60]}... -> PIX: R$ {price_pix}")
        else:
            print("Kabum Response:", r.text[:200])
    except Exception as e:
        print("Kabum Error:", e)

def test_terabyte():
    print("\n--- TESTANDO TERABYTE ---")
    url = "https://www.terabyteshop.com.br/busca?str=RTX+5070"
    try:
        r = client.get(url)
        print(f"Terabyte Status: {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select(".product-item, .pbox")
        print(f"Terabyte Itens encontrados: {len(items)}")
        for it in items[:3]:
            title_el = it.select_one(".prod-name, a.title")
            price_el = it.select_one(".prod-new-price, .pbox-val-pix")
            title = title_el.text.strip() if title_el else "N/A"
            price = price_el.text.strip() if price_el else "N/A"
            print(f"  * {title[:60]}... -> {price}")
    except Exception as e:
        print("Terabyte Error:", e)

if __name__ == "__main__":
    test_mercadolivre()
    test_kabum()
    test_terabyte()
