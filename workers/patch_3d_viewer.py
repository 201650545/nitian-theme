# -*- coding: utf-8 -*-
"""3D 王林查看器：立牌 3D 按钮 → 全屏 three.js 可旋转模型"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

# 1) CSS
old = ".insp{position:absolute;inset:0;pointer-events:auto;display:none;"
new = """.v3d{position:absolute;inset:0;pointer-events:auto;display:none;background:radial-gradient(ellipse at 50% 60%,#101826,#04060a);z-index:6}
.v3d.on{display:block}
.v3d canvas{width:100%;height:100%;display:block}
.v3d .ld{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:#e6ddc8;font-size:13px;letter-spacing:.2em}
.v3d .x{position:absolute;right:24px;top:24px;color:#8a93a6;font-size:12px;letter-spacing:.2em;cursor:pointer;border:1px solid #2a3348;border-radius:999px;padding:7px 24px;pointer-events:auto}
.v3d .x:hover{color:var(--m);border-color:var(--m)}
.v3d .hint{position:absolute;left:50%;bottom:26px;transform:translateX(-50%);color:#79839a;font-size:11px;letter-spacing:.24em}
.insp{position:absolute;inset:0;pointer-events:auto;display:none;"""
assert old in c, "css anchor"
c = c.replace(old, new, 1)

# 2) DOM
old = '<div class="insp"><img alt=""><div class="q"></div><div class="x">收起神游</div></div>'
new = ('<div class="v3d"><canvas></canvas><div class="ld">3D 资产加载中…</div>'
       '<div class="x">收起 3D</div><div class="hint">拖拽旋转 · 滚轮缩放</div></div>\n'
       '<div class="insp"><img alt=""><div class="q"></div><div class="x">收起神游</div></div>')
assert old in c, "dom anchor"
c = c.replace(old, new, 1)

# 3) 立牌 3D 按钮
old = '<div class="comp"><button class="cmin" title="收起/展开">–</button>'
new = '<div class="comp"><button class="cmin" title="收起/展开">–</button><button class="c3d" title="3D 模式">3D</button>'
assert old in c, "comp anchor"
c = c.replace(old, new, 1)

# 4) c3d 按钮 CSS
old = ".comp .cmin{position:absolute;top:4px;right:4px;"
new = (".comp .c3d{position:absolute;top:4px;right:28px;width:26px;height:20px;border-radius:9px;border:1px solid #2a3348;"
       "background:rgba(11,14,21,.92);color:#8a93a6;font-size:9px;cursor:pointer;z-index:3;padding:0}\n"
       ".comp .c3d:hover{color:var(--m);border-color:var(--m)}\n"
       ".comp.mini .c3d{display:none}\n"
       ".comp .cmin{position:absolute;top:4px;right:4px;")
assert old in c, "c3d css anchor"
c = c.replace(old, new, 1)

# 5) 3D 逻辑
old = '$(".cmin").addEventListener("click", (e) => {'
new = """let v3dInit = false, v3dStop = null;
			async function open3D() {
				const ov = $(".v3d"); ov.classList.add("on");
				const cv = ov.querySelector("canvas"), ld = ov.querySelector(".ld");
				ld.style.display = ""; ld.textContent = "3D 资产加载中…";
				if (!v3dInit) {
					const THREE = await import(A + "/ui/vendor/three.module.js");
					const { GLTFLoader } = await import(A + "/ui/vendor/addons/loaders/GLTFLoader.js");
					const { OrbitControls } = await import(A + "/ui/vendor/addons/controls/OrbitControls.js");
					const renderer = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true });
					const scene = new THREE.Scene();
					const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
					camera.position.set(0, 0.6, 3.2);
					scene.add(new THREE.AmbientLight(0xffffff, 1.1));
					const key = new THREE.DirectionalLight(0xfff2d0, 2.2); key.position.set(3, 5, 4); scene.add(key);
					const rim = new THREE.DirectionalLight(0x7fb2e8, 1.4); rim.position.set(-4, 2, -3); scene.add(rim);
					const loader = new GLTFLoader();
					loader.load(A + "/ui/models/wanglin_3d.glb", (g) => {
						const m = g.scene;
						const box = new THREE.Box3().setFromObject(m);
						const size = box.getSize(new THREE.Vector3()), ctr = box.getCenter(new THREE.Vector3());
						const s = 2.2 / Math.max(size.x, size.y, size.z);
						m.scale.setScalar(s);
						m.position.sub(ctr.multiplyScalar(s));
						m.rotation.y = 0.4;
						scene.add(m);
						ld.style.display = "none";
					}, (ev) => { if (ev.total) ld.textContent = "3D 资产加载中… " + Math.round(ev.loaded / ev.total * 100) + "%"; });
					const ctl = new OrbitControls(camera, cv);
					ctl.autoRotate = true; ctl.autoRotateSpeed = 2.2; ctl.enableDamping = true;
					let alive = true;
					(function loop() { if (!alive) return; requestAnimationFrame(loop); ctl.update(); renderer.render(scene, camera); })();
					const fit = () => { const w = ov.clientWidth, hh = ov.clientHeight; renderer.setSize(w, hh, false); camera.aspect = w / hh; camera.updateProjectionMatrix(); };
					fit(); window.addEventListener("resize", fit);
					v3dStop = () => { alive = false; window.removeEventListener("resize", fit); };
					v3dInit = true;
				}
			}
			$(".c3d").addEventListener("click", (e) => { e.stopPropagation(); open3D(); });
			$(".v3d .x").addEventListener("click", () => { $(".v3d").classList.remove("on"); if (v3dStop) v3dStop(); });
			$(".cmin").addEventListener("click", (e) => {"""
assert old in c, "logic anchor"
c = c.replace(old, new, 1)

f.write_text(c, encoding="utf-8")
print("3D viewer fused 5/5")
