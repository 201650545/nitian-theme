# -*- coding: utf-8 -*-
"""破境视频按大境界选档"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

T4 = "\t" * 4

old = T4 + 'vid.src = A + "/animations/breakthrough_major.mp4";'
assert old in c, "video src anchor"
new = (
    T4 + "const btVid = { 3: \"bt_m\", 6: \"bt_b\", 10: \"bt_t\", 15: \"bt_p\" }[i] || \"breakthrough_major\";\n" +
    T4 + 'vid.src = A + "/animations/" + btVid + ".mp4";'
)
c = c.replace(old, new, 1)
f.write_text(c, encoding="utf-8")
print("bt video per-realm OK")
