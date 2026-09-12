import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../db.dart';
import '../models.dart';
import '../prefs.dart';
import '../theme.dart';

/// 设置页：统计、语言偏好、数据包导入与恢复。
class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  late Future<UserPrefs> _prefsFuture;
  Future<DbStats>? _statsFuture;
  Future<String?>? _infoFuture;

  @override
  void initState() {
    super.initState();
    _prefsFuture = UserPrefs.load();
    _statsFuture = AppDatabase.instance.stats();
    _infoFuture = AppDatabase.instance.importedInfo();
  }

  void _refresh() {
    setState(() {
      _prefsFuture = UserPrefs.load();
      _statsFuture = AppDatabase.instance.stats();
      _infoFuture = AppDatabase.instance.importedInfo();
    });
  }

  Future<void> _import() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['db'],
      dialogTitle: '选择离线数据包（.db 文件）',
    );
    if (result == null || result.files.isEmpty) return;
    final path = result.files.single.path;
    if (path == null) return;
    try {
      await AppDatabase.instance.importFromFile(path);
      _refresh();
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('数据包导入成功')));
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text('导入失败：$e')));
    }
  }

  Future<void> _reset() async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('恢复内置数据？'),
        content: const Text('将删除当前导入的自定义数据包，恢复为内置题库。'),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(ctx, false),
              child: const Text('取消')),
          FilledButton(
              onPressed: () => Navigator.pop(ctx, true),
              child: const Text('恢复')),
        ],
      ),
    );
    if (ok == true) {
      await AppDatabase.instance.resetToBundled();
      _refresh();
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<UserPrefs>(
      future: _prefsFuture,
      builder: (context, snap) {
        final prefs = snap.data;
        return ListView(
          padding: const EdgeInsets.all(20),
          children: [
            const Text('统计',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
            const SizedBox(height: 10),
            FutureBuilder<DbStats>(
              future: _statsFuture,
              builder: (context, s) {
                if (!s.hasData) {
                  return const SizedBox(
                      height: 80,
                      child: Center(child: CircularProgressIndicator()));
                }
                final st = s.data!;
                final solvedCount =
                    prefs?.solved.length ?? 0;
                return Column(
                  children: [
                    _statRow('题目总数', '${st.problems}'),
                    _statRow('题解总数', '${st.solutions}'),
                    _statRow('简单 / 中等 / 困难',
                        '${st.easy} / ${st.medium} / ${st.hard}'),
                    _statRow('Hot 100 题', '${st.hot}'),
                    _statRow('双语言代码块（Go+Python）', '${st.dualGroups}'),
                    _statRow('已完成', '$solvedCount'),
                    const SizedBox(height: 12),
                    LinearProgressIndicator(
                      value: st.problems == 0
                          ? 0
                          : solvedCount / st.problems,
                      backgroundColor:
                          Theme.of(context).colorScheme.surfaceContainerHighest,
                    ),
                  ],
                );
              },
            ),
            const Divider(height: 32),
            const Text('外观',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
            const SizedBox(height: 6),
            Text('白色主题白天使用偏亮，可切换为深色或跟随系统。',
                style: TextStyle(
                    fontSize: 12,
                    color: Theme.of(context).colorScheme.onSurfaceVariant)),
            const SizedBox(height: 6),
            if (prefs != null)
              RadioGroup<String>(
                groupValue: prefs.themeMode,
                onChanged: (v) async {
                  if (v == null) return;
                  await prefs.setThemeMode(v);
                  themeModeNotifier.value = themeModeFromString(v);
                  if (mounted) setState(() {});
                },
                child: const Column(
                  children: [
                    RadioListTile<String>(
                      value: 'system',
                      title: Text('跟随系统'),
                      dense: true,
                      contentPadding: EdgeInsets.zero,
                    ),
                    RadioListTile<String>(
                      value: 'light',
                      title: Text('浅色'),
                      dense: true,
                      contentPadding: EdgeInsets.zero,
                    ),
                    RadioListTile<String>(
                      value: 'dark',
                      title: Text('深色'),
                      dense: true,
                      contentPadding: EdgeInsets.zero,
                    ),
                  ],
                ),
              ),
            const Divider(height: 32),
            const Text('代码语言偏好',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
            const SizedBox(height: 6),
            Text('题解默认展示的语言，可随时在题解页切换。',
                style: TextStyle(
                    fontSize: 12,
                    color: Theme.of(context).colorScheme.onSurfaceVariant)),            const SizedBox(height: 6),
            if (prefs != null)
              RadioGroup<String>(
                groupValue: prefs.lang,
                onChanged: (v) async {
                  if (v == null) return;
                  await prefs.setLang(v);
                  if (mounted) setState(() {});
                },
                child: const Column(
                  children: [
                    RadioListTile<String>(
                      value: 'python',
                      title: Text('Python（优先）'),
                      dense: true,
                      contentPadding: EdgeInsets.zero,
                    ),
                    RadioListTile<String>(
                      value: 'go',
                      title: Text('Go'),
                      dense: true,
                      contentPadding: EdgeInsets.zero,
                    ),
                  ],
                ),
              ),
            const Divider(height: 32),
            const Text('数据包',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
            const SizedBox(height: 6),
            FutureBuilder<String?>(
              future: _infoFuture,
              builder: (context, s) => ListTile(
                contentPadding: EdgeInsets.zero,
                dense: true,
                leading: const Icon(Icons.storage_outlined),
                title: Text(s.data ?? '…'),
                subtitle: const Text(
                    '当前数据源（内置 / 用户导入）\n可通过 PC 端 collector 重新采集导出后导入'),
              ),
            ),
            const SizedBox(height: 8),
            FilledButton.icon(
              onPressed: _import,
              icon: const Icon(Icons.file_download_outlined),
              label: const Text('导入数据包（.db）'),
            ),
            const SizedBox(height: 8),
            OutlinedButton.icon(
              onPressed: _reset,
              icon: const Icon(Icons.restore),
              label: const Text('恢复为内置数据'),
            ),
            const Divider(height: 32),
            const Text('关于',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
            const SizedBox(height: 6),
            const ListTile(
              contentPadding: EdgeInsets.zero,
              dense: true,
              leading: Icon(Icons.info_outline),
              title: Text('LeetCode 离线题库 v1.0'),
              subtitle: Text(
                  '离线浏览力扣题目与题解（Go / Python 双语言）\n'
                  '数据来源：力扣官方题解 + 热门题解（见 collector 目录）\n'
                  '仅供个人学习使用'),
            ),
            const SizedBox(height: 8),
            Center(
              child: TextButton.icon(
                onPressed: () => Clipboard.setData(const ClipboardData(
                    text: 'https://github.com/hzfsls/leetcode-supercrawl')),
                icon: const Icon(Icons.link, size: 14),
                label: const Text('数据仓库：leetcode-supercrawl',
                    style: TextStyle(fontSize: 11)),
              ),
            ),
          ],
        );
      },
    );
  }

  Widget _statRow(String label, String value) {
    final dim = Theme.of(context).colorScheme.onSurfaceVariant;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3),
      child: Row(
        children: [
          Expanded(
              child: Text(label,
                  style: TextStyle(fontSize: 13.5, color: dim))),
          Text(value,
              style: const TextStyle(
                  fontSize: 13.5,
                  fontWeight: FontWeight.w600,
                  fontFamily: 'monospace')),
        ],
      ),
    );
  }
}
