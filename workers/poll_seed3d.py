# -*- coding: utf-8 -*-
"""轮询两个 Seed3D 任务并下载 GLB"""
import json
import os
import sys
import time
import urllib.request
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(r"D:\项目\data\search_gateway\channels.json", encoding="utf-8-sig"))
key = d["keys"]["ark"]
JOBS = {
    "nianfan2": open(r"D:\逆天主题\workers\seed3d_nianfan2.txt").read().strip(),
    "movie1": open(r"D:\逆天主题\workers\seed3d_movie1.txt").read().strip(),
}
OUT = r"D:\逆天主题\assets\ui\models"


def poll(tid):
    req = urllib.request.Request("https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/" + tid, headers={"Authorization": "Bearer " + key})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def download(name, url, target):
    zpath = os.path.join(OUT, name + "_seed3d.zip")
    urllib.request.urlretrieve(url, zpath)
    z = zipfile.ZipFile(zpath)
    glb = [n for n in z.namelist() if n.endswith(".glb")]
    if glb:
        z.extract(glb[0], os.path.join(OUT, name))
        src = os.path.join(OUT, name, glb[0])
        dst = os.path.join(OUT, name + ".glb")
        os.replace(src, dst)
        os.remove(zpath)
        return dst
    return None


done = 0
while done < len(JOBS):
    for name, tid in JOBS.items():
        target = os.path.join(OUT, name + ".glb")
        if os.path.exists(target) or (name + "_done") in globals().get("_f", {}):
            continue
        r = poll(tid)
        st = r.get("status")
        print(name, st, flush=True)
        if st == "succeeded":
            url = r["content"]["file_url"]
            dst = download(name, url, target)
            print("  saved", dst, os.path.getsize(dst) // 1024 // 1024, "MB", flush=True)
            done += 1
        elif st in ("failed", "cancelled"):
            print("  FAILED", name, flush=True)
            done += 1
    time.sleep(15)
print("ALL DONE")
