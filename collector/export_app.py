# -*- coding: utf-8 -*-
"""从 problems.db 导出 App 离线数据包（SQLite），写入 app/assets/data/leetcode.db。

App 端直接使用 SQLite 查询，无需在手机上解析大 JSON。
"""
import json
import os
import shutil
import sqlite3

HERE = os.path.dirname(__file__)
SRC_DB = os.path.join(HERE, "output", "problems.db")
DEST = os.path.join(HERE, "..", "app", "assets", "data", "leetcode.db")


def main():
    src = sqlite3.connect(SRC_DB)
    dst_dir = os.path.dirname(DEST)
    os.makedirs(dst_dir, exist_ok=True)
    # 用备份方式复制数据库（保证完整性）
    src.backup(sqlite3.connect(DEST))
    # 校验
    con = sqlite3.connect(DEST)
    n_prob = con.execute("select count(*) from problems").fetchone()[0]
    n_sol = con.execute("select count(*) from solutions").fetchone()[0]
    # 统计双语言覆盖
    both = 0
    for (codes,) in con.execute("select codes_json from solutions"):
        for c in json.loads(codes):
            if c.get("python") and c.get("go"):
                both += 1
    size = os.path.getsize(DEST)
    print(f"problems={n_prob} solutions={n_sol} dual_lang_groups={both}")
    print(f"saved: {os.path.normpath(DEST)} ({size/1024/1024:.1f} MB)")


if __name__ == "__main__":
    main()
