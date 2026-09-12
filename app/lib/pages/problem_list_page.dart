import 'package:flutter/material.dart';

import '../db.dart';
import '../models.dart';
import '../prefs.dart';
import '../widgets/difficulty_badge.dart';

/// 题目列表页：搜索 + 难度切换 + Hot100 + 标签 + 收藏/进度。
class ProblemListPage extends StatefulWidget {
  final UserPrefs prefs;
  final void Function(int problemId)? onTapProblem;

  const ProblemListPage({super.key, required this.prefs, this.onTapProblem});

  @override
  State<ProblemListPage> createState() => _ProblemListPageState();
}

class _ProblemListPageState extends State<ProblemListPage> {
  final _searchController = TextEditingController();
  String _difficulty = ''; // '' | Easy | Medium | Hard
  bool _onlyHot = false;
  String? _tag;
  List<String> _tags = [];
  List<Problem>? _problems;
  bool _loading = true;
  String _filterLabel = '';

  @override
  void initState() {
    super.initState();
    _loadTags();
    _load();
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _loadTags() async {
    try {
      final tags = await AppDatabase.instance.topTags(limit: 24);
      if (!mounted) return;
      setState(() => _tags = tags);
    } catch (e) {
      // 标签加载失败不阻塞主列表
    }
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final problems = await AppDatabase.instance.queryProblems(
        search: _searchController.text,
        difficulty: _difficulty.isEmpty ? null : _difficulty,
        onlyHot: _onlyHot,
        tag: _tag,
      );
      // 收藏 / 已完成过滤在内存中完成
      final list = problems.toList();
      if (!mounted) return;
      setState(() {
        _problems = list;
        _loading = false;
        _filterLabel = _describe();
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _problems = [];
        _loading = false;
        _filterLabel = '加载失败：$e';
      });
    }
  }

  String _describe() {
    final parts = <String>[];
    if (_difficulty.isNotEmpty) parts.add('难度：${_difficultyLabel(_difficulty)}');
    if (_onlyHot) parts.add('Hot 100');
    if (_tag != null) parts.add('标签：$_tag');
    if (_searchController.text.trim().isNotEmpty) parts.add('搜索：${_searchController.text.trim()}');
    return parts.isEmpty ? '全部题目' : parts.join('  ·  ');
  }

  static String _difficultyLabel(String d) => switch (d) {
        'Easy' => '简单',
        'Hard' => '困难',
        _ => '中等',
      };

  void _apply() => _load();

  @override
  Widget build(BuildContext context) {
    final problems = _problems ?? [];
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // 搜索框
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
          child: TextField(
            controller: _searchController,
            onSubmitted: (_) => _apply(),
            onChanged: (_) => _apply(),
            decoration: InputDecoration(
              hintText: '搜索题号 / 标题 / slug…',
              prefixIcon: const Icon(Icons.search),
              suffixIcon: _searchController.text.isEmpty
                  ? null
                  : IconButton(
                      icon: const Icon(Icons.clear),
                      onPressed: () {
                        _searchController.clear();
                        _apply();
                      },
                    ),
              isDense: true,
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10),
              ),
            ),
          ),
        ),
        // 难度筛选：简单 / 中等 / 困难 可切换
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: Wrap(
            spacing: 8,
            runSpacing: 6,
            crossAxisAlignment: WrapCrossAlignment.center,
            children: [
              _filterChip('全部', _difficulty.isEmpty, () {
                setState(() => _difficulty = '');
                _apply();
              }, color: null),
              _filterChip('简单', _difficulty == 'Easy', () {
                setState(() => _difficulty = 'Easy');
                _apply();
              }, color: const Color(0xFF00B8A3)),
              _filterChip('中等', _difficulty == 'Medium', () {
                setState(() => _difficulty = 'Medium');
                _apply();
              }, color: const Color(0xFFFFB800)),
              _filterChip('困难', _difficulty == 'Hard', () {
                setState(() => _difficulty = 'Hard');
                _apply();
              }, color: const Color(0xFFFF375F)),
              FilterChip(
                label: const Text('🔥 Hot 100'),
                selected: _onlyHot,
                onSelected: (v) {
                  setState(() => _onlyHot = v);
                  _apply();
                },
                visualDensity: VisualDensity.compact,
              ),
            ],
          ),
        ),
        // 标签筛选（横向滚动）
        if (_tags.isNotEmpty)
          SizedBox(
            height: 42,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
              children: [
                for (final t in _tags)
                  Padding(
                    padding: const EdgeInsets.only(right: 6),
                    child: ChoiceChip(
                      label: Text(t),
                      selected: _tag == t,
                      visualDensity: VisualDensity.compact,
                      onSelected: (v) {
                        setState(() => _tag = v ? t : null);
                        _apply();
                      },
                    ),
                  ),
              ],
            ),
          ),
        // 结果统计
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 2, 16, 6),
          child: Text(
            '$_filterLabel · 共 ${problems.length} 题',
            style: TextStyle(
                fontSize: 12,
                color: Theme.of(context).colorScheme.onSurfaceVariant),
          ),
        ),
        const Divider(height: 1),
        // 题目列表
        Expanded(
          child: _loading
              ? const Center(child: CircularProgressIndicator())
              : problems.isEmpty
                  ? const Center(child: Text('没有符合条件的题目'))
                  : ListView.builder(
                      itemCount: problems.length,
                      itemBuilder: (context, index) {
                        final p = problems[index];
                        return _ProblemTile(
                          problem: p,
                          prefs: widget.prefs,
                          onTap: () => widget.onTapProblem?.call(p.id),
                        );
                      },
                    ),
        ),
      ],
    );
  }

  Widget _filterChip(String label, bool selected, VoidCallback onTap,
      {Color? color}) {
    return FilterChip(
      label: Text(label),
      labelStyle: TextStyle(
        color: selected ? (color ?? Theme.of(context).colorScheme.primary) : null,
        fontWeight: selected ? FontWeight.w600 : null,
      ),
      selected: selected,
      showCheckmark: false,
      visualDensity: VisualDensity.compact,
      onSelected: (_) => onTap(),
    );
  }
}

