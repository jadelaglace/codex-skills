#!/usr/bin/env python3
"""End-to-end tests for scripts/gitea.py against a fake Gitea.

    python -X utf8 tests/run_tests.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLIENT = HERE.parent / "scripts" / "gitea.py"

sys.path.insert(0, str(HERE))
import stub_server  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))


def run(args: list[str], base: str | None, token: str | None = "good-token") -> tuple[int, str, str]:
    env = dict(os.environ)
    for key in ("GITEA_URL", "GITEA_TOKEN"):
        env.pop(key, None)
    if base:
        env["GITEA_URL"] = base
    if token:
        env["GITEA_TOKEN"] = token
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, "-X", "utf8", str(CLIENT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return proc.returncode, proc.stdout, proc.stderr


def with_server():
    httpd, state, base = stub_server.start()
    return httpd, state, base


def case_api() -> None:
    httpd, state, base = with_server()
    try:
        code, out, err = run(["api", "GET", "/version"], base)
        payload = json.loads(out)
        check("api: exit 0", code == 0, err.strip())
        check("api: /api/v1 appended automatically", payload["status"] == 200 and payload["body"]["version"] == "1.22.0", out[:160])
        check("api: token sent as 'token <value>'", state.calls[0]["auth"] == "token good-token", state.calls[0]["auth"])

        code, out, _err = run(["api", "POST", "/repos/me/proj/issues", "--data", '{"title":"from cli"}'], base)
        payload = json.loads(out)
        check("api: post carries the JSON body", payload["body"]["title"] == "from cli", out[:160])
        check("api: post returns 201", payload["status"] == 201, str(payload["status"]))

        code, _out, err = run(["api", "GET", "/version"], base, token="bad-token")  # noqa: secret-scan
        check("auth: exit 5 on a rejected token", code == 5, f"got {code}: {err[:120]}")
        check("auth: says scope or token", "token" in err.lower(), err[:120])
    finally:
        httpd.shutdown()


def case_pr_and_issue() -> None:
    httpd, state, base = with_server()
    try:
        code, out, err = run(
            ["pr-merge", "--owner", "me", "--repo", "proj", "--number", "7", "--style", "squash", "--delete-branch"],
            base,
        )
        payload = json.loads(out)
        check("pr-merge: exit 0", code == 0, err.strip())
        call = [c for c in state.calls if c["path"].endswith("/pulls/7/merge")][0]
        check("pr-merge: squash by default here explicit", call["data"]["Do"] == "squash", str(call["data"]))
        check("pr-merge: delete_branch_after_merge passed", call["data"]["delete_branch_after_merge"] is True, str(call["data"]))
        check("pr-merge: server reports merged", payload["merge"]["merged"] is True, out[:160])

        code, _out, err = run(["pr-merge", "--owner", "me", "--repo", "proj", "--number", "999"], base)
        check("pr-merge: 404 becomes exit 6", code == 6, f"got {code}: {err[:120]}")

        code, out, err = run(["issue-close", "--owner", "me", "--repo", "proj", "--number", "12"], base)
        check("issue-close: exit 0", code == 0, err.strip())
        check("issue-close: state closed", state.issues[12]["state"] == "closed", str(state.issues[12]))
    finally:
        httpd.shutdown()


def case_config() -> None:
    code, _out, err = run(["api", "GET", "/version"], None)
    check("config: missing URL exits 3", code == 3, f"got {code}")
    check("config: names the env var", "GITEA_URL" in err, err[:120])

    code, _out, err = run(["api", "GET", "/version"], "http://127.0.0.1:1", token=None)
    check("config: missing token exits 3", code == 3, f"got {code}")
    check("config: names the token var", "GITEA_TOKEN" in err, err[:120])

    code, _out, err = run(["api", "GET", "/version"], "http://127.0.0.1:1")
    check("connect: unreachable exits 4", code == 4, f"got {code}: {err[:120]}")

    code, _out, err = run(["api", "POST", "/repos/me/p/issues", "--data", "{oops"], "http://127.0.0.1:1")
    check("usage: bad JSON exits 2", code == 2, f"got {code}: {err[:120]}")


def main() -> int:
    case_api()
    case_pr_and_issue()
    case_config()

    width = max(len(name) for name, _, _ in RESULTS)
    failed = 0
    for name, ok, detail in RESULTS:
        print(f"{name.ljust(width)}  {'PASS' if ok else 'FAIL'}  {detail if not ok else ''}".rstrip())
        failed += 0 if ok else 1
    print(f"\n{len(RESULTS) - failed}/{len(RESULTS)} passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
