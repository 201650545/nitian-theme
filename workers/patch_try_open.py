# -*- coding: utf-8 -*-
"""补 try { 开头"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

T4 = "\t" * 4
old = T4 + 'ld.style.display = ""; ld.textContent = "3D 资产加载中…";' + "\n" + T4 + "if (!v3dInit) {"
assert old in c, "start anchor"
new = (T4 + 'ld.style.display = ""; ld.textContent = "3D 资产加载中…";' + "\n" +
       T4 + "try {\n" + T4 + "if (!v3dInit) {")
c = c.replace(old, new, 1)
f.write_text(c, encoding="utf-8")
print("try { added")
