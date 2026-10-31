#!/usr/bin/env python3
"""Pre-push checks for a solo or small-team git workflow.

Checks the things a human reviewer would otherwise catch late: branch naming,
commit message shape, secrets, credentials embedded in URLs, oversized files,
and AI attribution trailers.

    python scripts/preflight.py --repo . --base main
    python scripts/preflight.py --repo . --base main --json

Exit 0 = nothing found, 1 = at least one ERROR, 2 = usage problem.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CONVENTIONAL = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]+\))?!?: .{4,}"
)
BRANCH = re.compile(r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)/[a-z0-9][a-z0-9._-]*$")
TRAILERS = re.compile(
    r"(?im)^(co-authored-by:|generated with|generated-by:|🤖 generated|assisted-by:)"
)

SECRETS = [
    ("private-key", re.compile(r"-----BEGIN (RSA|OPENSSH|EC|DSA|PGP) PRIVATE KEY-----"), "error"),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "error"),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), "error"),
    ("url-credentials", re.compile(r"https?://[^\s/:@]+:[^\s/@]+@"), "error"),
    (
        "assigned-secret",
        re.compile(r"(?i)\b(password|passwd|pwd|token|secret|api[_-]?key)\b\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
        "error",
    ),
    ("private-ip", re.compile(r"\b(10\.\d{1,3}|192\.168|172\.(1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b"), "warn"),
]


class Finding(dict):
    def __init__(self, severity: str, code: str, message: str, where: str = ""):
        super().__init__(severity=severity, code=code, message=message, where=where)


def git(repo: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8"
    )
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def current_branch(repo: Path) -> str:
    return git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()


def default_branch(repo: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    for candidate in ("main", "master"):
        if git(repo, "rev-parse", "--verify", "--quiet", candidate, check=False).strip():
            return candidate
    return "HEAD"


def resolve_base(repo: Path, base: str) -> str | None:
    """Prefer the merge-base with the remote, fall back to the local branch."""
    for ref in (f"origin/{base}", base):
        out = git(repo, "rev-parse", "--verify", "--quiet", ref, check=False).strip()
        if not out:
            continue
        merge = git(repo, "merge-base", "HEAD", ref, check=False).strip()
        return merge or out
    return None


def staged_files(repo: Path) -> list[str]:
    out = git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR", check=False)
    return [line for line in out.splitlines() if line.strip()]


def added_lines(repo: Path) -> list[tuple[str, str]]:
    """(path, line) for lines added in the staged diff."""
    out = git(repo, "diff", "--cached", "--unified=0", "--no-color", check=False)
    rows: list[tuple[str, str]] = []
    path = ""
    for line in out.splitlines():
        if line.startswith("+++ b/"):
            path = line[6:]
        elif line.startswith("+") and not line.startswith("+++"):
            rows.append((path, line[1:]))
    return rows


def check_branch(repo: Path, base: str) -> list[Finding]:
    findings: list[Finding] = []
    branch = current_branch(repo)
    if branch in (base, "HEAD"):
        findings.append(
            Finding("warn", "on-default-branch", f"committing straight to {branch}: fine for typos, not for features")
        )
    elif branch not in ("main", "master") and not BRANCH.match(branch):
        findings.append(
            Finding(
                "error",
                "branch-name",
                f"'{branch}' does not match <type>/<kebab-name> (feat/, fix/, docs/, refactor/…)",
                branch,
            )
        )
    return findings


def check_commits(repo: Path, base_sha: str | None) -> list[Finding]:
    findings: list[Finding] = []
    if not base_sha:
        return findings
    log = git(repo, "log", "--format=%H%x1f%s%x1f%b%x1e", f"{base_sha}..HEAD", check=False)
    for record in log.split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        parts = record.split("\x1f")
        if len(parts) < 2:
            continue
        sha, subject = parts[0], parts[1]
        body = parts[2] if len(parts) > 2 else ""
        if not CONVENTIONAL.match(subject):
            findings.append(
                Finding("error", "commit-subject", f"'{subject}' is not a conventional commit", sha[:8])
            )
        if TRAILERS.search(body) or TRAILERS.search(subject):
            findings.append(
                Finding("error", "ai-trailer", "commit carries an AI attribution trailer", sha[:8])
            )
    return findings


def check_content(repo: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path, line in added_lines(repo):
        if "noqa: secret-scan" in line:
            continue  # deliberate test fixture, marked by its author
        for code, pattern, severity in SECRETS:
            if pattern.search(line):
                findings.append(
                    Finding(severity, code, f"{code} pattern in added line: {line.strip()[:80]}", path)
                )
    return findings


def check_sizes(repo: Path, max_mb: float) -> list[Finding]:
    findings: list[Finding] = []
    limit = int(max_mb * 1024 * 1024)
    for name in staged_files(repo):
        target = repo / name
        if target.is_file() and target.stat().st_size > limit:
            size = target.stat().st_size / 1024 / 1024
            findings.append(
                Finding("error", "large-file", f"{size:.1f} MB exceeds {max_mb} MB; use git-lfs", name)
            )
    return findings


def check_whitespace(repo: Path) -> list[Finding]:
    findings: list[Finding] = []
    out = git(repo, "diff", "--cached", "--check", "--no-color", check=False)
    for line in out.splitlines():
        if ": trailing whitespace" in line or ": space before tab" in line:
            findings.append(Finding("warn", "whitespace", line.strip()))
    return findings


def run(repo: Path, base_arg: str | None, max_mb: float) -> dict:
    base = default_branch(repo, base_arg)
    findings: list[Finding] = []
    findings += check_branch(repo, base)
    findings += check_commits(repo, resolve_base(repo, base))
    findings += check_content(repo)
    findings += check_sizes(repo, max_mb)
    findings += check_whitespace(repo)
    errors = [f for f in findings if f["severity"] == "error"]
    return {
        "repo": str(repo),
        "branch": current_branch(repo),
        "base": base,
        "errors": len(errors),
        "warnings": len(findings) - len(errors),
        "findings": findings,
        "verdict": "fail" if errors else "pass",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Pre-push checks")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--base", help="default branch to compare against (auto: main, then master)")
    ap.add_argument("--max-mb", type=float, default=5.0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    repo = Path(args.repo).resolve()
    if not (repo / ".git").exists():
        print(f"error: {repo} is not a git repository", file=sys.stderr)
        return 2
    try:
        report = run(repo, args.base, args.max_mb)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for f in report["findings"]:
            where = f" [{f['where']}]" if f["where"] else ""
            print(f"{f['severity'].upper():5} {f['code']:18}{where} {f['message']}")
        print(
            f"\nbranch {report['branch']} vs {report['base']}: "
            f"{report['errors']} error(s), {report['warnings']} warning(s)"
        )
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
