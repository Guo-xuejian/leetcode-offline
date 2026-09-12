# LeetCode 离线题库（LeetCode Offline）

离线浏览力扣（LeetCode）题目与题解的跨平台 App：**题解只保留 Go + Python 双语言**（默认优先 Python、题解页可随时切换），**难度简单/中等/困难可筛选**，代码语法高亮、超长行可横向拖动，题干含示例与约束范围。Windows 桌面版已构建验证；Android / iOS 可直接编译。

```
collector/   数据采集与处理管道（纯 Python 标准库）
app/         Flutter 跨平台应用（Windows / Android / iOS / Web）
```

## 已内置数据（app/assets/data/leetcode.db，23.4 MB）

| 指标 | 数量 |
|---|---|
| 题目总数 | 2837（Easy 710 / Medium 1503 / Hard 624） |
| 题解总数 | 2825（官方 1678 + 热门 1147） |
| 有题解的题目 | 2083 |
| Go+Python 双语言代码组 | 2340（含人工转换 185 组） |
| Hot 100 标记 | 100 题（已入库可筛选） |

数据来源：github.com/hzfsls/leetcode-supercrawl（MIT，力扣官方题解 + 中文热门题解），元数据来自 leetcode.com GraphQL。仅供个人学习使用。

## 快速开始

### Windows 桌面版（已构建）

```
app\build\windows\x64\runner\Release\leetcode_offline.exe
```

双击即可运行。首次启动会把内置数据包复制到应用支持目录并自动打开。设置页可切换深色 / 浅色 / 跟随系统主题。

## 手机版（编译 APK）

```
cd app
flutter build apk --release
# 产物：build\app\outputs\flutter-apk\app-release.apk（可直接安装到 Android 手机）
```

> 构建提示：sqflite 依赖的 sqlite3 包构建时会从 GitHub 下载各平台预编译库，
> 网络受限时请开启代理/VPN；若报 hooks 超时，先检查是否有残留 dart 进程占用
> `.dart_tool/hooks_runner` 锁（`Get-Process dart` 后结束残留进程）。

iOS（需要 Mac）：`flutter build ipa`。代码为响应式布局（窄屏自动切换为底部导航单栏模式），无需改动。

### 重新构建数据包（可选）

```
cd collector
python fetch_metadata.py      # 拉取题目元数据（leetcode.com/graphql）
python fetch_hot100.py        # 拉取 Hot 100 题单
python html2md.py             # HTML 题干 → Markdown
python parse_solutions.py     # 解析题解（只保留 Python/Go，自动合并 conversions/）
python build_db.py            # 汇总生成 collector/output/problems.db
python export_app.py          # 导出到 app/assets/data/leetcode.db
python verify_db.py           # 校验
```

## App 功能

- 搜索（题号 / 中文标题 / 英文标题 / slug）
- 难度筛选：全部 / 简单 / 中等 / 困难（可组合 Hot 100、标签）
- Hot 100 与常用标签横向筛选
- 题干：中文 / English 切换（含示例、约束范围）
- 题解：官方题解 + 热门题解（作者 / 点赞数），Markdown 渲染
- 每个代码组 **Python ↔ Go 一键切换**（默认跟随设置页偏好，优先 Python）
- 代码查看器：Monokai 语法高亮、**超长行左右拖动**、一键复制
- 收藏星标、标记已完成、进度统计（设置页）
- 外观：浅色 / 深色 / 跟随系统（设置页切换，深色模式护眼，适合白天室外使用）
- 自定义 .db 数据包导入 / 恢复内置
- 响应式：宽屏（≥900px）双栏（NavigationRail + 列表 + 详情），窄屏底部导航 + 页面跳转

## 项目结构

```
collector/
  fetch_metadata.py        题目元数据（标题/难度/标签/题干）→ output/metadata.json
  fetch_hot100.py          Hot 100 题单 → output/hot100.json
  html2md.py               HTML 题干转 Markdown（含上标转 Unicode）
  parse_solutions.py       题解解析：按标题分组代码块，只保留 Python/Go
  build_db.py              汇总 → output/problems.db（SQLite）
  verify_db.py             抽样校验
  export_app.py            导出 App 离线数据包
  gen_todo.py / dump_todo.py        生成语言转换任务清单（缺 Go/Py 的题）
  extract_src*.py          导出待转换源码用于人工核实
  conv_data_part1/2.py     人工翻译（Go 转换，3–138 / 139–1143 题）
  conv_data_py.py          人工翻译（Python 转换，66 条）
  make_conversions.py      展开为 collector/conversions/<pid>.json
  check_conversions.py     校验 185 条转换全部覆盖
  make_plugin_junctions.py Windows 构建辅助：为 Flutter 插件创建 junction
  scan_windows_plugins.py  Windows 插件扫描

app/
  lib/
    main.dart              入口（Material 3 中文主题）
    models.dart            Problem / Solution / CodeGroup / DbStats
    db.dart                AppDatabase（桌面 ffi / 移动 sqflite，导入/恢复）
    prefs.dart             收藏 / 已完成 / 语言偏好
    pages/                 home（响应式外壳）、problem_list、settings
    widgets/               code_viewer（高亮+横向拖动）、problem_detail_view、difficulty_badge
  assets/data/leetcode.db  离线数据包
  integration_test/        Windows 真实环境端到端测试
  test/                    单元 + 组件测试（11 项）
```

## 测试

```
cd app
flutter analyze          # 0 issues
flutter test             # 11 项单元/组件测试
flutter test integration_test -d windows   # 3 项真实数据包端到端测试
```

## Windows 构建环境说明

本机未开启 Windows「开发者模式」时，Flutter 为插件创建 symlink 会失败。已用 junction 绕过：

```
python collector/make_plugin_junctions.py    # 每次 flutter pub get 后报 symlink 错误时重跑
```

或开启开发者模式（设置 → 隐私和安全性 → 开发者选项）一劳永逸。
