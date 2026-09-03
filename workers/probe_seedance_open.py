# -*- coding: utf-8 -*-
"""ARK 开通管理探测：Seedance 全系视频模型可用性 + 免费额度验证（2026-08-27）
对每个候选模型提交最小 t2v 任务（480p/5s/无水印）：
  - 任务受理(cgt-*) = 已开通可用 → 轮询到完成并下载 assets/animations/probe_<model>.mp4
  - ModelNotOpen = 未开通；ModelNotFound = ID 不对
产物即各模型质量样品，花的额度本身就是开通赠送额度验证。
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(r"D:\项目\data\search_gateway\channels.json", encoding="utf-8-sig"))
KEY = d["keys"]["ark"]
BASE = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
OUT = Path(r"D:\逆天主题\assets\animations")

CANDIDATES = [
    "doubao-seedance-1-5-pro",
    "doubao-seedance-1-5-pro-251228",
    "doubao-seedance-1-5-pro-251215",
    "doubao-seedance-1-5-lite",
    "doubao-seedance-2-0-260128",
    "doubao-seedance-2-0-fast-260128",
    "doubao-seedance-2-0-mini-260128",
    "doubao-seedance-2-5-260628",
    "doubao-seedance-1-0-pro-fast-251015",  # 已知可用，对照
]

PROMPT = "仙侠风格：白衣修士立于山巅云海，金色灵气自丹田升起环绕周身，破境瞬间金光爆发冲天，镜头缓慢环绕，史诗感，动漫风格"


def submit(model):
    body = {
        "model": model,
        "content": [{"type": "text", "text": PROMPT}],
        "ratio": "16:9",
        "resolution": "480p",
        "duration": 5,
        "watermark": False,
    }
    req = urllib.request.Request(BASE, data=json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"},
                                 method="POST")
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=60).read())
        return {"ok": True, "id": r.get("id")}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "ignore")[:260]
        try:
            j = json.loads(detail)
            code = j.get("error", {}).get("code", "")
        except Exception:
            code = detail[:80]
        return {"ok": False, "code": code, "detail": detail}


def poll(tid):
    req = urllib.request.Request(BASE + "/" + tid, headers={"Authorization": "Bearer " + KEY})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def main():
    live = []
    for model in CANDIDATES:
        r = submit(model)
        if r["ok"]:
            print("[OPEN]", model, "->", r["id"], flush=True)
            live.append((model, r["id"]))
        else:
            print("[NO ]", model, "->", r["code"], flush=True)
        time.sleep(1)

    print("\n=== 轮询已受理任务 ===", flush=True)
    deadline = time.time() + 900
    pending = dict(live)
    while pending and time.time() < deadline:
        for model, tid in list(pending.items()):
            try:
                st = poll(tid)
            except Exception as e:
                print(model, "poll err", str(e)[:80], flush=True)
                continue
            s = st.get("status")
            if s == "succeeded":
                url = st.get("content", {}).get("video_url", "")
                dst = OUT / ("probe_" + model + ".mp4")
                if url:
                    urllib.request.urlretrieve(url, dst)
                usage = st.get("usage", {})
                print("[DONE]", model, dst.stat().st_size // 1024, "KB usage:", json.dumps(usage, ensure_ascii=False)[:160], flush=True)
                del pending[model]
            elif s in ("failed", "cancelled"):
                print("[FAIL]", model, str(st.get("error", ""))[:160], flush=True)
                del pending[model]
            else:
                print("[....]", model, s, flush=True)
        if pending:
            time.sleep(15)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()
