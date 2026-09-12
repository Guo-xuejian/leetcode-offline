# -*- coding: utf-8 -*-
"""导出待转换组的源码到 output/todo_src.txt，供人工翻译对照。"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "leetcode-supercrawl-main", "data")
sys.path.insert(0, HERE)
import parse_solutions as ps

hot = json.load(open(os.path.join(HERE, "output", "hot100.json"), encoding="utf-8"))
hot_slugs = {str(x["id"]): x["slug"] for x in hot}

lines = []
for line in open(os.path.join(HERE, "output", "todo.txt"), encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("===") or "\t" not in line:
        continue
    pid, fname, idx, need, cap = line.split("\t", 4)
    slug = hot_slugs[pid]
    path = os.path.join(DATA, f"{int(pid):04d}.{slug}", "solutions", fname)
    md = open(path, encoding="utf-8", errors="ignore").read()
    sol = ps.parse_solution(md, fname == "Official.md", None)
    g = sol["codes"][int(idx)]
    src = g["python"] if need == "GO" else g["go"]
    lines.append(f"### [PID={pid} FILE={fname} IDX={idx} NEED={need}] CAP={cap}")
    lines.append(src.rstrip())
    lines.append("")

with open(os.path.join(HERE, "output", "todo_src.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("saved todo_src.txt, lines:", len(lines))
