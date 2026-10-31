#!/usr/bin/env python3
"""End-to-end tests for the ComfyUI client against a local stub server.

Run with the same interpreter you use for the client:
    python -X utf8 tests/run_tests.py

Every assertion is behavioural: exit code, files written, or the payload the
server actually received. No real GPU and no network access are involved.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
CLIENT = SKILL / "scripts" / "comfy.py"
FIXTURE = HERE / "fixtures" / "txt2img.json"
WITH_IMAGE = HERE / "fixtures" / "img2img.json"

sys.path.insert(0, str(HERE))
import stub_server  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))


def run(args: list[str], server: str | None, cwd: Path) -> tuple[int, str, str]:
    env = dict(os.environ)
    env.pop("COMFYUI_URL", None)
    if server:
        env["COMFYUI_URL"] = server
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, "-X", "utf8", str(CLIENT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        cwd=str(cwd),
    )
    return proc.returncode, proc.stdout, proc.stderr


def with_server(scenario: str):
    httpd, state, url = stub_server.start(scenario)
    return httpd, state, url


def case_ok(tmp: Path) -> None:
    httpd, state, url = with_server("ok")
    try:
        code, out, err = run(
            ["run", "--workflow", str(FIXTURE), "--prompt", "a red ball", "--seed", "42",
             "--output-dir", str(tmp), "--prefix", "t"],
            url,
            tmp,
        )
        check("ok: exit 0", code == 0, err.strip())
        files = sorted(p.name for p in tmp.glob("t_*.png"))
        check("ok: two files downloaded", len(files) == 2, str(files))
        line = [ln for ln in out.splitlines() if ln.startswith("RESULT_JSON: ")]
        payload = json.loads(line[0][len("RESULT_JSON: "):]) if line else {}
        outputs = payload.get("outputs", [])
        check("ok: RESULT_JSON lists both", len(outputs) == 2, str(payload)[:200])
        alphas = [o for o in outputs if "transparent_rate" in o]
        check("ok: alpha stats only on RGBA", len(alphas) == 1, str(alphas)[:200])
        check("ok: seed passed through", payload.get("seed") == 42, str(payload.get("seed")))
        prompt = next(iter(state.prompts.values()))["prompt"]
        check(
            "ok: placeholders resolved in payload",
            prompt["6"]["inputs"]["text"] == "a red ball"
            and prompt["3"]["inputs"]["seed"] == 42
            and prompt["9"]["inputs"]["filename_prefix"] == "t",
            json.dumps(prompt["6"], ensure_ascii=False)[:160],
        )
    finally:
        httpd.shutdown()


def case_rename(tmp: Path) -> None:
    httpd, state, url = with_server("rename")
    img = tmp / "in.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 32)
    try:
        code, out, err = run(
            ["run", "--workflow", str(WITH_IMAGE), "--image", str(img), "--prompt", "x",
             "--output-dir", str(tmp), "--prefix", "r"],
            url,
            tmp,
        )
        check("rename: exit 0", code == 0, err.strip())
        prompt = next(iter(state.prompts.values()))["prompt"]
        check(
            "rename: graph uses the server-side name",
            prompt["12"]["inputs"]["image"] == "renamed_in.png",
            prompt["12"]["inputs"]["image"],
        )
    finally:
        httpd.shutdown()


def case_failures(tmp: Path) -> None:
    base = ["run", "--workflow", str(FIXTURE), "--prompt", "x", "--output-dir", str(tmp)]
    for scenario, expected, needle in [
        ("node_error", 6, "node 4"),
        ("exec_error", 7, "workflow failed"),
        ("empty", 8, "produced no images"),
    ]:
        httpd, _state, url = with_server(scenario)
        try:
            code, _out, err = run(base + ["--prefix", scenario], url, tmp)
            check(f"{scenario}: exit {expected}", code == expected, f"got {code}: {err.strip()[:160]}")
            check(f"{scenario}: explains itself", needle in err, err.strip()[:160])
        finally:
            httpd.shutdown()

    httpd, _state, url = with_server("slow")
    try:
        code, _out, err = run(base + ["--prefix", "slow", "--timeout", "1", "--interval", "0.2"], url, tmp)
        check("timeout: exit 9", code == 9, f"got {code}: {err.strip()[:160]}")
    finally:
        httpd.shutdown()

    httpd, _state, url = with_server("auth")
    try:
        code, _out, err = run(base + ["--prefix", "auth"], url, tmp)
        check("auth: exit 5", code == 5, f"got {code}: {err.strip()[:160]}")
    finally:
        httpd.shutdown()


def case_offline(tmp: Path) -> None:
    code, _out, _err = run(["run", "--workflow", str(FIXTURE), "--prompt", "x", "--dry-run"], None, tmp)
    check("dry-run: no server needed", code == 0, f"got {code}")

    code, out, _err = run(["run", "--workflow", str(FIXTURE), "--prompt", "x"], None, tmp)
    check("no server: exit 3", code == 3, f"got {code}")
    check("no server: says how to fix", "COMFYUI_URL" in out or "COMFYUI_URL" in _err, out[:160])

    code, out, _err = run(
        ["run", "--workflow", str(FIXTURE), "--prompt", "x", "--dry-run"], None, tmp
    )
    check("dry-run: reports resolved placeholders", '"unresolved": []' in out, out[:200])

    code, _out, err = run(
        ["run", "--workflow", str(FIXTURE), "--image", str(tmp / "missing.png")],
        "http://127.0.0.1:1",
        tmp,
    )
    check("missing image: exit 2", code == 2, f"got {code}: {err[:160]}")

    code, _out, err = run(
        ["run", "--workflow", str(FIXTURE), "--prompt", "x", "--output-dir", str(tmp)],
        "http://127.0.0.1:1",
        tmp,
    )
    check("unreachable: exit 4", code == 4, f"got {code}: {err[:160]}")
    check("unreachable: names the URL", "127.0.0.1:1" in err, err[:160])

    bad = tmp / "ui.json"
    bad.write_text(json.dumps({"nodes": [], "links": []}), encoding="utf-8")
    code, _out, err = run(["run", "--workflow", str(bad), "--dry-run"], None, tmp)
    check("UI-format graph: exit 2", code == 2, f"got {code}: {err[:160]}")
    check("UI-format graph: names the fix", "API format" in err, err[:160])


def case_nodes(tmp: Path) -> None:
    httpd, _state, url = with_server("ok")
    try:
        code, out, err = run(["nodes", "--filter", "sampler"], url, tmp)
        check("nodes: exit 0", code == 0, err.strip())
        payload = json.loads(out)
        check("nodes: filters by name", payload["count"] == 1 and payload["nodes"][0]["node"] == "KSampler", out[:200])
    finally:
        httpd.shutdown()


def main() -> int:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        case_ok(tmp)
        case_rename(tmp)
        case_failures(tmp)
        case_offline(tmp)
        case_nodes(tmp)

    width = max(len(name) for name, _, _ in RESULTS)
    failed = 0
    for name, ok, detail in RESULTS:
        print(f"{name.ljust(width)}  {'PASS' if ok else 'FAIL'}  {detail if not ok else ''}".rstrip())
        failed += 0 if ok else 1
    print(f"\n{len(RESULTS) - failed}/{len(RESULTS)} passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())