# -*- coding: utf-8 -*-
"""fixup 双模式替换：'../three.module.js' 与 "three" 都指向 blob URL"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

Q = chr(39)  # 单引号
old = (
    'return URL.createObjectURL(new Blob([txt.split("' + Q + 'three' + Q + '").join('
    '"' + Q + '" + threeUrl + "' + Q + '")], { type: "application/javascript" }));'
)
assert old in c, "fixup anchor missing"

new = (
    'return URL.createObjectURL(new Blob(['
    'txt.split("' + Q + '../three.module.js' + Q + '").join("' + Q + '" + threeUrl + "' + Q + '")'
    '.split("' + Q + 'three' + Q + '").join("' + Q + '" + threeUrl + "' + Q + '")'
    '], { type: "application/javascript" }));'
)
c = c.replace(old, new, 1)
f.write_text(c, encoding="utf-8")
print("fixup dual-pattern OK")
