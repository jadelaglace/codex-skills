#!/usr/bin/env python3
"""Tests for scripts/course_check.py on synthetic course documents."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "course_check.py"
RESULTS: list[tuple[str, bool, str]] = []

GOOD = """# 从零学排队论

## 第1课：为什么排队

### 目标

知道排队论解决什么问题。

### 概念

到达率与服务率。

### 示例

银行窗口。

### 练习

数一数食堂的队伍。

### 验收

能说出两个参数。

## 第2课：用第1课的参数算等待

### 目标

算平均等待。

### 概念

利用第1课的到达率。

### 示例

窗口两台。

### 练习

算一次。

### 验收

结果误差 10% 以内。
"""


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))


def run(text: str, *extra: str) -> tuple[int, dict]:
    with tempfile.TemporaryDirectory() as raw:
        path = Path(raw) / "course.md"
        path.write_text(text, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), str(path), "--json", *extra],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        try:
            return proc.returncode, json.loads(proc.stdout)
        except json.JSONDecodeError:
            return proc.returncode, {"stderr": proc.stderr}


def codes(report: dict) -> set[str]:
    return {i["check"] for i in report.get("issues", [])}


def main() -> int:
    code, report = run(GOOD)
    check("good: exit 0", code == 0, str(report)[:200])
    check("good: two lessons found", report.get("lessons") == 2, str(report.get("lessons")))

    code, report = run(GOOD.replace("### 练习", "#### 随便写点"))
    check("missing section: exit 1", code == 1, str(report)[:160])
    check("missing section: names practice", any(i.get("missing") == ["练习"] for i in report["issues"]), str(report["issues"])[:200])

    code, report = run(GOOD.replace("利用第1课的到达率", "利用第3课的公式"))
    check("forward reference: flagged", code == 1 and "forward_reference" in codes(report), str(codes(report)))
    check("forward reference: names the target", any(i.get("refers_to") == 3 for i in report["issues"]), str(report["issues"])[:200])

    code, report = run(GOOD.replace("## 第2课", "## 第4课"))
    check("numbering: gap flagged", code == 1 and "lesson_numbering" in codes(report), str(codes(report)))

    code, report = run(GOOD.replace("### 概念", "##### 概念"))
    check("heading jump: flagged", "heading_jump" in codes(report), str(codes(report)))

    code, report = run("# 空文档\n\n没什么内容。\n")
    check("no lessons: exit 1", code == 1 and "no_lessons" in codes(report), str(codes(report)))

    code, report = run(GOOD, "--require-coverage")
    check("coverage required: flagged when absent", code == 1 and "coverage_table" in codes(report), str(codes(report)))

    code, report = run(GOOD + "\n## 五维覆盖\n\n概念/操作/原理/实践/延伸。\n", "--require-coverage")
    check("coverage required: passes when present", code == 0, str(report)[:200])

    width = max(len(name) for name, _, _ in RESULTS)
    failed = 0
    for name, ok, detail in RESULTS:
        print(f"{name.ljust(width)}  {'PASS' if ok else 'FAIL'}  {detail if not ok else ''}".rstrip())
        failed += 0 if ok else 1
    print(f"\n{len(RESULTS) - failed}/{len(RESULTS)} passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())