class _ProblemTile extends StatefulWidget {
  final Problem problem;
  final UserPrefs prefs;
  final VoidCallback onTap;

  const _ProblemTile(
      {required this.problem, required this.prefs, required this.onTap});

  @override
  State<_ProblemTile> createState() => _ProblemTileState();
}

class _ProblemTileState extends State<_ProblemTile> {
  @override
  Widget build(BuildContext context) {
    final p = widget.problem;
    final prefs = widget.prefs;
    final fav = prefs.favorites.contains(p.id);
    final solved = prefs.solved.contains(p.id);
    return ListTile(
      onTap: widget.onTap,
      leading: solved
          ? const Icon(Icons.check_circle_rounded,
              color: Color(0xFF00B8A3), size: 22)
          : Text(
              '${p.id}',
              style: TextStyle(
                  fontSize: 13,
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                  fontFamily: 'monospace'),
            ),
      title: Row(
        children: [
          Flexible(
            child: Text(
              p.displayTitle,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(
                  fontSize: 15, fontWeight: FontWeight.w600),
            ),
          ),
          if (p.isHot)
            const Padding(
              padding: EdgeInsets.only(left: 6),
              child: Text('🔥',
                  style: TextStyle(fontSize: 12)),
            ),
        ],
      ),
      subtitle: Padding(
        padding: const EdgeInsets.only(top: 3),
        child: Wrap(
          spacing: 6,
          runSpacing: 2,
          crossAxisAlignment: WrapCrossAlignment.center,
          children: [
            DifficultyBadge(difficulty: p.difficulty),
            for (final t in p.tags.take(3))
              Text(t,
                  style: TextStyle(
                      fontSize: 11,
                      color: Theme.of(context).colorScheme.onSurfaceVariant)),
            if (p.tags.length > 3)
              Text('+${p.tags.length - 3}',
                  style: TextStyle(
                      fontSize: 11,
                      color: Theme.of(context).colorScheme.onSurfaceVariant)),
          ],
        ),
      ),
      trailing: IconButton(
        tooltip: fav ? '取消收藏' : '收藏',
        icon: Icon(
          fav ? Icons.star_rounded : Icons.star_border_rounded,
          size: 20,
          color: fav
              ? const Color(0xFFFFB800)
              : Theme.of(context).colorScheme.onSurfaceVariant,
        ),
        onPressed: () async {
          await prefs.toggleFavorite(p.id);
          if (mounted) setState(() {});
        },
      ),
    );
  }
}
