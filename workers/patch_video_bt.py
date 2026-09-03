# -*- coding: utf-8 -*-
"""破境演出视频接入引擎"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

# 1) CSS: 视频层
old = ".bt.major{animation:bshake 2.6s ease-in-out}"
new = (
    ".bt .vid{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:none;background:#04060a}\n"
    ".bt.playvid .vid{display:block;animation:vfade 1s ease}\n"
    ".bt.playvid .flash,.bt.playvid .ring,.bt.playvid .shard{display:none}\n"
    "@keyframes vfade{from{opacity:0}to{opacity:1}}\n"
    ".bt.major{animation:bshake 2.6s ease-in-out}"
)
assert old in c, "css anchor"
c = c.replace(old, new, 1)

# 2) DOM: video 元素
old = '<div class="bt"><div class="flash"></div><div class="ring"></div>'
new = '<div class="bt"><video class="vid" muted playsinline></video><div class="flash"></div><div class="ring"></div>'
assert old in c, "dom anchor"
c = c.replace(old, new, 1)

# 3) enter(): 大境界播视频
old = 'ui.bt.classList.toggle("major", major);'
new = (
    'ui.bt.classList.toggle("major", major);\n' +
    "\t\t\t\tconst vid = ui.bt.querySelector(\".vid\");\n" +
    "\t\t\t\tif (major && vid) {\n" +
    "\t\t\t\t\tvid.src = A + \"/animations/breakthrough_major.mp4\";\n" +
    "\t\t\t\t\tvid.currentTime = 0;\n" +
    "\t\t\t\t\tui.bt.classList.add(\"playvid\");\n" +
    "\t\t\t\t\tvid.play().catch(() => { });\n" +
    "\t\t\t\t\tvid.onended = () => ui.bt.classList.remove(\"playvid\");\n" +
    "\t\t\t\t}"
)
assert old in c, "enter anchor"
c = c.replace(old, new, 1)

# 4) 收尾时长
old = "setTimeout(() => { ui.bt.classList.remove(\"on\", \"major\"); [...ui.bt.querySelectorAll(\".pt\")].forEach(x => x.remove()); }, major ? 6800 : 4300);"
new = "setTimeout(() => { ui.bt.classList.remove(\"on\", \"major\", \"playvid\"); [...ui.bt.querySelectorAll(\".pt\")].forEach(x => x.remove()); try { vid.pause(); } catch { } }, major ? 7600 : 4300);"
assert old in c, "timer anchor"
c = c.replace(old, new, 1)

f.write_text(c, encoding="utf-8")
print("video breakthrough fused 4/4")
