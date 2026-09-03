# -*- coding: utf-8 -*-
"""破境视频批量铺开（27 境 · 2D 动漫风 · AGNES 免费通道）

任务书：workers/破境视频批量铺开任务书-2D动漫风-v1.md
风格标杆：bt_2d_anime_demo.mp4（大境界）/ bt_minor_demo.mp4（小境界），用户已确认合格。

要点：
- 提示词 = 公共前缀 A + 档位模板（B 大境界 / C 小境界）+ 该境焦点意象与主色，
  场景与环境细节从 chronicle.json 对应 scene 提炼，全部要求「无文字无水印」。
- 断点续跑：输出已存在且 >500KB 即跳过；但 bt_m/bt_b/bt_t/bt_p 是本次风格替换对象，
  默认**强制重生成**（旧版不覆盖不算完成），下载成功后才 os.replace 换掉旧文件。
- 限流（实测）：AGNES 视频接口按 **5 requests / 1 minute** 限流，不是日配额。默认每批
  5 个、批间 sleep 60s；提交遇 402/429 立即停止轰炸，已完成部分落盘，换时段重跑续上。
- 密钥运行时从 D:\\项目\\data\\search_gateway\\channels.json 读取，脚本与汇报均不含明文。
- 每轮把逐境状态写 workers/bt_batch_status.json，供汇报文件直接取用。

用法：
  python gen_bt_batch.py --dry-run              # 只打印 27 条提示词，不花配额
  python gen_bt_batch.py                        # 全量跑（4 大境界 + 23 小境界）
  python gen_bt_batch.py --only 01_ningshi      # 指定境界（逗号分隔多个）
  python gen_bt_batch.py --limit 5 --keep-major # 只跑前 5 个未完成项，且不动已有大境界
"""
import argparse
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://apihub.agnes-ai.com/v1"
MODEL = "agnes-video-2.5-flash"
OUT_DIR = r"D:\逆天主题\assets\animations"
CHRONICLE = r"D:\逆天主题\assets\ui\chronicle.json"
KEYS_FILE = r"D:\项目\data\search_gateway\channels.json"
STATUS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bt_batch_status.json")

MIN_BYTES = 500 * 1024
PREFIX = ("腾讯仙逆动画官方画风，2D动漫风格。主角王林：黑发少年修士，麻衣或战袍古装，"
          "面容坚毅清冷。")
# 实测结论（2026-08-29 对照实验，见汇报）：只写「无文字」压不住模型；
# 而负面句里点名「石碑/墓碑/竹简/壁画」这类可刻字物体，等于提示它去画——不仅画出来，
# 还必然写满汉字；正向描述「碑面光滑无字」同样无效。唯一有效写法是**不点名任何可刻字物体**，
# 改用抽象光纹/记忆光影表达同一剧情意象。故本约束句只描述画面纯净，绝不提物体名。
ANTI_TEXT = "画面纯净，只有光影、雾气与抽象纹饰"
MAJOR_OUTS = {"bt_m.mp4", "bt_b.mp4", "bt_t.mp4", "bt_p.mp4"}

