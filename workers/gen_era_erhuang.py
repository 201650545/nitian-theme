# -*- coding: utf-8 -*-
"""Seedream 4.5 图生图 · 官方王林形象二创（10 时代立绘）
参考图 = 已验证官方海报；要求保持人物设计一致，仅改时代/服装/场景。
"""
import base64
import json
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

ST = json.load(open(r"D:\项目\data\search_gateway\api_state.json", encoding="utf-8-sig"))
GW_KEY = ST["api_key"]
P = Path(r"D:\游戏\逆天主题\workers\officials\posters_season_general")
OUT = Path(r"D:\游戏\逆天主题\assets\ui\chars")
URL = "http://127.0.0.1:3100/v1/images/generations"
MODEL = "doubao-seedream-4-5-251128"

KEEP = "保持参考图中王林的面部、发型、人物设计完全一致，仙逆动画官方画风，国漫3D渲染，电影级打光，竖版全身立绘构图，人物清晰，无文字"


def to_data_url(p: Path) -> str:
    b = p.read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(b).decode()


JOBS = [
    ("era_01_ningshi", P / "poster_season_movie2_01.jpg", "凝气期的少年王林，粗布麻衣，清瘦坚韧，站在恒岳山后山悬崖，云雾缭绕的冷青山谷"),
    ("era_02_zhuji", P / "poster_season_movie2_01.jpg", "筑基期的王林，青灰宗门弟子服，背佩铁剑，站在铁柱峰演武场，云海翻涌"),
    ("era_03_jiedan", P / "poster_season_movie2_01.jpg", "结丹期的王林，玄黑色杀伐劲装银纹刺绣，周身金色丹光，赵国古城夜色背景"),
    ("era_04_yuanying", P / "poster_season_movie1_01.jpg", "元婴期的王林，白发红衣煞星，立于百万人头塔前，暗红血色与星蓝微光"),
    ("era_05_huashen", P / "poster_season_nianfan3_01.jpg", "化神期的王林，朴素青衫胜雪，木雕师气质，道韵光环缭绕，雨之仙界飞瀑流云"),
    ("era_06_yingbian", P / "poster_season_nianfan2_01.jpg", "婴变期的王林，白发狂舞红衣，蜕变之始的压迫感，紫黑雷云背景"),
    ("era_07_wending", P / "poster_season_nianfan3_01.jpg", "问鼎期的王林，墨黑华服金线刺绣，问鼎巅峰的威严，水墨群山之巅"),
    ("era_08_yinyang", P / "poster_season_nianfan2_01.jpg", "阴虚阳实期的王林，半阴半阳双色气场交织，星蓝与暗红分流"),
    ("era_12_kongnie", P / "poster_season_movie1_01.jpg", "空之四境的王林，古神形态，白发星纹，立于星空虚空，古神虚影沉眠身后"),
    ("era_16_tatian", P / "poster_season_nianfan2_01.jpg", "踏天九桥的王林，鎏金道袍，立于横贯云海的金色天桥，金光大道通向彼岸"),
]


def gen(prompt: str, ref_dataurl: str):
    body = json.dumps({
        "model": MODEL,
        "prompt": prompt + "。" + KEEP,
        "image": [ref_dataurl],
        "size": "2048x2732",
        "response_format": "url",
        "watermark": False,
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": "Bearer " + GW_KEY, "Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=300).read())
    item = r["data"][0]
    if item.get("b64_json"):
        return Image.open(__import__("io").BytesIO(base64.b64decode(item["b64_json"]))).convert("RGB")
    return Image.open(__import__("io").BytesIO(urllib.request.urlopen(item["url"], timeout=120).read())).convert("RGB")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for name, ref, prompt in JOBS:
        out = OUT / (name + ".png")
        if out.exists():
            print("[skip]", name)
            continue
        t0 = time.time()
        try:
            img = gen(prompt, to_data_url(ref))
            # 裁掉底部 6%（去 AI 生成水印，若有）
            w, h = img.size
            img = img.crop((0, 0, w, int(h * 0.94)))
            img.save(out, "PNG")
            print(f"[OK] {name} {img.size} {time.time()-t0:.0f}s", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] {name}: {str(e)[:140]}", flush=True)
        time.sleep(3)


if __name__ == "__main__":
    main()
