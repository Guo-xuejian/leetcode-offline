import 'dart:convert';

/// 题目模型（来自 SQLite problems 表）
class Problem {
  final int id;
  final String title;
  final String titleCn;
  final String slug;
  final String difficulty; // Easy / Medium / Hard
  final List<String> tags;
  final bool isHot;
  final String contentCn;
  final String contentEn;

  Problem({
    required this.id,
    required this.title,
    required this.titleCn,
    required this.slug,
    required this.difficulty,
    required this.tags,
    required this.isHot,
    required this.contentCn,
    required this.contentEn,
  });

  factory Problem.fromRow(Map<String, Object?> row) {
    List<String> tags = [];
    final rawTags = row['tags'];
    if (rawTags is String && rawTags.isNotEmpty) {
      try {
        tags = (jsonDecode(rawTags) as List).cast<String>();
      } catch (_) {}
    }
    return Problem(
      id: row['id'] as int,
      title: (row['title'] as String?) ?? '',
      titleCn: (row['title_cn'] as String?) ?? '',
      slug: (row['slug'] as String?) ?? '',
      difficulty: (row['difficulty'] as String?) ?? 'Medium',
      tags: tags,
      isHot: ((row['is_hot'] as int?) ?? 0) == 1,
      contentCn: (row['content_cn'] as String?) ?? '',
      contentEn: (row['content_en'] as String?) ?? '',
    );
  }

  String get displayTitle => titleCn.isNotEmpty ? titleCn : title;
  String get difficultyLabel => switch (difficulty) {
        'Easy' => '简单',
        'Hard' => '困难',
        _ => '中等',
      };
}

/// 代码组：同一解法的一个代码块，含 Python / Go 两版
class CodeGroup {
  final String caption;
  final String? python;
  final String? go;

  CodeGroup({required this.caption, this.python, this.go});

  factory CodeGroup.fromJson(Map<String, dynamic> json) => CodeGroup(
        caption: (json['caption'] as String?) ?? '',
        python: json['python'] as String?,
        go: json['go'] as String?,
      );

  String? codeOf(String lang) => lang == 'go' ? go : python;
  bool has(String lang) => (codeOf(lang) ?? '').isNotEmpty;
}

/// 题解（官方或热门）
class Solution {
  final String kind; // official / popular
  final int seq;
  final String title;
  final String author;
  final String votes;
  final String text;
  final List<CodeGroup> codes;

  Solution({
    required this.kind,
    required this.seq,
    required this.title,
    required this.author,
    required this.votes,
    required this.text,
    required this.codes,
  });

  factory Solution.fromRow(Map<String, Object?> row) {
    List<CodeGroup> codes = [];
    final raw = row['codes_json'];
    if (raw is String && raw.isNotEmpty) {
      try {
        codes = (jsonDecode(raw) as List)
            .map((e) => CodeGroup.fromJson(e as Map<String, dynamic>))
            .toList();
      } catch (_) {}
    }
    return Solution(
      kind: (row['kind'] as String?) ?? 'popular',
      seq: (row['seq'] as int?) ?? 0,
      title: (row['title'] as String?) ?? '',
      author: (row['author'] as String?) ?? '',
      // 真实数据包中 votes 可能是整数或字符串，统一转文本
      votes: row['votes']?.toString() ?? '',
      text: (row['text'] as String?) ?? '',
      codes: codes,
    );
  }

  String get kindLabel => kind == 'official' ? '官方题解' : '热门题解';
}

/// 统计信息
class DbStats {
  final int problems;
  final int solutions;
  final int easy;
  final int medium;
  final int hard;
  final int hot;
  final int dualGroups;

  DbStats({
    required this.problems,
    required this.solutions,
    required this.easy,
    required this.medium,
    required this.hard,
    required this.hot,
    required this.dualGroups,
  });
}
