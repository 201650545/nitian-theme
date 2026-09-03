# -*- coding: utf-8 -*-
"""商汤日日新 sensenova-u1.5-lite 背景生成（逆天主题 MVP）
- 端点：https://token.sensenova.cn/v1/images/generations（OpenAI images 兼容）
- key 从 D:\\项目\\data\\search_gateway\\channels.json 读取（不打印）
- 只补官方缺失：01_ningshi / 04_yuanying 的横版纯背景
"""
import base64
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

STYLE = "动漫CG，官方仙逆画风，仙侠世界，冷色调，体积光，史诗电影构图，细节丰富，无文字无边框"
PROMPTS = {
    "01_ningshi": (
        "恒岳宗后山悬崖全景，云雾缭绕的陡峭石崖与连绵青山，山脚小径与茅屋，"
        "冷青色山雾，清晨微光，空灵朴素初入修真氛围。" + STYLE
    ),
    "04_yuanying": (
        "赵国古城墙前巨大的百万人头塔远景，阴森震撼的塔形轮廓直入苍穹，"
        "暗红血色云层与星蓝微光交织，肃杀古战场氛围，无人空景。" + STYLE
    ),
}
SIZES_TO_TRY = ["2048x1152", "1024x576", "1024x1024"]


def load_key() -> str:
    d = json.loads(KEYS_PATH.read_bytes().decode("utf-8-sig"))
    k = d["keys"]["sensetime"]
    key = k.get("api_key") or k.get("key") if isinstance(k, dict) else k
    if not key:
        raise RuntimeError("sensetime key 未配置")
    return key


def gen(key: str, prompt: str):
    last = None
    for size in SIZES_TO_TRY:
        body = json.dumps({"model": MODEL, "prompt": prompt, "n": 1, "size": size}).encode()
        req = urllib.request.Request(
            URL, data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        try:
            r = json.loads(urllib.request.urlopen(req, timeout=180).read())
            item = r["data"][0]
            if item.get("b64_json"):
                img = Image.open(__import__("io").BytesIO(base64.b64decode(item["b64_json"])))
            else:
                img = Image.open(__import__("io").BytesIO(urllib.request.urlopen(item["url"], timeout=120).read()))
            return img.convert("RGB"), size
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "ignore")[:200]
            last = f"{size}: HTTP {e.code} {msg}"
            print(f"  [retry] {last}", flush=True)
            continue
        except Exception as e:  # noqa: BLE001
            last = f"{size}: {e}"
            print(f"  [retry] {last}", flush=True)
            continue
    raise RuntimeError(f"全部尺寸失败，最后错误 {last}")


def center_crop_169(img: Image.Image) -> Image.Image:
    w, h = img.size
    target = 16 / 9
    cur = w / h
    if abs(cur - target) < 0.005:
        return img
    if cur > target:
        nw = int(h * target)
        x = (w - nw) // 2
        return img.crop((x, 0, x + nw, h))
    nh = int(w / target)
    y = (h - nh) // 2
    return img.crop((0, y, w, y + nh))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    key = load_key()
    for rid, prompt in PROMPTS.items():
        rd = OUT_ROOT / rid
        raw_dir = rd / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        # 归档旧 bg
        old = rd / "bg.webp"
        if old.exists():
            old.replace(raw_dir / "prev_bg.webp")
        print(f"[{rid}] 生成中…", flush=True)
        t0 = time.time()
        img, used_size = gen(key, prompt)
        img.save(raw_dir / "ai_bg_master.png", "PNG")
        final = center_crop_169(img)
        final.save(rd / "bg.webp", "WEBP", quality=88, method=6)
        t = final.copy()
        t.thumbnail((480, 480))
        t.save(rd / "bg_thumb.jpg", "JPEG", quality=80)
        print(f"[{rid}] OK 请求尺寸={used_size} 实得={img.size} 最终={final.size} 用时{time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
