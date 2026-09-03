# -*- coding: utf-8 -*-
"""REALMS 全部 15 境接入新徽印 + 大境界破境动画（粒子/三环/震屏）"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

# 1) 每个境界的 seal 字段：null → seal_XX_id.png（15 境全配）
SEALS = {
    "01_ningshi": "A + \"/ui/seals/seal_01_ningshi.png\"",
    "02_zhuji": "A + \"/ui/seals/seal_02_zhuji.png\"",
    "03_jiedan": "A + \"/ui/seals/seal_03_jiedan.png\"",
    "04_yuanying": "A + \"/ui/seals/seal_04_yuanying.png\"",
    "05_huashen": "A + \"/ui/seals/seal_05_huashen.png\"",
    "06_yingbian": "A + \"/ui/seals/seal_06_yingbian.png\"",
    "07_wending": "A + \"/ui/seals/seal_07_wending.png\"",
    "08_yinyang": "A + \"/ui/seals/seal_08_yinyang.png\"",
    "09_kunie": "A + \"/ui/seals/seal_09_kunie.png\"",
    "10_jingnie": "A + \"/ui/seals/seal_10_jingnie.png\"",
    "11_suinie": "A + \"/ui/seals/seal_11_suinie.png\"",
    "12_kongnie": "A + \"/ui/seals/seal_12_kongnie.png\"",
    "13_kongling": "A + \"/ui/seals/seal_13_kongling.png\"",
    "14_kongxuan": "A + \"/ui/seals/seal_14_kongxuan.png\"",
    "15_kongjie": "A + \"/ui/seals/seal_15_kongjie.png\"",
}
n = 0
for rid, seal in SEALS.items():
    # 行内 seal 位置：char 之后、enemy 之前的最后一个参数；现有为 seal 串或 null
    pat = re.compile(r'(R\("%s".*?, )(?:A \+ "/ui/seals/[^"]+"|null)(, )' % rid)
    c, k = pat.subn(lambda m, s=seal: m.group(1) + s + m.group(2), c, count=1)
    n += k
print(f"seal fields: {n}/15")

# 2) CSS：大境界动画（粒子/三环/震屏）
old_css = """.bt .verdict{position:absolute;left:50%;bottom:19%;transform:translateX(-50%);text-align:center;animation:vf 1.6s .9s both;width:100%}"""
new_css = """.bt.major{animation:bshake 2.6s ease-in-out}
@keyframes bshake{0%,100%{transform:none}16%{transform:translate(3px,-2px)}34%{transform:translate(-3px,2px)}52%{transform:translate(2px,2px)}70%{transform:translate(-2px,-1px)}}
.bt.major .flash{background:radial-gradient(circle at 50% 46%,#fffdf2,#ffe9a8 30%,color-mix(in srgb,var(--m) 55%,transparent) 58%,transparent 78%);animation-duration:3.6s}
.bt.major .ring{border-width:3px;box-shadow:0 0 44px var(--m)}
.bt.major .ring.r2{animation-delay:.35s;border-color:#fff3cf}
.bt.major .ring.r3{animation-delay:.7s;border-style:dashed}
.bt .pt{position:absolute;left:50%;top:45%;width:5px;height:5px;border-radius:50%;background:var(--pc,#ffd97a);box-shadow:0 0 8px var(--pc,#ffd97a);animation:ptfly 1.9s cubic-bezier(.15,.75,.3,1) forwards;opacity:0}
@keyframes ptfly{0%{transform:translate(0,0) scale(1.2);opacity:1}100%{transform:translate(var(--px),var(--py)) scale(.15);opacity:0}}
.bt .verdict{position:absolute;left:50%;bottom:19%;transform:translateX(-50%);text-align:center;animation:vf 1.6s .9s both;width:100%}"""
assert old_css in c
c = c.replace(old_css, new_css)

# 3) enter()：大境界判定 + 粒子 + 时长
old_enter = """			function enter(i, silent) {
				idx = i;
				localStorage.setItem(LS.demo, String(Math.max(demoTokens(), REALMS[i].from - realTokens)));
				paint(idx);
				if (silent) return;
				if (opts.audio) { sfxRise(); setTimeout(sfxGong, 900); }
				const r = REALMS[i];
				if (r.seal && i < 15) { ui.newSeal.src = r.seal; ui.newSeal.style.display = ""; ui.glyph.style.display = "none"; }
				else { ui.newSeal.style.display = "none"; ui.glyph.style.display = "flex"; ui.glyph.textContent = i >= 15 ? ["一","二","三","四","五","六","七","八","九"][i - 15] : "境"; }
				ui.vH.textContent = r.name; ui.vP.textContent = r.sub;
				ui.bt.classList.add("on");
				setTimeout(() => ui.bt.classList.remove("on"), 4300);
			}"""
new_enter = """			function enter(i, silent) {
				const prev = idx;
				idx = i;
				localStorage.setItem(LS.demo, String(Math.max(demoTokens(), REALMS[i].from - realTokens)));
				paint(idx);
				if (silent) return;
				const major = i > prev && [3, 6, 10, 15].includes(i);
				if (opts.audio) { sfxRise(); setTimeout(sfxGong, major ? 1200 : 900); }
				const r = REALMS[i];
				if (r.seal && i < 15) { ui.newSeal.src = r.seal; ui.newSeal.style.display = ""; ui.glyph.style.display = "none"; }
				else { ui.newSeal.style.display = "none"; ui.glyph.style.display = "flex"; ui.glyph.textContent = i >= 15 ? ["一","二","三","四","五","六","七","八","九"][i - 15] : "境"; }
				ui.vH.textContent = r.name; ui.vP.textContent = r.sub;
				ui.bt.classList.toggle("major", major);
				if (major) {
					for (let k = 0; k < 46; k++) {
						const p = document.createElement("i");
						p.className = "pt";
						const ang = Math.random() * Math.PI * 2, dist = 240 + Math.random() * 460;
						p.style.setProperty("--px", Math.cos(ang) * dist + "px");
						p.style.setProperty("--py", Math.sin(ang) * dist + "px");
						p.style.setProperty("--pc", ["#ffd97a", "#7fe0d0", "#fff3cf", "#8fb7ff"][k % 4]);
						p.style.animationDelay = (Math.random() * 0.9).toFixed(2) + "s";
						ui.bt.appendChild(p);
						setTimeout(() => p.remove(), 3400);
					}
				}
				ui.bt.classList.add("on");
				setTimeout(() => { ui.bt.classList.remove("on", "major"); [...ui.bt.querySelectorAll(".pt")].forEach(x => x.remove()); }, major ? 6800 : 4300);
			}"""
assert old_enter in c
c = c.replace(old_enter, new_enter)

f.write_text(c, encoding="utf-8")
print("animation + seals OK")
