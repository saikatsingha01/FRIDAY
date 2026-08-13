import urllib.request
import urllib.parse
import ssl
import gzip
import http.cookiejar

# Use cookie jar to maintain session
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('Accept-Language', 'en-US,en;q=0.9'),
    ('Accept-Encoding', 'gzip, deflate, br'),
    ('Accept-Language', 'en-US,en;q=0.9'),
    ('Connection', 'keep-alive'),
    ('Upgrade-Insecure-Requests', '1'),
    ('Sec-Fetch-Dest', 'document'),
    ('Sec-Fetch-Mode', 'navigate'),
    ('Sec-Fetch-Site', 'none'),
    ('Sec-Fetch-User', '?1'),
    ('Cache-Control', 'max-age=0'),
]

url = 'https://duckduckgo.com/html/?q=' + urllib.parse.quote('current weather Siliguri')

try:
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    })
    
    with opener.open(req, timeout=15) as resp:
        raw = resp.read()
        if resp.headers.get('Content-Encoding') == 'gzip':
            raw = gzip.decompress(raw)
        page = raw.decode('utf-8', errors='replace')
    
    print('With cookies - Page length:', len(page))
    with open('ddg_cookies2.html', 'w', encoding='utf-8') as f:
        f.write(page[:50000])
    
    if 'captcha' in page.lower() or 'challenge' in page.lower() or 'anomaly' in page.lower():
        print('CAPTCHA/Challenge detected!')
    else:
        print('No CAPTCHA detected')
        if 'result' in page.lower() or 'snippet' in page.lower():
            print('Results found!')

except Exception as e:
    print('Error:', e)
    import traceback
    traceback.print_exc()