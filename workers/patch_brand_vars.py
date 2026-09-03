# -*- coding: utf-8 -*-
"""品牌改名 + 侧栏主题变量注入 root"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

# 1) 品牌改名（relabel 字典加一条）
old = '[/^skills$/i, "神通"],'
assert old in c, "relabel anchor missing"
c = c.replace(old, '[/^DSH Local Build$/i, "逆天修行录"],\n\t\t\t[/^skills$/i, "神通"],', 1)

# 2) paint() 注入 root 级 CSS 变量
old2 = 'function paint(i) {\n\t\t\t\tconst r = REALMS[i];\n\t\t\t\tnr.style.setProperty("--m", r.main);'
assert old2 in c, "paint anchor missing"
new2 = (
    'function paint(i) {\n'
    '\t\t\t\tconst r = REALMS[i];\n'
    '\t\t\t\tnr.style.setProperty("--m", r.main);\n'
    '\t\t\t\tconst de = document.documentElement;\n'
    '\t\t\t\tde.style.setProperty("--nit-m", r.main);\n'
    '\t\t\t\tde.style.setProperty("--nit-a", r.accent);\n'
    '\t\t\t\tde.style.setProperty("--nit-seal", "url(" + (r.seal || CH.ningshi) + ")");'
)
c = c.replace(old2, new2, 1)

f.write_text(c, encoding="utf-8")
print("brand rename + root vars OK")
