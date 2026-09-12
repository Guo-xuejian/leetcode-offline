import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leetcode_offline/db.dart';
import 'package:leetcode_offline/main.dart';
import 'package:leetcode_offline/prefs.dart';
import 'package:leetcode_offline/theme.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';

import 'db_test.dart' show createTestDb;

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUpAll(() async {
    sqfliteFfiInit();
    final db = await createTestDb();
    AppDatabase.useDatabaseForTest(db);
    SharedPreferences.setMockInitialValues({});
  });

  /// DB 查询通过真实 isolate 异步完成，需在 runAsync 中等待后渲染。
  Future<void> settleDb(WidgetTester tester) async {
    await tester.runAsync(
        () => Future<void>.delayed(const Duration(milliseconds: 100)));
    await tester.pumpAndSettle();
  }

  Future<void> pumpApp(WidgetTester tester,
      {double width = 420, double height = 800}) async {
    await tester.binding.setSurfaceSize(Size(width, height));
    themeModeNotifier.value = ThemeMode.system;
    final prefs = await UserPrefs.load();
    await tester.pumpWidget(LeetcodeOfflineApp(prefs: prefs));
    await settleDb(tester);
  }

  testWidgets('窄屏（手机）题库列表加载并显示难度', (tester) async {
    await pumpApp(tester);

    // 三道题都出现
    expect(find.text('两数之和'), findsOneWidget);
    expect(find.text('三数之和'), findsOneWidget);
    expect(find.text('接雨水'), findsOneWidget);

    // 难度筛选：简单/中等/困难三档
    expect(find.widgetWithText(FilterChip, '简单'), findsOneWidget);
    expect(find.widgetWithText(FilterChip, '中等'), findsOneWidget);
    expect(find.widgetWithText(FilterChip, '困难'), findsOneWidget);
  });

  testWidgets('难度筛选：点击“简单”只显示 Easy 题', (tester) async {
    await pumpApp(tester);

    await tester.tap(find.widgetWithText(FilterChip, '简单'));
    await settleDb(tester);

    expect(find.text('两数之和'), findsOneWidget);
    expect(find.text('三数之和'), findsNothing);
    expect(find.text('接雨水'), findsNothing);
  });

  testWidgets('搜索过滤', (tester) async {
    await pumpApp(tester);

    await tester.enterText(find.byType(TextField), '接雨');
    await settleDb(tester);

    expect(find.text('接雨水'), findsOneWidget);
    expect(find.text('两数之和'), findsNothing);
  });

  testWidgets('点击题目进入详情，题解页可切换 Go/Python', (tester) async {
    await pumpApp(tester);

    await tester.tap(find.text('两数之和'));
    await settleDb(tester);

    // 详情页：题目 tab 渲染题干（头部含题号）
    expect(find.text('1. 两数之和'), findsOneWidget);
    expect(find.textContaining('返回两数之和'), findsOneWidget);
    expect(find.text('题解（2）'), findsOneWidget);

    // 切到题解 tab
    await tester.tap(find.text('题解（2）'));
    await settleDb(tester);

    expect(find.text('官方题解'), findsOneWidget);
    expect(find.text('方法一：暴力枚举'), findsOneWidget);

    // 默认语言 Python（优先）：能看到 Python 代码（官方+热门共 2 个代码块）
    expect(find.textContaining('def twoSum', findRichText: true), findsWidgets);

    // 切换到 Go：官方题解的第一个代码组
    await tester.tap(find.widgetWithText(SegmentedButton<String>, 'Go').first);
    await settleDb(tester);
    expect(find.textContaining('func twoSum', findRichText: true), findsWidgets);
  });

  testWidgets('热门题解与点赞数展示', (tester) async {
    await pumpApp(tester);

    await tester.tap(find.text('两数之和'));
    await settleDb(tester);
    await tester.tap(find.text('题解（2）'));
    await settleDb(tester);

    expect(find.textContaining('2.1k'), findsOneWidget);
    expect(find.text('哈希表一次遍历'), findsOneWidget);
  });

  testWidgets('主题切换：设置页切换深色/浅色并持久化', (tester) async {
    await pumpApp(tester);

    // 窄屏底部导航进入设置
    await tester.tap(find.text('设置'));
    await settleDb(tester);

    // 默认跟随系统
    expect(themeModeNotifier.value, ThemeMode.system);

    // 切深色：立即生效（MaterialApp 重建为 dark 主题）
    await tester.tap(find.text('深色'));
    await settleDb(tester);
    expect(themeModeNotifier.value, ThemeMode.dark);

    // 切浅色
    await tester.tap(find.text('浅色'));
    await settleDb(tester);
    expect(themeModeNotifier.value, ThemeMode.light);
  });
}
