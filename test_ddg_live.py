import urllib.request
import urllib.parse
import ssl
import gzip
import re
import html

url = 'https://duckduckgo.com/html/?q=' + urllib.parse.quote('current weather Siliguri')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

with urllib.request.urlopen(urllib.request.Request('https://duckduckgo.com/html/?q=' + urllib.parse.quote('current weather Siliguri'), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}), timeout=15, context=ssl.create_default_context()) as resp:
    raw = resp.read()
    if resp.headers.get('Content-Encoding') == 'gzip':
        raw = gzip.decompress(raw)
    page = raw.decode('utf-8', errors='replace')

print('DDG Page length:', len(page))

# Check for CAPTCHA
if 'captcha' in page.lower() or 'challenge' in page.lower() or 'anomaly' in page.lower():
    print('CAPTCHA detected!')
else:
    print('No CAPTCHA')

# Check what's in the page
import re
_TITLE_RE = re.compile(r'class="result__a"[^>]*href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>')
_SNIPPET_RE = re.compile(r'class="result__snippet"[^>]*>(?P<snippet>.*?)</a>')
titles = list(_TITLE_RE.finditer(page))
snippets = list(_SNIPPET_RE.finditer(page))
print('Title matches:', len(titles))
print('Snippet matches:', len(snippets))

if len(titles) > 0:
    for m in titles[:3]:
        print('Title:', m.group('title')[:100])
        print('Href:', m.group('href')[:100])

# Save page for inspection
with open('ddg_live_debug.html', 'w', encoding='utf-8') as f:
    f.write(page[:50000])
print('Saved page to ddg_live_debug.html')