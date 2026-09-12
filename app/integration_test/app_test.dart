import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:leetcode_offline/db.dart';
import 'package:leetcode_offline/main.dart';
import 'package:leetcode_offline/prefs.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// 桌面端集成测试：使用真实离线数据包（assets/data/leetcode.db），
/// 在真实 Windows 窗口内渲染并断言完整业务流程。
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('真实数据包端到端流程', (tester) async {
    SharedPreferences.setMockInitialValues({});
    await AppDatabase.instance.init();
    final prefs = await UserPrefs.load();
    await tester.pumpWidget(LeetcodeOfflineApp(prefs: prefs));
    await tester.pumpAndSettle(const Duration(milliseconds: 500));

    // 1. 列表加载真实数据库：2837 题，难度筛选三档都在
    expect(find.textContaining('共 2837 题'), findsOneWidget);
    expect(find.text('两数之和'), findsWidgets);

    // 2. 难度筛选：简单 → 只显示简单题
    await tester.tap(find.widgetWithText(FilterChip, '简单'));
    await tester.pumpAndSettle(const Duration(milliseconds: 500));
    expect(find.text('全部题目 · 共 710 题', findRichText: true), findsNothing);
    expect(find.textContaining('共 710 题'), findsOneWidget);

    // 3. 打开简单题（两数之和）
    await tester.tap(find.text('两数之和').first);
    await tester.pumpAndSettle(const Duration(milliseconds: 500));

    // 详情头部：题号 + 中文标题 + 题干
    expect(find.text('1. 两数之和'), findsOneWidget);
    expect(find.textContaining('给定一个整数数组'), findsOneWidget);

    // 4. 题干含约束范围（Markdown 渲染）
    expect(find.textContaining('10'), findsWidgets);

    // 5. 切到题解 tab
    await tester.tap(find.textContaining('题解（'));
    await tester.pumpAndSettle(const Duration(milliseconds: 500));

    // 官方题解 + 热门题解 至少一个，Python 代码默认可见（高亮渲染）
    expect(find.text('官方题解'), findsWidgets);
    expect(find.textContaining('def twoSum', findRichText: true), findsWidgets);

    // 6. 切换到 Go 语言（先滚动到可见）
    final goBtn = find.widgetWithText(SegmentedButton<String>, 'Go').first;
    await tester.ensureVisible(goBtn);
    await tester.pumpAndSettle(const Duration(milliseconds: 300));
    await tester.tap(goBtn);
    await tester.pumpAndSettle(const Duration(milliseconds: 500));
    expect(find.textContaining('func twoSum', findRichText: true), findsWidgets);

    // 7. 切回 Python（题解页语言切换）
    final pyBtn =
        find.widgetWithText(SegmentedButton<String>, 'Python').first;
    await tester.ensureVisible(pyBtn);
    await tester.pumpAndSettle(const Duration(milliseconds: 300));
    await tester.tap(pyBtn);
    await tester.pumpAndSettle(const Duration(milliseconds: 500));
    expect(find.textContaining('def twoSum', findRichText: true), findsWidgets);

    // 收藏标记（回到题目 tab 顶部点收藏）
    await tester.tap(find.text('题目'));
    await tester.pumpAndSettle(const Duration(milliseconds: 500));
    final favBtn = find.byIcon(Icons.star_border_rounded).first;
    await tester.ensureVisible(favBtn);
    await tester.pumpAndSettle();
    await tester.tap(favBtn);
    await tester.pumpAndSettle();
    expect(find.byIcon(Icons.star_rounded), findsWidgets);
  });

  testWidgets('宽屏双栏布局', (tester) async {
    await tester.binding.setSurfaceSize(const Size(1280, 800));
    SharedPreferences.setMockInitialValues({});
    await AppDatabase.instance.init();
    final prefs = await UserPrefs.load();
    await tester.pumpWidget(LeetcodeOfflineApp(prefs: prefs));
    await tester.pumpAndSettle(const Duration(milliseconds: 500));

    // 宽屏：左侧列表 + 右侧详情区（NavigationRail 在）
    expect(find.byType(NavigationRail), findsOneWidget);
    expect(find.textContaining('从左侧选择一道题目开始刷题'), findsOneWidget);

    await tester.tap(find.text('两数之和').first);
    await tester.pumpAndSettle(const Duration(milliseconds: 500));
    expect(find.text('1. 两数之和'), findsOneWidget);
  });

  testWidgets('搜索过滤', (tester) async {
    await tester.binding.setSurfaceSize(const Size(420, 800));
    SharedPreferences.setMockInitialValues({});
    await AppDatabase.instance.init();
    final prefs = await UserPrefs.load();
    await tester.pumpWidget(LeetcodeOfflineApp(prefs: prefs));
    await tester.pumpAndSettle(const Duration(milliseconds: 500));

    await tester.enterText(find.byType(TextField), '接雨水');
    await tester.pumpAndSettle(const Duration(milliseconds: 500));
    // 输入框内文本与列表项都会命中，用 ListTile 精确定位
    expect(find.widgetWithText(ListTile, '接雨水'), findsOneWidget);
    expect(find.text('两数之和'), findsNothing);
  });
}
