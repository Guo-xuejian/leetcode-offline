# -*- coding: utf-8 -*-
"""提取第四批条目源码（need_py 中尚未核实的 Go 源码）。"""
import os
import re

SRC = os.path.join(os.path.dirname(__file__), "output", "todo_src.txt")
OUT = os.path.join(os.path.dirname(__file__), "output", "extract4.txt")

WANT = {
    ("2", "Official.md"), ("31", "1.md"), ("32", "Official.md"), ("34", "Official.md"),
    ("35", "Official.md"), ("39", "Official.md"), ("45", "Official.md"), ("53", "Official.md"),
    ("70", "Official.md"), ("74", "Official.md"), ("76", "Official.md"),
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
print("saved extract4.txt lines:", len(blocks))
