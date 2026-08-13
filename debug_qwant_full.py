import urllib.request
import urllib.parse
import ssl
import gzip
import re

url = 'https://www.qwant.com/search?q=' + urllib.parse.quote('current weather Siliguri')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

try:
    with urllib.request.urlopen(req, timeout=15, context=ssl.create_default_context()) as resp:
        raw = resp.read()
        if resp.headers.get('Content-Encoding') == 'gzip':
            raw = gzip.decompress(raw)
        page = raw.decode('utf-8', errors='replace')
    
    print('Qwant full length:', len(page))
    with open('qwant_full.html', 'w', encoding='utf-8') as f:
        f.write(page[:50000])
    
    import re
    for pattern in ['result', 'snippet', 'title', 'href', 'class=', 'data-', 'article', 'result', 'item']:
        matches = len([m for m in re.finditer(pattern, page, re.IGNORECASE)])
        if matches > 0:
            print(f'{pattern}: {matches}')
    
    if 'captcha' in page.lower() or 'challenge' in page.lower():
        print('CAPTCHA!')
    else:
        print('No CAPTCHA')
        if 'result' in page.lower():
            print('Results found!')
except Exception as e:
    print('Error:', e)
    import traceback
    traceback.print_exc()