# 27 境配置。tier=MAJOR 用模板 B（seal/vision/sky），tier=MINOR 用模板 C（env）。
# ck = chronicle.json 的 key（空劫 4 子境共用 15_kongjie；踏天桥 chronicle 编号比引擎小 3）。
REALMS = [
    {"rid": "01_ningshi", "name": "凝气期", "tier": "MINOR", "out": "bt_01_ningshi.mp4",
     "color": "淡金", "ck": "01_ningshi", "place": "恒岳派后山夜色中",
     "focus": "恒岳后山夜，血色月光，荒草乱石间咬破指尖滴血起誓，天逆珠微光，杀意初生",
     "env": "血色月光洒在荒草乱石上，指尖血珠滴落泥土，远处村落火光未熄，掌心天逆珠微光一闪"},
    {"rid": "02_zhuji", "name": "筑基期", "tier": "MINOR", "out": "bt_02_zhuji.mp4",
     "color": "青绿", "ck": "02_zhuji", "place": "迷雾森林深处",
     "focus": "迷雾森林，藤蔓尸傀，吞噬修为，血雾弥漫",
     "env": "蓝线藤影在雾气中游走，尸傀静立一旁，藤条间血雾缓缓散去"},
    {"rid": "03_jiedan", "name": "结丹期", "tier": "MINOR", "out": "bt_03_jiedan.mp4",
     "color": "血红", "ck": "03_jiedan", "place": "修魔海血雾之上",
     "focus": "修魔海血雾，极境之光，一剑斩敌，杀伐果断",
     "env": "极境之光自指尖收束，一道剑光余痕划过血雾，海面血雾渐薄"},
    {"rid": "04_yuanying", "name": "元婴期", "tier": "MAJOR", "out": "bt_m.mp4",
     "color": "星蓝", "ck": "04_yuanying", "place": "星空古神遗迹",
     "focus": "丹炉炸裂引天地异象，星蓝灵气光柱冲天，古神星点印记，百万人头塔虚影，金雷裂空",
     "seal": "古神星点印记", "vision": "百万人头塔虚影", "sky": "金色闪电"},
    {"rid": "05_huashen", "name": "化神期", "tier": "MINOR", "out": "bt_05_huashen.mp4",
     "color": "灰蓝", "ck": "05_huashen", "place": "赵国藤家祖宅前",
     "focus": "雷劫淬体，人头塔冲天，血雾千里，古神指威压",
     "env": "雷劫余辉洒落，远处人头塔剪影冲天，血雾千里渐收"},
    {"rid": "06_yingbian", "name": "婴变期", "tier": "MINOR", "out": "bt_06_yingbian.mp4",
     "color": "紫", "ck": "06_yingbian", "place": "朱雀星祭坛前",
     "focus": "朱雀星祭坛，杀戮珠吞万魂，血雨纷飞，天地变色",
     "env": "血雨渐歇，杀戮珠吞下最后一缕魂光，祭坛紫纹明灭"},
    {"rid": "07_wending", "name": "问鼎期", "tier": "MAJOR", "out": "bt_b.mp4",
     "color": "鎏金", "ck": "07_wending", "place": "雨之仙界踏天桥",
     "focus": "雨之仙界踏天桥，独战群雄，一步踏破虚空，天地轰鸣",
     "seal": "鎏金道纹", "vision": "破碎虚空裂隙", "sky": "天地轰鸣雷云"},
    {"rid": "08_yinyang", "name": "阴虚阳实", "tier": "MINOR", "out": "bt_08_yinyang.mp4",
     "color": "黑白", "ck": "08_yinyang", "place": "阴阳桥桥心",
     "focus": "阴阳桥太极图，阴阳二气凝巨掌，黑白交融珠升",
     "env": "黑白云雾翻滚成太极图，一枚黑白交融的珠子自桥面裂缝缓缓升起"},
    {"rid": "09_kunie", "name": "窥涅境", "tier": "MINOR", "out": "bt_09_kunie.mp4",
     "color": "青蓝", "ck": "09_kunie", "place": "九劫洞府之内",
     "focus": "九劫洞府，万魂撕裂，金骨重塑，空气中浮动青蓝发光纹路",
     "env": "洞府禁制血雾散去，青蓝色发光纹路与流火在空气中明灭流动，金骨初成"},
    {"rid": "10_jingnie", "name": "净涅境", "tier": "MINOR", "out": "bt_10_jingnie.mp4",
     "color": "碧青", "ck": "10_jingnie", "place": "轮回之巅",
     "focus": "轮回之巅，破灭法目金光，虚空尽碎",
     "env": "无数虚影周身闪灭，破灭法目金光初收，碎裂虚空碧青如洗"},
    {"rid": "11_suinie", "name": "碎涅境", "tier": "MAJOR", "out": "bt_t.mp4",
     "color": "赤金", "ck": "11_suinie", "place": "天运海轮回树前",
     "focus": "天运海轮回树，肉身硬抗天地之力，轮回之光映照众生",
     "seal": "轮回印记", "vision": "轮回树虚影", "sky": "轮回之光"},
    {"rid": "12_kongnie", "name": "空涅境", "tier": "MINOR", "out": "bt_12_kongnie.mp4",
     "color": "紫青", "ck": "12_kongnie", "place": "轮回树前",
     "focus": "轮回树前，万道因果丝线缠绕，残夜之剑剑光如残阳",
     "env": "万道因果丝线缠绕树根，残夜之剑剑光如残阳落尽"},
    {"rid": "13_kongling", "name": "空灵境", "tier": "MINOR", "out": "bt_13_kongling.mp4",
     "color": "星紫", "ck": "13_kongling", "place": "虚空轮回盘之上",
     "focus": "虚空轮回盘，因果珠碎片化光雨，法则碎片星环环绕",
     "env": "头顶因果珠碎片化作光雨，法则碎片如星环缓缓旋转"},
    {"rid": "14_kongxuan", "name": "空玄境", "tier": "MINOR", "out": "bt_14_kongxuan.mp4",
     "color": "玄蓝", "ck": "14_kongxuan", "place": "洞府界虚空踏天桥虚影之上",
     "focus": "踏天桥虚影初现，脚下雷霆万钧，目光如电",
     "env": "脚下雷霆万钧，天逆珠悬顶，远处云海星域溃散修士的大军残光"},
    {"rid": "15_kongjin", "name": "空劫·金尊", "tier": "MINOR", "out": "bt_15_kongjin.mp4",
     "color": "金", "ck": "15_kongjie", "place": "赵国藤家祖宅上空",
     "focus": "极境神识黑波纹，元神崩碎，父亲与母亲化作一男一女两道金色光影，金尊威严",
     "env": "极境神识黑色波纹层层荡开，身后浮现两道金色光影，左侧父亲儒雅男子右侧母亲温婉女子，金尊法相初凝"},
    {"rid": "16_kongzun", "name": "空劫·天尊", "tier": "MINOR", "out": "bt_16_kongzun.mp4",
     "color": "鎏金", "ck": "15_kongjie", "place": "赵国藤家祖宅上空",
     "focus": "极境神识黑波纹未散，元神崩碎之余，父母音容金色光影，天尊法相凝实，鎏金光轮",
     "env": "黑色波纹仍在天地间震荡，父母音容化作的金色光影依旧朦胧，天尊法相较先前更为凝实，鎏金光轮缓缓转动"},
    {"rid": "17_kongyue", "name": "空劫·跃天尊", "tier": "MINOR", "out": "bt_17_kongyue.mp4",
     "color": "明金", "ck": "15_kongjie", "place": "赵国藤家祖宅上空",
     "focus": "跃阶破境，明金光瀑倾泻，父母音容金色光影，神识黑波纹被冲散",
     "env": "跃阶之力自脚下腾起，明金光瀑倾泻过父母音容化作的金色光影，黑色波纹被冲得四散"},
    {"rid": "18_kongda", "name": "空劫·大天尊", "tier": "MINOR", "out": "bt_18_kongda.mp4",
     "color": "灿金", "ck": "15_kongjie", "place": "赵国藤家祖宅上空",
     "focus": "圆满破境，灿金霞光漫天，父亲与母亲化作一男一女两道金色光影，天地间唯余独立身影",
     "env": "灿金霞光漫天铺展，身后浮现两道金色光影，左侧父亲儒雅男子右侧母亲温婉女子，神识波纹尽数平息"},
    {"rid": "19_qiao1", "name": "踏天一桥", "tier": "MAJOR", "out": "bt_p.mp4",
     "color": "天金", "ck": "16_qiao1", "place": "踏天桥深渊上空",
     "focus": "踏天桥与天运子对峙，星辰道念碰撞，桥碎深渊，定界罗盘定时空，因果线交织",
     "seal": "定界罗盘印记", "vision": "崩碎桥身与星辰道念", "sky": "漫天因果线"},
    {"rid": "20_qiao2", "name": "踏天二桥", "tier": "MINOR", "out": "bt_20_qiao2.mp4",
     "color": "金", "ck": "17_qiao2", "place": "无尽虚空之中",
     "focus": "无尽虚空轮回漩涡，轮回镜照万古，抬手碎漩涡",
     "env": "前方巨大轮回漩涡被抬手震碎，身后轮回镜照耀万古，踏天桥虚影横跨苍穹"},
    {"rid": "21_qiao3", "name": "踏天三桥", "tier": "MINOR", "out": "bt_21_qiao3.mp4",
     "color": "金赤", "ck": "18_qiao3", "place": "踏天三桥之巅",
     "focus": "万道雷霆如瀑布倒挂，无形之剑斩断因果，黑白恢复色彩",
     "env": "脚下万道雷霆如瀑布倒挂，无形之剑斩落，世界由黑白渐渐恢复色彩"},
    {"rid": "22_qiao4", "name": "踏天四桥", "tier": "MINOR", "out": "bt_22_qiao4.mp4",
     "color": "金褐", "ck": "19_qiao4", "place": "始古原始山前",
     "focus": "始古原始山，五大本源真身虚影，随手击退大天尊",
     "env": "五大本源真身虚影在山间明灭，随手一击的余波扫过云海，全场寂静跪伏，人物面部立体厚涂、发丝衣纹精细，电影级光影质感"},
    {"rid": "23_qiao5", "name": "踏天五桥", "tier": "MINOR", "out": "bt_23_qiao5.mp4",
     "color": "三色", "ck": "20_qiao5", "place": "始古祖庙深处",
     "focus": "祖庙深处三色尊阳环绕，黑白金光芒交织，问心终了",
     "env": "三色尊阳环绕周身，黑白金光芒交织，幻象面孔散去后脚下虚空生桥"},
    {"rid": "24_qiao6", "name": "踏天六桥", "tier": "MINOR", "out": "bt_24_qiao6.mp4",
     "color": "金橙", "ck": "21_qiao6", "place": "混沌之上的第六桥",
     "focus": "混沌之上裂痕桥，裂痕映照执念，幻影分身尽灭",
     "env": "桥身每一道裂痕都映出前世今生的执念，幻影分身尽数化作虚无，桥体轰然震颤"},
    {"rid": "25_qiao7", "name": "踏天七桥", "tier": "MINOR", "out": "bt_25_qiao7.mp4",
     "color": "七彩", "ck": "22_qiao7", "place": "七彩界第七桥",
     "focus": "七彩界七彩光晕，天逆珠光芒，决战天道虚影",
     "env": "天空裂开七彩光晕，天逆珠光芒吞吐，对面天道虚影寸寸碎裂成光点"},
    {"rid": "26_qiao8", "name": "踏天八桥", "tier": "MINOR", "out": "bt_26_qiao8.mp4",
     "color": "深金", "ck": "23_qiao8", "place": "罗天星域战场上空",
     "focus": "罗天星域，踏天八桥光芒万丈，因果锁链缚天道，轮回剑斩出",
     "env": "无数因果锁链束缚天道化身，轮回剑光斩过，身后女子虚影泪眼含笑"},
    {"rid": "27_qiao9", "name": "踏天九桥", "tier": "MINOR", "out": "bt_27_qiao9.mp4",
     "color": "黄金", "ck": "24_qiao9", "place": "第九桥之巅",
     "focus": "第九桥之巅，万线崩碎成因果花瓣，踏碎桥身超脱天道",
     "env": "万道因果线崩碎成漫天因果花瓣，桥身在脚下寸寸碎裂，黄金之光超脱而上"},
]

