# -*- coding: utf-8 -*-
"""提取第三批待核对条目源码（need_go 中尚未核实的全部）。"""
import os
import re

SRC = os.path.join(os.path.dirname(__file__), "output", "todo_src.txt")
OUT = os.path.join(os.path.dirname(__file__), "output", "extract3.txt")

WANT = {
    ("3", "1.md"), ("5", "Official.md"), ("11", "1.md"), ("11", "Official.md"), ("15", "1.md"),
    ("17", "1.md"), ("17", "2.md"), ("20", "1.md"), ("20", "2.md"), ("21", "1.md"),
    ("21", "Official.md"), ("22", "1.md"), ("22", "2.md"), ("22", "Official.md"),
    ("23", "1.md"), ("33", "Official.md"), ("39", "1.md"), ("41", "1.md"), ("46", "1.md"),
    ("46", "Official.md"), ("48", "2.md"), ("53", "1.md"), ("55", "Official.md"),
    ("56", "Official.md"), ("62", "1.md"), ("64", "1.md"), ("70", "2.md"), ("72", "1.md"),
    ("72", "Official.md"), ("73", "1.md"), ("74", "2.md"), ("75", "1.md"), ("76", "1.md"),
    ("78", "2.md"), ("79", "1.md"), ("84", "1.md"), ("94", "1.md"), ("94", "2.md"),
    ("101", "1.md"), ("104", "2.md"), ("121", "Official.md"), ("146", "Official.md"),
    ("300", "Official.md"), ("322", "Official.md"), ("543", "Official.md"),
    ("994", "Official.md"), ("199", "Official.md"), ("230", "Official.md"),
    ("148", "1.md"), ("198", "1.md"), ("138", "1.md"), ("105", "2.md"), ("118", "1.md"),
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
print("saved extract3.txt lines:", len(blocks))
