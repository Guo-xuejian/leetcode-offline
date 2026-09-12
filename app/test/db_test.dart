import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:leetcode_offline/db.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';

/// 按真实 schema 创建内存数据库并灌入样例数据。
/// 使用 NoIsolate 工厂：SQLite 在当前 isolate 直接执行，
/// 避免测试的 FakeAsync 时钟与真实 isolate 通信的时序竞争。
Future<Database> createTestDb() async {
  sqfliteFfiInit();
  final db = await databaseFactoryFfiNoIsolate.openDatabase(
    inMemoryDatabasePath,
    options: OpenDatabaseOptions(
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE problems (
            id INTEGER PRIMARY KEY,
            title TEXT, title_cn TEXT, slug TEXT,
            difficulty TEXT, tags TEXT, is_hot INTEGER,
            content_cn TEXT, content_en TEXT
          )
        ''');
        await db.execute('''
          CREATE TABLE solutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id INTEGER, kind TEXT, seq INTEGER,
            title TEXT, author TEXT, votes TEXT,
            text TEXT, codes_json TEXT
          )
        ''');
      },
    ),
  );

  Future<void> addProblem(
    int id,
    String title,
    String titleCn,
    String slug,
    String difficulty,
    List<String> tags,
    int hot,
  ) async {
    await db.insert('problems', {
      'id': id,
      'title': title,
      'title_cn': titleCn,
      'slug': slug,
      'difficulty': difficulty,
      'tags': jsonEncode(tags),
      'is_hot': hot,
      'content_cn': '# 题目\n\n返回两数之和。\n\n- 1 <= nums.length <= 10^4',
      'content_en': '# Title\n\ncontent',
    });
  }

  await addProblem(1, 'Two Sum', '两数之和', 'two-sum', 'Easy',
      ['数组', '哈希表'], 1);
  await addProblem(15, '3Sum', '三数之和', '3sum', 'Medium', ['数组'], 1);
  await addProblem(42, 'Trapping Rain Water', '接雨水', 'trapping-rain-water',
      'Hard', ['数组'], 1);

  await db.insert('solutions', {
    'problem_id': 1,
    'kind': 'official',
    'seq': 0,
    'title': '方法一：暴力枚举',
    'author': 'LeetCode',
    'votes': '',
    'text': '遍历数组，寻找两数之和。',
    'codes_json': jsonEncode([
      {
        'caption': 'Python',
        'python': 'class Solution:\n    def twoSum(self, nums, target):\n        for i in range(len(nums)):\n            for j in range(i + 1, len(nums)):\n                if nums[i] + nums[j] == target:\n                    return [i, j]\n        return []',
        'go': 'func twoSum(nums []int, target int) []int {\n    for i := 0; i < len(nums); i++ {\n        for j := i + 1; j < len(nums); j++ {\n            if nums[i]+nums[j] == target {\n                return []int{i, j}\n            }\n        }\n    }\n    return nil\n}',
      },
    ]),
  });
  await db.insert('solutions', {
    'problem_id': 1,
    'kind': 'popular',
    'seq': 0,
    'title': '哈希表一次遍历',
    'author': 'windliang',
    'votes': '2.1k',
    'text': '使用哈希表存储已遍历元素。',
    'codes_json': jsonEncode([
      {
        'caption': 'Python',
        'python': 'class Solution:\n    def twoSum(self, nums, target):\n        m = {}\n        for i, x in enumerate(nums):\n            if target - x in m:\n                return [m[target - x], i]\n            m[x] = i\n        return []',
        'go': 'func twoSum(nums []int, target int) []int {\n    m := make(map[int]int)\n    for i, x := range nums {\n        if j, ok := m[target-x]; ok {\n            return []int{j, i}\n        }\n        m[x] = i\n    }\n    return nil\n}',
      },
    ]),
  });

  return db;
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late Database db;

  setUpAll(() async {
    db = await createTestDb();
    AppDatabase.useDatabaseForTest(db);
  });

  test('统计数据正确', () async {
    final stats = await AppDatabase.instance.stats();
    expect(stats.problems, 3);
    expect(stats.easy, 1);
    expect(stats.medium, 1);
    expect(stats.hard, 1);
    expect(stats.hot, 3);
    expect(stats.dualGroups, 2);
  });

  test('按难度过滤', () async {
    final easy = await AppDatabase.instance
        .queryProblems(difficulty: 'Easy');
    expect(easy.length, 1);
    expect(easy.first.id, 1);
    expect(easy.first.difficultyLabel, '简单');

    final hard = await AppDatabase.instance
        .queryProblems(difficulty: 'Hard');
    expect(hard.length, 1);
    expect(hard.first.id, 42);
  });

  test('搜索（中英文标题 / slug）', () async {
    expect((await AppDatabase.instance.queryProblems(search: 'two')).length, 1);
    expect((await AppDatabase.instance.queryProblems(search: '两数')).length, 1);
    expect((await AppDatabase.instance.queryProblems(search: '3sum')).length, 1);
    expect((await AppDatabase.instance.queryProblems(search: '不存在xyz')).length, 0);
  });

  test('标签与 Hot100 过滤', () async {
    final tag = await AppDatabase.instance.queryProblems(tag: '哈希表');
    expect(tag.length, 1);
    expect(tag.first.id, 1);

    final hot = await AppDatabase.instance.queryProblems(onlyHot: true);
    expect(hot.length, 3);
  });

  test('题解解析（双语言代码组）', () async {
    final solutions = await AppDatabase.instance.loadSolutions(1);
    expect(solutions.length, 2);
    expect(solutions.first.kind, 'official');
    expect(solutions.first.kindLabel, '官方题解');

    final group = solutions.first.codes.first;
    expect(group.has('python'), true);
    expect(group.has('go'), true);
    expect(group.codeOf('python'), contains('def twoSum'));
    expect(group.codeOf('go'), contains('func twoSum'));

    final popular = solutions[1];
    expect(popular.votes, '2.1k');
  });

  test('无题解题目返回空列表', () async {
    final solutions = await AppDatabase.instance.loadSolutions(42);
    expect(solutions, isEmpty);
  });
}
