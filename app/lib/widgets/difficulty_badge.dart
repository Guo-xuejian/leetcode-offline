import 'package:flutter/material.dart';

/// 难度徽章：Easy 绿 / Medium 橙 / Hard 红
class DifficultyBadge extends StatelessWidget {
  final String difficulty;

  const DifficultyBadge({super.key, required this.difficulty});

  @override
  Widget build(BuildContext context) {
    final (color, label) = switch (difficulty) {
      'Easy' => (const Color(0xFF00B8A3), '简单'),
      'Hard' => (const Color(0xFFFF375F), '困难'),
      _ => (const Color(0xFFFFB800), '中等'),
    };
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: color.withValues(alpha: 0.6)),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: color,
          fontSize: 12,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }
}
