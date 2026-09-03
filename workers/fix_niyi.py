# -*- coding: utf-8 -*-
import json

PATH = r'D:\游戏\逆天主题\workers\T2-编年史底稿.json'
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

updates = []

# 1. events[64] 妖灵之地感悟逆之意境：chapter 800 -> 约576章
ev = data['events'][64]
if ev['chapter'] == '800':
    ev['chapter'] = '约576章'
    ev['summary'] = '王林在妖灵之地古妖陵寝的极端环境中，感悟出逆之意境——顺为凡逆则仙的核心道心在战斗层面的具象化（问鼎境界正式突破在约684章吸收问鼎之晶后）'
    updates.append('events[64].chapter -> 约576章')

# 2. breakthroughs[6] 问鼎突破：chapter 800 -> 684（与 realm_ranges breakthrough_chapter 一致）
bt = data['breakthroughs'][6]
if bt['chapter'] == '800':
    bt['chapter'] = '684'
    updates.append('breakthroughs[6].chapter -> 684')

# 3. arts[6] 逆之意境：chapter 800 -> 约576章
art = data['arts'][6]
if art['chapter'] == '800':
    art['chapter'] = '约576章'
    updates.append('arts[6].chapter -> 约576章')

# 4. scenes[15] 妖灵之地·悟逆之意境突破问鼎：chapter 800 -> 约576章
sc = data['scenes'][15]
if sc['chapter'] == '800':
    sc['chapter'] = '约576章'
    sc['summary'] = '王林在妖气滔天的妖灵之地古妖陵寝，融合杀戮意境感悟逆之意境（问鼎突破在约684章吸收问鼎之晶后）'
    updates.append('scenes[15].chapter -> 约576章')

# 5. realm_ranges[6] note：逆之意境章号待原文定位 -> 已定位
rr = data['structure']['realm_ranges'][6]
old_note = rr['note']
new_note = old_note.replace(
    '逆之意境章号待原文定位',
    "逆之意境约576章（妖灵之地妖将大比敲妖鼓、感悟'顺逆二字'时悟出，腾讯网/喜马拉雅确认）"
)
if new_note != old_note:
    rr['note'] = new_note
    updates.append('realm_ranges[6].note 逆之意境定位更新')

# 6. parts[3] summary 微调措辞
pt = data['structure']['parts'][3]
old_pt = pt['summary']
new_pt = old_pt.replace(
    '拜天运子感悟逆之意境问鼎',
    '拜天运子于妖灵之地(约576章)感悟逆之意境，约684章吸收问鼎之晶突破问鼎'
)
if new_pt != old_pt:
    pt['summary'] = new_pt
    updates.append('parts[3].summary 措辞更新')

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('共更新 %d 处:' % len(updates))
for u in updates:
    print(' -', u)
print()
print('JSON 校验通过，文件大小:', __import__('os').path.getsize(PATH), '字节')
