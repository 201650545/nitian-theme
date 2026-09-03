# -*- coding: utf-8 -*-
"""编年史卷轴引言生成（快速模型重复性操作，2026-08-27）
- 渠道：modelscope 免费渠道 deepseek-ai/DeepSeek-V4-Flash-0731（key 从 channels.json 读，不打印）
- 输入：assets/ui/chronicle.json 各境界 events 摘要 + 引擎 REALMS 表
- 输出：assets/ui/chronicle-img/digests.json  {"<rid>": "≤18字卷轴引言"}
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"D:\游戏\逆天主题")
KEYS_PATH = Path(r"D:\项目\data\search_gateway\channels.json")
OUT_DIR = ROOT / "assets" / "ui" / "chronicle-img"
CHRON_PATH = ROOT / "assets" / "ui" / "chronicle.json"

CHANNELS = [
    # (渠道名, base_url, model, extra_headers)
    ("modelscope", "https://api-inference.modelscope.cn/v1/chat/completions",
     "deepseek-ai/DeepSeek-V4-Flash-0731", {}),
    ("opencode", "https://opencode.ai/zen/go/v1/chat/completions",
     "deepseek-v4-flash", {"User-Agent": "openai-completions/pi-ai"}),
    ("sensetime", "https://token.sensenova.cn/v1/chat/completions",
     "deepseek-v4-flash", {}),
]

# 与引擎 REALMS 同步的 28 境（id, 名称）
REALM_NAMES = [
    ("01_ningshi", "凝气期"), ("02_zhuji", "筑基期"), ("03_jiedan", "结丹期"),
    ("04_yuanying", "元婴期"), ("05_huashen", "化神期"), ("06_yingbian", "婴变期"),
    ("07_wending", "问鼎期"), ("08_yinyang", "阴虚阳实"), ("09_kunie", "窥涅境"),
    ("10_jingnie", "净涅境"), ("11_suinie", "碎涅境"), ("12_kongnie", "空涅境"),
    ("13_kongling", "空灵境"), ("14_kongxuan", "空玄境"), ("15_kongjin", "空劫·金尊"),
    ("16_kongzun", "空劫·天尊"), ("17_kongyue", "空劫·跃天尊"), ("18_kongda", "空劫·大天尊"),
    ("19_qiao1", "踏天一桥"), ("20_qiao2", "踏天二桥"), ("21_qiao3", "踏天三桥"),
    ("22_qiao4", "踏天四桥"), ("23_qiao5", "踏天五桥"), ("24_qiao6", "踏天六桥"),
    ("25_qiao7", "踏天七桥"), ("26_qiao8", "踏天八桥"), ("27_qiao9", "踏天九桥"),
]

chron_alias = {
    "15_kongjin": "15_kongjie", "16_kongzun": "15_kongjie", "17_kongyue": "15_kongjie",
    "18_kongda": "15_kongjie", "19_qiao1": "16_qiao1", "20_qiao2": "17_qiao2",
    "21_qiao3": "18_qiao3", "22_qiao4": "19_qiao4", "23_qiao5": "20_qiao5",
    "24_qiao6": "21_qiao6", "25_qiao7": "22_qiao7", "26_qiao8": "23_qiao8", "27_qiao9": "24_qiao9",
}


def load_key(channel: str) -> str:
    d = json.loads(KEYS_PATH.read_bytes().decode("utf-8-sig"))
    k = d["keys"][channel]
    key = (k.get("api_key") or k.get("key")) if isinstance(k, dict) else k
    if not key:
        raise RuntimeError(channel + " key 未配置")
    return key


def build_prompt(chron: dict, realm_slice) -> str:
    lines = []
    for rid, name in realm_slice:
        c = chron.get(chron_alias.get(rid, rid), {})
        evs = c.get("events") or []
        ev_txt = "；".join(
            f"{e.get('title','')}({(e.get('summary') or '')[:52]})" for e in evs[:3]
        )
        scene = c.get("scene") or ""
        lines.append(f"{rid}|{name}|{scene}|{ev_txt}")
    body = "\n".join(lines)
    return (
        "你是仙侠文案编辑。下面每行是一条境界记录：id|名称|名场面|事件摘要。\n"
        "为每个境界写一句『卷轴引言』：要求古意凝练、贴合剧情、不超过18个汉字、不带标点句号、"
        "禁止出现英文和数字id。输出必须是严格的 JSON 对象：{\"<id>\":\"<引言>\",...}，"
        "不要任何解释或代码块标记。\n\n" + body
    )


def call_llm(prompt: str) -> str:
    payload = {
        "model": "",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 6000,
    }
    last_err = None
    for name, base, model, extra in CHANNELS:
        payload["model"] = model
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + load_key(name)}
        headers.update(extra)
        try:
            req = urllib.request.Request(base, data=json.dumps(payload).encode("utf-8"),
                                         headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=120) as r:
                j = json.loads(r.read().decode("utf-8"))
            msg = j["choices"][0]["message"]
            content = msg.get("content") or ""
            if not content and msg.get("reasoning"):  # sensetime 响应字段是 reasoning
                content = msg["reasoning"]
            if content.strip():
                print("[llm]", name, "ok")
                return content
        except Exception as e:  # noqa: BLE001
            last_err = e
            print("[llm]", name, "fail:", str(e)[:120])
    raise RuntimeError("所有渠道失败: " + str(last_err))


def main() -> None:
    chron = json.loads(CHRON_PATH.read_text(encoding="utf-8")).get("realms", {})
    out = {}
    batches = [REALM_NAMES[i:i + 10] for i in range(0, len(REALM_NAMES), 10)]
    for bi, batch in enumerate(batches):
        content = call_llm(build_prompt(chron, batch))
        m = re.search(r"\{.*\}", content, re.S)
        if not m:
            raise RuntimeError(f"批次{bi} 模型未返回 JSON: " + content[:300])
        part = json.loads(m.group(0))
        for rid, name in batch:
            v = str(part.get(rid, "")).strip()
            out[rid] = v if v and len(v) <= 24 else name + " · 道途一程"
        print(f"[batch {bi}] ok {len(part)}/{len(batch)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "digests.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("OK digests:", len(out))
    for rid in list(out)[:6]:
        print(" ", rid, out[rid])


if __name__ == "__main__":
    main()
