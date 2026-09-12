import 'dart:convert';
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:sqflite/sqflite.dart' as sqf;
import 'package:sqflite_common_ffi/sqflite_ffi.dart';

import 'models.dart';

/// 应用数据库管理：打开/导入/查询离线数据包（SQLite）。
class AppDatabase {
  AppDatabase._();

  static AppDatabase instance = AppDatabase._();

  /// 测试用：注入已打开的数据库实例（跳过文件/平台逻辑）
  @visibleForTesting
  static void useDatabaseForTest(Database db) {
    final inst = AppDatabase._();
    inst._db = db;
    inst._currentPath = ':memory:';
    instance = inst;
  }

  Database? _db;
  String? _currentPath;

  static bool get isDesktop =>
      !kIsWeb &&
      (Platform.isWindows || Platform.isLinux || Platform.isMacOS);

  Future<Database> _openFile(String path) async {
    if (isDesktop) {
      return databaseFactoryFfi.openDatabase(path);
    }
    return sqf.openDatabase(path);
  }

  /// 应用文档目录下的数据库路径
  Future<String> get _dbDir async {
    final dir = await getApplicationSupportDirectory();
    await dir.create(recursive: true);
    return dir.path;
  }

  /// 数据包来源：优先使用用户导入的文件，否则使用内置 asset。
  Future<String> _resolveSource() async {
    final dir = await _dbDir;
    final imported = p.join(dir, 'leetcode_imported.db');
    if (await File(imported).exists()) {
      return imported;
    }
    return 'assets/data/leetcode.db'; // asset 引用（内部使用）
  }

  Future<void> _copyAssetTo(String dest) async {
    final data = await rootBundle.load('assets/data/leetcode.db');
    final file = File(dest);
    await file.writeAsBytes(
      data.buffer.asUint8List(data.offsetInBytes, data.lengthInBytes),
      flush: true,
    );
  }

  /// 初始化：首次启动把内置数据包复制到应用目录并打开。
  Future<void> init() async {
    if (_db != null) return;
    if (isDesktop) sqfliteFfiInit();
    final source = await _resolveSource();
    if (source.startsWith('assets/')) {
      final dir = await _dbDir;
      final dest = p.join(dir, 'leetcode_bundled.db');
      if (!await File(dest).exists()) {
        await _copyAssetTo(dest);
      }
      _currentPath = dest;
    } else {
      _currentPath = source;
    }
    _db = await _openFile(_currentPath!);
  }

  Database get db {
    final d = _db;
    if (d == null) {
      throw StateError('AppDatabase 尚未初始化，请先调用 init()');
    }
    return d;
  }

  /// 导入用户提供的数据包文件（.db），替换当前数据。
  Future<void> importFromFile(String filePath) async {
    final dir = await _dbDir;
    final dest = p.join(dir, 'leetcode_imported.db');
    await File(filePath).copy(dest);
    await _db?.close();
    _db = null;
    await init();
  }

  /// 恢复为内置数据包。
  Future<void> resetToBundled() async {
    final dir = await _dbDir;
    final imported = p.join(dir, 'leetcode_imported.db');
    if (await File(imported).exists()) {
      await File(imported).delete();
    }
    await _db?.close();
    _db = null;
    await init();
  }

  Future<String?> importedInfo() async {
    final dir = await _dbDir;
    final imported = p.join(dir, 'leetcode_imported.db');
    if (await File(imported).exists()) {
      final f = File(imported);
      final size = await f.length();
      return '自定义数据包（${_fmtSize(size)}）';
    }
    return '内置数据包';
  }

  static String _fmtSize(int bytes) {
    if (bytes >= 1024 * 1024) return '${(bytes / 1024 / 1024).toStringAsFixed(1)} MB';
    return '${(bytes / 1024).toStringAsFixed(0)} KB';
  }

  // ---------------- 查询 ----------------

  static const _problemCols = 'id, title, title_cn, slug, difficulty, tags, '
      'is_hot, content_cn, content_en';

