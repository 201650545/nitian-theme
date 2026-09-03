# -*- coding: utf-8 -*-
"""v2.6 逐境背景补齐 — 06~18 共 13 张（Seedream 5.0 via 网关 :3100，可断点续跑）

背景缺口：06~18 十三境复用 4 张共享背景（kong/jiedan/huashen/zhuji）。
提示词核心沿用 gen_bt_batch.py 中已验证干净（无文字污染）的逐境意象，
输出 assets/ui/bgs/bg_<rid>.jpg（横版 2048x1152 优先）。
提示词约束沿用 2026-08-29 实验结论：绝不点名可刻字物体（碑/简/壁画），
改用抽象光纹/光影表达同一意象。
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
OUT_DIR = ROOT / "assets" / "ui" / "bgs"
MODEL = "doubao-seedream-5-0-260128"  # 背景（沿用 gen_gap_assets 成功模型）

TAIL_COLD = "腾讯仙逆动画官方画风，2D动漫风格，横版电影构图，场景宏大，冷色调体积光，史诗氛围，细节丰富，无文字无水印无边框"
TAIL_WARM = "腾讯仙逆动画官方画风，2D动漫风格，横版电影构图，场景宏大，暖金色体积光，史诗氛围，细节丰富，无文字无水印无边框"

# 13 境提示词（意象源自 chronicle.json scene + bt 视频已验证措辞）
JOBS = [
    ("06_yingbian", "朱雀星上古祭坛，环形石台矗立于血海中央，天空血雨纷飞渐歇，一颗暗红魂珠悬浮吞纳万千魂光，祭坛紫色纹路明灭，远处修士逃散剪影，紫红色调，" + TAIL_COLD),
    ("07_wending", "雨之仙界，一条鎏金长桥横贯云海，桥身血迹斑驳，桥面裂开虚空裂隙，两侧雷云轰鸣翻涌，一道剑光余痕划过天际，鎏金色调，" + TAIL_WARM),
    ("08_yinyang", "阴阳桥横跨混沌虚空，黑白云雾在桥面翻滚交织成巨大太极图纹，桥心石面裂开细缝，一枚黑白交融的光珠缓缓升起映照天穹，黑白色调，" + TAIL_COLD),
    ("09_kunie", "上古洞府内部幽暗石室，禁制血雾渐散，空气中青蓝色发光符文纹路与流火明灭流动，金色骨影微光隐现，肃穆压迫，青蓝冷色调，" + TAIL_COLD),
    ("10_jingnie", "轮回之巅孤峰绝顶，脚下虚空碎裂如镜面崩散，无数虚影在四周明灭闪过，一道碧青金光自天穹垂落，碧青色调，" + TAIL_COLD),
    ("11_suinie", "天运海浩瀚无垠，海心一座参天轮回树虚影贯通天地，轮回之光自树冠洒落映照海面，波光赤金交织，天穹云层透光，赤金色调，" + TAIL_WARM),
    ("12_kongnie", "虚空之中轮回树参天而立，树冠遮蔽天穹，万道因果丝线如金色细线缠绕树根垂落，一道残阳色调剑光余痕划过天际，紫青色调，" + TAIL_COLD),
    ("13_kongling", "浩瀚虚空，一座巨大轮回盘缓缓旋转，因果珠碎片化作漫天光雨洒落，法则碎片如星环环绕天穹，一座空灵桥虚影隐现，星紫色调，" + TAIL_COLD),
    ("14_kongxuan", "洞府界虚空，踏天桥虚影横贯天际，脚下万钧雷霆炸裂纵横，一颗古珠悬浮头顶微光流转，远处云海星域中修士大军残光溃散，玄蓝色调，" + TAIL_COLD),
    ("15_kongjin", "赵国古城上空，极境神识化作黑色波纹层层荡开席卷天穹，两道金色人影在波纹深处朦胧浮现，城郭灯火零星，暗金色调，" + TAIL_WARM),
    ("16_kongzun", "古城上空天穹震荡，黑色神识波纹席卷四方，一座鎏金光轮缓缓转动悬于天际，法相威仪如山岳剪影，鎏金色调，" + TAIL_WARM),
    ("17_kongyue", "金色天门在苍穹中洞开，明金光瀑倾泻而下，黑色波纹被光瀑冲散四逸，天穹尽染明金，跃动升腾之势，明金色调，" + TAIL_WARM),
    ("18_kongda", "灿金霞光漫天铺展，天穹尽染金色，虚空之巅寂静庄严，金色光雨点点洒落，神识波纹平息归寂，灿金色调，" + TAIL_WARM),
]


def gen(prompt: str, sizes) -> Image.Image:
    last = None
    for size in sizes:
        body = json.dumps({"model": MODEL, "prompt": prompt, "size": size,
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


def main():
    done = 0
    for rid, prompt in JOBS:
        out = OUT_DIR / f"bg_{rid}.jpg"
        if out.exists():
            print(f"[skip] {out.name}", flush=True)
            done += 1
            continue
        t0 = time.time()
        try:
            img = gen(prompt, ["2560x1440", "2048x2048"])
            img.save(out, "JPEG", quality=90)
            print(f"[OK] {out.name} {img.size} {time.time()-t0:.0f}s {out.stat().st_size//1024}KB", flush=True)
            done += 1
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] {out.name}: {str(e)[:120]}", flush=True)
        time.sleep(2)
    print(f"=== 完成 {done}/{len(JOBS)} ===", flush=True)


if __name__ == "__main__":
    main()
