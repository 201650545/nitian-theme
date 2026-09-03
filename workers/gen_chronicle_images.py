# -*- coding: utf-8 -*-
"""编年史配图映射清单生成（2026-08-27）
原则：官方优先，绝不硬凑假图；无官方人物的境界用「官方主视觉/AI立绘/徽印」补位，
     踏天九桥用桥字大印，不做虚构画面。
输出 assets/ui/chronicle-img/index.json：
  {"<rid>": {"kind":"poster|char|bg|seal|glyph","src":"/officials/..|/ui/..","credit":"...","digest":"..."}}
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"D:\逆天主题")
UI = ROOT / "assets" / "ui"
OFFICIALS = ROOT / "workers" / "officials"
OUT_DIR = UI / "chronicle-img"

A_NI = "/nitian-assets"

GENERAL = "posters_season_general"
ENTRIES = {
    # rid: (kind, 磁盘校验相对路径或None, 服务端src或None, credit)
    # 以下 6 张为剧情真实对得上的官方单人海报，保留
    "01_ningshi": ("poster", OFFICIALS / "ningqi/wanglin_shaonian_ningqi.jpg", "/officials/ningqi/wanglin_shaonian_ningqi.jpg", "官方海报"),
    "03_jiedan": ("poster", OFFICIALS / "jiedan/wanglin_xiumohai_jiedan.jpg", "/officials/jiedan/wanglin_xiumohai_jiedan.jpg", "官方海报 · 修魔海"),
    "05_huashen": ("poster", OFFICIALS / "huashen/wanglin_baifa_huashen.jpg", "/officials/huashen/wanglin_baifa_huashen.jpg", "官方海报"),
    "06_yingbian": ("poster", OFFICIALS / "yingbian/wanglin_ziyi_yingbian.jpg", "/officials/yingbian/wanglin_ziyi_yingbian.jpg", "官方海报"),
    "07_wending": ("poster", OFFICIALS / "wending/wanglin_heihong_wending.jpg", "/officials/wending/wanglin_heihong_wending.jpg", "官方海报"),
    "08_yinyang": ("poster", OFFICIALS / "yangshi/wanglin_lanbai_yangshi.jpg", "/officials/yangshi/wanglin_lanbai_yangshi.jpg", "官方海报"),
}

# Seedream 5.0 生成图（官方形象锚定提示词，2026-08-27 用户拍板：官方没有就用已有形象生成）
GEN_CREDIT = "即梦5.0 · 官方形象锚定"
GEN_REALMS = [
    "02_zhuji", "04_yuanying", "09_kunie", "10_jingnie", "11_suinie",
    "12_kongnie", "13_kongling", "14_kongxuan", "15_kongjin", "16_kongzun",
    "17_kongyue", "18_kongda", "19_qiao1", "20_qiao2", "21_qiao3", "22_qiao4",
    "23_qiao5", "24_qiao6", "25_qiao7", "26_qiao8", "27_qiao9",
]

BRIDGE_CREDIT = "踏天桥印"


def main() -> None:
    digests_path = OUT_DIR / "digests.json"
    digests = json.loads(digests_path.read_text(encoding="utf-8")) if digests_path.exists() else {}

    idx = {}
    missing_disk = []
    for i in range(1, 28):
        rid = f"{i:02d}_{"ningshi zhuji jiedan yuanying huashen yingbian wending yinyang kunie jingnie suinie kongnie kongling kongxuan kongjin kongzun kongyue kongda qiao1 qiao2 qiao3 qiao4 qiao5 qiao6 qiao7 qiao8 qiao9".split()[i - 1]}"
        if rid in ENTRIES:
            kind, disk, src, credit = ENTRIES[rid]
            if disk and not disk.exists():
                missing_disk.append(str(disk))
            idx[rid] = {"kind": kind, "src": src, "credit": credit,
                        "digest": digests.get(rid, "")}
        elif rid in GEN_REALMS:
            gen_file = OUT_DIR / "gen" / (rid + ".png")
            if not gen_file.exists():
                missing_disk.append(str(gen_file))
            idx[rid] = {"kind": "gen", "src": f"/ui/chronicle-img/gen/{rid}.png",
                        "credit": GEN_CREDIT, "digest": digests.get(rid, "")}

    if missing_disk:
        raise RuntimeError("映射指向了不存在的文件:\n" + "\n".join(missing_disk))

    out = OUT_DIR / "index.json"
    out.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OK index:", len(idx), "->", out)
    kinds = {}
    for v in idx.values():
        kinds[v["kind"]] = kinds.get(v["kind"], 0) + 1
    print("kinds:", kinds)
    no_digest = [k for k, v in idx.items() if not v.get("digest")]
    print("no_digest:", no_digest)


if __name__ == "__main__":
    main()
