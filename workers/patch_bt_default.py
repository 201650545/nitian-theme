# -*- coding: utf-8 -*-
"""大境界破境默认视频改为官方王林脸版"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

T4 = "\t" * 4
old = T4 + 'const btVid = { 3: "bt_m", 6: "bt_b", 10: "bt_t", 15: "bt_p" }[i] || "breakthrough_major";'
assert old in c, "bt select anchor"
new = T4 + 'const btVid = { 3: "bt_m", 6: "bt_b", 10: "bt_t", 15: "bt_p" }[i] || "bt_wanglin_face";'
c = c.replace(old, new, 1)
f.write_text(c, encoding="utf-8")
print("default bt video = wanglin face")
