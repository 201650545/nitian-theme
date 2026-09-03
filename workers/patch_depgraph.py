# -*- coding: utf-8 -*-
"""open3D 依赖图解析：three → BufferGeometryUtils → GLTFLoader/OrbitControls"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

T = "\t" * 5
old_start = '\t\t\t\t\tconst asModule = async (path) => {'
old_end = '\t\t\t\t\tconst { OrbitControls } = await import(await fixup(A + "/ui/vendor/addons/controls/OrbitControls.js"));'
i0 = c.index(old_start)
i1 = c.index(old_end) + len(old_end)
old = c[i0:i1]

new = (
    T + "const asModule = async (path) => {\n" +
    T + "\tconst txt = await (await fetch(path)).text();\n" +
    T + "\treturn URL.createObjectURL(new Blob([txt], { type: \"application/javascript\" }));\n" +
    T + "};\n" +
    T + "const mk = async (path, repl) => {\n" +
    T + "\tlet txt = await (await fetch(path)).text();\n" +
    T + "\tfor (const [spec, url] of Object.entries(repl)) {\n" +
    T + "\t\ttxt = txt.split(\"'\" + spec + \"'\").join(\"'\" + url + \"'\");\n" +
    T + "\t\ttxt = txt.split('\"' + spec + '\"').join('\"' + url + '\"');\n" +
    T + "\t}\n" +
    T + "\treturn URL.createObjectURL(new Blob([txt], { type: \"application/javascript\" }));\n" +
    T + "};\n" +
    T + "const threeUrl = await asModule(A + \"/ui/vendor/three.module.js\");\n" +
    T + "const bufUrl = await mk(A + \"/ui/vendor/addons/utils/BufferGeometryUtils.js\", { three: threeUrl });\n" +
    T + "const gltfUrl = await mk(A + \"/ui/vendor/addons/loaders/GLTFLoader.js\", { three: threeUrl, \"../utils/BufferGeometryUtils.js\": bufUrl });\n" +
    T + "const orbUrl = await mk(A + \"/ui/vendor/addons/controls/OrbitControls.js\", { three: threeUrl });\n" +
    T + "const { GLTFLoader } = await import(gltfUrl);\n" +
    T + "const { OrbitControls } = await import(orbUrl);"
)
c = c.replace(old, new, 1)
f.write_text(c, encoding="utf-8")
print("dep-graph loader OK")
