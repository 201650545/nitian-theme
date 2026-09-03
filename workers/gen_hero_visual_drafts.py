# -*- coding: utf-8 -*-
"""商汤日日新 U1.5 Lite · 三境 Hero Visual 草稿生成
提示词 = AI生成手册三境模板完整版（含人物）。产出为草稿：只落 raw\，不覆盖引擎 hero.webp。
"""
import base64
import io
import json
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

KEYS_PATH = Path(r"D:\项目\data\search_gateway\channels.json")
OUT_ROOT = Path(r"D:\逆天主题\assets\realms")
MODEL = "sensenova-u1.5-lite"
URL = "https://token.sensenova.cn/v1/images/generations"

STYLE = "动漫CG，官方仙逆画风，体积光，史诗电影构图，细节丰富，无文字无边框"
JOBS = {
    "01_ningshi": (
        "恒岳山后山悬崖，云雾缭绕，陡峭石崖，少年王林满身伤痛跪触天逆珠，"
        "青涩农家少年，粗布麻衣，丹凤眼，黑发，冷峻，冷青色山雾环绕，竖版主视觉海报。" + STYLE
    ),
    "04_yuanying": (
        "赵国藤家城前百万人头塔前，白发狂舞红衣煞气王林立于塔下仰视，"
        "眉心两颗古神星点，暗红血色与星蓝微光交织，煞气冲天，竖版主视觉海报。" + STYLE
    ),
    "05_huashen": (
        "雨之仙界仙玉祭坛，飞瀑流云，青衫胜雪的王林渡化神劫，道韵环绕，"
        "眼神深邃沧桑，超凡脱俗，清冷青色银白辉光，空灵意境，竖版主视觉海报。" + STYLE
    ),
}
SIZES_TO_TRY = ["1152x1536", "768x1024"]


def load_key() -> str:
    d = json.loads(KEYS_PATH.read_bytes().decode("utf-8-sig"))
    k = d["keys"]["sensetime"]
    return k.get("api_key") or k.get("key") if isinstance(k, dict) else k


def gen(key: str, prompt: str) -> Image.Image:
    last = None
    for size in SIZES_TO_TRY:
        body = json.dumps({"model": MODEL, "prompt": prompt, "n": 1, "size": size}).encode()
        req = urllib.request.Request(
            URL, data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        try:
            r = json.loads(urllib.request.urlopen(req, timeout=240).read())
            item = r["data"][0]
            if item.get("b64_json"):
                return Image.open(io.BytesIO(base64.b64decode(item["b64_json"]))).convert("RGB")
            return Image.open(io.BytesIO(urllib.request.urlopen(item["url"], timeout=120).read())).convert("RGB")
        except urllib.error.HTTPError as e:
            last = f"{size}: HTTP {e.code} {e.read().decode('utf-8','ignore')[:150]}"
            print(f"  [retry] {last}", flush=True)
        except Exception as e:  # noqa: BLE001
            last = f"{size}: {e}"
            print(f"  [retry] {last}", flush=True)
    raise RuntimeError(last)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    key = load_key()
    for rid, prompt in JOBS.items():
        raw_dir = OUT_ROOT / rid / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        print(f"[{rid}] Hero Visual 草稿生成中…", flush=True)
        t0 = time.time()
        img = gen(key, prompt)
        out = raw_dir / "ai_hero_draft_v1.png"
        img.save(out, "PNG")
        t = img.copy()
        t.thumbnail((420, 560))
        t.save(raw_dir / "ai_hero_draft_v1_thumb.jpg", "JPEG", quality=85)
        print(f"[{rid}] OK {img.size} -> {out} 用时{time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
