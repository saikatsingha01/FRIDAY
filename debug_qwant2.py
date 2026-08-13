with open('qwant_debug.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Look for actual result links - search for the pattern around weather/siliguri
import re
matches = list(re.finditer(r'href="([^"]+)"', open('qwant_debug.html', 'r', encoding='utf-8').read()))
print(f'Total href matches: {len(matches)}')
for m in matches[:20]:
    print(m.group(0)[:100])

# Look for actual result patterns
content = open('qwant_debug.html', 'r', encoding='utf-8').read()
# Find result containers
for m in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', content):
    print(f'Link: {m.group(1)[:80]} -> Text: {m.group(1)[:80]}')
    if len(matches) > 20:
        break