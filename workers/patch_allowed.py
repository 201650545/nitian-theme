# -*- coding: utf-8 -*-
"""host ALLOWED 加 /animations/"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\src\index.ts")
c = f.read_text(encoding="utf-8")
old = "['/officials/', join(PROJECT_ROOT, 'workers', 'officials') + sep],"
assert old in c, "allowed anchor"
new = (
    "['/officials/', join(PROJECT_ROOT, 'workers', 'officials') + sep],\n"
    "  ['/animations/', join(PROJECT_ROOT, 'assets', 'animations') + sep],"
)
c = c.replace(old, new, 1)
f.write_text(c, encoding="utf-8")
print("animations route added")
