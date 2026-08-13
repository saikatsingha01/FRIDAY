import urllib.request
import urllib.parse
import ssl
import re

url = 'https://lite.duckduckgo.com/lite/?q=' + urllib.parse.quote('current weather Siliguri')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

with urllib.request.urlopen(req, timeout=15, context=ssl.create_default_context()) as resp:
    raw = resp.read()
    page = raw.decode('utf-8', errors='replace')

print('Lite DDG length:', len(page))
with open('ddg_lite2.html', 'w', encoding='utf-8') as f:
    f.write(page[:50000])

import re
links = re.findall(r'href="([^"]+)"', page)
print('Links found:', len(links))
for link in links[:10]:
    print(link)