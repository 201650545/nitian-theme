# -*- coding: utf-8 -*-
"""生成 cmd /c 版读取命令"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
one = Path(r"C:\Users\887E~1\AppData\Local\Temp\opencode\gpt-read-len.one.txt").read_text(encoding="utf-8")
cmd = 'cmd /c opencli browser gpt-crawl eval "' + one.replace('"', '\\"') + '"'
Path(r"C:\Users\887E~1\AppData\Local\Temp\opencode\gpt-read-cmd.ps1").write_text(cmd, encoding="utf-8")
print("cmd file ok")
