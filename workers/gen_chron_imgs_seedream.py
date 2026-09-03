# -*- coding: utf-8 -*-
"""卷轴配图重做 — Seedream 5.0 官方形象锚定（2026-08-27，用户指示：官方找不到就用已有形象生成，先用即梦5.0额度）
输出 assets/ui/chronicle-img/gen/<rid>.png，竖版 3:4。
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
URL = "http://127.0.0.1:3100/v1/images/generations"
OUT = Path(r"D:\逆天主题\assets\ui\chronicle-img\gen")
MODEL = "doubao-seedream-5-0-260128"

TAIL = "腾讯仙逆动画官方画风，2D动漫风格，竖版海报构图，人物半身居中偏下，背景场景分明，冷色调体积光，史诗电影感，发丝衣袍细节丰富，无文字无水印无边框"

JOBS = {
    "02_zhuji": "麻衣黑发少年修士王林，双眸隐现紫色电弧，神情阴郁狠辣，立于火焚国赤红荒原，身后城郭火光与浓烟",
    "04_yuanying": "白发狂舞的绝世煞星王林，眉心闪烁古神星点，黑袍猎猎，身后赵国古城前百万人头塔直入苍穹，星蓝夜空血色云层",
    "09_kunie": "白发红袍修士王林，双眼化作洞察虚妄的涅槃法目，周身万魂幡虚影与金色骨光环绕，深蓝虚空",
    "10_jingnie": "白发红袍修士王林盘坐莲台，净莲光雨洒落洗炼周身，身后巨大轮回法环缓缓旋转，青蓝圣洁光晕",
    "11_suinie": "红发古神形态王林，周身暗红雷霆与碎星之力迸发，脚下方碎裂的大道金桥，暗红赤金色调",
    "12_kongnie": "红发古神形态王林，身前一扇虚空之门缓缓开启，星云缠身，紫金色调神秘威严",
    "13_kongling": "白发红袍修士王林立于月下，数只发光灵蝶绕月飞舞，意境空灵静谧，淡紫银白色调",
    "14_kongxuan": "红发古神形态王林，周身玄冰法阵层层旋转，霜花与星光交织，败雷仙后睥睨之姿，冰蓝紫色调",
    "15_kongjin": "红发古神形态王林金尊威严，头顶暗金劫云汇聚成天眼，金之极道气息，暗金鎏金色调",
    "16_kongzun": "红发古神形态王林天尊之姿，一令出而万法随，周身金色天雷缠绕，宝相威严，暗金色调",
    "17_kongyue": "红发古神形态王林跃出巨大金色天门的瞬间，动势凌厉，碎片纷飞，跃天尊超脱之意，金白色调",
    "18_kongda": "红发古神形态王林大天尊圆满之境，眉心神识光环全开，古往今来独尊之势，浩瀚星空背景，鎏金圣白色调",
    "19_qiao1": "踏天境白发王林初登横贯云海的金色天桥，一桥之影，定界罗盘法阵在脚下旋转，圣洁金辉",
    "20_qiao2": "踏天境白发王林行至二桥，身后天道化身虚影哀嚎崩散，因果丝线断裂，金蓝对撞色调",
    "21_qiao3": "踏天境白发王林三桥之上，手握断裂道果，轮回法环镇压天道虚影，鎏金玄黑色调",
    "22_qiao4": "踏天境白发王林立于始古山前挥袖定计，山岳巨大剪影，衣袍鼓荡，古朴苍茫金灰色调",
    "23_qiao5": "踏天境白发王林五桥问心，三个自身虚影合而为一，道门微启透出彼岸光，金白色调",
    "24_qiao6": "踏天境白发王林行于六桥，周遭幻影破碎，唯真我前行，古道苍茫，金烬色调",
    "25_qiao7": "踏天境白发王林七桥决战，一拳轰碎巨大天道之影，金色冲击波撕裂云海，史诗爆发构图",
    "26_qiao8": "踏天境白发王林八桥之上持剑斩落，因果长河逆转，生死轮回倒卷，金红对撞色调",
    "27_qiao9": "踏天境白发王林立于九桥尽头，脚下天运子陨落化作因果花雨，彼岸大门在望，大道尽头的璀璨金白",
}

SIZES = ["1728x2304", "2048x2732", "1920x1920"]


def gen(prompt: str) -> Image.Image:
    last = None
    for size in SIZES:
        body = json.dumps({"model": MODEL, "prompt": prompt + "，" + TAIL, "size": size,
                           "response_format": "url", "watermark": False}).encode()
        req = urllib.request.Request(URL, data=body, headers={
            "Authorization": "Bearer " + ST["api_key"], "Content-Type": "application/json"})
        try:
            r = json.loads(urllib.request.urlopen(req, timeout=300).read())
            item = r["data"][0]
            if item.get("b64_json"):
                return Image.open(io.BytesIO(base64.b64decode(item["b64_json"]))).convert("RGB")
            return Image.open(urllib.request.urlopen(item["url"], timeout=120)).convert("RGB")
        except Exception as e:  # noqa: BLE001
            last = e
            print("  size", size, "fail:", str(e)[:100], flush=True)
    raise RuntimeError("gen fail: " + str(last))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1:] or list(JOBS)
    for rid in only:
        out = OUT / (rid + ".png")
        if out.exists():
            print("[skip]", rid, flush=True)
            continue
        t0 = time.time()
        img = gen(JOBS[rid])
        img.save(out, "PNG")
        print(rid, img.size, f"{(time.time()-t0):.0f}s", f"{out.stat().st_size//1024}KB", flush=True)


if __name__ == "__main__":
    main()
