# -*- coding: utf-8 -*-
"""读取 GPT 回复长度/状态"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
js = """
(() => {
  const arts = [...document.querySelectorAll("[data-message-author-role=assistant], .markdown, .agent-turn")];
  if (!arts.length) return "no-reply-yet";
  const last = arts[arts.length - 1];
  const txt = (last.innerText || "").trim();
  return JSON.stringify({ len: txt.length, has_json: txt.indexOf("{") >= 0, tail: txt.slice(-60) });
})()
"""
one = " ".join(line.strip() for line in js.splitlines() if line.strip())
Path(r"C:\Users\887E~1\AppData\Local\Temp\opencode\gpt-read-len.one.txt").write_text(one, encoding="utf-8")
print("ok")
