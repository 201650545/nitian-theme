# -*- coding: utf-8 -*-
"""编年史配图清单：搜索网关抓每境界官方图片 URL"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"D:\逆天主题\workers")
OUT = ROOT / "编年史图片清单.json"

REALMS = [
    ("01_ningshi", "凝气期"), ("02_zhuji", "筑基期"), ("03_jiedan", "结丹期"),
    ("04_yuanying", "元婴期"), ("05_huashen", "化神期"), ("06_yingbian", "婴变期"),
    ("07_wending", "问鼎期"), ("08_yinyang", "阴虚阳实期"), ("09_kunie", "窥涅期"),
    ("10_jingnie", "净涅期"), ("11_suinie", "碎涅期"), ("12_kongnie", "空涅期"),
    ("13_kongling", "空灵期"), ("14_kongxuan", "空玄期"), ("15_kongjie", "空劫期"),
    ("16_qiao1", "踏天"), ("24_qiao9", "踏天"),
]

IMG_RE = re.compile(r'https?://[^\s\]"<>]+')
IMG_EXT = re.compile(r"\.(jpg|jpeg|png|webp|gif)", re.I)
BAD_HOST = ("bing.com", "google.", "baidu.", "zhihu.com", "bilibili.com/video", "douyin.com")


def search(q):
    try:
        u = "http://127.0.0.1:3000/api/search_json?q=" + urllib.parse.quote(q) + "&engines=kimi"
        d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "nitian/1.0"}), timeout=180).read())
        return "\n".join((r.get("answer") or "") for r in d.get("records", []))
    except Exception as e:  # noqa: BLE001
        return str(e)


def main():
    out = {}
    if OUT.exists():
        try:
            out = json.loads(OUT.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            out = {}
    done = [x["realm"] for x in out] if isinstance(out, list) else []
    results = []
    for rid, name in REALMS:
        if rid in done:
            continue
        q = f"仙逆 动画 {name} 王林 海报 高清 图片 壁纸"
        text = search(q)
        urls = IMG_RE.findall(text)
        cands = []
        for u2 in urls:
            if IMG_EXT.search(u2) and not any(b in u2.lower() for b in BAD_HOST):
                if u2 not in [c["url"] for c in cands]:
                    cands.append({"realm": rid, "url": u2, "source": "search", "desc": name})
        print(f"[{rid}] 候选 {len(cands)}", flush=True)
        results.extend(cands[:6])
        OUT.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
        time.sleep(3)
    print("total:", len(results), "->", OUT)


if __name__ == "__main__":
    main()
