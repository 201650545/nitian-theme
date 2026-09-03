# -*- coding: utf-8 -*-
"""检查 REALMS 尾部 + 硬编码索引"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
c = open(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js", encoding="utf-8").read()
i = c.find('R("15_kongjie"')
print("--- 15_kongjie 行 ---")
print(c[i:i + 340])
print()
print("--- 踏天各桥行 ---")
j = c.find('R("16_qiao1"')
print(c[j:j + 240])
print()
for pat in ["isBridge = i >=", "[i - 15]", "[3, 6, 10, 15]", "{ 3: ", "i < 15", "15_kongjie", "15_kongling"]:
    print(pat, "->", c.count(pat))
