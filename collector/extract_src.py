# -*- coding: utf-8 -*-
"""提取指定条目（need_py 全部 + 几个特殊 need_go 条目）的源码到 output/extract.txt"""
import os
import re

SRC = os.path.join(os.path.dirname(__file__), "output", "todo_src.txt")
OUT = os.path.join(os.path.dirname(__file__), "output", "extract.txt")

# 需要核对的特殊 need_go 条目（方法名不直观/片段型）
SPECIAL = {
    ("105", "2.md", "0"), ("118", "1.md", "0"), ("138", "1.md", "0"), ("138", "1.md", "1"),
    ("146", "Official.md", "0"), ("207", "2.md", "0"), ("215", "1.md", "0"),
    ("230", "Official.md", "2"), ("189", "1.md", "0"), ("763", "1.md", "2"),
    ("1143", "1.md", "1"), ("1143", "2.md", "1"), ("198", "1.md", "0"), ("198", "1.md", "1"),
    ("199", "Official.md", "0"), ("199", "Official.md", "1"), ("148", "1.md", "0"), ("148", "1.md", "1"),
}

blocks = []
cur = None
for line in open(SRC, encoding="utf-8"):
    m = re.match(r"^### \[PID=(\d+) FILE=([\w.]+) IDX=(\d+) NEED=(\w+)\]", line)
    if m:
        cur = m.groups()
        if cur[3] == "PY" or (cur[0], cur[1], cur[2]) in SPECIAL:
            blocks.append("")
            blocks.append(line.strip())
    else:
        if cur and (cur[3] == "PY" or (cur[0], cur[1], cur[2]) in SPECIAL):
            blocks.append(line)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(blocks))
print("saved extract.txt lines:", len(blocks))
