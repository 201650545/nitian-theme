# -*- coding: utf-8 -*-
"""open3D 改 Blob 模块加载（绕过 MIME 限制）"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

old = """\t\t\t\tif (!v3dInit) {
\t\t\t\t\tconst THREE = await import(A + "/ui/vendor/three.module.js");
\t\t\t\t\tconst { GLTFLoader } = await import(A + "/ui/vendor/addons/loaders/GLTFLoader.js");
\t\t\t\t\tconst { OrbitControls } = await import(A + "/ui/vendor/addons/controls/OrbitControls.js");"""
new = """\t\t\t\tif (!v3dInit) {
\t\t\t\t\tconst asModule = async (path) => {
\t\t\t\t\t\tconst txt = await (await fetch(path)).text();
\t\t\t\t\t\treturn URL.createObjectURL(new Blob([txt], { type: "application/javascript" }));
\t\t\t\t\t};
\t\t\t\t\tconst threeUrl = await asModule(A + "/ui/vendor/three.module.js");
\t\t\t\t\tconst THREE = await import(threeUrl);
\t\t\t\t\tconst fixup = async (path) => {
\t\t\t\t\t\tconst txt = await (await fetch(path)).text();
\t\t\t\t\t\treturn URL.createObjectURL(new Blob([txt.split("\\"three\\"").join("\\"" + threeUrl + "\\"")], { type: "application/javascript" }));
\t\t\t\t\t};
\t\t\t\t\tconst { GLTFLoader } = await import(await fixup(A + "/ui/vendor/addons/loaders/GLTFLoader.js"));
\t\t\t\t\tconst { OrbitControls } = await import(await fixup(A + "/ui/vendor/addons/controls/OrbitControls.js"));"""
assert old in c, "open3d anchor missing"
c = c.replace(old, new, 1)
f.write_text(c, encoding="utf-8")
print("blob loader OK")
