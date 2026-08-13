import sys
sys.path.insert(0, r'C:\project friday\src')
from skills.web_search import DuckDuckGoEngine

engine = DuckDuckGoEngine()
results = engine.search('current weather Siliguri', 5)
print(f'Results: {len(results)}')
for r in results:
    print('Title:', r["title"][:80])
    print('URL:', r["url"][:80])
    print('Snippet:', r["snippet"][:100])
    print('---')