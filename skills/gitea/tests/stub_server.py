#!/usr/bin/env python3
"""Fake Gitea API for the tests: just the endpoints the client touches.

    python tests/stub_server.py --port 3000
"""

from __future__ import annotations

import argparse
import json
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class State:
    def __init__(self, token: str = "good-token"):
        self.token = token
        self.calls: list[dict] = []
        self.issues: dict[int, dict] = {12: {"number": 12, "title": "existing", "state": "open"}}
        self.pulls: dict[int, dict] = {7: {"number": 7, "state": "open"}}
        self.lock = threading.Lock()


def make_handler(state: State):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args):
            return

        def _send(self, code: int, payload):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _handle(self, method: str):
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""
            data = json.loads(raw.decode("utf-8")) if raw else None
            auth = self.headers.get("Authorization", "")
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path
            with state.lock:
                state.calls.append({"method": method, "path": path, "data": data, "auth": auth})

            if not path.startswith("/api/v1/"):
                return self._send(404, {"message": "missing /api/v1 prefix"})
            if auth != f"token {state.token}":
                return self._send(401, {"message": "unauthorized"})
            rest = path[len("/api/v1") :]

            if rest == "/version" and method == "GET":
                return self._send(200, {"version": "1.22.0"})

            parts = rest.strip("/").split("/")
            if len(parts) == 4 and parts[0] == "repos" and parts[3] == "issues":
                owner, repo = parts[1], parts[2]
                if method == "POST":
                    number = 100 + len(state.issues)
                    issue = {"number": number, "title": (data or {}).get("title"), "state": "open", "repo": f"{owner}/{repo}"}
                    state.issues[number] = issue
                    return self._send(201, issue)
                if method == "GET":
                    return self._send(200, list(state.issues.values()))
            if len(parts) == 5 and parts[0] == "repos" and parts[3] == "issues":
                number = int(parts[4])
                issue = state.issues.get(number)
                if not issue:
                    return self._send(404, {"message": "issue not found"})
                if method == "PATCH":
                    issue.update(data or {})
                    return self._send(200, issue)
                return self._send(200, issue)
            if len(parts) == 6 and parts[0] == "repos" and parts[3] == "pulls" and parts[5] == "merge":
                number = int(parts[4])
                pull = state.pulls.get(number)
                if not pull:
                    return self._send(404, {"message": "pull not found"})
                pull["merged"] = True
                pull["merged_by"] = (data or {}).get("Do")
                return self._send(200, {"merged": True, "message": "pull merged"})
            if len(parts) == 4 and parts[0] == "repos" and parts[3] == "branches" and method == "DELETE":
                return self._send(204, {})
            return self._send(404, {"message": f"no route for {method} {rest}"})

        def do_GET(self):
            self._handle("GET")

        def do_POST(self):
            self._handle("POST")

        def do_PATCH(self):
            self._handle("PATCH")

        def do_DELETE(self):
            self._handle("DELETE")

    return Handler


def start(token: str = "good-token") -> tuple[ThreadingHTTPServer, State, str]:
    state = State(token)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(state))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, state, f"http://127.0.0.1:{httpd.server_address[1]}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=3000)
    ns = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", ns.port), make_handler(State()))
    print(f"stub Gitea on http://127.0.0.1:{ns.port} (token: good-token)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass