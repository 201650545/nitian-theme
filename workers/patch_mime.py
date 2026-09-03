# -*- coding: utf-8 -*-
"""host MIME 表补 .js/.glb/.mp4 等"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\src\index.ts")
c = f.read_text(encoding="utf-8")
anchor = "'.svg': 'image/svg+xml',"
assert anchor in c, "mime anchor missing"
add = (
    anchor
    + "\n  '.js': 'application/javascript',"
    + "\n  '.mjs': 'application/javascript',"
    + "\n  '.glb': 'model/gltf-binary',"
    + "\n  '.mp4': 'video/mp4',"
    + "\n  '.zip': 'application/zip',"
)
c = c.replace(anchor, add, 1)
f.write_text(c, encoding="utf-8")
print("MIME added")
