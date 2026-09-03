# -*- coding: utf-8 -*-
"""编年史 id 别名映射（新拆分 id → 旧爬取 id）"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

T3 = "\t" * 3

# 1) 加别名表 + chronOf 助手（插在 CHRON 声明后）
old = T3 + "let CHRON = {};"
assert old in c, "chron anchor"
new = (
    T3 + "let CHRON = {};\n" +
    T3 + 'const chronAlias = { "15_kongjin":"15_kongjie","16_kongzun":"15_kongjie","17_kongyue":"15_kongjie","18_kongda":"15_kongjie",' +
    '"19_qiao1":"16_qiao1","20_qiao2":"17_qiao2","21_qiao3":"18_qiao3","22_qiao4":"19_qiao4","23_qiao5":"20_qiao5",' +
    '"24_qiao6":"21_qiao6","25_qiao7":"22_qiao7","26_qiao8":"23_qiao8","27_qiao9":"24_qiao9" };\n' +
    T3 + "const chronOf = (rid) => CHRON[chronAlias[rid] || rid] || {};"
)
c = c.replace(old, new, 1)

# 2) 替换 4 处 CHRON[..] 查询为 chronOf
def repl(c, old, new):
    assert old in c, "missing: " + old[:60]
    return c.replace(old, new, 1)

c = repl(c, "(CHRON[REALMS[idx].id] || {}).quotes", "chronOf(REALMS[idx].id).quotes")
c = repl(c, "const cr = CHRON[REALMS[idx].id];", "const cr = chronOf(REALMS[idx].id);")
c = repl(c, "const crQ = (CHRON[rr.id] || {}).quotes || [];", "const crQ = chronOf(rr.id).quotes || [];")
c = repl(c, "const crS = (CHRON[r.id] || {}).scene;", "const crS = chronOf(r.id).scene;")
c = repl(c, "const q0 = ((CHRON[r.id] || {}).quotes || [])[0];", "const q0 = chronOf(r.id).quotes[0];")

f.write_text(c, encoding="utf-8")
print("chronAlias + chronOf OK")