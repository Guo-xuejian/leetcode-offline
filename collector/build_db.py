# -*- coding: utf-8 -*-
"""
build_db.py — 汇总数据源生成离线题库 problems.db。

输入:
  - collector/data/leetcode-supercrawl-main/   题解数据集（描述+官方/热门题解）
  - collector/output/metadata.json             题目元数据（tags，来自 leetcode.com GraphQL）
  - collector/output/hot100.json               热题 HOT 100 题单
  - collector/conversions/<id>.json            人工转换缓存（补齐缺失 Go/Python）

输出:
  - collector/output/problems.db

表:
  problems(id PK, title, title_cn, slug, difficulty, tags, content_cn, content_en, is_hot, solution_count)
  solutions(id PK AUTOINC, problem_id, kind, seq, title, author, votes, votes_raw, text, codes_json)
"""
import json
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "leetcode-supercrawl-main")
OUT = os.path.join(HERE, "output", "problems.db")

import html2md
import parse_solutions as ps

POPULAR_MAX = 2          # 每题最多保留的热门题解数
CONV_DIR = os.path.join(HERE, "conversions")


# ---------- README 表格解析 ----------
def parse_readme_tables():
    """返回 {dirname: {id, title, difficulty, votes:{filename:(votes_raw,views_raw)}}}"""
    info = {}
    for fname in ["0001-1000.md", "1001-2000.md", "2001-3000.md"]:
        path = os.path.join(DATA, fname)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line.startswith("| ") or line.startswith("| #"):
                    continue
                cols = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cols) < 7:
                    continue
                num, title_cell, _tag, _link, diff, _desc, _off, pop_cell = cols[:8]
                m = re.match(r"\[(.+)\]\(data/([^)]+)\)", title_cell)
                if not m:
                    continue
                title, dirname = m.group(1), m.group(2)
                votes = {}
                for vm in re.finditer(r"\[(\d)\(([\d.]+[kK]?)?👍?/?([\d.]+[kK]?)?👀?\)\]\(data/[^)]+/solutions/(\d+)\.md\)", pop_cell):
                    seq, v_raw, _views, _fn = vm.groups()
                    votes[str(seq)] = v_raw or ""
                info[dirname] = {"id": int(num), "title": title, "difficulty": diff, "votes": votes}
    return info


def norm_votes(raw: str) -> int:
    if not raw:
        return 0
    try:
        v = float(raw)
        return int(v)
    except ValueError:
        pass
    m = re.match(r"^([\d.]+)([kK])$", raw)
    if m:
        return int(float(m.group(1)) * 1000)
    try:
        return int(raw)
    except ValueError:
        return 0


