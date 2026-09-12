# -*- coding: utf-8 -*-
"""生成热题100转换任务清单（按丢弃前的代码组顺序），供人工转换使用。"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "leetcode-supercrawl-main", "data")
sys.path.insert(0, HERE)
import parse_solutions as ps

hot = json.load(open(os.path.join(HERE, "output", "hot100.json"), encoding="utf-8"))
hot_slugs = {str(x["id"]): x["slug"] for x in hot}

need_go, need_py, dropped = [], [], []

for pid, slug in hot_slugs.items():
    d = os.path.join(DATA, f"{int(pid):04d}.{slug}")
    sol_dir = os.path.join(d, "solutions")
    if not os.path.isdir(sol_dir):
        continue
    files = ["Official.md"] + [f for f in sorted(os.listdir(sol_dir)) if f.endswith(".md") and f != "Official.md"][:2]
    for fname in files:
        path = os.path.join(sol_dir, fname)
        if not os.path.exists(path):
            continue
        md = open(path, encoding="utf-8", errors="ignore").read()
        sol = ps.parse_solution(md, fname == "Official.md", None)
        for i, g in enumerate(sol["codes"]):
            if g.get("python") and not g.get("go"):
                need_go.append((pid, fname, i, g["caption"]))
            elif g.get("go") and not g.get("python"):
                need_py.append((pid, fname, i, g["caption"]))
        # 记录被丢弃的组（无 python/go）— 仅统计官方
        if fname == "Official.md":
            # parse_solution 不返回 dropped 组明细，这里单独统计
            for i, g in enumerate(sol["codes"]):
                if not g.get("python") and not g.get("go"):
                    dropped.append((pid, fname, i, g["caption"]))

with open(os.path.join(HERE, "output", "todo.txt"), "w", encoding="utf-8") as f:
    f.write("=== need_go ===\n")
    for pid, fn, i, cap in sorted(need_go, key=lambda x: (int(x[0]), x[1], x[2])):
        f.write(f"{pid}\t{fn}\t{i}\tGO\t{cap}\n")
    f.write("=== need_py ===\n")
    for pid, fn, i, cap in sorted(need_py, key=lambda x: (int(x[0]), x[1], x[2])):
        f.write(f"{pid}\t{fn}\t{i}\tPY\t{cap}\n")
    f.write("=== dropped_official ===\n")
    for pid, fn, i, cap in sorted(dropped, key=lambda x: (int(x[0]), x[2])):
        f.write(f"{pid}\t{fn}\t{i}\tDROP\t{cap}\n")

print("need_go:", len(need_go), "| need_py:", len(need_py), "| dropped(official):", len(dropped))
print("saved: output/todo.txt")
