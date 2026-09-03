# -*- coding: utf-8 -*-
"""逆天主题 · 运行时资产生成（MVP 三境：凝气/元婴/化神）
按 workers/运行时资产制作任务书.md 规范执行：
- bg.webp 16:9 | wanglin.png 3:4 透明底 | hero.webp 3:4 竖版
- 三件套：raw/ MASTER PNG + RUNTIME WEBP/PNG + THUMB JPG
- 源文件只读；质量 85~90
"""
import sys
from pathlib import Path

from PIL import Image
from rembg import remove, new_session

ROOT = Path(r"D:\游戏\逆天主题")
ASSETS = ROOT / "assets"
W, H = Image.open(ROOT / "workers/officials/posters_season_general/poster_season_all_01.jpg").size[:2] if False else (0, 0)

JOBS = {
    "01_ningshi": {
        "bg": ROOT / "workers/officials/posters_season_general/poster_season_all_01.jpg",
        "char": ROOT / "workers/officials/ningqi/wanglin_shaonian_ningqi.jpg",
        "hero": ROOT / "workers/officials/ningqi/wanglin_shaonian_ningqi.jpg",
    },
    "04_yuanying": {
        "bg": ROOT / "workers/collected/yuanying/bg-01.jpg",
        "char": ROOT / "workers/collected/yuanying/figure-01.jpg",
        "hero": ROOT / "workers/officials/posters_season_general/poster_season_movie1_01.jpg",
    },
    "05_huashen": {
        "bg": ROOT / "workers/officials/huashen/huashen_02.jpg",
        "char": ROOT / "workers/officials/huashen/wanglin_baifa_huashen.jpg",
        "hero": ROOT / "workers/officials/huashen/huashen_01.jpg",
    },
}


def center_crop(img: Image.Image, ratio: float) -> Image.Image:
    """居中裁切到目标宽高比（不拉伸）。ratio = 宽/高"""
    w, h = img.size
    cur = w / h
    if abs(cur - ratio) < 0.005:
        return img
    if cur > ratio:
        nw = int(h * ratio)
        x = (w - nw) // 2
        return img.crop((x, 0, x + nw, h))
    nh = int(w / ratio)
    y = (h - nh) // 2
    return img.crop((0, y, w, y + nh))


def emit(img: Image.Image, out_dir: Path, stem: str, ext: str, quality: int = 88):
    """三件套：raw MASTER PNG + RUNTIME 文件 + THUMB JPG。返回 (runtime, master, thumb) 尺寸信息"""
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = out_dir / "raw"
    raw_dir.mkdir(exist_ok=True)
    master = raw_dir / f"{stem}.png"
    img.save(master, "PNG")
    runtime = out_dir / f"{stem}.{ext}"
    if ext == "webp":
        img.save(runtime, "WEBP", quality=quality, method=6)
    else:
        img.save(runtime, "PNG")
    thumb = out_dir / f"{stem}_thumb.jpg"
    base = img.convert("RGB") if img.mode in ("RGBA", "P", "LA") else img
    t = base.copy()
    t.thumbnail((480, 480))
    t.save(thumb, "JPEG", quality=80)
    return img.size


def make_bg(src: Path, realm_dir: Path):
    img = Image.open(src).convert("RGB")
    src_size = img.size
    img = center_crop(img, 16 / 9)
    size = emit(img, realm_dir, "bg", "webp")
    return src_size, size


def make_hero(src: Path, realm_dir: Path):
    img = Image.open(src).convert("RGB")
    src_size = img.size
    img = center_crop(img, 3 / 4)
    size = emit(img, realm_dir, "hero", "webp")
    return src_size, size


def make_character(src: Path, realm_dir: Path, session):
    img = Image.open(src).convert("RGBA")
    src_size = img.size
    cut = remove(img, session=session, post_process_mask=True)
    bbox = cut.getbbox()
    if not bbox:
        raise RuntimeError(f"抠图失败（全空 alpha）：{src}")
    cut = cut.crop(bbox)
    w, h = cut.size
    tw = max(w, round(h * 3 / 4))
    th = max(h, round(tw * 4 / 3))
    canvas = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    canvas.paste(cut, ((tw - w) // 2, (th - h) // 2), cut)
    out = realm_dir / "wanglin.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, "PNG")
    # 抠像 MASTER 单独存 raw
    raw_dir = realm_dir / "raw"
    raw_dir.mkdir(exist_ok=True)
    canvas.save(raw_dir / "wanglin_cutout.png", "PNG")
    # 缩略图用白底合成便于人眼检查
    chk = Image.new("RGB", canvas.size, (255, 0, 255))  # 品红底暴露毛边
    chk.paste(canvas, (0, 0), canvas)
    t = chk.copy()
    t.thumbnail((480, 480))
    t.save(realm_dir / "wanglin_cutout_check_thumb.jpg", "JPEG", quality=85)
    return src_size, canvas.size


def main():
    session = new_session("u2net")
    report = []
    for rid, job in JOBS.items():
        rd = ASSETS / "realms" / rid
        r = {"realm": rid}
        r["bg"] = make_bg(job["bg"], rd)
        r["char"] = make_character(job["char"], rd, session)
        r["hero"] = make_hero(job["hero"], rd)
        report.append(r)
        print(f"[OK] {rid}: bg {r['bg'][0]}->{r['bg'][1]} | char {r['char'][0]}->{r['char'][1]} | hero {r['hero'][0]}->{r['hero'][1]}", flush=True)
    print(json_dumps(report))


def json_dumps(report):
    import json
    return json.dumps(report, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
