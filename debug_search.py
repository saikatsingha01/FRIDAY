import urllib.parse
import urllib.request
import re

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}

query = "current price of nvidia rtx 5070"
url = "https://duckduckgo.com/html/?q=" + urllib.parse.quote(query)

req = urllib.request.Request(url, headers=_HEADERS)

with urllib.request.urlopen(req, timeout=15) as resp:
    page = resp.read().decode("utf-8", errors="replace")

print("Page length:", len(page))

# Check for title pattern
_TITLE_RE = re.compile(
    r'class="result__a"[^>]*href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>'
)
titles = list(_TITLE_RE.finditer(page))
print("Title matches:", len(titles))

# Check for snippet pattern
_SNIPPET_RE = re.compile(
    r'class="result__snippet"[^>]*>(?P<snippet>.*?)</a>'
)
snippets = list(_SNIPPET_RE.finditer(page))
print("Snippet matches:", len(snippets))

# Print first 5000 chars of page to see structure
print("--- PAGE START ---")
print(page[:5000])
print("--- PAGE END ---")