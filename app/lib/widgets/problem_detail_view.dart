import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';

import '../db.dart';
import '../models.dart';
import '../prefs.dart';
import '../widgets/code_viewer.dart';
import '../widgets/difficulty_badge.dart';

/// 题目详情 + 题解查看（宽屏双栏的右栏 / 窄屏详情页共用）。
class ProblemDetailView extends StatefulWidget {
  final int problemId;
  final UserPrefs prefs;

  const ProblemDetailView(
      {super.key, required this.problemId, required this.prefs});

  @override
  State<ProblemDetailView> createState() => _ProblemDetailViewState();
}

class _ProblemDetailViewState extends State<ProblemDetailView>
    with SingleTickerProviderStateMixin {
  late TabController _tab;
  Problem? _problem;
  List<Solution>? _solutions;
  bool _loading = true;
  String _descLang = 'cn'; // cn | en

  @override
  void initState() {
    super.initState();
    _tab = TabController(length: 2, vsync: this);
    _load();
  }

  @override
  void didUpdateWidget(covariant ProblemDetailView oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.problemId != widget.problemId) {
      _load();
    }
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    final problem = await AppDatabase.instance.getProblem(widget.problemId);
    final solutions =
        await AppDatabase.instance.loadSolutions(widget.problemId);
    if (!mounted) return;
    setState(() {
      _problem = problem;
      _solutions = solutions;
      _loading = false;
      _descLang = 'cn';
      _tab.index = 0;
    });
  }

  @override
  void dispose() {
    _tab.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Center(child: CircularProgressIndicator());
    }
    final p = _problem;
    if (p == null) {
      return const Center(child: Text('题目不存在'));
    }
    final isFavorite = widget.prefs.favorites.contains(p.id);
    final isSolved = widget.prefs.solved.contains(p.id);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // 头部信息
        Container(
          padding: const EdgeInsets.fromLTRB(20, 16, 12, 8),
          decoration: BoxDecoration(
            border: Border(
                bottom: BorderSide(
                    color: Theme.of(context).colorScheme.outlineVariant)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '${p.id}. ${p.displayTitle}',
                          style: const TextStyle(
                              fontSize: 20, fontWeight: FontWeight.w700),
                        ),
                        if (p.titleCn.isNotEmpty && p.titleCn != p.title)
                          Padding(
                            padding: const EdgeInsets.only(top: 2),
                            child: Text(
                              p.title,
                              style: TextStyle(
                                  fontSize: 13,
                                  color: Theme.of(context)
                                      .colorScheme
                                      .onSurfaceVariant),
                            ),
                          ),
                      ],
                    ),
                  ),
                  IconButton(
                    tooltip: isFavorite ? '取消收藏' : '收藏',
                    icon: Icon(
                      isFavorite
                          ? Icons.star_rounded
                          : Icons.star_border_rounded,
                      color: isFavorite
                          ? const Color(0xFFFFB800)
                          : Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                    onPressed: () async {
                      await widget.prefs.toggleFavorite(p.id);
                      setState(() {});
                    },
                  ),
                  IconButton(
                    tooltip: isSolved ? '标记未完成' : '标记已完成',
                    icon: Icon(
                      isSolved
                          ? Icons.check_circle_rounded
                          : Icons.radio_button_unchecked,
                      color: isSolved
                          ? const Color(0xFF00B8A3)
                          : Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                    onPressed: () async {
                      await widget.prefs.toggleSolved(p.id);
                      setState(() {});
                    },
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Wrap(
                spacing: 8,
                runSpacing: 6,
                crossAxisAlignment: WrapCrossAlignment.center,
                children: [
                  DifficultyBadge(difficulty: p.difficulty),
                  if (p.isHot)
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 2),
                      decoration: BoxDecoration(
                        color: const Color(0xFFFF375F).withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(6),
                        border: Border.all(
                            color: const Color(0xFFFF375F)
                                .withValues(alpha: 0.5)),
                      ),
                      child: const Text('🔥 Hot 100',
                          style: TextStyle(
                              fontSize: 12,
                              color: Color(0xFFFF375F),
                              fontWeight: FontWeight.w600)),
                    ),
                  ...p.tags.map(
                    (t) => Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 2),
                      decoration: BoxDecoration(
                        color: Colors.blueGrey.withValues(alpha: 0.08),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text(t,
                          style: const TextStyle(
                              fontSize: 12, color: Colors.blueGrey)),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        // 选项卡：题目 / 题解
        TabBar(
          controller: _tab,
          tabs: [
            const Tab(text: '题目'),
            Tab(text: '题解（${_solutions?.length ?? 0}）'),
          ],
          onTap: (_) => setState(() {}),
        ),
        Expanded(
          child: TabBarView(
            controller: _tab,
            children: [
              _buildDescriptionTab(p),
              _buildSolutionsTab(p),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildDescriptionTab(Problem p) {
    final content = _descLang == 'cn' ? p.contentCn : p.contentEn;
    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 12, 20, 40),
      children: [
        Row(
          children: [
            const Text('题干语言：', style: TextStyle(fontSize: 13)),
            SegmentedButton<String>(
              showSelectedIcon: false,
              style: const ButtonStyle(
                  visualDensity: VisualDensity.compact,
                  tapTargetSize: MaterialTapTargetSize.shrinkWrap),
              segments: const [
                ButtonSegment(value: 'cn', label: Text('中文')),
                ButtonSegment(value: 'en', label: Text('English')),
              ],
              selected: {_descLang},
              onSelectionChanged: (s) => setState(() => _descLang = s.first),
            ),
          ],
        ),
        const SizedBox(height: 8),
        MarkdownBody(
          data: content.isEmpty ? '（无题干内容）' : content,
          selectable: true,
          styleSheet: MarkdownStyleSheet.fromTheme(Theme.of(context)).copyWith(
            p: const TextStyle(fontSize: 14.5, height: 1.6),
            code: TextStyle(
              fontFamily: 'monospace',
              fontSize: 13,
              backgroundColor:
                  Theme.of(context).colorScheme.surfaceContainerHighest,
            ),
            codeblockDecoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
              borderRadius: BorderRadius.circular(6),
              border: Border.all(
                  color: Theme.of(context).colorScheme.outlineVariant),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSolutionsTab(Problem p) {
    final solutions = _solutions ?? [];
    if (solutions.isEmpty) {
      return const Center(child: Text('该题暂无题解'));
    }
    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 12, 20, 40),
      children: [
        for (final s in solutions) _SolutionCard(solution: s, prefs: widget.prefs),
        if (solutions.isNotEmpty) const SizedBox(height: 8),
      ],
    );
  }
}

class _SolutionCard extends StatefulWidget {
  final Solution solution;
  final UserPrefs prefs;

  const _SolutionCard({required this.solution, required this.prefs});

  @override
  State<_SolutionCard> createState() => _SolutionCardState();
}

class _SolutionCardState extends State<_SolutionCard> {
  /// 每个代码组当前选择的语言（默认跟随全局偏好，优先 Python）
  final Map<int, String> _langs = {};

  @override
  void initState() {
    super.initState();
    final pref = widget.prefs.lang;
    for (var i = 0; i < widget.solution.codes.length; i++) {
      final c = widget.solution.codes[i];
      _langs[i] = c.has(pref)
          ? pref
          : (c.has('go') ? 'go' : (c.has('python') ? 'python' : pref));
    }
  }

  @override
  Widget build(BuildContext context) {
    final s = widget.solution;
    final codeCount = s.codes.length;
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
        side: BorderSide(color: Theme.of(context).colorScheme.outlineVariant),
      ),
      child: Padding(
        padding: const EdgeInsets.fromLTRB(16, 14, 16, 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                  decoration: BoxDecoration(
                    color: s.kind == 'official'
                        ? const Color(0xFF3D6FF2).withValues(alpha: 0.1)
                        : const Color(0xFF7C4DFF).withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    s.kindLabel,
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                      color: s.kind == 'official'
                          ? const Color(0xFF3D6FF2)
                          : const Color(0xFF7C4DFF),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    s.title,
                    style: const TextStyle(
                        fontSize: 16, fontWeight: FontWeight.w700),
                  ),
                ),
              ],
            ),
            if (s.author.isNotEmpty || s.votes.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 4, bottom: 4),
                child: Text(
                  [
                    if (s.author.isNotEmpty) '作者：${s.author}',
                    if (s.votes.isNotEmpty) '👍 ${s.votes}',
                  ].join('  ·  '),
                  style: TextStyle(
                      fontSize: 12,
                      color: Theme.of(context).colorScheme.onSurfaceVariant),
                ),
              ),
            if (s.text.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 6),
                child: MarkdownBody(
                  data: s.text,
                  selectable: true,
                  styleSheet:
                      MarkdownStyleSheet.fromTheme(Theme.of(context)).copyWith(
                    p: const TextStyle(fontSize: 14, height: 1.6),
                    code: TextStyle(
                      fontFamily: 'monospace',
                      fontSize: 13,
                      backgroundColor:
                          Theme.of(context).colorScheme.surfaceContainerHighest,
                    ),
                  ),
                ),
              ),
            if (codeCount > 0) ...[
              const SizedBox(height: 12),
              for (var i = 0; i < codeCount; i++) _buildCodeGroup(i),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildCodeGroup(int i) {
    final c = widget.solution.codes[i];
    final lang = _langs[i] ?? 'python';
    final code = c.codeOf(lang) ?? '';
    final hasPy = c.has('python');
    final hasGo = c.has('go');
    return Padding(
      padding: const EdgeInsets.only(bottom: 14),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (c.caption.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(bottom: 6),
              child: Text(c.caption,
                  style: TextStyle(
                      fontSize: 13.5,
                      fontWeight: FontWeight.w600,
                      color: Theme.of(context).colorScheme.onSurface)),
            ),
          if (hasPy || hasGo) ...[
            // 语言切换（Python / Go）
            Row(
              children: [
                SegmentedButton<String>(
                  showSelectedIcon: false,
                  style: const ButtonStyle(
                      visualDensity: VisualDensity.compact,
                      tapTargetSize: MaterialTapTargetSize.shrinkWrap),
                  segments: [
                    if (hasPy)
                      const ButtonSegment(value: 'python', label: Text('Python')),
                    if (hasGo)
                      const ButtonSegment(value: 'go', label: Text('Go')),
                  ],
                  selected: {lang},
                  onSelectionChanged: (s) =>
                      setState(() => _langs[i] = s.first),
                ),
                const SizedBox(width: 8),
                if (!c.has(lang))
                  Expanded(
                    child: Text(
                      '当前语言不可用，已自动切换到可用版本',
                      style: TextStyle(
                          fontSize: 12, color: Colors.orange[800]),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 8),
            CodeViewer(code: code, language: lang),
          ] else ...[
            const SizedBox(height: 4),
            Text('（该解法暂无 Go / Python 代码）',
                style: TextStyle(
                    fontSize: 12,
                    color: Theme.of(context).colorScheme.onSurfaceVariant)),
          ],
        ],
      ),
    );
  }
}
