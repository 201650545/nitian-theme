# -*- coding: utf-8 -*-
"""九桥阈值补修（Infinity 行此前未匹配）"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")
pat = re.compile(r'(R\("24_qiao9".*?, )[-\de.]+, Infinity(, )')
c, k = pat.subn(lambda m: m.group(1) + "1e19, Infinity" + m.group(2), c, count=1)
f.write_text(c, encoding="utf-8")
print("qiao9 fixed:", k)
