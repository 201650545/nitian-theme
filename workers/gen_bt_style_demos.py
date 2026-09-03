# -*- coding: utf-8 -*-
"""两风格破境视频示例 + 小境界示例（AGNES 免费通道，2026-08-27）
- 2D动漫风大境界示例：元婴破境 bt_2d_anime_demo
- 真人修仙风大境界示例：同剧情真人风 bt_real_demo
- 小境界示例（2D动漫风）：凝气→筑基 bt_minor_demo
断点续跑：已有文件跳过。
"""
import json
import os
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(r"D:\项目\data\search_gateway\channels.json", encoding="utf-8-sig"))
key = d["keys"]["agnes"]
BASE = "https://apihub.agnes-ai.com/v1"
OUT = r"D:\游戏\逆天主题\assets\animations"

JOBS = {
    # 风格A：2D动漫风（对标腾讯《仙逆》动画）· 大境界破境示例
    "bt_2d_anime_demo": (
        "腾讯仙逆动画官方画风，2D动漫风格。黑发少年修士王林在星空古神遗迹中突破元婴期："
        "周身星蓝灵气漩涡汇聚成光柱冲天，发丝狂舞由黑转白，眉心浮现古神星点印记，"
        "身后巨大百万人头塔虚影拔地而起直入苍穹，金色闪电撕裂夜空，"
        "镜头从全景缓慢推近至面部特写，眼神由隐忍转为凌厉霸气，白发煞星睁眼定格。"
        "史诗感，光影华丽，作画流畅，无缝过渡，无文字无水印"
    ),
    # 风格B：真人修仙风 · 大境界破境示例
    "bt_real_demo": (
        "真人影视剧风格，写实修仙大片质感。一位气质清冷的年轻古装男子在星空下山巅打坐，"
        "身着银色战甲黑发古装配饰，突破瞬间白发从发根蔓延生长狂舞，眉心亮起星形印记，"
        "身后云层中百万人头塔剪影缓缓显现，蓝色灵气光柱冲天而起，金色雷电交织环绕，"
        "镜头环绕上升，最后定格面部特写白发红眸，眼神凌厉。"
        "电影级打光，真人皮肤与布料细节，慢动作爆发，无缝过渡，无文字无水印"
    ),
    # 风格A · 小境界破境示例（凝气→筑基）
    "bt_minor_demo": (
        "腾讯仙逆动画官方画风，2D动漫风格。麻衣黑发少年修士王林在瀑布山崖前小境界突破："
        "周身淡金色灵气如细流汇聚，衣袍发丝轻扬，一圈柔和光环从头顶扩散至全身，"
        "崖边青竹随风弯腰，水雾中彩虹微光，突破完成睁眼露出坚定眼神，嘴角微扬。"
        "短小精炼，宁静修行氛围，光影柔和，无缝过渡，无文字无水印"
    ),
}


def submit(prompt):
    body = json.dumps({"model": "agnes-video-2.5-flash", "mode": "text", "prompt": prompt}).encode()
    req = urllib.request.Request(BASE + "/videos", data=body,
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
                                 method="POST")
    r = json.loads(urllib.request.urlopen(req, timeout=60).read())
    return r["id"]


def get(tid):
    req = urllib.request.Request(BASE + "/videos/" + tid, headers={"Authorization": "Bearer " + key})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def main():
    tids = {}
    for name, prompt in JOBS.items():
        dst = os.path.join(OUT, name + ".mp4")
        if os.path.exists(dst):
            print("[skip]", name, flush=True)
            continue
        try:
            tids[name] = submit(prompt)
            print(name, "submitted", tids[name], flush=True)
        except Exception as e:
            print(name, "submit err", str(e)[:120], flush=True)
        time.sleep(2)

    done = 0
    total = len(tids)
    deadline = time.time() + 1500
    while done < total and time.time() < deadline:
        for name, tid in list(tids.items()):
            dst = os.path.join(OUT, name + ".mp4")
            if os.path.exists(dst):
                continue
            try:
                r = get(tid)
            except Exception as e:
                print(name, "poll err", str(e)[:60], flush=True)
                continue
            st = r.get("status")
            if st == "completed":
                urllib.request.urlretrieve(r["metadata"]["url"], dst)
                print(name, "saved", os.path.getsize(dst) // 1024, "KB", flush=True)
                done += 1
            elif st in ("failed", "cancelled"):
                print(name, "FAILED", r.get("error", ""), flush=True)
                done += 1
        if done < total:
            time.sleep(12)
    print("ALL DONE", done, "/", total)


if __name__ == "__main__":
    main()
