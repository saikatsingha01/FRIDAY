with open('qwant_full.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Find result containers
matches = list(re.finditer(r'<div[^>]*class=\"[^"]*result', content, re.IGNORECASE))
print(f'Result divs: {len(matches)}')
for m in matches[:5]:
    print(content[m.start():m.start()+300])
    print('---')