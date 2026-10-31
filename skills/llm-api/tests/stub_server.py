#!/usr/bin/env python3
"""A fake OpenAI-compatible server for the tests.

Implements `POST /v1/chat/completions` only, with scenarios for the ways a real
server disappoints you: empty content with a populated reasoning channel, a
truncated reply, auth failure, a 500, a hang, and a non-JSON body.

    python tests/stub_server.py --scenario reasoning_only --port 8000
"""

from __future__ import annotations

import argparse
import json
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class State:
    def __init__(self, scenario: str):
        self.scenario = scenario
        self.requests: list[dict] = []
        self.lock = threading.Lock()


def make_handler(state: State):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args):
            return

        def _send(self, code: int, body: bytes, ctype: str = "application/json"):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _json(self, code: int, payload):
            self._send(code, json.dumps(payload, ensure_ascii=False).encode("utf-8"))

        def _completion(self, content: str, reasoning: str = "", finish: str = "stop") -> dict:
            return {
                "id": "chatcmpl-" + uuid.uuid4().hex[:8],
                "object": "chat.completion",
                "model": "stub-model",
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": content, "reasoning_content": reasoning},
                        "finish_reason": finish,
                    }
                ],
                "usage": {"prompt_tokens": 12, "completion_tokens": 8, "total_tokens": 20},
            }

        def do_GET(self):  # noqa: N802
            if self.path == "/health":
                return self._json(200, {"status": "ok"})
            return self._json(404, {"error": "not found"})

        def do_POST(self):  # noqa: N802
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""
            try:
                payload = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError:
                payload = {}
            with state.lock:
                state.requests.append({"path": self.path, "body": payload, "auth": self.headers.get("Authorization")})
                count = len(state.requests)
            scenario = state.scenario

            if scenario == "auth":
                return self._json(401, {"error": {"message": "invalid api key"}})
            if scenario == "http500":
                return self._send(500, b'{"error":{"message":"upstream exploded"}}')
            if scenario == "slow":
                time.sleep(3)
                try:
                    return self._json(200, self._completion("too late"))
                except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
                    return  # the client already gave up; that is the point of this scenario
            if scenario == "notjson":
                return self._send(200, b"<html>gateway error</html>", "text/html")
            if scenario == "flaky" and count == 1:
                return self._send(503, b'{"error":{"message":"try again"}}')
            if scenario == "reasoning_only":
                return self._json(200, self._completion("", reasoning="thinking hard about the answer", finish="length"))
            if scenario == "truncated":
                return self._json(200, self._completion("the answer is forty-two and then", finish="length"))
            if scenario == "empty":
                return self._json(200, self._completion("", "", "stop"))
            if scenario == "nochoice":
                return self._json(200, {"id": "x", "choices": []})
            return self._json(200, self._completion("hello from the stub"))

    return Handler


def start(scenario: str = "ok") -> tuple[ThreadingHTTPServer, State, str]:
    state = State(scenario)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(state))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, state, f"http://127.0.0.1:{httpd.server_address[1]}/v1"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", default="ok")
    ap.add_argument("--port", type=int, default=8000)
    ns = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", ns.port), make_handler(State(ns.scenario)))
    print(f"stub OpenAI server on http://127.0.0.1:{ns.port}/v1 scenario={ns.scenario}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
