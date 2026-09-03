# -*- coding: utf-8 -*-
"""岳天尊 → 跃天尊 全量修正"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
targets = [
    r"D:\逆天主题\dsh-plugin\pkg\lib\client.js",
    r"D:\逆天主题\workers\编年史彩蛋.json",
    r"D:\逆天主题\assets\ui\chronicle.json",
    r"D:\逆天主题\workers\gpt_extend_eggs.json",
]
for t in targets:
    p = Path(t)
    if not p.exists():
        continue
    c = p.read_text(encoding="utf-8")
    n = c.count("岳天尊")
    if n:
        c = c.replace("岳天尊", "跃天尊")
        p.write_text(c, encoding="utf-8")
    print(p.name, ":", n, "处修正")
