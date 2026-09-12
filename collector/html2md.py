# -*- coding: utf-8 -*-
"""
html2md.py — 力扣题干 HTML → Markdown 转换器（纯标准库）。

处理: p/div/h1-h6/pre/code/strong/b/em/i/ul/ol/li/a/br/sup/sub/table/img
- <pre> → ```text 代码块
- <code> → `内联代码`
- <sup> → Unicode 上标（10<sup>4</sup> → 10⁴）
- 图片丢弃（离线场景）
"""
from html.parser import HTMLParser

SUP_TABLE = str.maketrans("0123456789+-=()ni", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱ")
SUB_TABLE = str.maketrans("0123456789+-=()", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎")


class Html2Md(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []          # 输出的行/块列表
        self.cur = []          # 当前行缓冲
        self.in_pre = False
        self.pre_lines = []
        self.list_stack = []   # ("ul"|"ol", index)
        self.in_li = False
        self.table = None      # 表格收集
        self.href = None
        self.sup = False
        self.sub = False

    # ---------- 工具 ----------
    def flush_line(self, force=True):
        if self.cur:
            text = "".join(self.cur).strip()
            if text:
                self.out.append(text)
            self.cur = []
        elif force and self.out and self.out[-1] != "":
            self.out.append("")
        return

    def emit(self, s):
        self.cur.append(s)

    # ---------- 标签 ----------
    def handle_starttag(self, tag, attrs):
        if self.in_pre and tag != "pre":
            return  # pre 内忽略所有嵌套标签，只收文本
        attrs = dict(attrs)
        if tag in ("p", "div"):
            self.flush_line()
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.flush_line()
            self.emit("#" * int(tag[1]) + " ")
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag == "code":
            if not self.in_pre:
                self.emit("`")
        elif tag == "pre":
            self.flush_line()
            self.in_pre = True
            self.pre_lines = []
        elif tag == "br":
            self.emit("  \n")
        elif tag == "ul":
            self.flush_line()
            self.list_stack.append(("ul", 0))
        elif tag == "ol":
            self.flush_line()
            self.list_stack.append(("ol", 0))
        elif tag == "li":
            if self.in_li:
                self.flush_line()
            self.in_li = True
            kind, idx = self.list_stack[-1] if self.list_stack else ("ul", 0)
            if kind == "ol":
                idx += 1
                self.list_stack[-1] = (kind, idx)
                self.emit(f"{idx}. ")
            else:
                self.emit("- ")
        elif tag == "a":
            self.href = attrs.get("href", "")
            self.emit("[")
        elif tag == "sup":
            self.sup = True
        elif tag == "sub":
            self.sub = True
        elif tag == "table":
            self.flush_line()
            self.table = []
        elif tag in ("tr",):
            if self.table is not None:
                self.table.append([])
        elif tag in ("td", "th"):
            if self.table is not None and self.table:
                self.flush_line()
                # 行缓冲并入当前行
                text = "".join(self.cur).strip()
                self.cur = []
                self.table[-1].append(text)
        elif tag == "img":
            alt = attrs.get("alt", "").strip()
            if alt:
                self.emit(f"[图片：{alt}]")
        # span/em 等内联标签直接透传

    def handle_endtag(self, tag):
        if self.in_pre and tag != "pre":
            return
        if tag in ("p", "div"):
            self.flush_line()
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.flush_line()
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag == "code":
            if not self.in_pre:
                self.emit("`")
        elif tag == "pre":
            self.flush_line()
            code = "\n".join(self.pre_lines)
            code = code.strip("\n")
            self.out.append("```text")
            self.out.append(code)
            self.out.append("```")
            self.out.append("")
            self.in_pre = False
        elif tag == "ul":
            self.flush_line()
            if self.list_stack:
                self.list_stack.pop()
        elif tag == "ol":
            self.flush_line()
            if self.list_stack:
                self.list_stack.pop()
        elif tag == "li":
            self.flush_line()
            self.in_li = False
        elif tag == "a":
            self.emit("]")
            if self.href:
                self.emit(f"({self.href})")
                self.href = None
        elif tag == "sup":
            self.sup = False
        elif tag == "sub":
            self.sub = False
        elif tag == "table":
            self.flush_line()
            if self.table:
                rows = [r for r in self.table if r]
                if rows:
                    widths = max(len(r) for r in rows)
                    self.out.append("| " + " | ".join((rows[0] + [""] * widths)[:widths]) + " |")
                    self.out.append("| " + " | ".join(["---"] * widths) + " |")
                    for r in rows[1:]:
                        self.out.append("| " + " | ".join((r + [""] * widths)[:widths]) + " |")
                    self.out.append("")
            self.table = None

    def handle_data(self, data):
        if self.in_pre:
            self.pre_lines.append(data)
            return
        if self.sup:
            data = data.translate(SUP_TABLE)
        elif self.sub:
            data = data.translate(SUB_TABLE)
        self.emit(data)

    # ---------- 收尾 ----------
    def finish(self):
        self.flush_line()
        text = "\n".join(self.out)
        # 压缩多余空行
        while "\n\n\n" in text:
            text = text.replace("\n\n\n", "\n\n")
        return text.strip()


def html_to_markdown(html: str) -> str:
    if not html or not html.strip():
        return ""
    p = Html2Md()
    try:
        p.feed(html)
        return p.finish()
    except Exception:
        # 失败时退回纯文本
        import re
        txt = re.sub(r"<[^>]+>", "", html)
        return txt.strip()
