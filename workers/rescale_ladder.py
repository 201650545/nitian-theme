# -*- coding: utf-8 -*-
"""天梯重构：K→M→B→T→P 四大境界，踏天九桥 1P 起步"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
f = Path(r"D:\游戏\逆天主题\dsh-plugin\pkg\lib\client.js")
c = f.read_text(encoding="utf-8")

# 新阈值 (from, to)
T = {
    "01_ningshi": (0, 1e4), "02_zhuji": (1e4, 1e5), "03_jiedan": (1e5, 1e6),
    "04_yuanying": (1e6, 1e7), "05_huashen": (1e7, 1e8), "06_yingbian": (1e8, 1e9),
    "07_wending": (1e9, 5e9), "08_yinyang": (5e9, 2e10), "09_kunie": (2e10, 1e11),
    "10_jingnie": (1e11, 1e12), "11_suinie": (1e12, 4e12), "12_kongnie": (4e12, 2e13),
    "13_kongling": (2e13, 6e13), "14_kongxuan": (6e13, 3e14), "15_kongjie": (3e14, 1e15),
    "16_qiao1": (1e15, 3e15), "17_qiao2": (3e15, 1e16), "18_qiao3": (1e16, 3e16),
    "19_qiao4": (3e16, 1e17), "20_qiao5": (1e17, 3e17), "21_qiao6": (3e17, 1e18),
    "22_qiao7": (1e18, 3e18), "23_qiao8": (3e18, 1e19), "24_qiao9": (1e19, None),
}

def fmt_num(x):
    if x is None:
        return "Infinity"
    s = repr(float(x))
    return s.rstrip("0").rstrip(".") if "." in s else s

n = 0
for rid, (a, b) in T.items():
    pat = re.compile(r'(R\("%s".*?, )[-\de.]+, [-\de.]+(, )' % rid)
    c, k = pat.subn(lambda m: m.group(1) + fmt_num(a) + ", " + fmt_num(b) + m.group(2), c, count=1)
    n += k

# fmt 单位制：K/M/B/T/P
old_fmt = 'const fmt = (n) => n >= 1e8 ? (n / 1e8).toFixed(n >= 1e9 ? 1 : 2) + "亿" : n >= 1e4 ? (n / 1e4).toFixed(1) + "万" : String(Math.floor(n));'
new_fmt = ('const fmt = (n) => n >= 1e15 ? (n / 1e15).toFixed(2) + "P" : n >= 1e12 ? (n / 1e12).toFixed(2) + "T" '
           ': n >= 1e9 ? (n / 1e9).toFixed(2) + "B" : n >= 1e6 ? (n / 1e6).toFixed(2) + "M" '
           ': n >= 1e3 ? (n / 1e3).toFixed(1) + "K" : String(Math.floor(n));')
assert old_fmt in c, "fmt not found"
c = c.replace(old_fmt, new_fmt)

# 演示按钮：+1M / +1B / +1T
c = c.replace('<div class="row"><button class="a1">＋1万</button><button class="a2">＋100万</button><button class="a3">＋1亿</button></div>',
              '<div class="row"><button class="a1">＋1M</button><button class="a2">＋1B</button><button class="a3">＋1T</button></div>')
c = c.replace('$(".a1").addEventListener("click", () => addDemo(1e4));',
              '$(".a1").addEventListener("click", () => addDemo(1e6));')
c = c.replace('$(".a2").addEventListener("click", () => addDemo(1e6));',
              '$(".a2").addEventListener("click", () => addDemo(1e9));')
c = c.replace('$(".a3").addEventListener("click", () => addDemo(1e8));',
              '$(".a3").addEventListener("click", () => addDemo(1e12));')

f.write_text(c, encoding="utf-8")
print(f"thresholds replaced {n}/24; fmt/buttons updated")
