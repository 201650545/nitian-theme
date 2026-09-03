# -*- coding: utf-8 -*-
"""无逗号无双引号版读取脚本"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
js = "(() => { const r = window.__gptReply; return r ? ('LEN=' + r.length + ' TAIL=' + r.slice(-50)) : 'no-reply'; })()"
one = " ".join(line.strip() for line in js.splitlines() if line.strip())
Path(r"C:\Users\887E~1\AppData\Local\Temp\opencode\gpt-tail.one.txt").write_text(one, encoding="utf-8")

# 采集脚本（单引号JS + 无逗号挑战 → 用 window 变量分段存）
collector = """(() => { const arts = document.querySelectorAll('[data-message-author-role=assistant]'); if (!arts.length) { window.__g = 'none'; return 'none'; } const last = arts[arts.length - 1]; window.__g = (last.innerText || '').trim(); return 'len=' + window.__g.length; })()"""
col_one = " ".join(line.strip() for line in collector.splitlines() if line.strip())
Path(r"C:\Users\887E~1\AppData\Local\Temp\opencode\gpt-col.one.txt").write_text(col_one, encoding="utf-8")
print("ok")
