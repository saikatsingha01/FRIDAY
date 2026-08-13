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

# Try Brave Search
query = "current price of nvidia rtx 5070"
url = "https://search.brave.com/search?q=" + urllib.parse.quote(query)

# Use cookie jar
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
opener.addheaders = [(k, v) for k, v in _HEADERS.items()]

try:
    with opener.open(url, timeout=15) as resp:
        page = resp.read().decode("utf-8", errors="replace")
    
    print("Page length:", len(page))
    print("--- PAGE START ---")
    print(page[:5000])
    print("--- PAGE END ---")
except Exception as e:
    print("Error:", e)