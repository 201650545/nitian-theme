# -*- coding: utf-8 -*-
"""fixup 双模式替换（匹配转义引号版）"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

BS = chr(92)  # 反斜杠
Q = chr(34)   # 双引号
# JS 源码里的实际文本: txt.split("\"three\"").join("\"" + threeUrl + "\"")
old = (
    'txt.split("' + BS + Q + 'three' + BS + Q + '").join("' + BS + Q + '" + threeUrl + "' + BS + Q + '")'
)
assert old in c, "fixup anchor missing"

new = (
    'txt.split("' + BS + Q + '../three.module.js' + BS + Q + '").join("' + BS + Q + '" + threeUrl + "' + BS + Q + '")'
    + '.split("' + BS + Q + 'three' + BS + Q + '").join("' + BS + Q + '" + threeUrl + "' + BS + Q + '")'
)
c = c.replace(old, new, 1)
f.write_text(c, encoding="utf-8")
print("fixup dual-pattern OK")
