#!/usr/bin/env python3
"""Generic ComfyUI client: upload, submit, poll, download, classify.

Nothing about a particular server, model or graph is baked in. The workflow is
an API-format graph you pass in; every value you want driven is a placeholder
(`{{PROMPT}}`) or an explicit `--set node.input=value` override.

Standard library only (plus Pillow when you ask for alpha statistics).
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

PLACEHOLDER = re.compile(r"\{\{([A-Z0-9_]+)\}\}")

# exit codes are part of the contract: callers branch on the reason, not on logs
EXIT_OK = 0
EXIT_USAGE = 2
EXIT_CONFIG = 3
EXIT_CONNECT = 4
EXIT_AUTH = 5
EXIT_GRAPH = 6
EXIT_EXEC = 7
EXIT_EMPTY = 8
EXIT_TIMEOUT = 9


class ComfyError(Exception):
    def __init__(self, message: str, code: int, detail: dict | None = None):
        super().__init__(message)
        self.code = code
        self.detail = detail or {}


# ---------------------------------------------------------------- transport


def server_url(arg: str | None) -> str:
    raw = arg or os.environ.get("COMFYUI_URL") or ""
    if not raw:
        raise ComfyError(
            "no ComfyUI server configured: pass --server http://host:port or set COMFYUI_URL",
            EXIT_CONFIG,
        )
    return raw.rstrip("/")


def request(
    server: str,
    path: str,
    *,
    data: bytes | None = None,
    headers: dict | None = None,
    timeout: float = 120.0,
    method: str | None = None,
) -> tuple[int, bytes]:
    req = urllib.request.Request(server + path, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except urllib.error.URLError as exc:
        raise ComfyError(f"cannot reach {server}{path}: {exc.reason}", EXIT_CONNECT) from exc
    except TimeoutError as exc:
        raise ComfyError(f"timed out talking to {server}{path}", EXIT_TIMEOUT) from exc


def get_json(server: str, path: str, timeout: float = 120.0) -> dict:
    status, body = request(server, path, timeout=timeout)
    if status in (401, 403):
        raise ComfyError(f"{path} returned {status}: server wants credentials", EXIT_AUTH)
    if status != 200:
        raise ComfyError(f"{path} returned {status}: {body[:300]!r}", EXIT_CONNECT)
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ComfyError(f"{path} did not return JSON: {body[:200]!r}", EXIT_CONNECT) from exc


# ---------------------------------------------------------------- multipart


def multipart(fields: dict, files: dict) -> tuple[bytes, str]:
    boundary = "----comfy" + uuid.uuid4().hex
    out = bytearray()
    for name, value in fields.items():
        out += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode()
    for name, (filename, payload, ctype) in files.items():
        out += (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; filename=\"{filename}\"\r\n"
            f"Content-Type: {ctype}\r\n\r\n"
        ).encode()
        out += payload + b"\r\n"
    out += f"--{boundary}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={boundary}"


def upload(server: str, path: Path) -> str:
    payload = path.read_bytes()
    ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    body, ct = multipart(
        {"type": "input", "subfolder": "", "overwrite": "true"},
        {"image": (path.name, payload, ctype)},
    )
    status, raw = request(
        server, "/upload/image", data=body, headers={"Content-Type": ct}, timeout=300
    )
    if status in (401, 403):
        raise ComfyError("upload rejected: server wants credentials", EXIT_AUTH)
    if status != 200:
        raise ComfyError(f"upload failed ({status}): {raw[:300]!r}", EXIT_CONNECT)
    info = json.loads(raw.decode("utf-8"))
    # the server may rename a colliding file; always use the name it returned
    name = info.get("name")
    if not name:
        raise ComfyError(f"upload response has no name: {info}", EXIT_CONNECT)
    return name


# ---------------------------------------------------------------- graph


def load_graph(path: Path) -> dict:
    if not path.exists():
        raise ComfyError(f"workflow not found: {path}", EXIT_USAGE)
    try:
        graph = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ComfyError(f"workflow is not JSON: {exc}", EXIT_USAGE) from exc
    if isinstance(graph, dict) and "nodes" in graph and "links" in graph:
        raise ComfyError(
            "this is a UI-format workflow: export with Save (API format) instead", EXIT_USAGE
        )
    if not isinstance(graph, dict) or not graph:
        raise ComfyError("workflow must be a non-empty mapping of node id -> node", EXIT_USAGE)
    return graph


def substitute(value, mapping: dict[str, str]):
    if isinstance(value, str):
        whole = PLACEHOLDER.fullmatch(value)
        if whole and whole.group(1) in mapping:
            # keep the native type: seeds and sizes must not arrive as strings
            return mapping[whole.group(1)]
        return PLACEHOLDER.sub(lambda m: str(mapping.get(m.group(1), m.group(0))), value)
    if isinstance(value, list):
        return [substitute(v, mapping) for v in value]
    if isinstance(value, dict):
        return {k: substitute(v, mapping) for k, v in value.items()}
    return value


def unresolved(graph: dict) -> list[str]:
    text = json.dumps(graph)
    return sorted(set(PLACEHOLDER.findall(text)))


def apply_override(graph: dict, expr: str) -> dict:
    """`--set 74.inputs.text=hello` or `--set 3.inputs.seed=42`."""
    if "=" not in expr:
        raise ComfyError(f"--set needs key=value, got {expr!r}", EXIT_USAGE)
    dotted, raw = expr.split("=", 1)
    parts = dotted.split(".")
    node = graph
    for part in parts[:-1]:
        if part not in node:
            raise ComfyError(f"--set path not found: {dotted}", EXIT_USAGE)
        node = node[part]
    if not isinstance(node, dict):
        raise ComfyError(f"--set path is not an object: {dotted}", EXIT_USAGE)
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        value = raw
    node[parts[-1]] = value
    return graph


def dry_run(graph: dict, values: dict, template: Path) -> dict:
    resolved = substitute(graph, values)
    text = json.dumps(resolved, ensure_ascii=False, indent=2)
    return {
        "mode": "dry-run",
        "template": str(template),
        "nodes": len(resolved),
        "placeholders": values,
        "unresolved": unresolved(resolved),
        "graph_chars": len(text),
    }


# ---------------------------------------------------------------- execution


def submit(server: str, graph: dict) -> str:
    body = json.dumps(
        {"prompt": graph, "client_id": uuid.uuid4().hex}, ensure_ascii=False
    ).encode("utf-8")
    status, raw = request(
        server, "/prompt", data=body, headers={"Content-Type": "application/json"}, timeout=120
    )
    if status in (401, 403):
        raise ComfyError("submit rejected: server wants credentials", EXIT_AUTH)
    payload = {}
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        pass
    if status != 200:
        node_errors = payload.get("node_errors") or {}
        if node_errors:
            lines = []
            for node_id, info in node_errors.items():
                for err in info.get("errors", []) or [info]:
                    lines.append(f"node {node_id}: {err.get('message', err)}")
            raise ComfyError(
                "server rejected the graph:\n  " + "\n  ".join(lines), EXIT_GRAPH, payload
            )
        raise ComfyError(f"submit failed ({status}): {raw[:300]!r}", EXIT_GRAPH, payload)
    prompt_id = payload.get("prompt_id")
    if not prompt_id:
        raise ComfyError(f"submit response has no prompt_id: {payload}", EXIT_GRAPH)
    return prompt_id


def wait(server: str, prompt_id: str, timeout: float, interval: float) -> dict:
    deadline = time.time() + timeout
    while True:
        entry = get_json(server, f"/history/{prompt_id}").get(prompt_id)
        if entry:
            status = entry.get("status") or {}
            state = status.get("status_str")
            if state in ("error", "failed"):
                messages = status.get("messages") or []
                raise ComfyError(
                    f"workflow failed ({state}): {json.dumps(messages[:5], ensure_ascii=False)}",
                    EXIT_EXEC,
                    entry,
                )
            if status.get("completed") or entry.get("outputs"):
                return entry
        if time.time() > deadline:
            raise ComfyError(
                f"no result after {timeout:.0f}s (prompt {prompt_id} still queued)", EXIT_TIMEOUT
            )
        time.sleep(interval)


def download(server: str, item: dict, out_dir: Path, name: str) -> Path:
    query = urllib.parse.urlencode(
        {
            "filename": item.get("filename", "output.png"),
            "subfolder": item.get("subfolder", ""),
            "type": item.get("type", "output"),
        }
    )
    status, raw = request(server, f"/view?{query}", timeout=300)
    if status != 200:
        raise ComfyError(f"download failed for {item}: {status}", EXIT_CONNECT)
    target = out_dir / name
    target.write_bytes(raw)
    return target


def alpha_stats(path: Path) -> dict | None:
    try:
        from PIL import Image

        import numpy as np
    except ImportError:
        return None
    with Image.open(path) as im:
        if im.mode not in ("RGBA", "LA"):
            return None
        a = np.asarray(im.convert("RGBA"))[..., 3]
        return {
            "transparent_rate": round(float((a < 50).mean()), 4),
            "opaque_rate": round(float((a > 245).mean()), 4),
        }


def collect(server: str, entry: dict, out_dir: Path, prefix: str) -> list[dict]:
    files: list[dict] = []
    for node_id, output in (entry.get("outputs") or {}).items():
        images = output.get("images") or []
        for i, item in enumerate(images, 1):
            suffix = Path(item.get("filename", "out.png")).suffix or ".png"
            name = f"{prefix}_{node_id}_{i}{suffix}"
            path = download(server, item, out_dir, name)
            record = {"path": str(path), "node": node_id, "file": item.get("filename")}
            stats = alpha_stats(path)
            if stats:
                record.update(stats)
            files.append(record)
    return files


# ---------------------------------------------------------------- commands


def cmd_check(args) -> int:
    server = server_url(args.server)
    stats = get_json(server, "/system_stats")
    devices = stats.get("devices") or []
    summary = {
        "server": server,
        "devices": [
            {"name": d.get("name"), "vram_free": d.get("vram_free"), "vram_total": d.get("vram_total")}
            for d in devices
        ],
        "pillow": _has_pillow(),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return EXIT_OK


def _has_pillow() -> bool:
    try:
        import PIL  # noqa: F401

        return True
    except ImportError:
        return False


def cmd_nodes(args) -> int:
    server = server_url(args.server)
    info = get_json(server, "/object_info", timeout=300)
    needle = (args.filter or "").lower()
    rows = []
    for name, spec in sorted(info.items()):
        if needle and needle not in name.lower():
            continue
        inputs = spec.get("input") or {}
        rows.append(
            {
                "node": name,
                "required": sorted((inputs.get("required") or {}).keys()),
                "optional": sorted((inputs.get("optional") or {}).keys()),
            }
        )
    print(json.dumps({"count": len(rows), "nodes": rows}, ensure_ascii=False, indent=2))
    return EXIT_OK


def cmd_run(args) -> int:
    graph = load_graph(Path(args.workflow))
    values = {
        "PROMPT": args.prompt or "",
        "NEGATIVE": args.negative or "",
        "SEED": args.seed if args.seed is not None else random.randint(0, 2**48),
        "WIDTH": args.width,
        "HEIGHT": args.height,
        "STEPS": args.steps,
        "CFG": args.cfg,
        "PREFIX": args.prefix,
        "MODEL": args.model or "",
    }
    for expr in args.set or []:
        apply_override(graph, expr)

    if args.dry_run:
        print(json.dumps(dry_run(graph, values, Path(args.workflow)), ensure_ascii=False, indent=2))
        return EXIT_OK

    server = server_url(args.server)
    if args.image:
        names = []
        for i, image in enumerate(args.image, 1):
            local = Path(image)
            if not local.exists():
                raise ComfyError(f"image not found: {local}", EXIT_USAGE)
            names.append(upload(server, local))
        values["IMAGE"] = names[0]
        for i, name in enumerate(names, 1):
            values[f"IMAGE_{i}"] = name
        values["IMAGE2"] = names[1] if len(names) > 1 else ""
    resolved = substitute(graph, values)
    missing = unresolved(resolved)
    if missing:
        raise ComfyError(
            "workflow still has placeholders after substitution: " + ", ".join(missing), EXIT_GRAPH
        )

    prompt_id = submit(server, resolved)
    entry = wait(server, prompt_id, args.timeout, args.interval)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    files = collect(server, entry, out_dir, args.prefix)
    if not files:
        raise ComfyError("workflow completed but produced no images", EXIT_EMPTY, entry)
    summary = {
        "status": "ok",
        "prompt_id": prompt_id,
        "seed": values["SEED"],
        "outputs": files,
    }
    print("RESULT_JSON: " + json.dumps(summary, ensure_ascii=False))
    return EXIT_OK


def cmd_history(args) -> int:
    server = server_url(args.server)
    entry = get_json(server, f"/history/{args.prompt_id}").get(args.prompt_id) or {}
    print(json.dumps(entry, ensure_ascii=False, indent=2))
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Generic ComfyUI client")
    ap.add_argument("--server", help="http://host:port (overrides COMFYUI_URL)")
    ap.add_argument("--json", action="store_true", help="accepted for scripting symmetry")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="dependencies and /system_stats")
    c.set_defaults(func=cmd_check)

    n = sub.add_parser("nodes", help="list node classes from /object_info")
    n.add_argument("--filter")
    n.set_defaults(func=cmd_nodes)

    r = sub.add_parser("run", help="submit a workflow and download its outputs")
    r.add_argument("--workflow", required=True, help="API-format graph with placeholders")
    r.add_argument("--image", action="append", help="image to upload; repeat for more")
    r.add_argument("--prompt")
    r.add_argument("--negative")
    r.add_argument("--seed", type=int)
    r.add_argument("--width", type=int, default=1024)
    r.add_argument("--height", type=int, default=1024)
    r.add_argument("--steps", type=int, default=20)
    r.add_argument("--cfg", type=float, default=7.0)
    r.add_argument("--model")
    r.add_argument("--prefix", default="comfy")
    r.add_argument("--output-dir", default=".")
    r.add_argument("--set", action="append", metavar="NODE.FIELD=VALUE")
    r.add_argument("--timeout", type=float, default=600.0)
    r.add_argument("--interval", type=float, default=3.0)
    r.add_argument("--dry-run", action="store_true")
    r.set_defaults(func=cmd_run)

    h = sub.add_parser("history", help="print one history entry")
    h.add_argument("prompt_id")
    h.set_defaults(func=cmd_history)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except ComfyError as exc:
        payload = {"error": str(exc), "code": exc.code}
        if exc.detail:
            payload["detail"] = exc.detail
        print("error: " + json.dumps(payload, ensure_ascii=False), file=sys.stderr)
        return exc.code
    except KeyboardInterrupt:
        print("error: interrupted", file=sys.stderr)
        return EXIT_EXEC


if __name__ == "__main__":
    raise SystemExit(main())