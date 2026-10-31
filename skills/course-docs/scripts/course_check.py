#!/usr/bin/env python3
"""Structural checks for course documents.

It checks what can be checked mechanically: heading structure, the five parts of
a lesson, forward references, and lesson numbering. It does not judge whether the
teaching is good — that stays with a human.

    python scripts/course_check.py course.md
    python scripts/course_check.py course.md --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LESSON = re.compile(r"^(#{2})\s*第\s*(\d+)\s*课[：:\s]*(.*)$")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
SECTIONS = ["目标", "概念", "示例", "练习", "验收"]
REFERENCE = re.compile(r"第\s*(\d+)\s*课")


def parse(text: str) -> dict:
    lines = text.splitlines()
    lessons: list[dict] = []
    current = None
    prev_level = 0
    jumps: list[dict] = []
    for number, line in enumerate(lines, 1):
        match = LESSON.match(line)
        if match:
            current = {"number": int(match.group(2)), "title": match.group(3).strip(), "line": number, "sections": [], "text": []}
            lessons.append(current)
            prev_level = 2
            continue
        heading = HEADING.match(line)
        if heading:
            level = len(heading.group(1))
            if prev_level and level > prev_level + 1 and not LESSON.match(line):
                jumps.append({"line": number, "from": prev_level, "to": level, "text": heading.group(2).strip()})
            prev_level = level
            if current is not None:
                current["sections"].append(heading.group(2).strip())
            continue
        if current is not None:
            current["text"].append(line)
    return {"lessons": lessons, "jumps": jumps, "lines": len(lines)}


def check(text: str, require_coverage: bool = False) -> dict:
    parsed = parse(text)
    issues: list[dict] = []

    if not parsed["lessons"]:
        issues.append({"check": "no_lessons", "message": "no '## 第N课' headings found"})

    numbers = [lesson["number"] for lesson in parsed["lessons"]]
    if numbers and numbers != list(range(1, len(numbers) + 1)):
        issues.append({"check": "lesson_numbering", "found": numbers, "expected": list(range(1, len(numbers) + 1))})

    for lesson in parsed["lessons"]:
        missing = [s for s in SECTIONS if not any(s in heading for heading in lesson["sections"])]
        if missing:
            issues.append(
                {
                    "check": "lesson_sections",
                    "lesson": lesson["number"],
                    "title": lesson["title"],
                    "missing": missing,
                }
            )

    for lesson in parsed["lessons"]:
        body = "\n".join(lesson["text"])
        for ref in REFERENCE.finditer(body):
            target = int(ref.group(1))
            if target > lesson["number"]:
                issues.append(
                    {
                        "check": "forward_reference",
                        "lesson": lesson["number"],
                        "refers_to": target,
                        "message": "a lesson depends on one that comes later",
                    }
                )

    if parsed["jumps"]:
        issues.append({"check": "heading_jump", "jumps": parsed["jumps"]})

    if require_coverage and "五维" not in text and "覆盖" not in text:
        issues.append({"check": "coverage_table", "message": "no coverage section found"})

    return {
        "lessons": len(parsed["lessons"]),
        "lines": parsed["lines"],
        "issues": issues,
        "ok": not issues,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Course document structure check")
    ap.add_argument("path")
    ap.add_argument("--require-coverage", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    target = Path(args.path)
    if not target.exists():
        print(f"error: not found: {target}", file=sys.stderr)
        return 2
    report = check(target.read_text(encoding="utf-8"), args.require_coverage)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for issue in report["issues"]:
            print(f"{issue['check']}: {json.dumps({k: v for k, v in issue.items() if k != 'check'}, ensure_ascii=False)}")
        print(f"\n{report['lessons']} lesson(s), {'ok' if report['ok'] else str(len(report['issues'])) + ' issue(s)'}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())