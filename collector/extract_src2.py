# -*- coding: utf-8 -*-
"""提取第二批待核对条目源码。"""
import os
import re

SRC = os.path.join(os.path.dirname(__file__), "output", "todo_src.txt")
OUT = os.path.join(os.path.dirname(__file__), "output", "extract2.txt")

# (pid, filename) 需要查看源码的条目
WANT = {
    ("128", "1.md"), ("139", "2.md"), ("142", "1.md"), ("153", "1.md"), ("155", "2.md"),
    ("160", "2.md"), ("226", "1.md"), ("236", "1.md"), ("238", "2.md"), ("283", "1.md"),
    ("300", "1.md"), ("300", "2.md"), ("322", "1.md"), ("394", "1.md"), ("543", "2.md"),
    ("763", "1.md"), ("994", "1.md"), ("994", "2.md"), ("1143", "1.md"), ("1143", "2.md"),
    ("169", "Official.md"), ("206", "1.md"), ("215", "1.md"), ("207", "2.md"),
}

blocks = []
cur = None
for line in open(SRC, encoding="utf-8"):
    m = re.match(r"^### \[PID=(\d+) FILE=([\w.]+) IDX=(\d+) NEED=(\w+)\]", line)
    if m:
        cur = (m.group(1), m.group(2))
        if cur in WANT:
            blocks.append("")
            blocks.append(line.strip())
    else:
        if cur in WANT:
            blocks.append(line)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(blocks))
print("saved extract2.txt lines:", len(blocks))
