# -*- coding: utf-8 -*-
"""U1.5 Lite · 时代立绘×6 + 境界背景×5（全部落 verified 目录）"""
import base64
import io
import json
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

KEYS_PATH = Path(r"D:\项目\data\search_gateway\channels.json")
ROOT = Path(r"D:\游戏\逆天主题\assets")
URL = "https://token.sensenova.cn/v1/images/generations"

BASE = "仙逆动画官方画风，国漫3D渲染，王林，"
CHAR_TAIL = "竖版全身立绘构图，人物清晰居中，背景虚化，电影级打光，细节丰富，无文字"
BG_TAIL = "横版16:9场景，无人空景，电影级构图，体积光，细节丰富，无文字"

JOBS = [
    # (outrel, filename, size, prompt)
    ("ui/chars", "char_01_ningshi.png", "1152x1536",
     BASE + "青涩农家少年，粗布麻衣，黑发丹凤眼，眼神坚韧冷峻，恒岳山云雾石崖背景，" + CHAR_TAIL),
    ("ui/chars", "char_02_zhuji.png", "1152x1536",
     BASE + "青灰弟子服少年修士，黑发束冠，背佩铁剑，站在铁柱峰演武场云海之上，坚毅，" + CHAR_TAIL),
    ("ui/chars", "char_03_jiedan.png", "1152x1536",
     BASE + "黑衣杀伐修士，玄黑劲装银纹刺绣，周身金色丹光环绕，眼神狠辣，古城夜色背景，" + CHAR_TAIL),
    ("ui/chars", "char_05_huashen.png", "1152x1536",
     BASE + "朴素青衫胜雪，木雕师气质，眼神深邃沧桑，道韵光环缭绕，清冷银白意境，飞瀑流云背景，" + CHAR_TAIL),
    ("ui/chars", "char_12_kongjing.png", "1152x1536",
     BASE + "古神形态，白发狂舞，眉心古神星纹，星蓝与暗金神纹缠绕，立于星空虚空，威压苍穹，" + CHAR_TAIL),
    ("ui/chars", "char_16_tatian.png", "1152x1536",
     BASE + "鎏金道袍，白发无瑕，立于横贯云海的金色天桥之上，金光大道延伸天际，超然物外，" + CHAR_TAIL),
    ("realms/02_zhuji/raw", "ai_bg_master.png", "2048x1152",
     "仙逆动画官方画风，铁柱峰修真宗门建筑群，飞檐道殿沿山而建，云海翻涌，晨光金辉，" + BG_TAIL),
    ("realms/03_jiedan/raw", "ai_bg_master.png", "2048x1152",
     "仙逆动画官方画风，赵国古城夜景，城墙灯火与血月高悬，杀伐肃杀之气，暗红与玄墨色调，" + BG_TAIL),
    ("realms/05_huashen/raw2", "ai_bg_master.png", "2048x1152",
     "仙逆动画官方画风，雨之仙界仙玉祭坛，飞瀑流云环绕白玉祭坛，清冷青色银白辉光，空灵太虚意境，" + BG_TAIL),
    ("ui/bgs", "bg_kongjing.png", "2048x1152",
     "仙逆动画官方画风，古神虚空星域，巨大古神虚影沉眠于星云深处，星蓝暗金交织，苍茫神秘，" + BG_TAIL),
    ("ui/bgs", "bg_tatian.png", "2048x1152",
     "仙逆动画官方画风，金色天桥横跨无边云海直通彼岸光辉，九座桥影层层远去，鎏金圣洁，" + BG_TAIL),
]


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
    for rel, fname, size, prompt in JOBS:
        outdir = ROOT / rel
        outdir.mkdir(parents=True, exist_ok=True)
        out = outdir / fname
        if out.exists():
            print(f"[skip] {rel}/{fname}")
            continue
        t0 = time.time()
        ok = False
        for attempt in range(3):
            try:
                img = gen(key, prompt, size)
                img.save(out, "PNG")
                print(f"[OK] {rel}/{fname} {img.size} {time.time()-t0:.0f}s", flush=True)
                ok = True
                break
            except Exception as e:  # noqa: BLE001
                print(f"[retry{attempt+1}] {rel}/{fname}: {str(e)[:100]}", flush=True)
                time.sleep(8 * (attempt + 1))
        if not ok:
            print(f"[FAIL] {rel}/{fname}", flush=True)
        time.sleep(4)


if __name__ == "__main__":
    main()
