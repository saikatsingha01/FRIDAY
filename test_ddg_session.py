import urllib.parse
import urllib.request
import re
import http.cookiejar

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

# Use cookie jar for session persistence
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
opener.addheaders = [(k, v) for k, v in _HEADERS.items()]

# First, visit the homepage to get cookies
try:
    with opener.open("https://duckduckgo.com/", timeout=15) as resp:
        home_page = resp.read().decode("utf-8", errors="replace")
    print("Home page length:", len(home_page))
    
    # Now search
    query = "weather in Siliguri"
    url = "https://duckduckgo.com/html/?q=" + urllib.parse.quote(query) + "&kl=us-en&kp=-1"
    
    with opener.open(url, timeout=15) as resp:
        page = resp.read().decode("utf-8", errors="replace")
    
    print("Page length:", len(page))
    _TITLE_RE = re.compile(r'class="result__a"[^>]*href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>')
    titles = list(_TITLE_RE.finditer(page))
    print("Title matches:", len(titles))
    for m in titles[:5]:
        print("Title:", m.group("title")[:100])
        print("Href:", m.group("href")[:100])
    
    _SNIPPET_RE = re.compile(r'class="result__snippet"[^>]*>(?P<snippet>.*?)</a>')
    snippets = list(_SNIPPET_RE.finditer(page))
    print("Snippet matches:", len(snippets))
    for m in snippets[:5]:
        print("Snippet:", m.group("snippet")[:150])
        
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()