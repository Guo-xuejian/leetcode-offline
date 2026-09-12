import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

/// 用户偏好：收藏、刷题进度、默认语言、主题。
class UserPrefs {
  static const _kFav = 'fav_ids';
  static const _kSolved = 'solved_ids';
  static const _kLang = 'code_lang';
  static const _kTheme = 'theme_mode';

  final SharedPreferences _prefs;
  Set<int> _favorites = {};
  Set<int> _solved = {};
  String _lang = 'python'; // python | go
  String _theme = 'system'; // system | light | dark

  UserPrefs._(this._prefs) {
    _favorites = (_prefs.getStringList(_kFav) ?? [])
        .map(int.tryParse)
        .whereType<int>()
        .toSet();
    _solved = (_prefs.getStringList(_kSolved) ?? [])
        .map(int.tryParse)
        .whereType<int>()
        .toSet();
    _lang = _prefs.getString(_kLang) ?? 'python';
    _theme = _prefs.getString(_kTheme) ?? 'system';
  }

  static Future<UserPrefs> load() async =>
      UserPrefs._(await SharedPreferences.getInstance());

  Set<int> get favorites => _favorites;
  Set<int> get solved => _solved;
  String get lang => _lang;
  String get themeMode => _theme;

  Future<void> setLang(String lang) async {
    _lang = lang;
    await _prefs.setString(_kLang, lang);
  }

  Future<void> setThemeMode(String mode) async {
    _theme = mode;
    await _prefs.setString(_kTheme, mode);
  }

  Future<void> toggleFavorite(int id) async {
    if (!_favorites.add(id)) {
      _favorites.remove(id);
    }
    await _prefs.setStringList(
        _kFav, _favorites.map((e) => e.toString()).toList());
  }

  Future<void> toggleSolved(int id) async {
    if (!_solved.add(id)) {
      _solved.remove(id);
    }
    await _prefs.setStringList(
        _kSolved, _solved.map((e) => e.toString()).toList());
  }

  /// 序列化给测试使用
  Map<String, Object> debugDump() => {
        'favorites': jsonEncode(_favorites.toList()..sort()),
        'solved': jsonEncode(_solved.toList()..sort()),
        'lang': _lang,
        'theme': _theme,
      };
}
