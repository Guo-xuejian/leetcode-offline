# -*- coding: utf-8 -*-
"""校验 conversions 缓存是否完整覆盖 todo.txt 中的全部转换任务。"""
import json
import os
import sys

HERE = os.path.dirname(__file__)
CONV_DIR = os.path.join(HERE, "conversions")
TODO = os.path.join(HERE, "output", "todo.txt")


def main():
    problems = {}
    for line in open(TODO, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("==="):
            continue
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        pid, fname, idx, lang = parts[0], parts[1], int(parts[2]), parts[3].lower()
        lang = "python" if lang == "py" else lang
        problems.setdefault(pid, []).append((fname, idx, lang))

    ok = 0
    missing = []
    for pid in sorted(problems):
        path = os.path.join(CONV_DIR, f"{pid}.json")
        if not os.path.exists(path):
            for fname, idx, lang in problems[pid]:
                missing.append(f"{pid}/{fname}#{idx} {lang}: 文件缺失")
            continue
        data = json.load(open(path, encoding="utf-8"))
        for fname, idx, lang in problems[pid]:
            if fname not in data:
                missing.append(f"{pid}/{fname}#{idx} {lang}: 缺少文件键")
                continue
            lst = data[fname]
            if idx >= len(lst):
                missing.append(f"{pid}/{fname}#{idx} {lang}: 列表长度 {len(lst)} 不足")
                continue
            entry = lst[idx]
            if not entry.get(lang):
                missing.append(f"{pid}/{fname}#{idx} {lang}: 缺少 {lang} 字段")
                continue
            ok += 1

    total = sum(len(v) for v in problems.values())
    print(f"todo 条目总数: {total}")
    print(f"覆盖: {ok}  缺失: {len(missing)}")
    for m in missing:
        print("MISSING:", m)
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
