with open('qwant_full.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Find all <a> tags with href
matches = list(re.finditer(r'<a[^>]*href="([^"]+)"', content))
print(f'Total links: {len(matches)}')
for m in matches[:20]:
    print(m.group(0)[:200])
    print('---')