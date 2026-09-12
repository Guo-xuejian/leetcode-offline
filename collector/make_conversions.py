# -*- coding: utf-8 -*-
"""将 CONV1/CONV2/CONVPY 合并，展开为按组序号对齐的列表，写入 conversions/<pid>.json。"""
import json
import os

from conv_data_part1 import CONV1
from conv_data_part2 import CONV2
from conv_data_py import CONVPY


def merge(*dicts):
    out = {}
    for d in dicts:
        for pid, files in d.items():
            for fname, groups in files.items():
                out.setdefault(pid, {}).setdefault(fname, {})
                for idx, entry in groups.items():
                    out[pid][fname][idx] = entry
    return out


def expand(groups):
    n = max(groups) + 1 if groups else 0
    lst = [{} for _ in range(n)]
    for i, e in groups.items():
        lst[i] = e
    return lst


def main():
    conv = merge(CONV1, CONV2, CONVPY)
    outdir = os.path.join(os.path.dirname(__file__), "conversions")
    os.makedirs(outdir, exist_ok=True)
    for pid, files in sorted(conv.items()):
        data = {fname: expand(groups) for fname, groups in files.items()}
        with open(os.path.join(outdir, f"{pid}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", len(conv), "conversion files to", outdir)


if __name__ == "__main__":
    main()
