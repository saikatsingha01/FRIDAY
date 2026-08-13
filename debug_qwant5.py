with open('qwant_full.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Check for structured data
json_ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
print(f'JSON-LD scripts: {len(json_ld)}')
for script in json_ld[:2]:
    print(script[:500])
    print('---')

# Check for result containers
import re
for pattern in [r'<article[^>]*>', r'<div[^>]*class="result', r'data-testid', 'data-testid', 'data-result']:
    matches = list(re.finditer(pattern, content, re.IGNORECASE))
    if matches:
        print(f'{pattern}: {len(matches)} matches')