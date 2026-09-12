# -*- coding: utf-8 -*-
"""从已抓取的 HTML 解析力扣「热题 HOT 100」题单，输出 output/hot100.json。"""
import json
import os
import re
import sys
import urllib.request

URL = "https://pcs2.roj.ac.cn/problem-sets/leetcode-hot-100"
OUT = os.path.join(os.path.dirname(__file__), "output", "hot100.json")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")


def main():
    html = fetch(URL)
    pat = re.compile(r'<a href="https://leetcode\.cn/problems/([^"/]+)/">(\d+)\.\s*([^<]+)</a> · ([^<]+)')
    items = pat.findall(html)
    seen = set()
    out = []
    for slug, num, title, diff in items:
        if num in seen:
            continue
        seen.add(num)
        out.append({"id": int(num), "slug": slug, "title_cn": title.strip(), "difficulty": diff})
    out.sort(key=lambda x: x["id"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("count:", len(out), "saved:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
