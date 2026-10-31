#!/usr/bin/env python3
"""End-to-end tests for scripts/llm.py against a local stub server.

    python -X utf8 tests/run_tests.py

Assertions are behavioural: exit code, the text on stdout, the warning on
stderr, or the JSON body the server actually received.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLIENT = HERE.parent / "scripts" / "llm.py"

sys.path.insert(0, str(HERE))
import stub_server  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))


def run(args: list[str], base: str | None, stdin: str | None = None) -> tuple[int, str, str]:
    env = dict(os.environ)
    for key in ("LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL"):
        env.pop(key, None)
    if base:
        env["LLM_BASE_URL"] = base
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, "-X", "utf8", str(CLIENT), *args],
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return proc.returncode, proc.stdout, proc.stderr


def with_server(scenario: str):
    httpd, state, base = stub_server.start(scenario)
    return httpd, state, base


def case_ok() -> None:
    httpd, state, base = with_server("ok")
    try:
        code, out, err = run(["--model", "m1", "--prompt", "hi", "--json"], base)
        check("ok: exit 0", code == 0, err.strip())
        payload = json.loads(out)
        check("ok: text returned", payload["text"] == "hello from the stub", out[:120])
        check("ok: usage reported", payload["usage"]["total_tokens"] == 20, str(payload["usage"]))
        body = state.requests[0]["body"]
        check("ok: model and messages sent", body["model"] == "m1" and body["messages"][-1]["content"] == "hi", str(body)[:160])
        check("ok: no auth header without a key", state.requests[0]["auth"] is None, str(state.requests[0]["auth"]))
    finally:
        httpd.shutdown()


def case_stdin_and_system() -> None:
    httpd, state, base = with_server("ok")
    try:
        code, _out, err = run(["--model", "m", "--stdin", "--system", "be terse"], base, stdin="piped prompt")
        check("stdin: exit 0", code == 0, err.strip())
        body = state.requests[0]["body"]
        check(
            "stdin: system then user message",
            body["messages"][0] == {"role": "system", "content": "be terse"}
            and body["messages"][1]["content"] == "piped prompt",
            str(body["messages"])[:200],
        )
    finally:
        httpd.shutdown()


def case_thinking() -> None:
    httpd, state, base = with_server("ok")
    try:
        run(["--model", "m", "--prompt", "x", "--think", "off"], base)
        check("think: effort style sends reasoning_effort=none", state.requests[0]["body"].get("reasoning_effort") == "none", str(state.requests[0]["body"])[:160])
        run(["--model", "m", "--prompt", "x", "--think", "off", "--think-style", "template"], base)
        body = state.requests[1]["body"]
        check(
            "think: template style sends enable_thinking=false",
            body.get("chat_template_kwargs") == {"enable_thinking": False} and "reasoning_effort" not in body,
            str(body)[:160],
        )
        run(["--model", "m", "--prompt", "x", "--think", "high"], base)
        check("think: high maps to reasoning_effort", state.requests[2]["body"].get("reasoning_effort") == "high", str(state.requests[2]["body"])[:160])
    finally:
        httpd.shutdown()


def case_reasoning_only() -> None:
    httpd, _state, base = with_server("reasoning_only")
    try:
        code, out, err = run(["--model", "m", "--prompt", "x", "--json"], base)
        check("reasoning: exit 0 (not a silent blank)", code == 0, err.strip())
        payload = json.loads(out)
        check("reasoning: falls back to the reasoning text", payload["text"].startswith("thinking hard"), out[:120])
        check("reasoning: warns about the cause", "reasoning_content" in err and "--max-tokens" in err, err.strip()[:200])
        check("reasoning: also warns on truncation", "finish_reason=length" in err, err.strip()[:200])
    finally:
        httpd.shutdown()


def case_failures() -> None:
    for scenario, expected, needle in [
        ("truncated", 0, "finish_reason=length"),
        ("auth", 5, "rejected the key"),
        ("http500", 6, "HTTP 500"),
        ("notjson", 6, "not JSON"),
        ("empty", 7, "empty reply"),
        ("nochoice", 7, "no choices"),
    ]:
        httpd, _state, base = with_server(scenario)
        try:
            code, _out, err = run(["--model", "m", "--prompt", "x"], base)
            check(f"{scenario}: exit {expected}", code == expected, f"got {code}: {err.strip()[:160]}")
            check(f"{scenario}: explains itself", needle in err, err.strip()[:160])
        finally:
            httpd.shutdown()

    httpd, _state, base = with_server("slow")
    try:
        code, _out, err = run(["--model", "m", "--prompt", "x", "--timeout", "1"], base)
        check("timeout: exit 4", code == 4, f"got {code}: {err.strip()[:160]}")
    finally:
        httpd.shutdown()


def case_retry() -> None:
    httpd, state, base = with_server("flaky")
    try:
        code, out, err = run(["--model", "m", "--prompt", "x", "--retry", "--retry-delay", "0"], base)
        check("retry: succeeds on the second attempt", code == 0 and "hello from the stub" in out, f"{code}: {err[:160]}")
        check("retry: server saw two requests", len(state.requests) == 2, str(len(state.requests)))
        check("retry: says it retried", "retrying once" in err, err[:160])
    finally:
        httpd.shutdown()

    httpd, state, base = with_server("http500")
    try:
        code, _out, _err = run(["--model", "m", "--prompt", "x"], base)
        check("no retry by default: single request", len(state.requests) == 1, str(len(state.requests)))
        check("no retry by default: exit 6", code == 6, f"got {code}")
    finally:
        httpd.shutdown()


def case_usage() -> None:
    code, _out, err = run(["--model", "m", "--prompt", "x"], None)
    check("no base url: exit 3", code == 3, f"got {code}")
    check("no base url: names the env var", "LLM_BASE_URL" in err, err[:160])

    code, _out, err = run(["--model", "m"], "http://127.0.0.1:1/v1")
    check("no prompt: exit 2", code == 2, f"got {code}: {err[:160]}")

    code, out, _err = run(["--model", "m", "--prompt", "x", "--dry-run"], None)
    check("dry-run: no server needed", code == 0, f"got {code}")
    check("dry-run: prints the target url", "/chat/completions" in out, out[:160])

    code, _out, err = run(["--model", "m", "--prompt", "x"], "http://127.0.0.1:1/v1")
    check("unreachable: exit 4", code == 4, f"got {code}: {err[:160]}")


def main() -> int:
    case_ok()
    case_stdin_and_system()
    case_thinking()
    case_reasoning_only()
    case_failures()
    case_retry()
    case_usage()

    width = max(len(name) for name, _, _ in RESULTS)
    failed = 0
    for name, ok, detail in RESULTS:
        print(f"{name.ljust(width)}  {'PASS' if ok else 'FAIL'}  {detail if not ok else ''}".rstrip())
        failed += 0 if ok else 1
    print(f"\n{len(RESULTS) - failed}/{len(RESULTS)} passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())