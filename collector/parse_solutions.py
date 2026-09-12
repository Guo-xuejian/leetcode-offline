# -*- coding: utf-8 -*-
"""
parse_solutions.py — 解析题解 markdown，提取 Python/Go 代码块，按解法分组。

只保留用户需要的两种语言（Python 优先，Go 同步）。
- 官方题解 Official.md：每个"方法"标题下的多语言代码块，取 Python + Golang
- 热门题解 N.md：博客式题解，取 Python/Go 代码块
- 其他语言（C/C++/Java/JS 等）代码块：丢弃；若 conversion 缓存提供对应语言则补齐
- 输出: {title, author, votes, text, codes:[{caption, python, go}]}
"""
import json
import os
import re

PY_LANGS = {"python", "python3", "py"}
GO_LANGS = {"go", "golang"}
FENCE_RE = re.compile(r"^```\s*([A-Za-z0-9+#-]*)\s*(?:\[[^\]]*\])?\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s*(.+)$")
DOLLAR_RE = re.compile(r"\$([^$]*)\$")
IMG_RE = re.compile(r"^!\[[^\]]*\]\((?!https?://)[^)]*\)\s*$")


def norm_lang(lang: str):
    return lang.strip().lower()


def split_fences(md: str):
    """把 markdown 拆成 [('text', None, None), ('code', lang, code), ...]"""
    parts = []
    lines = md.split("\n")
    i = 0
    buf = []
    while i < len(lines):
        m = FENCE_RE.match(lines[i])
        if m:
            if buf:
                parts.append(("text", None, "\n".join(buf)))
                buf = []
            lang = norm_lang(m.group(1))
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1  # 跳过结束围栏
            parts.append(("code", lang, "\n".join(code)))
        else:
            buf.append(lines[i])
            i += 1
    if buf:
        parts.append(("text", None, "\n".join(buf)))
    return parts


def clean_meta(lines):
    """去掉题解文件头部的标题行/作者行/图片行，返回 (文本行, title, author)"""
    title, author = "", ""
    out = []
    for ln in lines:
        s = ln.strip()
        if not title and s.startswith("## [") and s.endswith(")"):
            title = s[4:].rsplit("]", 1)[0].strip()
            title = re.sub(r"^\d+\.\s*", "", title)
            continue
        m = re.match(r"^作者[:：]\s*\[([^\]]+)\]", s)
        if m:
            author = m.group(1).strip()
            continue
        if IMG_RE.match(s):
            continue
        out.append(ln)
    return out, title, author


def strip_video_section(lines):
    """去掉「视频题解」小节（## 📺 视频题解 到 ### 📖 文字题解 之间）"""
    start = -1
    end = -1
    for i, ln in enumerate(lines):
        if "📺 视频题解" in ln:
            start = i
        elif "📖 文字题解" in ln and start >= 0:
            end = i
            break
    if start >= 0 and end > start:
        return lines[:start] + lines[end:]
    return lines


def strip_latex(text: str) -> str:
    return DOLLAR_RE.sub(r"\1", text)


def parse_solution(md: str, is_official: bool, conversions: list = None):
    """
    conversions: 与该文件代码块按顺序对齐的列表 [{"python":..,"go":..}, ...]，
    仅用于填充缺失语言。
    返回 {title, author, text, codes, dropped}
    """
    lines = md.split("\n")
    if is_official:
        lines = strip_video_section(lines)
    lines, title, author = clean_meta(lines)

    parts = split_fences("\n".join(lines))

    # 遍历 parts，收集文本与代码块（代码块带最近标题作为 caption）
    text_chunks = []
    caption = "解法"
    groups = []           # [{"caption", "python", "go", "other_langs"}]
    for typ, lang, content in parts:
        if typ == "text":
            # 记录标题行作为下一个代码块的 caption
            for ln in content.split("\n"):
                m = HEADING_RE.match(ln.strip())
                if m and "复杂度" not in m.group(2):
                    caption = m.group(2).strip()
            text_chunks.append(content)
        else:
            g = None
            if groups and groups[-1]["caption"] == caption:
                g = groups[-1]
            else:
                g = {"caption": caption, "python": None, "go": None, "other": []}
                groups.append(g)
            if lang in PY_LANGS:
                g["python"] = content
            elif lang in GO_LANGS:
                g["go"] = content
            else:
                g["other"].append(lang)

    # 应用人工转换缓存
    if conversions:
        for i, g in enumerate(groups):
            if i < len(conversions):
                c = conversions[i]
                if g["python"] is None and c.get("python"):
                    g["python"] = c["python"]
                if g["go"] is None and c.get("go"):
                    g["go"] = c["go"]

    # 丢弃无 Python/Go 的代码块组
    kept = []
    for g in groups:
        if g["python"] or g["go"]:
            kept.append({"caption": g["caption"], "python": g["python"], "go": g["go"]})
    dropped = len(groups) - len(kept)

    text = strip_latex("\n".join(text_chunks)).strip()
    return {"title": title, "author": author, "text": text, "codes": kept, "dropped": dropped}


def load_conversions(conversions_dir: str, problem_id: str):
    """读取 conversions/<id>.json → {filename: [ {...} ]}"""
    if not conversions_dir:
        return {}
    path = os.path.join(conversions_dir, f"{problem_id}.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)
