import urllib.request
import urllib.parse
import re
import ssl

url = 'https://duckduckgo.com/html/?q=' + urllib.parse.quote('current weather Siliguri')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

with urllib.request.urlopen(req, timeout=15, context=ssl_context) as resp:
    page = resp.read().decode('utf-8', errors='replace')

print('Page length:', len(page))

_TITLE_RE = re.compile(r'class="result__a"[^>]*href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>')
_SNIPPET_RE = re.compile(r'class="result__snippet"[^>]*>(?P<snippet>.*?)</a>')

titles = list(_TITLE_RE.finditer(page))
snippets = list(_SNIPPET_RE.finditer(page))
print('Title matches:', len(titles))
print('Snippet matches:', len(snippets))

for m in titles[:5]:
    print('Title:', m.group('title'))
    print('Href:', m.group('href'))
    print('---')