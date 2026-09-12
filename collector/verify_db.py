# -*- coding: utf-8 -*-
"""验证 problems.db 质量：双语言覆盖、抽样内容。"""
import json, os, sqlite3

DB = os.path.join(os.path.dirname(__file__), "output", "problems.db")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

total = db.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
with_sol = db.execute("SELECT COUNT(DISTINCT problem_id) FROM solutions").fetchone()[0]
print(f"problems={total}, with_solution={with_sol}")

# 双语言覆盖统计
both = py_only = go_only = 0
rows = db.execute("SELECT codes_json FROM solutions").fetchall()
for r in rows:
    codes = json.loads(r["codes_json"])
    for c in codes:
        if c.get("python") and c.get("go"):
            both += 1
        elif c.get("python"):
            py_only += 1
        elif c.get("go"):
            go_only += 1
print(f"code groups: both={both}, python_only={py_only}, go_only={go_only}")

# 每题的解法数与语言覆盖
stats = db.execute("""
  SELECT p.id, p.title_cn, p.difficulty, p.solution_count,
         (SELECT COUNT(*) FROM solutions s WHERE s.problem_id=p.id AND s.kind='official') off,
         (SELECT COUNT(*) FROM solutions s WHERE s.problem_id=p.id AND s.kind='popular') pop
  FROM problems p WHERE p.id IN (1, 15, 42, 206, 283, 300) ORDER BY p.id
""").fetchall()
for r in stats:
    print(dict(r))

# 抽样：两数之和的官方题解
r = db.execute("SELECT * FROM solutions WHERE problem_id=1 AND kind='official'").fetchone()
if r:
    codes = json.loads(r["codes_json"])
    print("== 1.two-sum official:", r["title"], "| text len:", len(r["text"]))
    for c in codes:
        print("   caption:", c["caption"], "| py:", bool(c.get("python")), "| go:", bool(c.get("go")))
        print("   go head:", (c.get("go") or "")[:120].replace("\n", " "))
        print("   py head:", (c.get("python") or "")[:120].replace("\n", " "))

# 抽样：热门题解
r = db.execute("SELECT * FROM solutions WHERE problem_id=15 AND kind='popular'").fetchone()
if r:
    codes = json.loads(r["codes_json"])
    print("== 15.3sum popular:", r["title"], "| author:", r["author"], "| votes:", r["votes_raw"])
    for c in codes:
        print("   caption:", c["caption"], "| py:", bool(c.get("python")), "| go:", bool(c.get("go")))

# 描述抽样（含约束范围）
p = db.execute("SELECT id, title_cn, content_cn FROM problems WHERE id=1").fetchone()
print("== desc 1:", p["title_cn"])
print(p["content_cn"][-500:])
db.close()
