import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9',
}

url = 'https://www.kabum.com.br/produto/1017203/monitor-gamer-asus-tuf-27-qhd-255hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aqme5f'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    if m:
        data = json.loads(m.group(1))
        pp = data.get('props', {}).get('pageProps', {})
        print('pageProps keys:', list(pp.keys()))
        for k in pp.keys():
            val = str(pp[k])
            print(f"Key {k} (len {len(val)}): {val[:200]}")