KEY_CACHE = {}


def check_chronicle():
    """校验配置表里的 chronicle key 是否存在（任务书特别提示踏天桥引擎 id 与剧情 key 错位）。"""
    try:
        with open(CHRONICLE, encoding="utf-8") as f:
            keys = set((json.load(f).get("realms") or {}).keys())
    except Exception as e:  # noqa: BLE001
        print("!! chronicle.json 不可读（%s），剧情依据退化为焦点意象兜底" % str(e)[:80])
        return False
    bad = [r["rid"] for r in REALMS if r["ck"] not in keys]
    if bad:
        print("!! 以下境界的 chronicle key 未命中：%s" % ", ".join(bad))
        return False
    print("chronicle key 校验：%d/%d 命中" % (len(REALMS), len(REALMS)))
    return True


def api_key():
    """运行时读密钥（不落任何文件/日志）。"""
    if "k" not in KEY_CACHE:
        with open(KEYS_FILE, encoding="utf-8-sig") as f:
            KEY_CACHE["k"] = json.load(f)["keys"]["agnes"]
    return KEY_CACHE["k"]


def build_prompt(r):
    head = "%s在%s突破%s：%s——" % (PREFIX, r["place"], r["name"], r["focus"])
    if r["tier"] == "MAJOR":
        body = ("周身%s灵气漩涡汇聚成光柱冲天，发丝狂舞由黑转白，眉心浮现%s，"
                "身后巨大%s拔地而起直入苍穹，%s撕裂夜空，"
                "镜头从全景缓慢推近至面部特写，眼神由隐忍转为凌厉霸气，白发煞星睁眼定格。"
                "史诗感，光影华丽，作画流畅，无缝过渡，无文字无水印"
                % (r["color"], r["seal"], r["vision"], r["sky"]))
    else:
        body = ("周身%s灵气如细流汇聚，衣袍发丝轻扬，一圈柔和光环从头顶扩散至全身，%s，"
                "突破完成睁眼露出坚定眼神，嘴角微扬。"
                "短小精炼，宁静修行氛围，光影柔和，无缝过渡，无文字无水印"
                % (r["color"], r["env"]))
    return head + body + "。" + ANTI_TEXT


