# -*- coding: utf-8 -*-
"""v2.7 bg_09 重生成 — agnes-image-2.1-flash 主路（seedream-5.0 账号暂停，4.5 备用）

bg_09_kunie 原版含骷髅骨影，用户拍板重生成。
提示词沿用 chronicle.json 窥涅意象但去掉骨影，用「先贤遗蜕化作光尘」抽象化表达。
agnes 512x512 起（可放大裁切）；若失败 fallback seedream-4.5（2560x1440 合规尺寸）。
输出 assets/ui/bgs/bg_09_kunie.jpg（2048x1152，与 v2.6 其余 12 张同规格）。
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

OUT = Path(r"D:\游戏\逆天主题\assets\ui\bgs\bg_09_kunie.jpg")
BACKUP = Path(r"D:\游戏\逆天主题\assets\ui\bgs\bg_09_kunie.skeleton.jpg")

PROMPT = (
    "腾讯仙逆动画官方画风，2D动漫风格，上古洞府内部幽暗石室，横版电影构图，"
    "空无一人的石室：禁制血雾缓缓消散，空气中青蓝色发光符文纹路与流火明灭流动，"
    "石室中央只有一团缓缓旋升的金色光尘汇聚成的螺旋光柱（没有人没有骷髅没有人物剪影）,"
    "四周石壁符文明灭，地面残存淡淡血渍痕迹，石室深处肃穆压迫，"
    "青蓝冷色调体积光，史诗氛围，细节丰富，无文字无水印无边框，画面中没有人物"
)


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


def main():
    if not BACKUP.exists():
        if OUT.exists():
            OUT.rename(BACKUP)
            print(f"[backup] {BACKUP.name}", flush=True)
    t0 = time.time()
    try:
        img = gen_agnes(PROMPT)
        src = "agnes-image-2.1-flash"
    except Exception as e:  # noqa: BLE001
        print(f"  [agnes fail] {str(e)[:120]} -> fallback ark 4.5", flush=True)
        img = gen_ark45(PROMPT)
        src = "doubao-seedream-4-5-251128"
    # 中心偏上裁切到 2048x1152
    w, h = img.size
    target = 2048 / 1152
    if w / h < target:
        nh = int(w / target)
        top = int((h - nh) * 0.42)
        img = img.crop((0, top, w, top + nh))
    else:
        nw = int(h * target)
        left = (w - nw) // 2
        img = img.crop((left, 0, left + nw, h))
    if img.size != (2048, 1152):
        img = img.resize((2048, 1152), Image.LANCZOS)
    img.save(OUT, "JPEG", quality=90)
    print(f"[OK] bg_09_kunie.jpg 2048x1152 via {src} {time.time()-t0:.0f}s {OUT.stat().st_size//1024}KB", flush=True)


if __name__ == "__main__":
    main()
