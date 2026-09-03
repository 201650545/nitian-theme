# -*- coding: utf-8 -*-
import json
with open(r'D:\逆天主题\workers\T2-编年史底稿.json', encoding='utf-8') as f:
    data = json.load(f)

for key in ['events', 'breakthroughs', 'arts', 'scenes', 'quotes']:
    arr = data.get(key, [])
    for i, item in enumerate(arr):
        s = json.dumps(item, ensure_ascii=False)
        if '逆之意境' in s or '逆意' in s or (key == 'events' and i == 64) or (key == 'breakthroughs' and i == 6) or (key == 'arts' and i == 6) or (key == 'scenes' and i == 15) or (key == 'quotes' and i == 19):
            print(f'=== {key}[{i}] ===')
            print(json.dumps(item, ensure_ascii=False, indent=2))
            print()
