# -*- coding: utf-8 -*-
"""引擎接入编年史彩蛋：随机彩蛋弹幕 + 原著语录替换 + 名场面"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

# 1) CSS：彩蛋 toast
old = ".gear{position:absolute;left:14px;bottom:14px;"
new = """.eggtoast{position:absolute;left:50%;bottom:120px;transform:translateX(-50%);max-width:520px;padding:10px 18px;border-radius:12px;background:linear-gradient(135deg,rgba(12,16,26,.95),rgba(20,27,42,.95));border:1px solid color-mix(in srgb,var(--m) 50%,transparent);color:#e6ddc8;font-size:12.5px;line-height:1.7;opacity:0;transition:opacity .6s;pointer-events:none;box-shadow:0 8px 30px rgba(0,0,0,.5)}
.eggtoast.on{opacity:1}
.eggtoast b{color:var(--m);display:block;font-size:10px;letter-spacing:.24em;margin-bottom:3px}
.gear{position:absolute;left:14px;bottom:14px;"""
assert old in c
c = c.replace(old, new, 1)

# 2) toast DOM
old = '<button class="gear">道</button>'
new = '<div class="eggtoast"><b>仙逆彩蛋</b><span class="t"></span></div>\n<button class="gear">道</button>'
assert old in c
c = c.replace(old, new, 1)

# 3) 编年史加载 + 彩蛋轮播 + 语录替换
old = """			// 真实修为轮询（网关配额）"""
new = """			// 编年史彩蛋（workers/编年史彩蛋.json → assets/ui/chronicle.json）
			let CHRON = {};
			fetch(A + "/ui/chronicle.json").then(r => r.ok ? r.json() : null).then(j => {
				if (j && j.realms) { CHRON = j.realms; ui.eq.textContent = (CHRON[REALMS[idx].id] || {}).quotes?.[0]?.text || ui.eq.textContent; }
			}).catch(() => { });
			setInterval(() => {
				const cr = CHRON[REALMS[idx].id];
				if (!cr || !cr.eggs || !cr.eggs.length) return;
				const t = $(".eggtoast"); if (!t) return;
				t.querySelector(".t").textContent = cr.eggs[Math.floor(Math.random() * cr.eggs.length)];
				t.classList.add("on");
				setTimeout(() => t.classList.remove("on"), 7000);
			}, 100000);

			// 真实修为轮询（网关配额）"""
assert old in c
c = c.replace(old, new, 1)

# 4) 心魔劫语录：优先编年史
old = 'ui.sayQ.textContent = QUOTES[rr.id] || QUOTES.default;'
new = ('const crQ = (CHRON[rr.id] || {}).quotes || [];\n'
       '				ui.sayQ.textContent = (crQ.length ? crQ[Math.floor(Math.random() * crQ.length)].text : "") || QUOTES[rr.id] || QUOTES.default;')
assert old in c
c = c.replace(old, new, 1)

# 5) 破境判词第二行：名场面
old = 'ui.vH.textContent = r.name; ui.vP.textContent = r.sub;'
new = ('const crS = (CHRON[r.id] || {}).scene;\n'
       '				ui.vH.textContent = r.name; ui.vP.textContent = crS ? String(crS).slice(0, 46) : r.sub;')
assert old in c
c = c.replace(old, new, 1)

# 6) 空状态语录：优先编年史
old = 'ui.eq.textContent = QUOTES[r.id] || QUOTES.default;'
new = 'ui.eq.textContent = ((CHRON[r.id] || {}).quotes || [])[0]?.text || QUOTES[r.id] || QUOTES.default;'
assert old in c
c = c.replace(old, new, 1)

f.write_text(c, encoding="utf-8")
print("chronicle fused OK")
