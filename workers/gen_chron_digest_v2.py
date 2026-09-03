# -*- coding: utf-8 -*-
"""卷轴引言 v2 — 逐条生成防错位（2026-08-27）
批量模式导致引言与境界错位，改为每境单独调用：给该境界完整剧情上下文，只生成一句。
渠道链：modelscope→opencode(UA)→sensetime；逐条落盘支持断点续跑。
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"D:\逆天主题")
KEYS_PATH = Path(r"D:\项目\data\search_gateway\channels.json")
OUT_PATH = ROOT / "assets" / "ui" / "chronicle-img" / "digests.json"
CHRON_PATH = ROOT / "assets" / "ui" / "chronicle.json"

CHANNELS = [
    ("modelscope", "https://api-inference.modelscope.cn/v1/chat/completions",
     "deepseek-ai/DeepSeek-V4-Flash-0731", {}),
    ("opencode", "https://opencode.ai/zen/go/v1/chat/completions",
     "deepseek-v4-flash", {"User-Agent": "openai-completions/pi-ai"}),
    ("sensetime", "https://token.sensenova.cn/v1/chat/completions",
     "deepseek-v4-flash", {}),
]

REALMS = [
    ("01_ningshi", "凝气期", "恒岳派杂役苦修，得天逆珠司徒南传道，决明谷以极境斩藤厉，藤家灭王林全族，王林立誓复仇"),
    ("02_zhuji", "筑基期", "肉身被毁夺舍马良，修成极境神识，火焚国与李慕婉初遇并护送，迷雾森林夺基"),
    ("03_jiedan", "结丹期", "携李慕婉入修魔海，三寒合一凝结极境金丹，碎星乱护婉儿炼丹，杀伐果断"),
    ("04_yuanying", "元婴期", "古神之地得涂司传承修成古神真身，回赵国灭藤家立百万人头塔复仇，白发狂舞绝世煞星"),
    ("05_huashen", "化神期", "大楚国化凡开木雕铺感悟生死轮回意境，雨之仙界战红蝶救周佚，青衫木雕师"),
    ("06_yingbian", "婴变期", "转化仙力仙躯，司徒南复活，朱雀墓决战夺朱雀仙冠，拜入天运宗紫系，紫袍金纹白发"),
    ("07_wending", "问鼎期", "妖灵之地古妖试炼，炼杀戮煞星分身，抗天劫吸收问鼎之晶达大圆满，黑金玄袍雷霆煞气"),
    ("08_yinyang", "阴虚阳实", "罗天星域化名许木，雷仙界掌御雷鼎，与清水师兄相认，突破阳实境，蓝白雷仙袍六星古神纹"),
    ("09_kunie", "窥涅境", "初窥涅槃本源，以万魂幡碎身炼金骨，窥探天道法则"),
    ("10_jingnie", "净涅境", "涅槃洗尘感悟轮回，法目破空洞察虚妄"),
    ("11_suinie", "碎涅境", "碎涅证道，肉身抗天运，以大因果大道逆转命运"),
    ("12_kongnie", "空涅境", "跨入空之四境第一境，虚空之门星云缠身，货币由仙玉转香火"),
    ("13_kongling", "空灵境", "空之四境第二境，灵蝶虚影绕月，渐悟空之真意"),
    ("14_kongxuan", "空玄境", "空之四境第三境，玄冰法阵演道，败雷仙扬名星域"),
    ("15_kongjin", "空劫·金尊", "空劫初境金尊，劫云天眼加身，金之极道"),
    ("16_kongzun", "空劫·天尊", "空劫中境天尊，号令一方天尊威严"),
    ("17_kongyue", "空劫·跃天尊", "空劫高境跃天尊，跃出寻常天道束缚"),
    ("18_kongda", "空劫·大天尊", "空劫圆满大天尊，极境神识冠绝古今"),
    ("19_qiao1", "踏天一桥", "初登踏天天桥，与天运子初战，定界罗盘定时空，货币转愿力"),
    ("20_qiao2", "踏天二桥", "二桥之上破轮回，天道化身哀嚎消散"),
    ("21_qiao3", "踏天三桥", "三桥斩道果，轮回镇压天道"),
    ("22_qiao4", "踏天四桥", "始古山前挥袖定计，计都承皇尊"),
    ("23_qiao5", "踏天五桥", "五桥问心，三身合一窥见道门"),
    ("24_qiao6", "踏天六桥", "六桥幻影破妄存真，跨越古道"),
    ("25_qiao7", "踏天七桥", "七桥决战天运子，拳碎天道之影"),
    ("26_qiao8", "踏天八桥", "八桥因果逆转生死，一剑斩天道"),
    ("27_qiao9", "踏天九桥", "九桥踏碎天道，因果花落天运陨落，大道尽头彼岸在望"),
]


def load_key(channel: str) -> str:
    d = json.loads(KEYS_PATH.read_bytes().decode("utf-8-sig"))
    k = d["keys"][channel]
    key = (k.get("api_key") or k.get("key")) if isinstance(k, dict) else k
    if not key:
        raise RuntimeError(channel + " key 未配置")
    return key


def call_llm(prompt: str) -> str:
    payload = {
        "model": "",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 4000,
    }
    last_err = None
    for name, base, model, extra in CHANNELS:
        payload["model"] = model
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + load_key(name)}
        headers.update(extra)
        try:
            req = urllib.request.Request(base, data=json.dumps(payload).encode("utf-8"),
                                         headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=90) as r:
                j = json.loads(r.read().decode("utf-8"))
            msg = j["choices"][0]["message"]
            content = msg.get("content") or ""
            if not content and msg.get("reasoning"):
                content = msg["reasoning"]
            if content.strip():
                return content.strip()
        except Exception as e:  # noqa: BLE001
            last_err = e
    raise RuntimeError("所有渠道失败: " + str(last_err))


def gen_one(rid: str, name: str, plot: str) -> str:
    prompt = (
        f"仙逆主角王林当前境界：【{name}】。此阶段剧情：{plot}。\n"
        "请为此境界写一句卷轴引言：8~14个汉字，古意凝练，必须紧扣上述剧情，"
        "不要句号，不要解释，只输出引言本身。"
    )
    out = call_llm(prompt)
    m = re.search(r"([\u4e00-\u9fa5·，、～]{6,22})", out)
    if not m:
        return name + " · 道途一程"
    v = m.group(1).strip("，、")
    return v if len(v) <= 20 else v[:20]


def main() -> None:
    done = json.loads(OUT_PATH.read_text(encoding="utf-8")) if OUT_PATH.exists() else {}
    for rid, name, plot in REALMS:
        if re.fullmatch(r"\S+ · 道途一程", done.get(rid, "")) or rid not in done:
            v = gen_one(rid, name, plot)
            done[rid] = v
            print(rid, v, flush=True)
            OUT_PATH.write_text(json.dumps(done, ensure_ascii=False, indent=2), encoding="utf-8")
            time.sleep(1)
        else:
            print("[keep]", rid, done[rid], flush=True)
    print("OK", len(done))


if __name__ == "__main__":
    main()
