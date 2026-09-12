import 'package:flutter/material.dart';

/// 全局主题模式通知器（浅色 / 深色 / 跟随系统）
final ValueNotifier<ThemeMode> themeModeNotifier =
    ValueNotifier(ThemeMode.system);

/// 构建主题：统一品牌色，支持浅色 / 深色两种亮度
ThemeData buildAppTheme(Brightness brightness) {
  final colorScheme = ColorScheme.fromSeed(
    seedColor: const Color(0xFF3D6FF2),
    brightness: brightness,
  );
  return ThemeData(
    colorScheme: colorScheme,
    useMaterial3: true,
    visualDensity: VisualDensity.adaptivePlatformDensity,
  );
}

/// 偏好字符串 → ThemeMode
ThemeMode themeModeFromString(String s) {
  switch (s) {
    case 'dark':
      return ThemeMode.dark;
    case 'light':
      return ThemeMode.light;
    default:
      return ThemeMode.system;
  }
}
