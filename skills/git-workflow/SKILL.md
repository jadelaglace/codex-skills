---
name: git-workflow
description: >-
  A small-team git workflow that keeps the default branch revertible: classify
  the change, branch, write conventional commits, run the pre-push checklist,
  and finish with a squash merge. Use when committing, choosing a branch name,
  writing a commit message, preparing a PR, cleaning up after a merge, running
  parallel tasks in one repository, or checking a diff for secrets and oversized
  files before it leaves the machine. Keywords — git, 提交, commit, 分支, branch,
  push, PR, 合并, squash, rebase, worktree, conventional commits, 回滚, revert,
  推送前检查, 密钥泄漏.
metadata:
  version: "1.0.0"
---

# Git Workflow

The default branch only receives reviewed, revertible changes. Everything else
happens on a branch that ends in a squash merge. This costs one command more
than committing straight to the default branch and buys a clean history and a
one-command rollback.

## Classify before touching git

| Change | Route |
| --- | --- |
| typo, comment, pure docs, a scratch repo | commit and push to the default branch |
| feature, fix, refactor, dependency or config change | branch → commit → PR → squash merge |
| destructive change, big refactor, shared library | same, plus the verification list before merging |

When unsure, take the branch. The cost is one merge, not a lost afternoon.

## Branch names

`<type>/<kebab-name>`, with the same type vocabulary as commits:

```
feat/qwen-pipeline   fix/alpha-bleed   docs/agent-usage   refactor/api-map   chore/deps
```

No spaces, no Chinese, no uppercase: the name lands in URLs and in API paths
where `/` must be percent-encoded.

## Commits

```
feat: add video-to-3D workflow
fix: stop alpha edges rendering black
docs: correct the token refresh command
```

- One intent per commit. Formatting and behaviour changes do not share a commit.
- Imperative present tense. The body explains *why*; the diff already shows what.
- Reference issues in the body (`Refs #12`). Closing happens through the PR body,
  not the commit: `Closes #12` closes the issue when the PR is squash-merged.
- **No AI attribution trailers.** No `Generated with …`, no `Co-Authored-By:`
  bot lines. The author is the person who ran the work.

## Pre-push checklist (30 seconds)

1. `git status` shows only files you meant to change; read `git diff --cached`
   file by file.
2. No secrets: passwords, tokens, keys, or a private host paired with an
   account. A clone URL with credentials inside a document counts.
3. Temporary files, `*.tmp`, `test_out/`, and large binaries are excluded;
   anything large that must live here goes through `git lfs track`.
4. Commit messages follow the format above.

`scripts/preflight.py` automates 1, 2, 3 and the message check:

```bash
python scripts/preflight.py --repo . --base main
```

It reports `branch-name`, `commit-subject`, `ai-trailer`, `private-key`,
`aws-access-key`, `github-token`, `url-credentials`, `assigned-secret`,
`large-file` (default > 5 MB), `private-ip` (warning only) and whitespace
problems. Exit 1 means at least one error; exit 2 means the path is not a repo.
A private IP is a warning because it is only a leak when paired with an account.

## Finishing a branch (five steps)

1. **Verify** — the change does what it claims: tests, build, or the artefact.
2. **Push** — `git push -u origin <branch>`.
3. **Summarise** — `git diff <base>...HEAD --stat` plus the commit list.
4. **Merge** — open a PR whose body says `Closes #n`, squash-merge it, delete
   the remote branch.
5. **Clean up locally** — switch to the default branch, `git pull`, delete the
   local branch; remove the worktree if you used one.

Squash is the default: the trial-and-error commits of a branch become one clean
commit. `gw flow`-style tooling can wrap steps 2–5, but the commands above are
the contract.

## Issue-driven work

For anything larger than a one-file change:

1. Split the work so one issue equals one implementation step, and keep an epic
   above them.
2. Each issue carries four things: background and traceability, what is in and
   out of scope, the decisions already made, and an acceptance checklist.
3. Put the branch name in the issue. Dependencies between issues decide the
   order.
4. Work the issue, commit conventionally, then open the PR with `Closes #n`.
5. The board closes itself as issues close; the epic closes when its issues do.

`preflight.py` does not create issues, labels or milestones — that is API work,
not git work.

## Safety rails

- Never `--force` a branch that has been pushed. Force is only for a local
  branch nobody has seen.
- Never `reset --hard` a pushed commit. Roll back with `git revert`, which adds
  an inverse commit and keeps history intact.
- Delete only the remote branch you just merged. Other people's branches are not
  yours to clean up.
- `rebase` is for tidying unpushed local commits, not for rewriting shared work.

## Parallel work: worktrees, not stashing

Two tasks in one repository means two working directories:

```bash
git worktree add ../repo-feat-a feat/a
git worktree add ../repo-fix-b fix/b
```

Each worktree has its own checkout and index, so neither can disturb the other's
uncommitted state, and no `git stash` juggling is needed. Remove a worktree with
`git worktree remove ../repo-feat-a` after its branch is merged; `git worktree
list` shows what is still registered.

Never run two Agents in the same worktree: they share one index, and a `git add`
from either can capture the other's half-finished file.

## Verification

```bash
python -X utf8 tests/run_tests.py     # 13 assertions on throwaway repos
```

The tests build real repositories in a temp directory, stage a known defect, and
assert the detector fires — and that a clean branch produces no findings.