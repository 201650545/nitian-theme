# -*- coding: utf-8 -*-
"""重试下载两个 Seed3D 结果"""
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


def extract(name, url):
    zpath = os.path.join(OUT, name + "_seed3d.zip")
    try:
        urllib.request.urlretrieve(url, zpath)
    except Exception as e:
        print(name, "retrieve err", str(e)[:80])
        return
    try:
        z = zipfile.ZipFile(zpath)
        glb = [n for n in z.namelist() if n.endswith(".glb")]
        if not glb:
            print(name, "no glb in zip")
            return
        dst = os.path.join(OUT, name + ".glb")
        with z.open(glb[0]) as f, open(dst, "wb") as o:
            o.write(f.read())
        print(name, "saved", dst, os.path.getsize(dst) // 1024 // 1024, "MB")
        try:
            os.remove(zpath)
        except Exception:
            pass
    except Exception as e:
        print(name, "extract err", str(e)[:80])


for name, tid in JOBS.items():
    dst = os.path.join(OUT, name + ".glb")
    if os.path.exists(dst):
        print(name, "already exists", os.path.getsize(dst) // 1024 // 1024, "MB")
        continue
    r = poll(tid)
    if r.get("status") == "succeeded":
        extract(name, r["content"]["file_url"])
    else:
        print(name, "status", r.get("status"))
    time.sleep(3)
print("DONE")
