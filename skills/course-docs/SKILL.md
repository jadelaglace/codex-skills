---
name: course-docs
description: >-
  Structure a course so each lesson earns the next one: one causal main line,
  abstraction that never goes backwards, every lesson carrying goal, concept,
  example, exercise and acceptance, and no lesson depending on one that comes
  later. Use when planning or reviewing a course, writing lesson outlines,
  checking that a curriculum is in a teachable order, or when lessons keep
  introducing terms the reader has not met yet. Keywords — 课程, 课程文档,
  课程规划, 大纲, 讲义, 每课结构, 因果主线, 抽象层级, 过渡验收, 五维覆盖,
  curriculum, lesson plan, course.
metadata:
  version: "1.0.0"
---

# Course Docs

A course is not a pile of chapters; it is a chain of dependencies. The single
structural rule that keeps it usable: **a lesson may only use what earlier
lessons established.** Everything below follows from that.

## The shape of a lesson

Five parts, in this order. If one is missing the lesson is not teachable yet.

| Part | Question it answers | Failure when missing |
| --- | --- | --- |
| 目标 | what can the reader do afterwards | the lesson has no destination |
| 概念 | what must be understood | the exercise becomes copy-paste |
| 示例 | what it looks like when it works | the reader cannot self-check |
| 练习 | what the reader does | the lesson is passive |
| 验收 | how the reader knows they got it | progress is a feeling, not a fact |

The acceptance part is the one people drop, and it is the one that makes a
course self-paced.

## Three ordering rules

1. **One causal main line.** Each lesson exists because the previous one raised
   the question it answers. If you cannot state that sentence, the lesson is an
   appendix, not a chapter.
2. **Abstraction decreases monotonically.** Do not open with the general theory,
   drop to a tool, climb back to theory, then down again. Each layer is
   introduced once and then used.
3. **No forward references.** A lesson that mentions "as we will see in lesson 5"
   has a dependency pointing backwards in the reading order — that is a
   reordering bug, not a writing style.

## Coverage and transitions

- **Five-dimension coverage**: for a course that claims to make someone
  productive, the outline should say which lessons cover 概念 / 操作 / 原理 /
  实践 / 延伸. Missing dimensions are visible as a gap in the table, not as a
  hunch during review.
- **Transition acceptance**: the end of lesson N and the start of N+1 must join
  on the same sentence. Write the handover sentence first; if it does not exist,
  the lessons are unrelated.
- **Demos and exercises are separate.** A demo shows a working path; an exercise
  makes the reader produce something. A course whose only exercises are "run the
  demo" teaches watching.

## Mechanical check

`scripts/course_check.py` enforces the structural half:

```bash
python scripts/course_check.py course.md
python scripts/course_check.py course.md --json
python scripts/course_check.py course.md --require-coverage
```

| Check | Catches |
| --- | --- |
| `lesson_sections` | a lesson missing 目标/概念/示例/练习/验收 |
| `forward_reference` | "第5课" mentioned inside 第2课 |
| `lesson_numbering` | gaps or duplicates in 第N课 |
| `heading_jump` | H2 → H4, i.e. a section that lost its parent |
| `no_lessons` | the file has no `## 第N课` headings at all |
| `coverage_table` | `--require-coverage` and no 五维/覆盖 section |

Exit 1 when anything is found. It checks structure, never pedagogy: the causal
line and the abstraction order still need a human read.

## Writing order that saves rewrites

1. Write the ten lesson titles as one-line claims ("读完这课你能…").
2. Read the list aloud: if a title needs the next lesson to make sense, move it.
3. Write the handover sentence between each pair.
4. Only then fill 目标/概念/示例/练习/验收.

Titles first means the structure is settled before any prose exists, which is
the only time it is cheap to change.

## Verification

```bash
python -X utf8 tests/run_tests.py     # 11 assertions on synthetic outlines
```

The tests build a valid two-lesson document, then break it one way at a time —
missing section, forward reference, numbering gap, heading jump, empty file,
missing coverage — and assert each is reported.