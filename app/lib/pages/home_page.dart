import 'package:flutter/material.dart';

import '../prefs.dart';
import '../widgets/problem_detail_view.dart';
import 'problem_list_page.dart';
import 'settings_page.dart';

/// 响应式主页：
/// - 宽屏（>= 900）：左侧题目列表 + 右侧详情双栏；
/// - 窄屏（手机）：底部导航 + 页面跳转。
class HomePage extends StatefulWidget {
  final UserPrefs prefs;

  const HomePage({super.key, required this.prefs});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _railIndex = 0; // 0 题库 / 1 设置
  int? _selectedId;
  int _detailKey = 0;

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(builder: (context, constraints) {
      final width = constraints.maxWidth;
      final wide = width >= 900;

      if (!wide) {
      // ---------- 移动端窄屏 ----------
      return Scaffold(
        appBar: AppBar(
          title: const Text('LeetCode 离线题库'),
          actions: [
            IconButton(
              tooltip: '设置',
              icon: const Icon(Icons.settings_outlined),
              onPressed: () => Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const SettingsPage()),
              ),
            ),
          ],
        ),
        body: _railIndex == 0
            ? ProblemListPage(
                prefs: widget.prefs,
                onTapProblem: (id) => Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (_) => Scaffold(
                      appBar: AppBar(
                        title: Text('题目 #$id'),
                        actions: [
                          IconButton(
                            tooltip: '设置',
                            icon: const Icon(Icons.settings_outlined),
                            onPressed: () => Navigator.of(context).push(
                              MaterialPageRoute(
                                  builder: (_) => const SettingsPage()),
                            ),
                          ),
                        ],
                      ),
                      body: ProblemDetailView(
                        problemId: id,
                        prefs: widget.prefs,
                      ),
                    ),
                  ),
                ),
              )
            : const SettingsPage(),
        bottomNavigationBar: NavigationBar(
          selectedIndex: _railIndex,
          onDestinationSelected: (i) => setState(() => _railIndex = i),
          destinations: const [
            NavigationDestination(
              icon: Icon(Icons.menu_book_outlined),
              selectedIcon: Icon(Icons.menu_book),
              label: '题库',
            ),
            NavigationDestination(
              icon: Icon(Icons.settings_outlined),
              selectedIcon: Icon(Icons.settings),
              label: '设置',
            ),
          ],
        ),
      );
    }

    // ---------- 桌面端宽屏双栏 ----------
    return Scaffold(
      body: Row(
        children: [
          NavigationRail(
            selectedIndex: _railIndex,
            onDestinationSelected: (i) => setState(() => _railIndex = i),
            labelType: NavigationRailLabelType.all,
            leading: const Padding(
              padding: EdgeInsets.only(top: 8, bottom: 8),
              child: Icon(Icons.code_rounded, size: 30, color: Color(0xFF3D6FF2)),
            ),
            destinations: const [
              NavigationRailDestination(
                icon: Icon(Icons.menu_book_outlined),
                selectedIcon: Icon(Icons.menu_book),
                label: Text('题库'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.settings_outlined),
                selectedIcon: Icon(Icons.settings),
                label: Text('设置'),
              ),
            ],
          ),
          const VerticalDivider(width: 1, thickness: 1),
          if (_railIndex == 0) ...[
            SizedBox(
              // 900~1000px 时收窄列表，避免挤压详情区
              width: constraints.maxWidth < 1000 ? 340 : 400,
              child: ProblemListPage(
                prefs: widget.prefs,
                onTapProblem: (id) => setState(() {
                  _selectedId = id;
                  _detailKey++;
                }),
              ),
            ),
            const VerticalDivider(width: 1, thickness: 1),
            Expanded(
              child: _selectedId == null
                  ? Center(
                      child: Text(
                        '← 从左侧选择一道题目开始刷题',
                        style: TextStyle(
                            fontSize: 15,
                            color: Theme.of(context)
                                .colorScheme
                                .onSurfaceVariant),
                      ),
                    )
                  : KeyedSubtree(
                      key: ValueKey('detail-$_detailKey'),
                      child: ProblemDetailView(
                        problemId: _selectedId!,
                        prefs: widget.prefs,
                      ),
                    ),
            ),
          ] else
            const Expanded(child: SettingsPage()),
        ],
      ),
    );
    });
  }
}
