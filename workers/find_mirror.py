# -*- coding: utf-8 -*-
"""找 GPT 镜像站 URL"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
targets = [
    r"D:\ai-hub-memory\global\RESOURCES.md",
    r"D:\ai-hub-memory\global\TOOLS.md",
]
pat = re.compile(r"https?://[^\s\)\"<>]+")
for t in targets:
    p = Path(t)
    if not p.exists():
        continue
    c = p.read_text(encoding="utf-8")
    for m in pat.finditer(c):
        u = m.group(0)
        low = u.lower()
        if any(s in low for s in ("gpt", "chat", "mirror", "aibao", "yiyan", "vip")) and "github" not in low:
            print(p.name, "->", u[:110])

# 找操作手册文件
import glob
for pat2 in [r"D:\ai-resource-hub\**\*手册*", r"D:\项目\docs\**\*手册*", r"D:\项目\**\*操作手册*"]:
    for f2 in glob.glob(pat2, recursive=True):
        print("MANUAL:", f2)
