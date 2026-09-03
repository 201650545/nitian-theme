# -*- coding: utf-8 -*-
"""空劫拆四境 + 桥顺延 + 索引更新"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

# 1) 15_kongjie 单行 → 四境
old15 = 'R("15_kongjie", "空劫境", "金尊 · 天尊 · 大天尊", 300000000000000, 1000000000000000, "#c9b45a", "#e2d494", "香火", CH.kong, BG.kong, A + "/ui/seals/seal_15_kongjie.png", null),'
assert old15 in c, "15 anchor"
SEAL = 'A + "/ui/seals/seal_15_kongjie.png"'
new15 = (
    'R("15_kongjin", "空劫·金尊", "空劫初境 · 金尊", 300000000000000, 450000000000000, "#c9b45a", "#e2d494", "香火", CH.kong, BG.kong, ' + SEAL + ', null),\n\t\t\t'
    'R("16_kongzun", "空劫·天尊", "空劫中境 · 天尊", 450000000000000, 650000000000000, "#d2bd5e", "#e6d494", "香火", CH.kong, BG.kong, ' + SEAL + ', null),\n\t\t\t'
    'R("17_kongyue", "空劫·岳天尊", "空劫高境 · 岳天尊", 650000000000000, 850000000000000, "#dcc96a", "#efde9a", "香火", CH.kong, BG.kong, ' + SEAL + ', null),\n\t\t\t'
    'R("18_kongda", "空劫·大天尊", "空劫圆满 · 大天尊", 850000000000000, 1000000000000000, "#e6d574", "#f8eaAe", "香火", CH.kong, BG.kong, ' + SEAL + ', null),'
)
c = c.replace(old15, new15, 1)

# 2) 桥 id 顺延 16-24 -> 19-27
for old, new in [("16_qiao1", "19_qiao1"), ("17_qiao2", "20_qiao2"), ("18_qiao3", "21_qiao3"),
                 ("19_qiao4", "22_qiao4"), ("20_qiao5", "23_qiao5"), ("21_qiao6", "24_qiao6"),
                 ("22_qiao7", "25_qiao7"), ("23_qiao8", "26_qiao8"), ("24_qiao9", "27_qiao9")]:
    # 只替换 R("id" 定义处
    oldp = 'R("' + old + '"'
    assert oldp in c, "bridge " + old
    c = c.replace(oldp, 'R("' + new + '"', 1)

# 3) 索引更新
def sub_count(c, old, new, expect):
    assert c.count(old) == expect, f"expected {expect} of [{old}], got {c.count(old)}"
    return c.replace(old, new)

c = sub_count(c, "isBridge = i >= 15", "isBridge = i >= 18", 1)
c = sub_count(c, "[i - 15]", "[i - 18]", 2)
c = sub_count(c, "[3, 6, 10, 15]", "[3, 6, 10, 18]", 1)
c = sub_count(c, '15: "bt_p"', '18: "bt_p"', 1)
c = sub_count(c, "i < 15", "i < 18", 1)

f.write_text(c, encoding="utf-8")
print("空劫四境拆分 OK")
