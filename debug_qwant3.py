with open('qwant_full.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', content))
print(f'Total links: {len(matches)}')
for m in matches[:20]:
    url = m.group(1)
    text = m.group(2)
    if 'weather' in text.lower() or 'siliguri' in text.lower() or 'temperature' in text.lower() or 'current' in text.lower():
        print(f'URL: {m.group(1)[:100]}')
        print(f'Text: {m.group(2)[:100]}')
        print('---')