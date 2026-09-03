# -*- coding: utf-8 -*-
"""3D 模型按境界切换"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

T5 = "\t" * 5

# 1) 模型映射 + 记录当前加载模型
old = T5 + "let v3dInit = false, v3dStop = null;"
assert old in c, "v3dInit anchor"
new = (T5 + "let v3dInit = false, v3dStop = null, v3dLoadedModel = \"\";\n" +
       T5 + "const v3dModelFor = (rid) => {\n" +
       T5 + "\tconst n = parseInt(rid, 10);\n" +
       T5 + "\tif (n >= 6 && n <= 8) return A + \"/ui/models/nianfan2.glb\";\n" +
       T5 + "\tif (n >= 9) return A + \"/ui/models/movie1.glb\";\n" +
       T5 + "\treturn A + \"/ui/models/wanglin_3d.glb\";\n" +
       T5 + "};")
c = c.replace(old, new, 1)

# 2) 加载前：若上次模型不同则清理旧场景对象并重载
old = T5 + 'const loader = new GLTFLoader();\n' + T5 + 'loader.load(A + "/ui/models/wanglin_3d.glb", (g) => {'
assert old in c, "loader anchor"
new = (T5 + 'const loader = new GLTFLoader();\n' +
       T5 + "const wantModel = v3dModelFor(REALMS[idx].id);\n" +
       T5 + "if (v3dLoadedModel && v3dLoadedModel !== wantModel) {\n" +
       T5 + "\tscene.clear();\n" +
       T5 + "\tscene.add(new THREE.AmbientLight(0xffffff, 1.1));\n" +
       T5 + "\tconst k2 = new THREE.DirectionalLight(0xfff2d0, 2.2); k2.position.set(3, 5, 4); scene.add(k2);\n" +
       T5 + "\tconst r2 = new THREE.DirectionalLight(0x7fb2e8, 1.4); r2.position.set(-4, 2, -3); scene.add(r2);\n" +
       T5 + "}\n" +
       T5 + "v3dLoadedModel = wantModel;\n" +
       T5 + 'loader.load(wantModel, (g) => {')
assert old in c, "loader2 anchor"
c = c.replace(old, new, 1)

f.write_text(c, encoding="utf-8")
print("realm 3D switching OK")
