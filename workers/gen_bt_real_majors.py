# -*- coding: utf-8 -*-
"""3 条大境界真人风破境视频（AGNES 免费通道，2026-09-02）
- 问鼎 bt_b_real / 碎涅 bt_t_real / 踏天一桥 bt_p_real
- 提示词 = 破境视频批量铺开任务书 v1 大境界模板 × bt_real_demo 真人风句式
网络韧性：显式走本机代理 7890（直连被掐），网络类错误指数退避重试，429 等 30s。
断点续跑：已有文件跳过。
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(r"D:\项目\data\search_gateway\channels.json", encoding="utf-8-sig"))
key = d["keys"]["agnes"]
BASE = "https://apihub.agnes-ai.com/v1"
OUT = r"D:\游戏\逆天主题\assets\animations"
PROXY = "http://127.0.0.1:7890"
urllib.request.install_opener(
    urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})))

PREFIX = "真人影视剧风格，写实修仙大片质感。一位气质清冷的年轻古装男子，黑发古装配饰，身着银色战甲，"
SUFFIX = "镜头从全景缓慢推近至面部特写，眼神由隐忍转为凌厉霸气，白发煞星睁眼定格。" \
         "电影级打光，真人皮肤与布料细节，慢动作爆发，无缝过渡，无文字无水印"

JOBS = {
    # 问鼎 bt_b：雨之仙界踏天桥 / 鎏金 / 鎏金道纹 / 破碎虚空裂隙+天地轰鸣雷云
    "bt_b_real": (
        PREFIX + "在雨之仙界踏天桥上突破问鼎期：独战群雄，一步踏破虚空——"
        "周身鎏金灵气漩涡汇聚成光柱冲天，发丝狂舞由黑转白，眉心浮现鎏金道纹印记，"
        "身后破碎虚空裂隙拔地而起直入苍穹，天地轰鸣雷云撕裂雨幕，"
        + SUFFIX
    ),
    # 碎涅 bt_t：天运海轮回树前 / 赤金 / 轮回印记 / 轮回树虚影+轮回之光
    "bt_t_real": (
        PREFIX + "在天运海轮回树前突破碎涅境：肉身硬抗天地之力，轮回之光映照众生——"
        "周身赤金灵气漩涡汇聚成光柱冲天，发丝狂舞由黑转白，眉心浮现轮回印记，"
        "身后巨大轮回树虚影拔地而起直入苍穹，赤金轮回之光撕裂夜空，"
        + SUFFIX
    ),
    # 踏天一桥 bt_p：踏天桥深渊上空 / 天金 / 定界罗盘印记 / 星辰道念碰撞+漫天因果线
    "bt_p_real": (
        PREFIX + "在踏天桥深渊上空与天运子对峙突破踏天一桥：星辰道念碰撞，桥身碎裂坠向深渊，"
        "罗盘虚影定住时空，漫天因果线交织——周身天金灵气漩涡汇聚成光柱冲天，"
        "发丝狂舞由黑转白，眉心浮现罗盘状印记，身后星辰虚影与万千金色因果光线上织成网直入苍穹，"
        "时空涟漪撕裂夜空，"
        + SUFFIX
    ),
}


def retry(fn, tries, label):
    last = ""
    for i in range(tries):
        try:
            return fn()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(label, "429 rate-limited, sleep 30s", flush=True)
                time.sleep(30)
                last = "429"
                continue
            raise RuntimeError(f"{label} HTTP {e.code} (non-retryable)")
        except Exception as e:
            last = str(e)[:100]
            wait = 10 * (i + 1)
            print(label, "net err", last, f"-> retry {i + 1}/{tries} in {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"{label} retries exhausted: {last}")


def submit(prompt):
    body = json.dumps({"model": "agnes-video-2.5-flash", "mode": "text", "prompt": prompt}).encode()
    req = urllib.request.Request(BASE + "/videos", data=body,
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
                                 method="POST")
    return retry(lambda: json.loads(urllib.request.urlopen(req, timeout=60).read()), 4, "submit")["id"]


def get(tid):
    req = urllib.request.Request(BASE + "/videos/" + tid, headers={"Authorization": "Bearer " + key})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def download(url, dst, label):
    retry(lambda: urllib.request.urlretrieve(url, dst), 4, label + " download")


def main():
    tids = {}
    failed = []
    for name, prompt in JOBS.items():
        dst = os.path.join(OUT, name + ".mp4")
        if os.path.exists(dst) and os.path.getsize(dst) > 500 * 1024:
            print("[skip]", name, flush=True)
            continue
        try:
            tids[name] = submit(prompt)
            print(name, "submitted", tids[name], flush=True)
        except Exception as e:
            print(name, "submit err", str(e)[:120], flush=True)
            failed.append((name, str(e)[:120]))
        time.sleep(2)

    done = 0
    total = len(tids)
    deadline = time.time() + 2400
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
                try:
                    download(r["metadata"]["url"], dst, name)
                    print(name, "saved", os.path.getsize(dst) // 1024, "KB", flush=True)
                except Exception as e:
                    print(name, "download err (id 保留:", tid, ")", str(e)[:100], flush=True)
                    failed.append((name, "download: " + str(e)[:100]))
                done += 1
            elif st in ("failed", "cancelled"):
                print(name, "FAILED", str(r.get("error", ""))[:160], flush=True)
                failed.append((name, str(r.get("error", ""))[:160]))
                done += 1
        if done < total:
            time.sleep(12)
    print("ALL DONE", done, "/", total)
    if failed:
        print("FAILED LIST:")
        for n, err in failed:
            print(" -", n, "|", err)


if __name__ == "__main__":
    main()
