# -*- coding: utf-8 -*-
import json
with open(r'D:\游戏\逆天主题\workers\T2-编年史底稿.json', encoding='utf-8') as f:
    data = json.load(f)

def find(obj, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            s = str(k) + str(v)
            if '逆之意境' in s or '逆意' in s:
                print(f'{path}.{k}: {str(v)[:100]}')
            find(v, f'{path}.{k}')
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            find(v, f'{path}[{i}]')

find(data)
print('---treasures---')
for i, t in enumerate(data['treasures']):
    if '逆' in str(t):
        print(i, ':', json.dumps(t, ensure_ascii=False)[:200])
print('---events---')
for i, e in enumerate(data['events']):
    if '逆' in str(e) or '妖灵' in str(e):
        print(i, ':', json.dumps(e, ensure_ascii=False)[:200])
print('---realm wending note---')
print(data['realm_ranges']['wending'].get('note', '')[:400])
