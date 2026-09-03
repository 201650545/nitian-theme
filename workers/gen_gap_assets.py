# -*- coding: utf-8 -*-
"""逆天主题资产缺口补齐 — 一次性生成脚本（可断点续跑，已存在的跳过）
覆盖 4 项（2026-08-31 用户拍板）：
  1. 元婴期背景   workers/collected/yuanying/bg-01.jpg  (Seedream 5.0, 横版 16:9)
  2. 印章 12 枚    seal_16~27                              (Seedream 4.5, 1024²)
  3. 踏天桥立绘 9 张 era_19_qiao1 ~ era_27_qiao9          (Seedream 5.0, 竖版 3:4)
  4. 心魔敌人 4 张 assets/enemies/fiend_*.png              (Seedream 5.0, 1024²)
模型路由走本地网关 :3100（生图端点，key 读 api_state.json，不打印）。
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

ST = json.load(open(r"D:\项目\data\search_gateway\api_state.json", encoding="utf-8-sig"))
GW_KEY = ST["api_key"]
URL = "http://127.0.0.1:3100/v1/images/generations"

ROOT = Path(r"D:\游戏\逆天主题")
MODEL_S5 = "doubao-seedream-5-0-260128"   # 立绘/背景/心魔（沿用 gen_chron_imgs 成功模型）
MODEL_S45 = "doubao-seedream-4-5-251128"  # 印章（沿用 gen_seals_v2 风格一致）

TAIL_LI = "腾讯仙逆动画官方画风，2D动漫风格，竖版海报构图，人物半身居中偏下，背景场景分明，冷色调体积光，史诗电影感，发丝衣袍细节丰富，无文字无水印无边框"
TAIL_BG = "腾讯仙逆动画官方画风，2D动漫风格，横版电影构图，场景宏大，冷色调体积光，史诗氛围，细节丰富，无文字无水印无边框"
TAIL_SEAL = "仙侠风境界徽章图标，圆形玉印构图，对称庄重，描线精致，宝石质感，纯深色背景居中，游戏UI图标，无文字"
TAIL_FOE = "腾讯仙逆动画官方画风，2D动漫风格，反派暗面心魔形象，半身居中，血月暗红背景，冷暗色调，邪异压迫感，发丝衣袍细节丰富，无文字无水印无边框"


_MODEL = MODEL_S5


def gen(prompt: str, sizes) -> Image.Image:
    last = None
    for size in sizes:
        body = json.dumps({"model": _MODEL, "prompt": prompt, "size": size,
                           "response_format": "url", "watermark": False}).encode()
        req = urllib.request.Request(URL, data=body, headers={
            "Authorization": "Bearer " + GW_KEY, "Content-Type": "application/json"})
        try:
            r = json.loads(urllib.request.urlopen(req, timeout=300).read())
            item = r["data"][0]
            if item.get("b64_json"):
                return Image.open(io.BytesIO(base64.b64decode(item["b64_json"]))).convert("RGB")
            return Image.open(io.BytesIO(urllib.request.urlopen(item["url"], timeout=120).read())).convert("RGB")
        except Exception as e:  # noqa: BLE001
            last = e
            print(f"  [retry {size}] {str(e)[:90]}", flush=True)
            time.sleep(4)
    raise RuntimeError("gen fail: " + str(last))


# ---- 任务定义 ---------------------------------------------------------------

JOBS = [
    # 1. 元婴期背景（官方CG 王林与李慕婉 横版）
    {
        "model": MODEL_S5, "sizes": ["2048x1152", "1920x1080", "1024x576"],
        "out": ROOT / "workers" / "collected" / "yuanying" / "bg-01.jpg",
        "fmt": "JPEG",
        "prompt": "白发仙侠修士王林与青衫女子李慕婉并肩立于赵国古城墙前，身后百万人头塔剪影直入苍穹，星蓝夜空血色云层，古战场肃杀氛围，" + TAIL_BG,
    },
    # 2. 印章 12 枚（16 空劫后期 + 19-27 踏天九桥）
    *[{"model": MODEL_S45, "sizes": ["1024x1024", "2048x2048"],
       "out": ROOT / "assets" / "ui" / "seals" / (f + ".png"), "fmt": "PNG",
       "prompt": d + "，" + TAIL_SEAL} for f, d in [
        ("seal_16_kongzun", "空劫天尊徽印：天尊宝相威严，金色天雷缠绕，暗金色 #d2bd5e 与鎏金描线"),
        ("seal_17_kongyue", "空劫跃天尊徽印：跃出金色天门的瞬间动势，金白色 #dcc96a 与暗金描线"),
        ("seal_18_kongda", "空劫大天尊徽印：神识光环全开，浩瀚星空独尊之势，鎏金圣白色 #e6d574 描线"),
        ("seal_19_qiao1", "踏天一桥徽印：初登横贯云海的金色天桥，定界罗盘法阵旋转，圣金 #e0c05a 描线"),
        ("seal_20_qiao2", "踏天二桥徽印：步步生莲，天道化身虚影崩散，金蓝 #dcb84f 描线"),
        ("seal_21_qiao3", "踏天三桥徽印：手握断裂道果，轮回法环镇压天道，鎏金玄黑 #d8b045 描线"),
        ("seal_22_qiao4", "踏天四桥徽印：始古山巨大剪影，挥袖定计俯瞰众生，古朴金灰 #d4a83b 描线"),
        ("seal_23_qiao5", "踏天五桥徽印：半渡之境，三个自身虚影合而为一，金白 #d0a031 描线"),
        ("seal_24_qiao6", "踏天六桥徽印：桥心悟道，幻影破碎唯真我前行，金烬 #cc9828 描线"),
        ("seal_25_qiao7", "踏天七桥徽印：一拳轰碎天道之影，金色冲击波，史诗金 #c89020 描线"),
        ("seal_26_qiao8", "踏天八桥徽印：持剑斩落，因果长河逆转，金红 #c48818 描线"),
        ("seal_27_qiao9", "踏天九桥徽印：彼岸大门在望，因果花雨洒落，璀璨金白 #ffd700 描线"),
    ]],
    # 3. 踏天桥立绘 9 张（竖版 3:4）
    *[{"model": MODEL_S5, "sizes": ["1728x2304", "2048x2732", "1920x1920"],
       "out": ROOT / "assets" / "ui" / "chars" / (f + ".png"), "fmt": "PNG",
       "prompt": d + "，" + TAIL_LI} for f, d in [
        ("era_19_qiao1", "踏天境白发王林初登横贯云海的金色天桥，一桥之影，定界罗盘法阵在脚下旋转，圣洁金辉"),
        ("era_20_qiao2", "踏天境白发王林行至二桥，身后天道化身虚影哀嚎崩散，因果丝线断裂，金蓝对撞色调"),
        ("era_21_qiao3", "踏天境白发王林三桥之上，手握断裂道果，轮回法环镇压天道虚影，鎏金玄黑色调"),
        ("era_22_qiao4", "踏天境白发王林立于始古山前挥袖定计，山岳巨大剪影，衣袍鼓荡，古朴苍茫金灰色调"),
        ("era_23_qiao5", "踏天境白发王林五桥问心，三个自身虚影合而为一，道门微启透出彼岸光，金白色调"),
        ("era_24_qiao6", "踏天境白发王林行于六桥，周遭幻影破碎，唯真我前行，古道苍茫，金烬色调"),
        ("era_25_qiao7", "踏天境白发王林七桥决战，一拳轰碎巨大天道之影，金色冲击波撕裂云海，史诗爆发构图"),
        ("era_26_qiao8", "踏天境白发王林八桥之上持剑斩落，因果长河逆转，生死轮回倒卷，金红对撞色调"),
        ("era_27_qiao9", "踏天境白发王林立于九桥尽头，脚下天运子陨落化作因果花雨，彼岸大门在望，大道尽头的璀璨金白"),
    ]],
    # 4. 心魔敌人 4 张（方形 1:1，按纪元分档）
    *[{"model": MODEL_S5, "sizes": ["1024x1024", "1920x1920"],
       "out": ROOT / "assets" / "enemies" / (f + ".png"), "fmt": "PNG",
       "prompt": d + "，" + TAIL_FOE} for f, d in [
        ("fiend_early", "黑发少年王林的暗面心魔，红瞳幽光，黑衣如墨，身后尸山血海虚影，邪异冷笑"),
        ("fiend_yuanying", "白发狂舞王林的暗面心魔，眉心古神星点化作血光，黑袍猎猎，身后百万人头塔血色剪影"),
        ("fiend_kongjie", "红发古神王林的暗面心魔，金色天雷缠绕却泛暗红，睥睨众生，周身虚空裂缝"),
        ("fiend_tatian", "踏天境白发王林的暗面心魔，立于崩碎金色天桥残骸，金色灵力染上猩红，大道尽头幽暗"),
    ]],
]


def main():
    global _MODEL
    done = 0
    for job in JOBS:
        if job["out"].exists():
            print("[skip]", job["out"].name, flush=True)
            done += 1
            continue
        _MODEL = job["model"]
        job["out"].parent.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        try:
            img = gen(job["prompt"], job["sizes"])
            img.save(job["out"], job["fmt"], quality=90)
            print(f"[OK] {job['out'].relative_to(ROOT)} {img.size} {time.time()-t0:.0f}s {job['out'].stat().st_size//1024}KB", flush=True)
            done += 1
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] {job['out'].name}: {str(e)[:120]}", flush=True)
        time.sleep(2)
    print(f"=== 完成 {done}/{len(JOBS)} ===", flush=True)


if __name__ == "__main__":
    main()
