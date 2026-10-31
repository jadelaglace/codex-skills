#!/usr/bin/env python3
"""Behavioural tests for scripts/preflight.py using throwaway repositories.

    python -X utf8 tests/run_tests.py

Each case builds a tiny repo, stages a known defect, and asserts that preflight
reports that defect (and does not report the clean case).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "preflight.py"
RESULTS: list[tuple[str, bool, str]] = []

GIT_ENV = {
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.com",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.com",
}


def git(repo: Path, *args: str) -> None:
    env = dict(os.environ, **GIT_ENV)
    subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, env=env, text=True
    )


def new_repo(root: Path) -> Path:
    repo = root / "repo"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    (repo / "README.md").write_text("# base\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "chore: initial commit")
    return repo


def preflight(repo: Path) -> tuple[int, dict]:
    proc = subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), "--repo", str(repo), "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    payload = {}
    if proc.stdout.strip():
        payload = json.loads(proc.stdout)
    return proc.returncode, payload


def codes(payload: dict) -> set[str]:
    return {f["code"] for f in payload.get("findings", [])}


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))


def case_clean(root: Path) -> None:
    repo = new_repo(root)
    git(repo, "checkout", "-b", "feat/clean-change")
    (repo / "a.txt").write_text("hello\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "feat: add a greeting")
    code, payload = preflight(repo)
    check("clean: exit 0", code == 0, str(payload.get("findings")))
    check("clean: no findings", not payload.get("findings"), str(payload.get("findings")))


def case_branch(root: Path) -> None:
    repo = new_repo(root)
    git(repo, "checkout", "-b", "MyFeature")
    code, payload = preflight(repo)
    check("branch: bad name fails", code == 1 and "branch-name" in codes(payload), str(codes(payload)))
    detail = next((f for f in payload["findings"] if f["code"] == "branch-name"), {})
    check("branch: explains the pattern", "<type>/<kebab-name>" in detail.get("message", ""), detail.get("message", ""))


def case_commit(root: Path) -> None:
    repo = new_repo(root)
    git(repo, "checkout", "-b", "fix/message")
    (repo / "b.txt").write_text("x\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "updated stuff")
    code, payload = preflight(repo)
    check("commit: non-conventional subject fails", code == 1 and "commit-subject" in codes(payload), str(codes(payload)))

    (repo / "c.txt").write_text("y\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "feat: add c", "-m", "Co-Authored-By: Claude <noreply@example.com>")
    code, payload = preflight(repo)
    check("commit: AI trailer fails", "ai-trailer" in codes(payload), str(codes(payload)))


def case_secrets(root: Path) -> None:
    repo = new_repo(root)
    git(repo, "checkout", "-b", "chore/secrets")
    (repo / "conf.py").write_text(
        'password = "hunter2hunter2"\nurl = "https://user:pa55@example.com/repo"\n',  # noqa: secret-scan
        encoding="utf-8",
    )
    git(repo, "add", ".")
    code, payload = preflight(repo)
    found = codes(payload)
    check("secrets: assigned secret caught", "assigned-secret" in found, str(found))
    check("secrets: URL credentials caught", "url-credentials" in found, str(found))

    (repo / "marked.py").write_text(
        '# noqa: secret-scan  fixture, not a real credential: password = "not-a-real-secret"\n',
        encoding="utf-8",
    )
    git(repo, "add", ".")
    code, payload = preflight(repo)
    marked = [f for f in payload["findings"] if f["where"] == "marked.py"]
    check("secrets: per-line marker suppresses the finding", not marked, str(marked))


def case_size_and_ip(root: Path) -> None:
    repo = new_repo(root)
    git(repo, "checkout", "-b", "chore/big")
    (repo / "blob.bin").write_bytes(b"0" * (6 * 1024 * 1024))
    (repo / "hosts.txt").write_text("server=10.20.30.40\n", encoding="utf-8")
    git(repo, "add", ".")
    code, payload = preflight(repo)
    found = codes(payload)
    check("size: large file fails", "large-file" in found, str(found))
    check("ip: private address warns", "private-ip" in found, str(found))
    sev = {f["code"]: f["severity"] for f in payload["findings"]}
    check("ip: warning is not an error", sev.get("private-ip") == "warn", str(sev.get("private-ip")))


def case_unborn_and_usage(root: Path) -> None:
    plain = root / "not-a-repo"
    plain.mkdir()
    proc = subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), "--repo", str(plain)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    check("usage: non-repo exits 2", proc.returncode == 2, f"got {proc.returncode}")

    repo = new_repo(root)
    git(repo, "checkout", "-b", "docs/readme")
    (repo / "README.md").write_text("# base\nmore\n", encoding="utf-8")
    git(repo, "add", ".")
    code, payload = preflight(repo)
    check("clean edit: passes without commits", code == 0, str(payload.get("findings")))


def main() -> int:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        for i, case in enumerate(
            [case_clean, case_branch, case_commit, case_secrets, case_size_and_ip, case_unborn_and_usage]
        ):
            sub = root / f"case{i}"
            sub.mkdir()
            case(sub)

    width = max(len(name) for name, _, _ in RESULTS)
    failed = 0
    for name, ok, detail in RESULTS:
        print(f"{name.ljust(width)}  {'PASS' if ok else 'FAIL'}  {detail if not ok else ''}".rstrip())
        failed += 0 if ok else 1
    print(f"\n{len(RESULTS) - failed}/{len(RESULTS)} passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
