import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_highlight/flutter_highlight.dart';
import 'package:flutter_highlight/themes/monokai-sublime.dart';

/// 代码查看器：语法高亮 + 超长行可横向拖动 + 一键复制。
class CodeViewer extends StatelessWidget {
  final String code;
  final String language; // python | go

  const CodeViewer({super.key, required this.code, required this.language});

  static const _langLabel = {'python': 'Python', 'go': 'Go'};

  @override
  Widget build(BuildContext context) {
    final label = _langLabel[language] ?? language;
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFF272822),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: const Color(0xFF3E3D32)),
      ),
      clipBehavior: Clip.antiAlias,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // 头部：语言标识 + 复制按钮
          Container(
            height: 34,
            padding: const EdgeInsets.symmetric(horizontal: 12),
            color: const Color(0xFF1E1F1A),
            child: Row(
              children: [
                Text(
                  label,
                  style: const TextStyle(
                    color: Color(0xFFA6E22E),
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const Spacer(),
                IconButton(
                  visualDensity: VisualDensity.compact,
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(minWidth: 36, minHeight: 30),
                  tooltip: '复制代码',
                  icon: const Icon(Icons.copy_rounded,
                      size: 16, color: Color(0xFFCFCFC2)),
                  onPressed: () =>
                      Clipboard.setData(ClipboardData(text: code)),
                ),
              ],
            ),
          ),
          // 代码区：外层横向滚动 → 超长行可左右拖动查阅
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: SingleChildScrollView(
              scrollDirection: Axis.vertical,
              child: HighlightView(
                code,
                language: language,
                theme: monokaiSublimeTheme,
                padding: const EdgeInsets.all(12),
                textStyle: const TextStyle(
                  fontFamily: 'monospace',
                  fontSize: 13.5,
                  height: 1.45,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
