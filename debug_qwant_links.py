with open('qwant_full.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find all links with meaningful text (>20 chars)
matches = list(re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>([^<]{20,})</a>', content, re.IGNORECASE))
print(f'Total links with text >20 chars: {len(matches)}')

for m in matches[:20]:
    url = m.group(1)
    text = m.group(2)
    if 'weather' in m.group(0).lower() or 'siliguri' in m.group(0).lower() or 'temperature' in m.group(0).lower() or 'current' in m.group(0).lower():
        print(f'URL: {m.group(1)[:100]}')
        print(f'Text: {m.group(2)[:100]}')
        print('---')

# Also check for JSON-LD structured data
import json
json_ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
print(f'JSON-LD scripts: {len(json_ld)}')
for script in json_ld[:2]:
    print(script[:500])
    print('---')