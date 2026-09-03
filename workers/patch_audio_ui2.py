# -*- coding: utf-8 -*-
"""音量滑杆 + 氛围垫底音接入（修正锚点）"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

# 1) 面板加音量滑杆 + 氛围开关
old = '<label>全局音效<input type="checkbox" class="tg-audio"></label>'
assert old in c, "audio label anchor"
new = ('<label>全局音效<input type="checkbox" class="tg-audio"></label>\n'
       '  <label>氛围垫底音<input type="checkbox" class="tg-amb"></label>\n'
       '  <label>音量<input type="range" class="vol" min="0" max="1" step="0.05"></label>')
c = c.replace(old, new, 1)

# 2) 复选框初始化 + 音量值
old = '$(".tg-audio").checked = opts.audio; $(".tg-comp").checked = opts.companion;'
assert old in c, "init anchor"
new = ('$(".tg-audio").checked = opts.audio; $(".tg-comp").checked = opts.companion;\n'
       '\t\t\t$(".tg-amb").checked = opts.ambient;\n'
       '\t\t\t$(".vol").value = parseFloat(localStorage.getItem("nitian.vol") || "0.6");')
c = c.replace(old, new, 1)

# 3) loadOpts 增加 ambient 默认
old = 'return Object.assign({ audio: true, companion: true, relabel: true, skin: true }, JSON.parse(localStorage.getItem(LS.opt) || "{}"));'
assert old in c, "loadOpts anchor"
new = 'return Object.assign({ audio: true, companion: true, relabel: true, skin: true, ambient: true }, JSON.parse(localStorage.getItem(LS.opt) || "{}"));'
c = c.replace(old, new, 1)

# 4) paint() 末尾调用 setAmbient
old = '\t\t\t\tui.ep.src = r.char;\n\t\t\t\tconst q0 = chronOf(r.id).quotes[0]; ui.eq.textContent = (q0 && q0.text) || QUOTES[r.id] || QUOTES.default;'
assert old in c, "paint end anchor"
new = ('\t\t\t\tif (opts.ambient) setAmbient(i);\n'
       '\t\t\t\tui.ep.src = r.char;\n'
       '\t\t\t\tconst q0 = chronOf(r.id).quotes[0]; ui.eq.textContent = (q0 && q0.text) || QUOTES[r.id] || QUOTES.default;')
c = c.replace(old, new, 1)

# 5) 事件绑定
old = '$(".tg-audio").addEventListener("change", (e) => { opts.audio = e.target.checked; saveOpts(opts); });'
assert old in c, "audio bind anchor"
new = ('$(".tg-audio").addEventListener("change", (e) => { opts.audio = e.target.checked; saveOpts(opts); });\n'
       '\t\t\t$(".tg-amb").addEventListener("change", (e) => { opts.ambient = e.target.checked; saveOpts(opts); if (!e.target.checked) setAmbient(0); else setAmbient(idx); });\n'
       '\t\t\t$(".vol").addEventListener("input", (e) => setVolume(parseFloat(e.target.value)));')
c = c.replace(old, new, 1)

f.write_text(c, encoding="utf-8")
print("volume slider + ambient OK")