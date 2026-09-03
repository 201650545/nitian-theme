# -*- coding: utf-8 -*-
"""AGNES 各境界专属破境视频（M/B/T/P 四档）"""
import json
import os
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(r"D:\项目\data\search_gateway\channels.json", encoding="utf-8-sig"))
key = d["keys"]["agnes"]
BASE = "https://apihub.agnes-ai.com/v1"
OUT = r"D:\逆天主题\assets\animations"

JOBS = {
    "bt_m": "元婴·罗天星域破境：青衫修士盘坐星海虚空，星蓝灵气漩涡汇聚，金色爆裂冲天，古神星纹法印浮现，星蓝鎏金调，史诗",
    "bt_b": "问鼎·问鼎巅峰破境：修士立于群山之巅云海，鎏金灵气喷薄，巨大青铜鼎法印浮现，金光四射，鎏金玄墨调，史诗",
    "bt_t": "碎涅·碎涅证道破境：修士悬浮暗红雷云，玄黑灵气崩碎重组，暗红与赤金能量爆发，碎星法印显现，暗红鎏金调，史诗",
    "bt_p": "踏天·金色天桥破境：鎏金修士立于横贯云海的金色天桥，金光大道冲天，九桥法印层叠浮现，璀璨金辉，圣洁史诗",
}


def submit(prompt):
    body = json.dumps({"model": "agnes-video-2.5-flash", "mode": "text", "prompt": prompt + "，仙逆动画官方画风，无缝过渡，无文字无水印"}).encode()
    req = urllib.request.Request(BASE + "/videos", data=body, headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")
    r = json.loads(urllib.request.urlopen(req, timeout=60).read())
    return r["id"]


def get(tid):
    req = urllib.request.Request(BASE + "/videos/" + tid, headers={"Authorization": "Bearer " + key})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


tids = {}
for name, prompt in JOBS.items():
    try:
        tids[name] = submit(prompt)
        print(name, "submitted", tids[name], flush=True)
    except Exception as e:
        print(name, "submit err", str(e)[:80], flush=True)
    time.sleep(2)

done = 0
while done < len(tids):
    for name, tid in list(tids.items()):
        dst = os.path.join(OUT, name + ".mp4")
        if os.path.exists(dst) or name not in tids:
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
            print(name, "FAILED", flush=True)
            done += 1
    time.sleep(10)
print("ALL DONE")
