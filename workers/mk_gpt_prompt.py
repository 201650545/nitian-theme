# -*- coding: utf-8 -*-
"""GPT-Extend 深爬提示词构造 + 注入 + 发送"""
import base64
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PROMPT = """你是《仙逆》（耳根小说+腾讯官方动画）资深书粉研究员。请联网搜索并深度整理，直接输出一个合法 JSON（不要 markdown 代码块，不要解释），用于游戏彩蛋系统。

要求覆盖以下境界（key 用英文 id）：
01_ningshi 凝气期 / 02_zhuji 筑基期 / 03_jiedan 结丹期 / 04_yuanying 元婴期 / 05_huashen 化神期 / 06_yingbian 婴变期 / 07_wending 问鼎期 / 08_yinyang 阴虚阳实 / 09_kunie 窥涅 / 10_jingnie 净涅 / 11_suinie 碎涅 / 12_kongnie 空涅 / 13_kongling 空灵 / 14_kongxuan 空玄 / 15_kongjie 空劫

每个境界输出：
{
  "id": "01_ningshi",
  "eggs": [4-6条 书粉彩蛋/趣梗/冷知识/反差萌，含原著细节],
  "quotes": [2-3条 原著/动画经典台词，附出处（章节/集数）],
  "scene": "该期最震撼名场面的一句话画面描述",
  "enemies": [{"name":"...","fun":"一句趣味点评"}]  (2-3个该期对手),
  "treasures": [{"name":"...","fun":"一句趣味点评"}]  (2-3件该期法宝/机缘),
  "friends": [{"name":"...","fun":"一句趣味点评"}]  (1-2个该期重要人物)
}

重点挖掘：王林"苟且隐忍vs杀伐果断"反差、经典名场面（如藤化元当磨刀石、百万人头塔、雨之仙界）、意难平角色、书粉才懂的梗。若联网搜索受限则凭你训练知识输出（都很熟），标注"_src":"model"。只输出 JSON 本体。"""

b64 = base64.b64encode(PROMPT.encode("utf-8")).decode()

inject = (
    "(()=>{const b=atob('" + b64 + "');const u=new Uint8Array(b.length);"
    "for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);"
    "const s=new TextDecoder().decode(u);"
    "const el=document.querySelector('#prompt-textarea[contenteditable=true]')||document.querySelector('[contenteditable=true]');"
    "el.focus();el.innerHTML='';document.execCommand('insertText',false,s);"
    "return JSON.stringify({len:el.innerText.length,tail:(el.innerText||'').slice(-30)});})()"
)
Path(r"C:\Users\887E~1\AppData\Local\Temp\opencode\gpt-inject.one.txt").write_text(inject, encoding="utf-8")

send = (
    '(()=>{const btn=[...document.querySelectorAll("button")].find(b=>(b.getAttribute("aria-label")||"").includes("Send")||(b.getAttribute("data-testid")||"")==="send-button");'
    'if(!btn)return "no-send-btn";btn.click();return "sent";})()'
)
Path(r"C:\Users\887E~1\AppData\Local\Temp\opencode\gpt-send.one.txt").write_text(send, encoding="utf-8")
print("inject/send 命令文件已生成")
