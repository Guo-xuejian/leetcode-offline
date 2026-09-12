# -*- coding: utf-8 -*-
"""
fetch_metadata.py — 从 LeetCode 中文站 GraphQL 接口拉取题目元数据（标签、难度、题目状态）。
输出: output/metadata.json
  { slug: { "id": "1", "difficulty": "Easy", "tags": ["数组","哈希表"], "paid": false } }
"""
import json
import os
import sys
import time
import urllib.request

API = "https://leetcode.com/graphql/"
QUERY = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(categorySlug: $categorySlug, limit: $limit, skip: $skip, filters: $filters) {
    total: totalNum
    questions: data {
      frontendQuestionId: questionFrontendId
      titleSlug
      title
      difficulty
      isPaidOnly
      topicTags { name slug }
    }
  }
}
"""

PAGE = 100
OUT = os.path.join(os.path.dirname(__file__), "output", "metadata.json")


def post(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(API, data=body, headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://leetcode.com/problemset/",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    total = None
    meta = {}
    skip = 0
    retry = 0
    while total is None or skip < total:
        try:
            data = post(QUERY, {"categorySlug": "", "skip": skip, "limit": PAGE, "filters": {}})
            ql = data["data"]["problemsetQuestionList"]
            total = ql["total"]
            questions = ql["questions"]
            for q in questions:
                meta[q["titleSlug"]] = {
                    "id": q["frontendQuestionId"],
                    "title": q["title"],
                    "difficulty": q["difficulty"],
                    "paid": q["isPaidOnly"],
                    "tags": [t["name"] for t in q["topicTags"]],
                }
            skip += len(questions)
            retry = 0
            print(f"fetched {skip}/{total}", flush=True)
            time.sleep(0.6)
        except Exception as e:
            retry += 1
            print(f"error at skip={skip}: {e} retry={retry}", flush=True)
            if retry >= 6:
                raise
            time.sleep(3 + retry * 2)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print("saved", OUT, "total", len(meta))


if __name__ == "__main__":
    sys.exit(main())