  /// 题目列表查询：支持搜索 / 难度 / Hot100 / 标签过滤。
  Future<List<Problem>> queryProblems({
    String search = '',
    String? difficulty,
    bool onlyHot = false,
    String? tag,
  }) async {
    final where = <String>[];
    final args = <Object?>[];
    final s = search.trim();
    if (s.isNotEmpty) {
      where.add('(title LIKE ? OR title_cn LIKE ? OR slug LIKE ?)');
      final like = '%$s%';
      args.addAll([like, like, like]);
    }
    if (difficulty != null && difficulty.isNotEmpty) {
      where.add('difficulty = ?');
      args.add(difficulty);
    }
    if (onlyHot) {
      where.add('is_hot = 1');
    }
    if (tag != null && tag.isNotEmpty) {
      where.add("tags LIKE ?");
      args.add('%${jsonEncode(tag)}%');
    }
    final sql = 'SELECT $_problemCols FROM problems'
        '${where.isEmpty ? '' : ' WHERE ${where.join(' AND ')}'}'
        ' ORDER BY id';
    final rows = await db.rawQuery(sql, args);
    return rows.map(Problem.fromRow).toList();
  }

  Future<Problem?> getProblem(int id) async {
    final rows = await db.query(
      'problems',
      columns: _problemCols.split(', '),
      where: 'id = ?',
      whereArgs: [id],
      limit: 1,
    );
    if (rows.isEmpty) return null;
    return Problem.fromRow(rows.first);
  }

  /// 按题目加载题解（官方在前，热门按 seq 排序）。
  Future<List<Solution>> loadSolutions(int problemId) async {
    final rows = await db.query(
      'solutions',
      columns: ['kind', 'seq', 'title', 'author', 'votes', 'text', 'codes_json'],
      where: 'problem_id = ?',
      whereArgs: [problemId],
      orderBy: "CASE kind WHEN 'official' THEN 0 ELSE 1 END, seq",
    );
    return rows.map(Solution.fromRow).toList();
  }

  /// 常用标签（按出现次数取前 N）。
  Future<List<String>> topTags({int limit = 20}) async {
    final rows = await db
        .rawQuery("SELECT tags FROM problems WHERE tags IS NOT NULL AND tags != ''");
    final counter = <String, int>{};
    for (final row in rows) {
      final raw = row['tags'] as String?;
      if (raw == null || raw.isEmpty) continue;
      try {
        for (final t in (jsonDecode(raw) as List).cast<String>()) {
          counter[t] = (counter[t] ?? 0) + 1;
        }
      } catch (_) {}
    }
    final sorted = counter.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    return sorted.take(limit).map((e) => e.key).toList();
  }

  Future<DbStats> stats() async {
    final p1 = db.rawQuery(
        'SELECT COUNT(*) c, '
        "SUM(CASE WHEN difficulty = 'Easy' THEN 1 ELSE 0 END) e, "
        "SUM(CASE WHEN difficulty = 'Medium' THEN 1 ELSE 0 END) m, "
        "SUM(CASE WHEN difficulty = 'Hard' THEN 1 ELSE 0 END) h, "
        'SUM(is_hot) hot FROM problems');
    final p2 = db.rawQuery('SELECT COUNT(*) c FROM solutions');
    final p3 = db.rawQuery('SELECT codes_json FROM solutions');
    final r1 = (await p1).first;
    final r2 = (await p2).first;
    var dual = 0;
    for (final row in await p3) {
      final raw = row['codes_json'] as String?;
      if (raw == null || raw.isEmpty) continue;
      try {
        for (final c in (jsonDecode(raw) as List).cast<Map<String, dynamic>>()) {
          if ((c['python'] as String? ?? '').isNotEmpty &&
              (c['go'] as String? ?? '').isNotEmpty) {
            dual++;
          }
        }
      } catch (_) {}
    }
    return DbStats(
      problems: r1['c'] as int,
      solutions: r2['c'] as int,
      easy: (r1['e'] as int?) ?? 0,
      medium: (r1['m'] as int?) ?? 0,
      hard: (r1['h'] as int?) ?? 0,
      hot: (r1['hot'] as int?) ?? 0,
      dualGroups: dual,
    );
  }
}