def _http(url, method="GET", body=None, timeout=60):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": "Bearer " + api_key(),
                                          "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8"))


def submit(prompt):
    return _http(BASE + "/videos", "POST",
                 {"model": MODEL, "mode": "text", "prompt": prompt}, timeout=90)["id"]


def poll(tid):
    return _http(BASE + "/videos/" + tid, timeout=30)


def download(url, dst):
    """先下临时文件再原子替换——覆盖旧版时不存在「删了没补上」的中间态。"""
    tmp = dst + ".part"
    urllib.request.urlretrieve(url, tmp)
    size = os.path.getsize(tmp)
    if size <= MIN_BYTES:
        os.remove(tmp)
        raise IOError("下载体积过小(%d B)，判为无效产出" % size)
    os.replace(tmp, dst)
    return size


def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_status(st):
    tmp = STATUS_FILE + ".part"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=1)
    os.replace(tmp, STATUS_FILE)


def select_jobs(args):
    jobs = []
    for r in REALMS:
        if args.only and r["rid"] not in args.only:
            continue
        dst = os.path.join(OUT_DIR, r["out"])
        major = r["out"] in MAJOR_OUTS
        if os.path.exists(dst) and os.path.getsize(dst) > MIN_BYTES:
            if (major and not args.keep_major) or args.force:
                pass  # 风格替换对象 / --force 修缺陷：必须重生成
            else:
                jobs.append((r, "skip", os.path.getsize(dst)))
                continue
        jobs.append((r, "run", os.path.getsize(dst) if os.path.exists(dst) else 0))
    return jobs