# ---------- 描述解析 ----------
def parse_description(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        md = f.read()
    # 去掉首个标题行（题目标题由 README/元数据提供）
    lines = md.split("\n")
    if lines and lines[0].strip().startswith("#"):
        lines = lines[1:]
    return html2md.html_to_markdown("\n".join(lines)).strip()


def title_from_desc(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            first = f.readline()
        m = re.match(r"^#+\s*\[(?:[\d.]+\s*)?([^\]]+)\]", first.strip())
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return ""


# ---------- 主流程 ----------
def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    table = parse_readme_tables()
    meta = json.load(open(os.path.join(HERE, "output", "metadata.json"), encoding="utf-8"))
    hot = {str(x["id"]): x for x in json.load(open(os.path.join(HERE, "output", "hot100.json"), encoding="utf-8"))}

    data_dir = os.path.join(DATA, "data")
    dirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    print("problem dirs:", len(dirs))

    if os.path.exists(OUT):
        os.remove(OUT)
    db = sqlite3.connect(OUT)
    db.execute("PRAGMA journal_mode=OFF")
    db.executescript("""
        CREATE TABLE problems(
          id INTEGER PRIMARY KEY,
          title TEXT, title_cn TEXT, slug TEXT,
          difficulty TEXT, tags TEXT,
          content_cn TEXT, content_en TEXT,
          is_hot INTEGER DEFAULT 0,
          solution_count INTEGER DEFAULT 0
        );
        CREATE TABLE solutions(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          problem_id INTEGER, kind TEXT, seq INTEGER,
          title TEXT, author TEXT,
          votes INTEGER DEFAULT 0, votes_raw TEXT,
          text TEXT, codes_json TEXT
        );
        CREATE INDEX idx_sol_problem ON solutions(problem_id);
    """)

    stat = {"official": 0, "popular": 0, "dropped": 0, "no_desc": 0}
    n_ok = 0
    for d in sorted(dirs):
        m = re.match(r"^(\d+)\.(.+)$", d)
        if not m:
            continue
        num, slug = m.group(1), m.group(2)
        pid = int(num)
        tinfo = table.get(d, {})
        mmeta = meta.get(slug, {})

        # 描述
        cn_path = os.path.join(data_dir, d, "description", "CN.md")
        en_path = os.path.join(data_dir, d, "description", "EN.md")
        content_cn = parse_description(cn_path) if os.path.exists(cn_path) else ""
        content_en = parse_description(en_path) if os.path.exists(en_path) else ""
        if not content_cn and not content_en:
            stat["no_desc"] += 1
        title_cn = title_from_desc(cn_path) if os.path.exists(cn_path) else ""
        title_en = tinfo.get("title") or mmeta.get("title") or title_from_desc(en_path)

        difficulty = tinfo.get("difficulty") or mmeta.get("difficulty") or "Unknown"
        if difficulty not in ("Easy", "Medium", "Hard"):
            difficulty = {"简单": "Easy", "中等": "Medium", "困难": "Hard"}.get(difficulty, "Unknown")
        tags = mmeta.get("tags", [])
        is_hot = 1 if str(pid) in hot else 0

        db.execute(
            "INSERT INTO problems(id,title,title_cn,slug,difficulty,tags,content_cn,content_en,is_hot) VALUES(?,?,?,?,?,?,?,?,?)",
            (pid, title_en, title_cn, slug, difficulty, json.dumps(tags, ensure_ascii=False),
             content_cn, content_en, is_hot))

        sol_dir = os.path.join(data_dir, d, "solutions")
        conv = ps.load_conversions(CONV_DIR, str(pid))
        seq = 0

        # 官方题解
        off_path = os.path.join(sol_dir, "Official.md")
        if os.path.exists(off_path):
            md = open(off_path, encoding="utf-8", errors="ignore").read()
            sol = ps.parse_solution(md, True, conv.get("Official.md"))
            if sol["codes"]:
                db.execute(
                    "INSERT INTO solutions(problem_id,kind,seq,title,author,votes,votes_raw,text,codes_json) VALUES(?,?,?,?,?,?,?,?,?)",
                    (pid, "official", seq, "官方题解", "LeetCode", 0, "",
                     sol["text"], json.dumps(sol["codes"], ensure_ascii=False)))
                seq += 1
                stat["official"] += 1
                stat["dropped"] += sol["dropped"]

        # 热门题解（按票数取前 N）
        votes_map = tinfo.get("votes", {})
        pop_files = [f for f in sorted(os.listdir(sol_dir)) if re.match(r"^\d+\.md$", f)] if os.path.isdir(sol_dir) else []
        pop_files.sort(key=lambda f: -norm_votes(votes_map.get(f[:-3], "")))
        for fname in pop_files[:POPULAR_MAX]:
            md = open(os.path.join(sol_dir, fname), encoding="utf-8", errors="ignore").read()
            sol = ps.parse_solution(md, False, conv.get(fname))
            if not sol["codes"]:
                stat["dropped"] += sol["dropped"]
                continue
            v_raw = votes_map.get(fname[:-3], "")
            db.execute(
                "INSERT INTO solutions(problem_id,kind,seq,title,author,votes,votes_raw,text,codes_json) VALUES(?,?,?,?,?,?,?,?,?)",
                (pid, "popular", seq, sol["title"] or f"热门题解 {fname[:-3]}", sol["author"],
                 norm_votes(v_raw), v_raw, sol["text"], json.dumps(sol["codes"], ensure_ascii=False)))
            seq += 1
            stat["popular"] += 1
            stat["dropped"] += sol["dropped"]

        db.execute("UPDATE problems SET solution_count=? WHERE id=?", (seq, pid))
        n_ok += 1

    db.commit()
    cur = db.execute("SELECT COUNT(*) FROM problems")
    total = cur.fetchone()[0]
    cur = db.execute("SELECT COUNT(*) FROM solutions")
    sol_total = cur.fetchone()[0]
    cur = db.execute("SELECT difficulty, COUNT(*) FROM problems GROUP BY difficulty")
    diff = dict(cur.fetchall())
    db.close()
    print("problems:", total, "| solutions:", sol_total, "| stats:", stat, "| difficulty:", diff)
    print("saved:", OUT)


if __name__ == "__main__":
    sys.exit(main())
