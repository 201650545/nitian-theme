# -*- coding: utf-8 -*-
"""找 GPT 真正回复的 JSON（跳过提示词回显）"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
t = open(r"C:\Users\887E~1\AppData\Local\Temp\opencode\gpt-reply.txt", encoding="utf-8-sig").read()

# 提示词回显结尾标志
mark = '只输出 JSON 本体。'
end_of_prompt = t.find(mark)
print("prompt echo end at:", end_of_prompt, "/", len(t))

# 从那之后找第一个 {
start = t.find("{", end_of_prompt if end_of_prompt > 0 else 0)
print("reply json starts:", start)

# 从尾往前找完整 JSON：尝试逐步扩展解析
best = None
for end in range(len(t), start, -200):
    seg = t[start:end]
    # 找最后一个 }
    j = seg.rfind("}")
    if j < 0:
        continue
    try:
        data = json.loads(seg[:j + 1])
        best = (seg[:j + 1], data)
        print("parsed at", j + 1, "chars, keys:", list(data.keys())[:5])
        break
    except Exception:
        continue

if best:
    seg, data = best
    out = Path(r"D:\逆天主题\workers\gpt_extend_eggs.json")
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    realms = data.get("realms", data)
    if isinstance(realms, dict):
        for k, v in list(realms.items()):
            if isinstance(v, dict):
                print(" ", k, "eggs:", len(v.get("eggs", [])), "quotes:", len(v.get("quotes", [])))
    print("saved ->", out)
else:
    print("no parseable JSON")
    print("tail 400:", t[-400:])
