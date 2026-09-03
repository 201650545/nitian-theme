# -*- coding: utf-8 -*-
import json
with open(r'D:\游戏\逆天主题\workers\T2-编年史底稿.json', encoding='utf-8') as f:
    data = json.load(f)

print('TOP KEYS:', list(data.keys()))
print()
print('structure keys:', list(data['structure'].keys()))
print()
rr = data['structure']['realm_ranges'][6]
print('realm_ranges[6] name:', rr.get('name'))
print('chapters:', rr.get('chapters'))
print('breakthrough_chapter:', rr.get('breakthrough_chapter'))
print('age:', rr.get('age'))
print('note:', rr.get('note'))
print()
print('parts[3]:', json.dumps(data['structure']['parts'][3], ensure_ascii=False, indent=2))
