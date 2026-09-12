import 'package:flutter/material.dart';

import 'db.dart';
import 'pages/home_page.dart';
import 'prefs.dart';
import 'theme.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await AppDatabase.instance.init();
  final prefs = await UserPrefs.load();
  themeModeNotifier.value = themeModeFromString(prefs.themeMode);
  runApp(LeetcodeOfflineApp(prefs: prefs));
}

class LeetcodeOfflineApp extends StatelessWidget {
  final UserPrefs prefs;

  const LeetcodeOfflineApp({super.key, required this.prefs});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<ThemeMode>(
      valueListenable: themeModeNotifier,
      builder: (context, mode, _) => MaterialApp(
        title: 'LeetCode 离线题库',
        debugShowCheckedModeBanner: false,
        theme: buildAppTheme(Brightness.light),
        darkTheme: buildAppTheme(Brightness.dark),
        themeMode: mode,
        home: HomePage(prefs: prefs),
      ),
    );
  }
}
