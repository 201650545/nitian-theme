# -*- coding: utf-8 -*-
"""探测 AGNES 图生视频（i2v）：官方王林脸做首帧"""
import base64
import json
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(r"D:\项目\data\search_gateway\channels.json", encoding="utf-8-sig"))
key = d["keys"]["agnes"]
BASE = "https://apihub.agnes-ai.com/v1"

# 官方弑战王林海报（近脸大头）做首帧
img = base64.b64encode(open(r"D:\逆天主题\workers\officials\posters_season_general\poster_season_movie2_01.jpg", "rb").read()).decode()
dataurl = "data:image/jpeg;base64," + img

probes = [
    ("mode=image+image", {"model": "agnes-video-2.5-flash", "mode": "image", "image": dataurl, "prompt": "仙逆官方王林银甲少年，周身金色灵气爆发破境变身"}),
    ("mode=i2v+image", {"model": "agnes-video-2.5-flash", "mode": "i2v", "image": dataurl, "prompt": "王林破境，金色灵气爆发"}),
    ("mode=text+image_url", {"model": "agnes-video-2.5-flash", "mode": "text", "image_url": dataurl, "prompt": "以此首帧人物为原型，王林破境变身，金色灵气爆发"}),
]

for name, body in probes:
    try:
        req = urllib.request.Request(BASE + "/videos", data=json.dumps(body).encode(),
                                     headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")
        r = json.loads(urllib.request.urlopen(req, timeout=60).read())
        print(name, "-> OK", r.get("id"), r.get("status"))
        break
    except urllib.error.HTTPError as e:
        print(name, "-> HTTP", e.code, e.read().decode("utf-8", "ignore")[:180])
    except Exception as e:
        print(name, "-> ERR", str(e)[:120])
