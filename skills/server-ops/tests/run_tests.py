#!/usr/bin/env python3
"""Tests for scripts/probe.py against a local server that misbehaves on purpose."""

from __future__ import annotations

import json
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "probe.py"
RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        return

    def _body(self, payload: bytes, code: int = 200, ctype: str = "application/json", extra: list | None = None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        for name, value in extra or []:
            self.send_header(name, value)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):  # noqa: N802
        if self.path == "/ok":
            return self._body(b'{"status":"ok"}')
        if self.path == "/dup":
            return self._body(b"x", extra=[("Set-Cookie", "a=1"), ("Set-Cookie", "b=2")])
        if self.path == "/nocharset":
            return self._body("中文".encode("utf-8"), ctype="text/plain")
        if self.path == "/boom":
            return self._body(b'{"error":"database down"}', code=500)
        if self.path == "/html":
            return self._body(b'{"error":"nope"}', ctype="text/html")
        if self.path == "/slow":
            time.sleep(3)
            return self._body(b"late")
        return self._body(b'{"error":"not found"}', code=404)

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        echo = json.dumps({"received": body.decode("utf-8", "replace"), "ctype": self.headers.get("Content-Type")}).encode()
        return self._body(echo)


def run(*args: str) -> tuple[int, dict]:
    proc = subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    try:
        return proc.returncode, json.loads(proc.stdout)
    except json.JSONDecodeError:
        return proc.returncode, {"stderr": proc.stderr}


def main() -> int:
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{httpd.server_address[1]}"
    try:
        code, report = run("--url", base + "/ok")
        check("ok: exit 0", code == 0, str(report)[:160])
        check("ok: status and version", report.get("status") == 200 and report.get("http_version") == "1.1", str(report)[:160])
        check("ok: body prefix kept", report.get("body_prefix") == '{"status":"ok"}', str(report.get("body_prefix")))

        code, report = run("--url", base + "/dup")
        check("dup headers: both reported as a list", report.get("duplicate_headers", {}).get("set-cookie") == 2, str(report.get("duplicate_headers")))
        check("dup headers: raises the list-collapse hint", any("duplicate headers" in p for p in report.get("patterns", [])), str(report.get("patterns")))

        code, report = run("--url", base + "/nocharset")
        check("charset: missing charset flagged", report.get("charset") is None and any("charset" in p for p in report.get("patterns", [])), str(report.get("patterns")))
        check("charset: body still decoded", "中文" in report.get("body_prefix", ""), str(report.get("body_prefix")))

        code, report = run("--url", base + "/boom")
        check("5xx: reported, not raised", code == 0 and report.get("status") == 500, f"{code} {report.get('status')}")
        check("5xx: pattern explains", any("5xx" in p for p in report.get("patterns", [])), str(report.get("patterns")))

        code, report = run("--url", base + "/html")
        check("html+json: spotted", any("content-type with a JSON body" in p for p in report.get("patterns", [])), str(report.get("patterns")))

        code, report = run("--url", base + "/missing")
        check("404: reported as a status", report.get("status") == 404, str(report.get("status")))

        code, report = run("--url", base + "/ok", "--method", "POST", "--data", '{"a":1}')
        check("post: body and content-type sent", '"received": "{\\"a\\":1}"' in report.get("body_prefix", "") or '"a":1' in report.get("body_prefix", ""), str(report.get("body_prefix")))
        check("post: json content-type default", "application/json" in report.get("body_prefix", ""), str(report.get("body_prefix")))

        code, report = run("--url", base + "/slow", "--timeout", "1")
        check("timeout: exit 5", code == 5, f"got {code}: {report}")

        code, report = run("--url", "http://127.0.0.1:1/", "--timeout", "1")
        check("unreachable: exit 4", code == 4, f"got {code}: {report}")

        code, report = run("--url", "ftp://example.com")
        check("bad scheme: exit 2", code == 2, f"got {code}")
    finally:
        httpd.shutdown()

    width = max(len(name) for name, _, _ in RESULTS)
    failed = 0
    for name, ok, detail in RESULTS:
        print(f"{name.ljust(width)}  {'PASS' if ok else 'FAIL'}  {detail if not ok else ''}".rstrip())
        failed += 0 if ok else 1
    print(f"\n{len(RESULTS) - failed}/{len(RESULTS)} passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())