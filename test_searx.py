import urllib.parse
import urllib.request
import re
import gzip

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
}

# Try a public Searx instance
query = "weather in Siliguri"
url = "https://searx.be/search?q=" + urllib.parse.quote(query)

req = urllib.request.Request(url, headers=_HEADERS)

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        page = raw.decode("utf-8", errors="replace")
    
    print("Page length:", len(page))
    with open("searx_debug.html", "w", encoding="utf-8") as f:
        f.write(page)
    print("Saved to searx_debug.html")
        
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()