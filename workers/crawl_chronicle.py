# -*- coding: utf-8 -*-
"""编年史彩蛋爬取管线（只用 Fast 免费模型）
搜索：:3000 /api/search_json（Kimi 引擎）
结构化：:3100 /v1/chat/completions → deepseek-v4-flash-260425（方舟 50 万免费额度）
断点续跑：每境界落盘，重跑自动跳过已完成。
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"D:\逆天主题\workers")
OUT = ROOT / "编年史彩蛋.json"
ST = json.load(open(r"D:\项目\data\search_gateway\api_state.json", encoding="utf-8-sig"))
GW_KEY = ST["api_key"]
LLM = "deepseek-v4-flash-260425"

REALMS = [
    ("01_ningshi", "凝气期"), ("02_zhuji", "筑基期"), ("03_jiedan", "结丹期"),
    ("04_yuanying", "元婴期"), ("05_huashen", "化神期"), ("06_yingbian", "婴变期"),
    ("07_wending", "问鼎期"), ("08_yinyang", "阴虚阳实期"), ("09_kunie", "窥涅期"),
    ("10_jingnie", "净涅期"), ("11_suinie", "碎涅期"), ("12_kongnie", "空涅期"),
    ("13_kongling", "空灵期"), ("14_kongxuan", "空玄期"), ("15_kongjie", "空劫期"),
    ("16_qiao1", "踏天一桥"), ("17_qiao2", "踏天二桥"), ("18_qiao3", "踏天三桥"),
    ("19_qiao4", "踏天四桥"), ("20_qiao5", "踏天五桥"), ("21_qiao6", "踏天六桥"),
    ("22_qiao7", "踏天七桥"), ("23_qiao8", "踏天八桥"), ("24_qiao9", "踏天九桥"),
]

SCHEMA = ('{"events":[{"title":"...","summary":"50字内"}],'
          '"enemies":[{"name":"...","who":"身份","result":"交手结果","fun":"一句趣味点评"}],'
          '"treasures":[{"name":"法宝名","origin":"来历","power":"能力"}],'
          '"friends":[{"name":"...","relation":"关系","fate":"结局一句话"}],'
          '"scene":"该期最值得做成演出的名场面（画面描述）",'
          '"eggs":["书粉彩蛋/趣梗","至少两条"],'
          '"quotes":[{"text":"台词","src":"出处章节或集数"}]}')


def http_json(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": "nitian-crawler/1.0"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())


def search(q):
    try:
        u = "http://127.0.0.1:3000/api/search_json?q=" + urllib.parse.quote(q) + "&engines=kimi"
        d = http_json(u, timeout=180)
        parts = []
        for r in d.get("records", []):
            a = (r.get("answer") or "").strip()
            if a:
                parts.append("【" + r.get("provider", "?") + "】" + a[:2500])
        return "\n".join(parts)[:7000]
    except Exception as e:  # noqa: BLE001
        return "（搜索失败：%s）" % str(e)[:100]


def llm(prompt):
    body = json.dumps({
        "model": LLM,
        "messages": [
            {"role": "system", "content": "你是《仙逆》（耳根小说/腾讯官方动画）编年史结构化助手。只输出合法 JSON，不要 markdown 代码块，不要解释。内容必须符合原著事实，不确定的字段值加 \"_unverified\": true 标记。趣味彩蛋优先：书粉梗、名场面、王林性格反差（苟且隐忍vs杀伐果断）都要挖。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
    }).encode()
    req = urllib.request.Request("http://127.0.0.1:3100/v1/chat/completions", data=body, headers={
        "Authorization": "Bearer " + GW_KEY, "Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=180).read())
    c = r["choices"][0]["message"]["content"].strip()
    if c.startswith("```"):
        c = c.split("```")[1].lstrip("json").strip()
    return json.loads(c)


def main():
    out = {}
    if OUT.exists():
        try:
            out = json.loads(OUT.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            out = {}
    out.setdefault("realms", {})
    todo = [(rid, name) for rid, name in REALMS if rid not in out["realms"]]
    print(f"待爬 {len(todo)}/{len(REALMS)}", flush=True)
    for rid, name in todo:
        t0 = time.time()
        q = f"仙逆 王林 {name} 剧情梗概 敌人 法宝 机缘 名场面 经典语录"
        print(f"[{rid}] 搜索: {q}", flush=True)
        text = search(q)
        prompt = (f"境界={rid}（{name}）。以下是网络搜索摘要，可能不完整，请结合你对《仙逆》的知识补全：\n"
                  f"{text}\n\n按此 JSON Schema 输出该境界的内容：{SCHEMA}\n"
                  f"要求：events 2-4条；eggs≥2条；quotes 1-2条；全部中文；踏天桥阶段如剧情少可写该阶段整体经历。")
        try:
            data = llm(prompt)
            data["era"] = name
            out["realms"][rid] = data
            OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"[OK] {rid} 用时{time.time()-t0:.0f}s eggs={len(data.get('eggs', []))} enemies={len(data.get('enemies', []))}", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] {rid}: {str(e)[:140]}", flush=True)
        time.sleep(2)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
