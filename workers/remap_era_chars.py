# -*- coding: utf-8 -*-
"""24 境立绘映射 → Seedream 官方形象二创版"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

# 1) 重写 CH 常量块
old_ch = re.search(r"const CH = \{.*?\};", c, re.S).group(0)
new_ch = """const CH = {
			ningshi: C + "/era_01_ningshi.png",
			zhuji: C + "/era_02_zhuji.png",
			jiedan: C + "/era_03_jiedan.png",
			yuanying: C + "/era_04_yuanying.png",
			huashen: C + "/era_05_huashen.png",
			yingbian: C + "/era_06_yingbian.png",
			wending: C + "/era_07_wending.png",
			yinyang: C + "/era_08_yinyang.png",
			kong: C + "/era_12_kongnie.png",
			tatian: C + "/era_16_tatian.png"
		};"""
c = c.replace(old_ch, new_ch)

# 2) 逐行替换 char 字段（按 realm id 锚定）
MAPPING = {
    "01_ningshi": "CH.ningshi", "02_zhuji": "CH.zhuji", "03_jiedan": "CH.jiedan",
    "04_yuanying": "CH.yuanying", "05_huashen": "CH.huashen", "06_yingbian": "CH.yingbian",
    "07_wending": "CH.wending", "08_yinyang": "CH.yinyang", "09_kunie": "CH.kong",
    "10_jingnie": "CH.yuanying", "11_suinie": "CH.wending", "12_kongnie": "CH.kong",
    "13_kongling": "CH.yuanying", "14_kongxuan": "CH.yingbian", "15_kongjie": "CH.kong",
}
for i in range(1, 10):
    MAPPING["%02d_qiao%d" % (15 + i, i)] = "CH.tatian"

count = 0
for rid, ch in MAPPING.items():
    pat = re.compile(r'(R\("%s".*?(?:"仙玉"|"香火"|"愿力"), )(?:V\.movie1|V\.movie2|V\.nianfan2|V\.nianfan3|CH\.\w+)(,)' % rid)
    c, n = pat.subn(r"\g<1>%s\g<2>" % ch, c, count=1)
    count += n

f.write_text(c, encoding="utf-8")
print(f"replaced {count}/24")
