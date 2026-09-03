# -*- coding: utf-8 -*-
"""提取 GPT 回复中的 JSON 并校验/合并进编年史"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
t = open(r"C:\Users\887E~1\AppData\Local\Temp\opencode\gpt-reply.txt", encoding="utf-8-sig").read()

i = t.find('{')
j = t.rfind('}')
seg = t[i:j + 1]
print("json seg len:", len(seg))

# 修常见问题：截断的 JSON → 尝试解析
try:
    data = json.loads(seg)
    print("PARSE OK, realms:", len(data.get("realms", data if isinstance(data, dict) else {})))
except Exception as e:
    print("PARSE FAIL:", str(e)[:120])
    # 尝试截到最后一个完整 } 处
    data = None

out = Path(r"D:\逆天主题\workers\gpt_extend_eggs.json")
if data:
    # 归一化：可能顶层就是按境界的 dict
    realms = data.get("realms", data)
    if isinstance(realms, dict):
        for k, v in list(realms.items()):
            print(" ", k, "eggs:", len(v.get("eggs", [])) if isinstance(v, dict) else "?")
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved ->", out)
