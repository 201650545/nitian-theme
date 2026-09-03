# -*- coding: utf-8 -*-
"""全文尾部采集"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
js = "(() => { const t = (document.body.innerText || ''); window.__g = t; return 'len=' + t.length + ' tail=' + t.slice(-80).replace(/\\n/g, ' '); })()"
one = " ".join(line.strip() for line in js.splitlines() if line.strip())
Path(r"C:\Users\887E~1\AppData\Local\Temp\opencode\gpt-body.one.txt").write_text(one, encoding="utf-8")

# 取全文存 window 后分片读取
getchunk = "(() => { const t = window.__g || ''; const a = parseInt(window.__cs || '0'); const chunk = t.slice(a, a + 6000); window.__cs = a + chunk.length; return JSON.stringify({chunk: chunk, done: window.__cs >= t.length}); })()"
Path(r"C:\Users\887E~1\AppData\Local\Temp\opencode\gpt-chunk.one.txt").write_text(" ".join(line.strip() for line in getchunk.splitlines() if line.strip()), encoding="utf-8")
print("ok")
