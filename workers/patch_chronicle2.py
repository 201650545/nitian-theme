# -*- coding: utf-8 -*-
"""编年史彩蛋接入（锚点修正版）"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

T = "\t"

# 1) 编年史加载 + 彩蛋轮播（锚点：async function poll）
old = T * 3 + "async function poll() {"
new = (
    T * 3 + "// 编年史彩蛋（assets/ui/chronicle.json）\n" +
    T * 3 + "let CHRON = {};\n" +
    T * 3 + 'fetch(A + "/ui/chronicle.json").then(r => r.ok ? r.json() : null).then(j => {\n' +
    T * 4 + "if (j && j.realms) { CHRON = j.realms; const q0 = (CHRON[REALMS[idx].id] || {}).quotes; if (q0 && q0[0]) ui.eq.textContent = q0[0].text; }\n" +
    T * 3 + "}).catch(() => { });\n" +
    T * 3 + "setInterval(() => {\n" +
    T * 4 + "const cr = CHRON[REALMS[idx].id];\n" +
    T * 4 + 'if (!cr || !cr.eggs || !cr.eggs.length) return;\n' +
    T * 4 + 'const t = $(".eggtoast"); if (!t) return;\n' +
    T * 4 + 't.querySelector(".t").textContent = cr.eggs[Math.floor(Math.random() * cr.eggs.length)];\n' +
    T * 4 + 't.classList.add("on");\n' +
    T * 4 + 'setTimeout(() => t.classList.remove("on"), 7000);\n' +
    T * 3 + "}, 100000);\n\n" +
    T * 3 + "async function poll() {"
)
assert old in c, "poll anchor missing"
c = c.replace(old, new, 1)

# 2) 心魔劫语录
old2 = 'ui.sayQ.textContent = QUOTES[rr.id] || QUOTES.default;'
new2 = ("const crQ = (CHRON[rr.id] || {}).quotes || [];\n" +
        T * 4 + 'ui.sayQ.textContent = (crQ.length ? crQ[Math.floor(Math.random() * crQ.length)].text : "") || QUOTES[rr.id] || QUOTES.default;')
assert old2 in c, "doom anchor missing"
c = c.replace(old2, new2, 1)

# 3) 破境判词：名场面
old3 = "ui.vH.textContent = r.name; ui.vP.textContent = r.sub;"
new3 = ("const crS = (CHRON[r.id] || {}).scene;\n" +
        T * 4 + "ui.vH.textContent = r.name; ui.vP.textContent = crS ? String(crS).slice(0, 46) : r.sub;")
assert old3 in c, "verdict anchor missing"
c = c.replace(old3, new3, 1)

# 4) 空状态语录
old4 = "ui.eq.textContent = QUOTES[r.id] || QUOTES.default;"
new4 = "const q0 = ((CHRON[r.id] || {}).quotes || [])[0]; ui.eq.textContent = (q0 && q0.text) || QUOTES[r.id] || QUOTES.default;"
assert old4 in c, "empty anchor missing"
c = c.replace(old4, new4, 1)

f.write_text(c, encoding="utf-8")
print("chronicle fused 4/4")
