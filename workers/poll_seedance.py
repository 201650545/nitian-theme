# -*- coding: utf-8 -*-
"""轮询 Seedance 破境视频并下载"""
import json
import os
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(r"D:\项目\data\search_gateway\channels.json", encoding="utf-8-sig"))
key = d["keys"]["ark"]
tid = open(r"D:\逆天主题\workers\seedance_task.txt").read().strip()
OUT = r"D:\逆天主题\assets\animations"

for i in range(60):
    req = urllib.request.Request("https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/" + tid, headers={"Authorization": "Bearer " + key})
    r = json.loads(urllib.request.urlopen(req, timeout=30).read())
    st = r.get("status")
    if i % 5 == 0 or st in ("succeeded", "failed", "cancelled"):
        print(i, st, flush=True)
    if st == "succeeded":
        url = r["content"]["file_url"]
        dst = os.path.join(OUT, "bt_wanglin_face.mp4")
        urllib.request.urlretrieve(url, dst)
        print("saved", dst, os.path.getsize(dst) // 1024, "KB", flush=True)
        break
    if st in ("failed", "cancelled"):
        print("FAILED", json.dumps(r, ensure_ascii=False)[:400], flush=True)
        break
    time.sleep(10)
