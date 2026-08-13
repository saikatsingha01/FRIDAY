import sys
sys.path.insert(0, r'C:\project friday\src')
from skills.web_search import QwantEngine

engine = QwantEngine()
results = engine.search('current weather Siliguri', 5)
print(f'Qwant results: {len(results)}')
for r in results:
    print(f'  Title: {r["title"][:80]}')
    print(f'  URL: {r["url"][:80]}')
    print(f'  Snippet: {r["snippet"][:100]}')
    print('---')