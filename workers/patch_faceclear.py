# -*- coding: utf-8 -*-
"""破境视频播放时：印章/法印移到底部不遮脸"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

# 在 .bt.playvid 规则后追加：印章/法印下移缩小子不遮脸；判词下移
old = ".bt.playvid .flash,.bt.playvid .ring,.bt.playvid .shard{display:none}"
assert old in c, "playvid anchor"
new = (
    old + "\n"
    ".bt.playvid .newseal,.bt.playvid .glyph{width:92px;height:92px;margin-left:-46px;left:50%;top:auto;bottom:6%;animation:none;opacity:1;font-size:30px;border-width:2px;box-shadow:0 0 30px var(--m)}\n"
    ".bt.playvid .verdict{bottom:15%;animation:vfade 1.2s 1.2s both}\n"
    ".bt.playvid .verdict h2{font-size:26px}"
)
c = c.replace(old, new, 1)
f.write_text(c, encoding="utf-8")
print("face-clear overlay OK")
