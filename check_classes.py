with open('ddg_page.html', 'r', encoding='utf-8') as f:
    content = f.read()
import re
classes = re.findall(r'class="([^"]+)"', content)
from collections import Counter
c = Counter(classes)
for cls, count in c.most_common(30):
    print(f'{cls}: {count}')