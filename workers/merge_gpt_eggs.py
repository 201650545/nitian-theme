# -*- coding: utf-8 -*-
"""GPT-Extend 补充彩蛋合并进编年史 + 复制部署"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CHRON = Path(r"D:\逆天主题\workers\编年史彩蛋.json")
GPT = Path(r"D:\逆天主题\workers\gpt_extend_eggs.json")
DEPLOY = Path(r"D:\逆天主题\assets\ui\chronicle.json")

chron = json.loads(CHRON.read_text(encoding="utf-8"))
gpt = json.loads(GPT.read_text(encoding="utf-8"))
gpt_realms = gpt.get("realms", {k: v for k, v in gpt.items() if isinstance(v, dict) and k != "_meta"})

added_eggs = added_quotes = 0
for rid, add in gpt_realms.items():
    if not isinstance(add, dict):
        continue
    dst = chron["realms"].setdefault(rid, {})
    for egg in add.get("eggs", []):
        if egg and egg not in dst.setdefault("eggs", []):
            dst["eggs"].append("[GPT] " + egg)
            added_eggs += 1
    for q in add.get("quotes", []):
        qtxt = q if isinstance(q, str) else q.get("text", "")
        if qtxt and not any(qtxt in (x.get("text", "") if isinstance(x, dict) else str(x)) for x in dst.get("quotes", [])):
            dst.setdefault("quotes", []).append({"text": qtxt, "src": "GPT-Extend: " + (q.get("src", "") if isinstance(q, dict) else "")})
            added_quotes += 1
    if add.get("scene") and not dst.get("scene"):
        dst["scene"] = add["scene"]
    # 敌人/法宝/友人趣评去重合并
    for key in ("enemies", "treasures", "friends"):
        have = {x.get("name") for x in dst.setdefault(key, []) if isinstance(x, dict)}
        for x in add.get(key, []):
            if isinstance(x, dict) and x.get("name") not in have:
                dst[key].append(x)

chron["sources"] = sorted(set(chron.get("sources", []) + ["GPT-5.6 Thinking·Extended (问达宝镜像) 2026-08-26"]))
CHRON.write_text(json.dumps(chron, ensure_ascii=False, indent=1), encoding="utf-8")
DEPLOY.write_text(json.dumps(chron, ensure_ascii=False, indent=1), encoding="utf-8")

eggs = sum(len(v.get("eggs", [])) for v in chron["realms"].values())
quotes = sum(len(v.get("quotes", [])) for v in chron["realms"].values())
print(f"合并完成：+{added_eggs} GPT彩蛋, +{added_quotes} 语录 | 总计彩蛋 {eggs} 语录 {quotes} -> 已部署 {DEPLOY}")
