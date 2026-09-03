# -*- coding: utf-8 -*-
"""open3D 错误透出"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

T4 = "\t" * 4
T5 = "\t" * 5
old = T4 + 'ld.style.display = ""; ld.textContent = "3D 资产加载中…";' + "\n" + T4 + "if (!v3dInit) {"
assert old in c, "start anchor"
new = (T4 + 'ld.style.display = ""; ld.textContent = "3D 资产加载中…";' + "\n" +
       T4 + "try {\n" + T4 + "if (!v3dInit) {")
c = c.replace(old, new, 1)

old2 = T5 + "v3dInit = true;\n" + T4 + "}\n" + T4 + "}"
assert old2 in c, "end anchor"
new2 = (T5 + "v3dInit = true;\n" +
        T4 + "}\n" +
        T4 + '} catch (e) { ld.style.display = ""; ld.textContent = "3D-ERR: " + String(e && e.message ? e.message : e).slice(0, 170); }\n' +
        T4 + "}")
c = c.replace(old2, new2, 1)

f.write_text(c, encoding="utf-8")
print("try/catch OK")
