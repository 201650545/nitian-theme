# -*- coding: utf-8 -*-
"""生成 opencli eval 单行 base64 注入命令"""
import base64
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
js = Path(sys.argv[1]).read_text(encoding="utf-8")
# 压成单行
js = " ".join(line.strip() for line in js.splitlines() if line.strip())
b64 = base64.b64encode(js.encode("utf-8")).decode()
# 手册式：外层双引号、内部单引号、atob 解码
one = "(()=>{const b=atob('" + b64 + "');const u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);const s=new TextDecoder().decode(u);return eval(s);})()"
out = Path(sys.argv[1]).with_suffix(".one.txt")
out.write_text(one, encoding="utf-8")
print("cmd file:", out)
