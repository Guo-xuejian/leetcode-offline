# -*- coding: utf-8 -*-
"""分析数据集：题解语言分布、官方题解语言覆盖、难度分布。"""
import os, re, collections, sys

BASE = os.path.join(os.path.dirname(__file__), "data", "leetcode-supercrawl-main", "data")
FENCE = re.compile(r"```([a-zA-Z0-9+#-]*)\s*(\[[^\]]*\])?\s*\n", re.M)

lang_counter = collections.Counter()
official_info = collections.Counter()   # official 中出现过的语言
official_count = 0
popular_py = 0          # 至少有 1 个热门题解含 Python
popular_go = 0          # 至少有 1 个热门题解含 Go
popular_total = 0
no_sol_dir = 0
difficulty = collections.Counter()

dirs = [d for d in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, d))]
print("problem dirs:", len(dirs))

for d in sorted(dirs):
    m = re.match(r"^(\d+)\.(.+)$", d)
    if not m:
        continue
    p = os.path.join(BASE, d, "solutions")
    if not os.path.isdir(p):
        no_sol_dir += 1
        continue
    files = sorted(os.listdir(p))
    popular = [f for f in files if f.endswith(".md") and f != "Official.md"]
    popular_total += len(popular)
    has_py, has_go = False, False
    for f in files:
        path = os.path.join(p, f)
        content = open(path, encoding="utf-8", errors="ignore").read()
        langs = [x.group(1).strip().lower() for x in FENCE.finditer(content) if x.group(1).strip()]
        for lg in langs:
            lang_counter[lg] += 1
        if f == "Official.md":
            official_count += 1
            for lg in langs:
                official_info[lg] += 1
        else:
            if any(lg in ("python", "py", "python3") for lg in langs):
                has_py = True
            if "go" in langs:
                has_go = True
    if has_py: popular_py += 1
    if has_go: popular_go += 1

print("official.md 数量:", official_count)
print("官方题解语言覆盖:", dict(official_info.most_common(20)))
print("热门题解总数:", popular_total)
print("含 Python 热门题解的题目数:", popular_py)
print("含 Go 热门题解的题目数:", popular_go)
print("无题解目录:", no_sol_dir)
print("所有代码块语言 Top25:", lang_counter.most_common(25))

# 难度分布（从 README 表格读取）
import csv, io
for fname in ["0001-1000.md", "1001-2000.md", "2001-3000.md"]:
    fpath = os.path.join(os.path.dirname(BASE), fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("| ") and not line.startswith("| #"):
                cols = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cols) >= 5 and cols[4] in ("Easy", "Medium", "Hard"):
                    difficulty[cols[4]] += 1
print("难度分布:", dict(difficulty))
