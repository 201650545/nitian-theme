# -*- coding: utf-8 -*-
"""U1.5 Lite 补齐生成系资产：化神敌人 + 三境境界印章"""
import base64
import io
import json
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

KEYS_PATH = Path(r"D:\项目\data\search_gateway\channels.json")
ROOT = Path(r"D:\逆天主题")
URL = "https://token.sensenova.cn/v1/images/generations"

STYLE = "动漫CG，官方仙逆画风，暗色调，细节丰富，无文字"
JOBS = {
    "enemy_huashen": (
        ROOT / "assets/realms/05_huashen/raw",
        "仙逆风格化神期强敌，古神虚影，银白与暗金交织的巨大神祇残念，威压苍穹，煞气逼人，头像半身构图",
        "1024x1024", "enemy_huashen.png",
    ),
    "seal_ningshi": (
        ROOT / "assets/ui/seals",
        "仙侠风境界印章纹章：凝气期，主题元素为云雾青山与新芽，冷青色 #5a9e8f 与玄墨描线，圆形玉印构图，SVG线条风格，扁平徽章，纯深色背景居中",
        "512x512", "seal_01_ningshi.png",
    ),
    "seal_yuanying": (
        ROOT / "assets/ui/seals",
        "仙侠风境界印章纹章：元婴期，主题元素为星点环绕的婴孩虚影与古神星纹，星蓝色 #3b7fd4 与暗金描线，圆形玉印构图，SVG线条风格，扁平徽章，纯深色背景居中",
        "512x512", "seal_04_yuanying.png",
    ),
    "seal_huashen": (
        ROOT / "assets/ui/seals",
        "仙侠风境界印章纹章：化神期，主题元素为青莲绽放与飞瀑流云道韵，清冷银白 #b8c6da 与淡青描线，圆形玉印构图，SVG线条风格，扁平徽章，纯深色背景居中",
        "512x512", "seal_05_huashen.png",
    ),
}


def load_key() -> str:
    d = json.loads(KEYS_PATH.read_bytes().decode("utf-8-sig"))
    k = d["keys"]["sensetime"]
    return k.get("api_key") or k.get("key") if isinstance(k, dict) else k


def gen(key: str, prompt: str, size: str) -> Image.Image:
    body = json.dumps({"model": "sensenova-u1.5-lite", "prompt": prompt, "n": 1, "size": size}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=240).read())
    item = r["data"][0]
    if item.get("b64_json"):
        return Image.open(io.BytesIO(base64.b64decode(item["b64_json"]))).convert("RGB")
    return Image.open(io.BytesIO(urllib.request.urlopen(item["url"], timeout=120).read())).convert("RGB")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    key = load_key()
    for name, (outdir, prompt, size, fname) in JOBS.items():
        outdir.mkdir(parents=True, exist_ok=True)
        out = outdir / fname
        if out.exists():
            print(f"[skip] {name} 已存在")
            continue
        print(f"[{name}] 生成中…", flush=True)
        t0 = time.time()
        img = gen(key, prompt, size)
        img.save(out, "PNG")
        print(f"[{name}] OK {img.size} -> {out} 用时{time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
