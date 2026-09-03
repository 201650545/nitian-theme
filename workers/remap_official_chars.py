# -*- coding: utf-8 -*-
"""立绘映射全面切换为腾讯仙逆官方设计（已目检真图）"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

PAIRS = [
    ('R("01_ningshi", "凝气期", "恒岳杂役 · 初心起步", 0, 1e5, "#c9a55c", "#5a9e8f", "仙玉", CH.ningshi,',
     'R("01_ningshi", "凝气期", "恒岳杂役 · 初心起步", 0, 1e5, "#c9a55c", "#5a9e8f", "仙玉", V.movie2,'),
    ('R("02_zhuji", "筑基期", "铁柱峰上 · 步步登天", 1e5, 1e6, "#7fa88f", "#a8c8b0", "仙玉", CH.zhuji,',
     'R("02_zhuji", "筑基期", "铁柱峰上 · 步步登天", 1e5, 1e6, "#7fa88f", "#a8c8b0", "仙玉", V.movie2,'),
    ('R("03_jiedan", "结丹期", "灵液化丹 · 杀伐初显", 1e6, 8e6, "#b8453a", "#d98a6a", "仙玉", CH.jiedan,',
     'R("03_jiedan", "结丹期", "灵液化丹 · 杀伐初显", 1e6, 8e6, "#b8453a", "#d98a6a", "仙玉", V.movie2,'),
    ('R("05_huashen", "化神期", "神游太虚 · 生死意境", 2e7, 5e7, "#8a9bb5", "#b8c6da", "仙玉", CH.huashen,',
     'R("05_huashen", "化神期", "神游太虚 · 生死意境", 2e7, 5e7, "#8a9bb5", "#b8c6da", "仙玉", V.nianfan3,'),
    ('R("09_kunie", "窥涅境", "初窥本源", 2.2e8, 3e8, "#6a89b8", "#a3bcd8", "仙玉", CH.kong,',
     'R("09_kunie", "窥涅境", "初窥本源", 2.2e8, 3e8, "#6a89b8", "#a3bcd8", "仙玉", V.nianfan2,'),
    ('R("12_kongnie", "空涅境", "空之四境 · 其一", 5.2e8, 6.4e8, "#7d6ab8", "#ab9cd8", "香火", CH.kong,',
     'R("12_kongnie", "空涅境", "空之四境 · 其一", 5.2e8, 6.4e8, "#7d6ab8", "#ab9cd8", "香火", V.movie1,'),
    ('R("15_kongjie", "空劫境", "金尊 · 天尊 · 大天尊", 8.8e8, 1e9, "#c9b45a", "#e2d494", "香火", CH.kong,',
     'R("15_kongjie", "空劫境", "金尊 · 天尊 · 大天尊", 8.8e8, 1e9, "#c9b45a", "#e2d494", "香火", V.movie1,'),
]
n = 0
for old, new in PAIRS:
    if old in c:
        c = c.replace(old, new)
        n += 1
    else:
        print("MISS:", old[:60])
f.write_text(c, encoding="utf-8")
print(f"replaced {n}/{len(PAIRS)}")
