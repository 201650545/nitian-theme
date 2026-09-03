# -*- coding: utf-8 -*-
"""15 境界徽印重做（Seedream 4.5）：故事元素 + 境界配色，游戏 UI 图标质感"""
import json
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

ST = json.load(open(r"D:\项目\data\search_gateway\api_state.json", encoding="utf-8-sig"))
GW_KEY = ST["api_key"]
URL = "http://127.0.0.1:3100/v1/images/generations"
OUT = Path(r"D:\逆天主题\assets\ui\seals")

STYLE = "仙侠风境界徽章图标，圆形玉印构图，对称庄重，描线精致，宝石质感，纯深色背景居中，游戏UI图标，无文字"
SEALS = [
    ("seal_01_ningshi", "凝气期徽印：缭绕云雾气旋与一株青竹新芽，冷青色 #5a9e8f 与淡金描线"),
    ("seal_02_zhuji", "筑基期徽印：铁柱峰剪影与基石裂纹，灰绿色 #7fa88f 与银灰描线"),
    ("seal_03_jiedan", "结丹期徽印：中央一颗旋转金丹与光涡，赤红色 #b8453a 与鎏金描线"),
    ("seal_04_yuanying", "元婴期徽印：星环环绕的婴孩虚影与古神星点，星蓝色 #3b7fd4 与银蓝描线"),
    ("seal_05_huashen", "化神期徽印：绽放青莲与飞瀑道韵环绕，银白色 #b8c6da 与清青描线"),
    ("seal_06_yingbian", "婴变期徽印：破茧裂痕与飘散白发红绸，紫红色 #9a6fb8 与暗金描线"),
    ("seal_07_wending", "问鼎期徽印：一尊青铜鼎矗立群山之巅，鎏金色 #d0a83c 与玄墨描线"),
    ("seal_08_yinyang", "阴虚阳实徽印：阴阳双鱼旋转漩涡，青碧色 #5a9e8f 与月银描线"),
    ("seal_09_kunie", "窥涅期徽印：一只洞察虚空的涅槃之眼，蓝紫色 #6a89b8 与星银描线"),
    ("seal_10_jingnie", "净涅期徽印：净莲涤尘光雨洒落，青蓝色 #4f9bb0 与月白描线"),
    ("seal_11_suinie", "碎涅期徽印：碎裂星核迸发光芒，橙金色 #b8763a 与赤金描线"),
    ("seal_12_kongnie", "空涅期徽印：一扇虚空之门与门后星云，紫金色 #7d6ab8 与暗金描线"),
    ("seal_13_kongling", "空灵期徽印：灵蝶虚影绕月飞舞，淡紫色 #8a7fc9 与银白描线"),
    ("seal_14_kongxuan", "空玄期徽印：玄冰纹法阵层层旋转，冰蓝色 #6f89c9 与霜银描线"),
    ("seal_15_kongjie", "空劫期徽印：劫云汇聚的天眼与雷霆，暗金色 #c9b45a 与朱砂描线"),
]


def gen(prompt, size):
    body = json.dumps({"model": "doubao-seedream-4-5-251128", "prompt": prompt, "size": size,
                       "response_format": "url", "watermark": False}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": "Bearer " + GW_KEY, "Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=300).read())
    item = r["data"][0]
    if item.get("b64_json"):
        import base64, io
        return Image.open(io.BytesIO(base64.b64decode(item["b64_json"]))).convert("RGB")
    return Image.open(__import__("io").BytesIO(urllib.request.urlopen(item["url"], timeout=120).read())).convert("RGB")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    for fname, desc in SEALS:
        out = OUT / (fname + ".png")
        if out.exists():
            print("[skip]", fname)
            continue
        t0 = time.time()
        ok = False
        for size in ("1024x1024", "2048x2048"):
            try:
                img = gen(desc + "，" + STYLE, size)
                img.save(out, "PNG")
                print(f"[OK] {fname} {img.size} {time.time()-t0:.0f}s", flush=True)
                ok = True
                break
            except Exception as e:  # noqa: BLE001
                print(f"[retry-{size}] {fname}: {str(e)[:110]}", flush=True)
                time.sleep(4)
        if not ok:
            print(f"[FAIL] {fname}", flush=True)
        time.sleep(2)


if __name__ == "__main__":
    main()
