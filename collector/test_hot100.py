# -*- coding: utf-8 -*-
"""测试 leetcode.cn 题单 GraphQL 接口，尝试拉取 HOT100 题单。"""
import json, urllib.request

API = "https://leetcode.cn/graphql/"
QUERY = """
query problemListQuery($listId: String, $page: Int) {
  problemList(listId: $listId, page: $page) {
    totalNum
    currentPage
    questions {
      frontendQuestionId
      titleSlug
      translatedTitle
      difficulty
    }
  }
}
"""

req = urllib.request.Request(API, data=json.dumps({
    "query": QUERY,
    "variables": {"listId": "2cktkvj", "page": 1},
}).encode(), headers={"Content-Type": "application/json",
                      "User-Agent": "Mozilla/5.0",
                      "Referer": "https://leetcode.cn/problem-list/2cktkvj/"})
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.loads(r.read().decode())
if "errors" in data:
    print("ERRORS:", json.dumps(data["errors"], ensure_ascii=False)[:800])
else:
    pl = data["data"]["problemList"]
    print("totalNum:", pl.get("totalNum"))
    for q in pl.get("questions", []):
        print(q["frontendQuestionId"], q["difficulty"], q["titleSlug"], q.get("translatedTitle"))
