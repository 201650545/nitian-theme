# -*- coding: utf-8 -*-
"""仙逆故事知识库种子数据生成：chronicle.json → 飞书 Base batch_create JSON"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")

d = json.load(open(r"D:\游戏\逆天主题\assets\ui\chronicle.json", encoding="utf-8"))
realms = d["realms"]

NAME = {
    "01_ningshi": "凝气期", "02_zhuji": "筑基期", "03_jiedan": "结丹期", "04_yuanying": "元婴期",
    "05_huashen": "化神期", "06_yingbian": "婴变期", "07_wending": "问鼎期", "08_yinyang": "阴虚阳实",
    "09_kunie": "窥涅境", "10_jingnie": "净涅境", "11_suinie": "碎涅境", "12_kongnie": "空涅境",
    "13_kongling": "空灵境", "14_kongxuan": "空玄境", "15_kongjie": "空劫·四尊（金/天/跃天/大天尊共用）",
    "16_qiao1": "踏天一桥", "17_qiao2": "踏天二桥", "18_qiao3": "踏天三桥", "19_qiao4": "踏天四桥",
    "20_qiao5": "踏天五桥", "21_qiao6": "踏天六桥", "22_qiao7": "踏天七桥", "23_qiao8": "踏天八桥",
    "24_qiao9": "踏天九桥",
}
MAJORS = {"元婴期", "问鼎期", "碎涅境", "踏天一桥"}

records = []
for key, e in realms.items():
    name = e.get("era") or NAME[key]
    ev = e.get("events") or []
    ev_txt = "；".join(f"{x.get('title','')}：{x.get('summary','')}" for x in ev[:3])
    scene = e.get("scene") or ""
    desc = scene + (("　|　大事记：" + ev_txt) if ev_txt else "")
    quotes = e.get("quotes") or []
    q_txt = "；".join(f"{q.get('text','')}（{q.get('src','')}）" for q in quotes[:2] if isinstance(q, dict))
    rec = {
        "_k": key,
        "名称": name,
        "类别": "境界设定",
        "所属阶段": name,
        "内容描述": desc,
        "原文摘录/台词": q_txt,
        "产品用途": ["编年史境界卡", "破境视频提示词"] if name in MAJORS else ["编年史境界卡"],
        "来源": "assets/ui/chronicle.json（引擎编年史，即梦5.0纠偏版）",
        "状态": "已整理",
        "备注": "★大境界：破境演出播全视频+粒子" if name in MAJORS else "",
    }
    records.append(rec)

records.sort(key=lambda r: r["_k"])
for r in records:
    del r["_k"]

records += [
    {"名称": "王林", "类别": "人物", "所属阶段": "全书主角", "内容描述":
     "主角。恒岳派记名弟子出身，资质平庸，靠天逆珠与狠绝心性一路逆天。标志形象：白发、眉心星印（2D对标腾讯仙逆；真人风银甲黑发转白发）。性格隐忍、狠辣、护短。", 
     "产品用途": ["立绘生成", "编年史境界卡", "破境视频提示词"], "来源": "自拟骨架，待补原著细节", "状态": "待整理", "备注": "本尊"},
    {"名称": "许木（分身）", "类别": "人物", "所属阶段": "筑基期～化神期", "内容描述":
     "王林前期魔道分身，以『许木』之名独立行走。产品中 02~05 境（筑基/结丹/元婴/化神）立牌可切分身立绘 fenshen_02~05。", 
     "产品用途": ["立绘生成"], "来源": "引擎 v2.8 任务C + 自拟", "状态": "待整理", "备注": "与『本尊』按钮互切"},
    {"名称": "天逆珠", "类别": "法宝道具", "所属阶段": "凝气期起", "内容描述":
     "远古空灭级法宝，王林坠崖所得。内含独立空间，可产灵液加速修炼，时间流速与外界不同，司徒南魂体寄居其中。", 
     "产品用途": ["破境视频提示词", "编年史境界卡"], "来源": "chronicle.json 01_ningshi treasures", "状态": "已整理", "备注": ""},
    {"名称": "百万人头塔", "类别": "重大事件", "所属阶段": "凝气期～元婴期", "内容描述":
     "藤家灭王林全族，王林立誓以藤家全族人头筑塔复仇。元婴破境标志性异象（bt_m 与 bt_m_real 核心画面：人头塔虚影拔地而起+金雷）。", 
     "产品用途": ["破境视频提示词", "编年史境界卡"], "来源": "chronicle.json 01_ningshi events", "状态": "已整理", "备注": ""},
    {"名称": "踏天桥", "类别": "地点场景", "所属阶段": "踏天桥篇（最后九境）", "内容描述":
     "登桥即突破，一桥一重天。踏天一桥为大境界关口（与天运子对峙、星辰道念、定界罗盘、因果线），二桥至九桥为小境界。", 
     "产品用途": ["破境视频提示词", "背景生成"], "来源": "破境视频任务书 v1", "状态": "待整理", "备注": ""},
    {"名称": "轮回树", "类别": "地点场景", "所属阶段": "碎涅境", "内容描述":
     "天运海轮回树，碎涅破境核心意象：肉身硬抗天地之力，轮回之光映照众生（bt_t / bt_t_real 核心画面）。", 
     "产品用途": ["破境视频提示词"], "来源": "破境视频任务书 v1", "状态": "已整理", "备注": ""},
]

out = {"create_records": records}
json.dump(out, open(r"D:\游戏\逆天主题\workers\xn_seed_batch.json", "w", encoding="utf-8"), ensure_ascii=False)
print("records:", len(records))

fields = [
    {"type": "text", "name": "名称", "description": "条目主名：境界/人物/法宝/事件/地点"},
    {"type": "select", "name": "类别", "multiple": False, "options": [
        {"name": "境界设定", "hue": "Purple"}, {"name": "人物", "hue": "Red"},
        {"name": "法宝道具", "hue": "Orange"}, {"name": "地点场景", "hue": "Turquoise"},
        {"name": "重大事件", "hue": "Blue"}, {"name": "名场面", "hue": "Carmine"},
        {"name": "语录台词", "hue": "Yellow"}, {"name": "势力组织", "hue": "Green"},
        {"name": "功法神通", "hue": "Wathet"}, {"name": "其他", "hue": "Gray"}]},
    {"type": "text", "name": "所属阶段", "description": "所属境界或剧情篇章，如：凝气期、修魔海篇、踏天桥篇"},
    {"type": "text", "name": "内容描述"},
    {"type": "text", "name": "原文摘录/台词"},
    {"type": "select", "name": "产品用途", "multiple": True, "options": [
        {"name": "破境视频提示词", "hue": "Blue"}, {"name": "编年史境界卡", "hue": "Purple"},
        {"name": "立绘生成", "hue": "Red"}, {"name": "背景生成", "hue": "Turquoise"},
        {"name": "语录彩蛋", "hue": "Yellow"}, {"name": "其他", "hue": "Gray"}]},
    {"type": "text", "name": "来源", "description": "原著章节/动画集数/chronicle.json/自拟"},
    {"type": "select", "name": "状态", "multiple": False, "default_value": ["待整理"], "options": [
        {"name": "待整理", "hue": "Orange"}, {"name": "已整理", "hue": "Blue"}, {"name": "已应用", "hue": "Green"}]},
    {"type": "text", "name": "备注"},
]
json.dump(fields, open(r"D:\游戏\逆天主题\workers\xn_fields.json", "w", encoding="utf-8"), ensure_ascii=False)
print("fields:", len(fields))
