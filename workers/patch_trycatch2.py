# -*- coding: utf-8 -*-
"""open3D try/catch（修正版）"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

old = "\t\t\t\t\tv3dInit = true;\n\t\t\t\t}\n\t\t\t}"
assert old in c, "end anchor"
new = (
    "\t\t\t\t\tv3dInit = true;\n"
    "\t\t\t\t}\n"
    "\t\t\t\t} catch (e) {\n"
    "\t\t\t\t\tconst ld = document.querySelector(\"#nitian-host\").shadowRoot.querySelector(\".v3d .ld\");\n"
    "\t\t\t\t\tif (ld) { ld.style.display = \"\"; ld.textContent = \"3D-ERR: \" + String(e && e.message ? e.message : e).slice(0, 170); }\n"
    "\t\t\t\t}\n"
    "\t\t\t}"
)
c = c.replace(old, new, 1)
f.write_text(c, encoding="utf-8")
print("try/catch OK")
