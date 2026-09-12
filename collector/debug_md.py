# -*- coding: utf-8 -*-
"""调试：检查 html2md 转换结果的异常行来源。"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import html2md

CN = os.path.join(os.path.dirname(__file__), "data", "leetcode-supercrawl-main", "data", "0001.two-sum", "description", "CN.md")
md = open(CN, encoding="utf-8").read()
out = html2md.html_to_markdown(md)
for i, ln in enumerate(out.split("\n")):
    if "****" in ln or "示例" in ln:
        print(i, repr(ln[:80]))

print("=== hr in source? ===")
print("hr" in md.lower())