def run_batch(batch, status, args):
    """提交一批 → 轮询下载。返回 (done_map, quota_hit)。"""
    tids = {}
    quota_hit = False
    for r in batch:
        prompt = build_prompt(r)
        if args.show_prompt:
            print("  [%s] prompt: %s" % (r["rid"], prompt), flush=True)
        try:
            tid = submit(prompt)
        except urllib.error.HTTPError as e:
            msg = "HTTP %d %s" % (e.code, e.read().decode("utf-8", "ignore")[:180])
            status[r["rid"]] = {"out": r["out"], "tier": r["tier"], "state": "failed",
                                "reason": msg, "at": datetime.datetime.now().isoformat(timespec="seconds")}
            print("  [%s] 提交失败 %s" % (r["rid"], msg), flush=True)
            if e.code in (402, 429):
                quota_hit = True
                break
            continue
        except Exception as e:  # noqa: BLE001
            status[r["rid"]] = {"out": r["out"], "tier": r["tier"], "state": "failed",
                                "reason": "提交异常 " + str(e)[:180]}
            print("  [%s] 提交异常 %s" % (r["rid"], str(e)[:180]), flush=True)
            continue
        tids[r["rid"]] = tid
        status[r["rid"]] = {"out": r["out"], "tier": r["tier"], "state": "submitted", "tid": tid}
        print("  [%s] 提交 id=%s" % (r["rid"], tid), flush=True)
        time.sleep(2)

    save_status(status)
    if not tids:
        return quota_hit

    pending = dict(tids)
    deadline = time.time() + args.poll_timeout
    while pending and time.time() < deadline:
        time.sleep(args.poll_interval)
        for rid, tid in list(pending.items()):
            r = next(x for x in REALMS if x["rid"] == rid)
            try:
                res = poll(tid)
            except Exception as e:  # noqa: BLE001
                print("  [%s] 轮询异常 %s" % (rid, str(e)[:60]), flush=True)
                continue
            st = res.get("status")
            if st == "completed":
                dst = os.path.join(OUT_DIR, r["out"])
                try:
                    size = download(res["metadata"]["url"], dst)
                except Exception as e:  # noqa: BLE001
                    status[rid] = {"out": r["out"], "tier": r["tier"], "state": "failed",
                                   "reason": "下载失败 " + str(e)[:180], "tid": tid}
                    print("  [%s] 下载失败 %s" % (rid, str(e)[:120]), flush=True)
                    pending.pop(rid)
                    continue
                status[rid] = {"out": r["out"], "tier": r["tier"], "state": "done",
                               "bytes": size, "tid": tid}
                print("  [%s] completed → %s %.0f KB" % (rid, r["out"], size / 1024.0), flush=True)
                pending.pop(rid)
            elif st in ("failed", "cancelled"):
                status[rid] = {"out": r["out"], "tier": r["tier"], "state": "failed",
                               "reason": "上游 %s %s" % (st, str(res.get("error"))[:150]), "tid": tid}
                print("  [%s] 上游 %s" % (rid, st), flush=True)
                pending.pop(rid)
        save_status(status)

    for rid in pending:
        status[rid] = dict(status.get(rid, {}))
        status[rid].update({"state": "timeout", "reason": "轮询超时 %ds" % args.poll_timeout})
        print("  [%s] 轮询超时，可稍后重跑续上" % rid, flush=True)
    save_status(status)
    return quota_hit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=lambda s: [x.strip() for x in s.split(",") if x.strip()])
    ap.add_argument("--limit", type=int, default=0, help="最多生成多少个（0=不限）")
    ap.add_argument("--batch-size", type=int, default=5,
                    help="实测硬上限：AGNES 视频接口 5 requests / 1 minute")
    ap.add_argument("--batch-gap", type=int, default=60)
    ap.add_argument("--poll-interval", type=int, default=12)
    ap.add_argument("--poll-timeout", type=int, default=1500)
    ap.add_argument("--keep-major", action="store_true",
                    help="已有 bt_m/bt_b/bt_t/bt_p 不重生成（默认要重生成覆盖）")
    ap.add_argument("--force", action="store_true",
                    help="已存在且合格的输出也强制重生成（配合 --only 修个别境的画面缺陷）")
    ap.add_argument("--show-prompt", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    check_chronicle()
    jobs = select_jobs(args)
    todo = [(r, sz) for r, act, sz in jobs if act == "run"]
    skipped = [(r, sz) for r, act, sz in jobs if act == "skip"]
    print("配置 27 境：待生成 %d，跳过（已存在 >500KB）%d" % (len(todo), len(skipped)))
    for r, sz in skipped:
        print("  [skip] %s %s 已存在 %.0f KB" % (r["rid"], r["out"], sz / 1024.0))
    if args.dry_run:
        for r, _ in todo:
            print("--- %s (%s) %s\n%s" % (r["rid"], r["tier"], r["out"], build_prompt(r)))
        print("dry-run 完成，未调用 API")
        return 0
    if args.limit:
        todo = todo[:args.limit]

    os.makedirs(OUT_DIR, exist_ok=True)
    status = load_status()
    started = time.time()
    for i in range(0, len(todo), args.batch_size):
        batch = [r for r, _ in todo[i:i + args.batch_size]]
        print("\n=== 批次 %d/%d：%s ===" % (i // args.batch_size + 1,
                                            (len(todo) + args.batch_size - 1) // args.batch_size,
                                            ", ".join(r["rid"] for r in batch)), flush=True)
        quota_hit = run_batch(batch, status, args)
        save_status(status)
        if quota_hit:
            print("\n!! AGNES 配额/限流命中，停止后续批次（不重试轰炸）。"
                  "换时段重跑本脚本即可从断点续上。", flush=True)
            break
        if i + args.batch_size < len(todo):
            time.sleep(args.batch_gap)

    done = [r for r in REALMS if status.get(r["rid"], {}).get("state") == "done"
            and os.path.getsize(os.path.join(OUT_DIR, r["out"])) > MIN_BYTES
            if os.path.exists(os.path.join(OUT_DIR, r["out"]))]
    failed = {rid: v for rid, v in status.items() if v.get("state") in ("failed", "timeout")}
    print("\nDONE %d/%d，用时 %.1f 分钟" % (len(done), len(REALMS), (time.time() - started) / 60.0))
    if failed:
        print("failed 清单：")
        for rid, v in failed.items():
            print("  %s %s | %s | %s" % (rid, v.get("out"), v.get("state"), v.get("reason")))
    else:
        print("failed 清单：空")
    return 0 if len(done) == len(REALMS) else 1


if __name__ == "__main__":
    sys.exit(main())
