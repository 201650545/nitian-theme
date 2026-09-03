# -*- coding: utf-8 -*-
"""探测 ARK Seedance i2v：官方王林脸做首帧"""
import base64
import json
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(r"D:\项目\data\search_gateway\channels.json", encoding="utf-8-sig"))
key = d["keys"]["ark"]
img = base64.b64encode(open(r"D:\游戏\逆天主题\workers\officials\posters_season_general\poster_season_movie2_01.jpg", "rb").read()).decode()
dataurl = "data:image/jpeg;base64," + img

for model in ["doubao-seedance-2-0-260128", "doubao-seedance-1-0-pro-fast-251015"]:
    body = {
        "model": model,
        "content": [
            {"type": "image_url", "image_url": {"url": dataurl}, "role": "reference_image"},
            {"type": "text", "text": "仙逆官方银甲少年王林，金色灵气在周身爆发汇聚，破境变身的瞬间，光芒冲天，史诗感"},
        ],
        "ratio": "16:9",
        "duration": 5,
        "watermark": False,
    }
    try:
        req = urllib.request.Request("https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks",
                                     data=json.dumps(body).encode(), headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")
        r = json.loads(urllib.request.urlopen(req, timeout=60).read())
        print(model, "-> OK", r.get("id"))
        open(r"D:\游戏\逆天主题\workers\seedance_task.txt", "w").write(r.get("id", ""))
        break
    except urllib.error.HTTPError as e:
        print(model, "-> HTTP", e.code, e.read().decode("utf-8", "ignore")[:200])
    except Exception as e:
        print(model, "-> ERR", str(e)[:140])
