import urllib.request
import urllib.parse
import ssl
import re

url = 'https://lite.qwant.com/?q=' + urllib.parse.quote('current weather Siliguri')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

with urllib.request.urlopen(req, timeout=15, context=ssl.create_default_context()) as resp:
    raw = resp.read()
    if resp.headers.get('Content-Encoding') == 'gzip':
        raw = gzip.decompress(raw)
    page = raw.decode('utf-8', errors='replace')

print('Page length:', len(page))
with open('qwant_debug.html', 'w', encoding='utf-8') as f:
    f.write(page[:50000])

import re
for pattern in ['result', 'snippet', 'title', 'href', 'link', 'url', 'class=', 'data-']:
    matches = len([m for m in re.finditer(pattern, page, re.IGNORECASE)])
    if matches > 0:
        print(f'{pattern}: {matches}')

if 'table' in page.lower():
    print('Has table')
if 'tr' in page.lower():
    print('Has tr')
if 'td' in page.lower():
    print('Has td')
if 'a href' in page.lower():
    print('Has a href')
if 'captcha' in page.lower() or 'challenge' in page.lower():
    print('CAPTCHA!')
else:
    print('No CAPTCHA')