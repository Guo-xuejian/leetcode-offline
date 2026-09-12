# -*- coding: utf-8 -*-
"""测试 LeetCode GraphQL 查询变体，找出可用的题目列表接口。"""
import json
import urllib.request

VARIANTS = [
    ("leetcode.cn categorySlug",
     "https://leetcode.cn/graphql/",
     "query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput){problemsetQuestionList: questionList(categorySlug: $categorySlug, limit: $limit, skip: $skip, filters: $filters){total: totalNum questions: data{frontendQuestionId: questionFrontendId titleSlug title difficulty isPaidOnly topicTags{name slug}}}}",
     {"categorySlug": "", "skip": 0, "limit": 3, "filters": {}}),
    ("leetcode.cn category",
     "https://leetcode.cn/graphql/",
     "query problemsetQuestionList($category: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput){questionList(category: $category, limit: $limit, skip: $skip, filters: $filters){total: totalNum questions: data{frontendQuestionId: questionFrontendId titleSlug title difficulty isPaidOnly topicTags{name slug}}}}",
     {"category": "", "skip": 0, "limit": 3, "filters": {}}),
    ("leetcode.com categorySlug",
     "https://leetcode.com/graphql/",
     "query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput){problemsetQuestionList: questionList(categorySlug: $categorySlug, limit: $limit, skip: $skip, filters: $filters){total: totalNum questions: data{frontendQuestionId: questionFrontendId titleSlug title difficulty isPaidOnly topicTags{name slug}}}}",
     {"categorySlug": "", "skip": 0, "limit": 3, "filters": {}}),
]


def post(url, query, variables):
    req = urllib.request.Request(url, data=json.dumps({"query": query, "variables": variables}).encode(),
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


for name, url, q, v in VARIANTS:
    try:
        data = post(url, q, v)
        if "errors" in data:
            print(f"[{name}] ERRORS:", json.dumps(data["errors"])[:300])
        else:
            ql = data["data"].get("problemsetQuestionList") or data["data"].get("questionList")
            print(f"[{name}] OK total={ql.get('total')} first={ql['questions'][0]['titleSlug']}")
    except Exception as e:
        print(f"[{name}] EXC: {e}")
