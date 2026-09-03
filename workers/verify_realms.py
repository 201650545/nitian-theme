# -*- coding: utf-8 -*-
"""验证 REALMS 数组完整 + 小境界故事文字"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
c = open(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js", encoding="utf-8").read()

# 统计 R("xx 定义
ids = re.findall(r'R\("(\d+_\w+)"', c)
print("REALMS 节点数:", len(ids))
print(ids)

# 小境界判词（enter 的 verdictP）— 检查是否已有 scene 故事文字
i = c.find("const crS = (CHRON[r.id] || {}).scene;")
print()
print("--- enter verdict 行 ---")
print(c[i - 30:i + 260])