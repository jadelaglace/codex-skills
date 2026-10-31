#!/usr/bin/env python3
"""A tiny fake ComfyUI used by the tests.

Implements just enough of the HTTP surface for `comfy.py`:
  GET  /system_stats
  POST /upload/image
  POST /prompt
  GET  /history/<id>
  GET  /view?filename=...
  GET  /object_info

Scenarios let a test drive the failure paths without a real server:
  ok | auth | node_error | exec_error | empty | slow | rename
"""

from __future__ import annotations

import io
import json
import threading
import time
import urllib.parse
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from PIL import Image, ImageDraw


def _png(mode: str = "RGBA", transparent: bool = True, size: tuple[int, int] = (160, 120)) -> bytes:
    im = Image.new(mode, size, (255, 255, 255, 0) if transparent and mode == "RGBA" else (200, 180, 160, 255))
    draw = ImageDraw.Draw(im)
    draw.ellipse((20, 20, size[0] - 20, size[1] - 20), fill=(200, 60, 60, 255) if mode == "RGBA" else (200, 60, 60))
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue()


class StubState:
    def __init__(self, scenario: str = "ok"):
        self.scenario = scenario
        self.prompts: dict[str, dict] = {}
        self.uploads: dict[str, bytes] = {}
        self.requests: list[tuple[str, str]] = []
        self.polls: dict[str, int] = {}
        self.lock = threading.Lock()


def make_handler(state: StubState):
    subject = _png("RGBA", True)
    flat = _png("RGB", False)

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args):  # keep the test output readable
            return

        def _send(self, code: int, body: bytes, ctype: str = "application/json"):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _json(self, code: int, payload):
            self._send(code, json.dumps(payload).encode("utf-8"))

        def do_GET(self):  # noqa: N802 - http.server API
            parsed = urllib.parse.urlparse(self.path)
            state.requests.append(("GET", parsed.path))
            if state.scenario == "auth" and parsed.path != "/system_stats":
                return self._json(401, {"error": "unauthorized"})
            if parsed.path == "/system_stats":
                return self._json(
                    200,
                    {"system": {"comfyui_version": "stub"}, "devices": [{"name": "stub-gpu", "vram_free": 1, "vram_total": 2}]},
                )
            if parsed.path == "/object_info":
                return self._json(
                    200,
                    {
                        "CheckpointLoaderSimple": {
                            "input": {"required": {"ckpt_name": [["m.safetensors"]]}}
                        },
                        "KSampler": {
                            "input": {
                                "required": {
                                    "model": ["MODEL"],
                                    "seed": ["INT"],
                                    "steps": ["INT"],
                                    "cfg": ["FLOAT"],
                                }
                            }
                        },
                    },
                )
            if parsed.path.startswith("/history/"):
                pid = parsed.path.rsplit("/", 1)[-1]
                with state.lock:
                    state.polls[pid] = state.polls.get(pid, 0) + 1
                    count = state.polls[pid]
                if state.scenario == "slow" or count < 2:
                    return self._json(200, {})
                if state.scenario == "exec_error":
                    return self._json(
                        200,
                        {
                            pid: {
                                "status": {
                                    "status_str": "error",
                                    "completed": False,
                                    "messages": [["execution_error", {"node_id": "3", "exception_message": "CUDA out of memory"}]],
                                },
                                "outputs": {},
                            }
                        },
                    )
                if state.scenario == "empty":
                    return self._json(
                        200, {pid: {"status": {"status_str": "success", "completed": True}, "outputs": {}}}
                    )
                return self._json(
                    200,
                    {
                        pid: {
                            "status": {"status_str": "success", "completed": True},
                            "outputs": {
                                "9": {
                                    "images": [
                                        {"filename": "ComfyUI_0001.png", "subfolder": "", "type": "output"},
                                        {"filename": "ComfyUI_0002.png", "subfolder": "", "type": "output"},
                                    ]
                                }
                            },
                        }
                    },
                )
            if parsed.path == "/view":
                q = urllib.parse.parse_qs(parsed.query)
                name = (q.get("filename") or ["x.png"])[0]
                body = subject if name.endswith("1.png") else flat
                return self._send(200, body, "image/png")
            return self._json(404, {"error": "not found"})

        def do_POST(self):  # noqa: N802 - http.server API
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""
            if state.scenario == "auth":
                return self._json(401, {"error": "unauthorized"})
            if self.path == "/upload/image":
                marker = b'filename="'
                start = raw.find(marker)
                name = "uploaded.png"
                if start != -1:
                    start += len(marker)
                    name = raw[start : raw.find(b'"', start)].decode("utf-8", "replace")
                if state.scenario == "rename":
                    name = "renamed_" + name
                with state.lock:
                    state.uploads[name] = raw
                return self._json(200, {"name": name, "subfolder": "", "type": "input"})
            if self.path == "/prompt":
                try:
                    payload = json.loads(raw.decode("utf-8"))
                except json.JSONDecodeError:
                    return self._json(400, {"error": "bad json"})
                if state.scenario == "node_error":
                    return self._json(
                        400,
                        {
                            "error": {"type": "prompt_outputs_failed_validation"},
                            "node_errors": {
                                "4": {
                                    "errors": [
                                        {
                                            "type": "value_not_in_list",
                                            "message": "ckpt_name: 'missing.safetensors' not in []",
                                        }
                                    ]
                                }
                            },
                        },
                    )
                pid = uuid.uuid4().hex
                with state.lock:
                    state.prompts[pid] = payload
                return self._json(200, {"prompt_id": pid, "number": 1})
            return self._json(404, {"error": "not found"})

    return Handler


def start(scenario: str = "ok") -> tuple[ThreadingHTTPServer, StubState, str]:
    state = StubState(scenario)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(state))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, state, f"http://127.0.0.1:{httpd.server_address[1]}"


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", default="ok")
    ap.add_argument("--port", type=int, default=8188)
    ns = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", ns.port), make_handler(StubState(ns.scenario)))
    print(f"stub ComfyUI on http://127.0.0.1:{ns.port} scenario={ns.scenario}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass