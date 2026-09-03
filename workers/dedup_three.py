# -*- coding: utf-8 -*-
"""去重 TWO THREE 声明"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")
count = c.count("const THREE = await import(threeUrl);")
if count == 2:
    # 保留第一条，删除第二条
    first = c.find("const THREE = await import(threeUrl);")
    second = c.find("const THREE = await import(threeUrl);", first + 1)
    # 删除第二条所在行
    line_start = c.rfind("\n", 0, second) + 1
    line_end = c.find("\n", second)
    c = c[:line_start] + c[line_end + 1:]
    print("dedup done")
else:
    print("count =", count, "skip")
f.write_text(c, encoding="utf-8")
