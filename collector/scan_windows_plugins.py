# -*- coding: utf-8 -*-
"""扫描 app 依赖中注册了 Windows 平台的 Flutter 插件，输出 (name, path)。"""
import json
import os
import sys

APP = r"R:\projects\Guopher\Leetcode\app"
pkg_cfg = os.path.join(APP, ".dart_tool", "package_config.json")


def main():
    with open(pkg_cfg, encoding="utf-8") as f:
        data = json.load(f)
    plugins = []
    for pkg in data["packages"]:
        name = pkg["name"]
        root = pkg["rootUri"]
        if root.startswith("file:///"):
            path = root[len("file:///"):].replace("/", os.sep)
        else:
            continue
        if not os.path.isdir(path):
            continue
        pubspec = os.path.join(path, "pubspec.yaml")
        if not os.path.exists(pubspec):
            continue
        # 解析 pubspec 的 flutter.plugin 部分（粗略 YAML 扫描）
        in_flutter = False
        in_plugin = False
        in_platforms = False
        has_windows = False
        is_plugin = False
        depth = 0
        with open(pubspec, encoding="utf-8", errors="ignore") as pf:
            for line in pf:
                stripped = line.strip()
                if stripped.startswith("#") or not stripped:
                    continue
                indent = len(line) - len(line.lstrip(" "))
                if indent == 0:
                    key = stripped.split(":")[0]
                    if key == "flutter":
                        in_flutter = True
                        continue
                    if in_flutter:
                        in_flutter = False
                if in_flutter and stripped.startswith("plugin:"):
                    in_plugin = True
                    continue
                if in_plugin and stripped.startswith("platforms:"):
                    in_platforms = True
                    continue
                if in_platforms:
                    if indent == 4 and ":" in stripped and not stripped.startswith("-"):
                        if stripped.split(":")[0].strip() == "windows":
                            has_windows = True
                            break
                    elif indent < 4:
                        break
                if in_flutter and stripped.startswith("uses-material-design:"):
                    break
        if has_windows:
            plugins.append((name, path))
    for name, path in sorted(plugins):
        print(f"{name}\t{path}")


if __name__ == "__main__":
    main()
