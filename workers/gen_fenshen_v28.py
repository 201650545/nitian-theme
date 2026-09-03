# -*- coding: utf-8 -*-
"""v2.8 任务C 分身立绘×4 — agnes-image-2.1-flash 主路（key 严禁打印）

分身 = 与王林容貌相同、气质木讷朴实的化身（化名许木），前期（筑基~化神）行走世间。
输出 assets/ui/chars/fenshen_XX_*.png，3:4 竖版 PNG（1536x2048），与 era_XX_*.png 同风格。
失败 fallback doubao-seedream-4-5（2560x1440 起步合规尺寸，走本机 3100 网关）。
"""
import base64
import io
import json
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

GW_KEY = json.load(open(r"D:\项目\data\search_gateway\api_state.json", encoding="utf-8-sig"))["api_key"]
CH = json.load(open(r"D:\项目\data\search_gateway\channels.json", encoding="utf-8-sig"))
KEYS = CH.get("keys") or {}
OUT_DIR = Path(r"D:\游戏\逆天主题\assets\ui\chars")

BASE = (
    "腾讯仙逆动画官方画风，2D动漫风格，修仙角色立绘，"
    "与主角王林容貌完全相同的分身（化名许木）：黑发束发，面容清瘦坚毅，"
    "气质木讷朴实、沉默内敛，眼神平静无波，"
    "单人全身竖版构图居中，简洁暗色渐变背景，"
    "细节丰富，无文字无水印无边框，画面中只有这一个人"
)

JOBS = [
    ("fenshen_02_zhuji", "粗布麻衣短打，凡人樵夫般朴素装束，腰间系旧布带，站姿端正，山道石阶背景虚化"),
    ("fenshen_03_jiedan", "灰色布袍，衣衫简朴但针脚细密，腰悬小小储物袋，气息内敛，云雾山巅背景虚化"),
    ("fenshen_04_yuanying", "深青色旧长袍，元婴修士气度，周身若有若无灵光，星空背景虚化"),
    ("fenshen_05_huashen", "素色宽袍，神识浩瀚悠远，衣袂微动，虚幻星河背景虚化"),
]


def gen_agnes(prompt: str) -> Image.Image:
    body = json.dumps({"model": "agnes-image-2.1-flash", "prompt": prompt, "n": 1, "size": "1024x1024"}).encode()
    req = urllib.request.Request(
        "https://apihub.agnes-ai.com/v1/images/generations", data=body,
        headers={"Authorization": "Bearer " + KEYS["agnes"], "Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=180).read())
    it = (r.get("data") or [{}])[0]
    if it.get("b64_json"):
        return Image.open(io.BytesIO(base64.b64decode(it["b64_json"]))).convert("RGB")
    return Image.open(io.BytesIO(urllib.request.urlopen(it["url"], timeout=120).read())).convert("RGB")


def gen_ark45(prompt: str) -> Image.Image:
    body = json.dumps({"model": "doubao-seedream-4-5-251128", "prompt": prompt, "size": "2560x1440",
                       "response_format": "url", "watermark": False}).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:3100/v1/images/generations", data=body,
        headers={"Authorization": "Bearer " + GW_KEY, "Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=300).read())
    it = (r.get("data") or [{}])[0]
    if it.get("b64_json"):
        return Image.open(io.BytesIO(base64.b64decode(it["b64_json"]))).convert("RGB")
    return Image.open(io.BytesIO(urllib.request.urlopen(it["url"], timeout=120).read())).convert("RGB")


def to_34(img: Image.Image) -> Image.Image:
    # 裁成 3:4 竖版：人脸在上半部，裁切重心偏上（0.35）
    w, h = img.size
    target = 3 / 4
    if w / h > target:
        nw = int(h * target)
        left = (w - nw) // 2
        img = img.crop((left, 0, left + nw, h))
    else:
        nh = int(w / target)
        top = int((h - nh) * 0.35)
        img = img.crop((0, top, w, top + nh))
    return img.resize((1536, 2048), Image.LANCZOS)


def main():
    only = sys.argv[1:] or [j[0] for j in JOBS]
    for name, era in JOBS:
        if name not in only:
            continue
        out = OUT_DIR / (name + ".png")
        if out.exists():
            print(f"[skip] {out.name} 已存在", flush=True)
            continue
        t0 = time.time()
        prompt = BASE + "，" + era
        try:
            img = gen_agnes(prompt)
            src = "agnes"
        except Exception as e:  # noqa: BLE001
            print(f"  [agnes fail] {str(e)[:120]} -> fallback ark 4.5", flush=True)
            img = gen_ark45(prompt)
            src = "ark45"
        img = to_34(img)
        img.save(out, "PNG")
        print(f"[OK] {out.name} 1536x2048 via {src} {time.time()-t0:.0f}s {out.stat().st_size//1024}KB", flush=True)


if __name__ == "__main__":
    main()
