# -*- coding: utf-8 -*-
"""为 Windows 插件创建 junction（替代 flutter 的 symlink，规避开发者模式要求）。"""
import os
import subprocess

SYMLINKS = r"R:\projects\Guopher\Leetcode\app\windows\flutter\ephemeral\.plugin_symlinks"

PLUGINS = [
    ("file_picker", r"C:\Users\guoxj\AppData\Local\Pub\Cache\hosted\pub.flutter-io.cn\file_picker-8.3.7"),
    ("jni", r"C:\Users\guoxj\AppData\Local\Pub\Cache\hosted\pub.flutter-io.cn\jni-1.0.3"),
    ("path_provider_windows", r"C:\Users\guoxj\AppData\Local\Pub\Cache\hosted\pub.flutter-io.cn\path_provider_windows-2.3.0"),
    ("shared_preferences_windows", r"C:\Users\guoxj\AppData\Local\Pub\Cache\hosted\pub.flutter-io.cn\shared_preferences_windows-2.4.1"),
]

os.makedirs(SYMLINKS, exist_ok=True)

for name, target in PLUGINS:
    link = os.path.join(SYMLINKS, name)
    if os.path.exists(link):
        print(f"skip existing: {name}")
        continue
    # mklink /J 创建 junction（无需管理员/开发者模式，支持跨卷）
    r = subprocess.run(
        ["cmd", "/c", "mklink", "/J", link, target],
        capture_output=True, text=True, encoding="gbk", errors="replace",
    )
    ok = os.path.isdir(link)
    print(f"{'OK ' if ok else 'FAIL'} {name}: {r.stdout.strip()} {r.stderr.strip()}")

print("\nresult:")
for name, _ in PLUGINS:
    link = os.path.join(SYMLINKS, name)
    print(f"  {name}: exists={os.path.exists(link)} isdir={os.path.isdir(link)}")
