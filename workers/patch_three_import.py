# -*- coding: utf-8 -*-
"""补回 THREE import"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

T5 = "\t" * 5
old = T5 + "const { OrbitControls } = await import(orbUrl);"
assert old in c, "anchor"
new = old + "\n" + T5 + "const THREE = await import(threeUrl);"
c = c.replace(old, new, 1)
f.write_text(c, encoding="utf-8")
print("THREE import OK")
