#!/usr/bin/env python3
"""Submit a layered-decomposition workflow to a ComfyUI server.

The graph itself is not hard-coded here: export the API-format workflow from the
ComfyUI instance that has the layering model installed, replace the values you
want to drive with the placeholders below, and pass it with --workflow.

Placeholders (exact string values anywhere in the graph):
  {{IMAGE}}   uploaded input filename
  {{PROMPT}}  layering prompt
  {{LAYERS}}  layer count
  {{SEED}}    seed
  {{PREFIX}}  output filename prefix

Commands run in this order: preflight (--check / GET /system_stats), upload,
submit, poll /history, download /view, classify and rename outputs.

Standard library only. Nothing is uploaded until --check has been run in the
same invocation, so a wrong host fails before any file leaves the machine.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import time
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PLACEHOLDERS = ("IMAGE", "PROMPT", "LAYERS", "SEED", "PREFIX")
DEFAULT_TEMPLATE = Path(__file__).resolve().parent.parent / "references" / "workflow.example.json"


def _request(url: str, data: bytes | None = None, headers: dict | None = None, timeout: float = 30.0) -> bytes:
    req = Request(url, data=data, headers=headers or {})
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:2000]
        raise RuntimeError(f"HTTP {exc.code} from {url}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"cannot reach {url}: {exc.reason}") from exc


def _json(url: str, payload: dict | None = None, timeout: float = 30.0) -> dict:
    if payload is None:
        return json.loads(_request(url, timeout=timeout))
    body = json.dumps(payload).encode("utf-8")
    return json.loads(_request(url, body, {"Content-Type": "application/json"}, timeout))


def server_url(cli_value: str | None) -> str:
    raw = cli_value or os.environ.get("COMFYUI_URL", "")
    if not raw.strip():
        raise SystemExit(
            "no ComfyUI server configured: pass --server http://host:port or set COMFYUI_URL"
        )
    return raw.strip().rstrip("/")


def check(server: str) -> dict:
    stats = _json(f"{server}/system_stats")
    devices = []
    for dev in stats.get("devices", []) or []:
        devices.append(
            {
                "name": dev.get("name"),
                "type": dev.get("type"),
                "vram_total_gb": round((dev.get("vram_total") or 0) / 1e9, 2),
                "vram_free_gb": round((dev.get("vram_free") or 0) / 1e9, 2),
            }
        )
    return {"server": server, "devices": devices}


def load_template(path: str | None) -> tuple[dict, str]:
    if path:
        p = Path(path)
    elif DEFAULT_TEMPLATE.exists():
        p = DEFAULT_TEMPLATE
    else:
        raise SystemExit(
            "no workflow given: export the API-format graph from your ComfyUI instance and pass "
            "--workflow path/to/workflow.json (see references/workflow.md for the placeholders)"
        )
    graph = json.loads(p.read_text(encoding="utf-8"))
    text = json.dumps(graph)
    missing = [k for k in PLACEHOLDERS if "{{" + k + "}}" not in text]
    if missing:
        raise SystemExit(f"template {p} is missing placeholders: {', '.join(missing)}")
    return graph, str(p)


def substitute(node, values: dict):
    if isinstance(node, dict):
        return {k: substitute(v, values) for k, v in node.items()}
    if isinstance(node, list):
        return [substitute(v, values) for v in node]
    if isinstance(node, str):
        for key, val in values.items():
            token = "{{" + key + "}}"
            if node == token:
                return val
            node = node.replace(token, str(val))
        return node
    return node


def upload(server: str, path: Path, name: str) -> dict:
    boundary = "----comfy" + uuid.uuid4().hex
    ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    parts = [
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n".encode(),
        (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\n"
            f"Content-Type: {ctype}\r\n\r\n"
        ).encode(),
        path.read_bytes(),
        f"\r\n--{boundary}--\r\n".encode(),
    ]
    body = b"".join(parts)
    raw = _request(
        f"{server}/upload/image",
        body,
        {"Content-Type": f"multipart/form-data; boundary={boundary}"},
        timeout=300,
    )
    return json.loads(raw)


def submit(server: str, graph: dict, client_id: str) -> str:
    res = _json(f"{server}/prompt", {"prompt": graph, "client_id": client_id})
    if res.get("node_errors"):
        raise RuntimeError(f"server rejected the graph: {json.dumps(res['node_errors'])[:1500]}")
    pid = res.get("prompt_id")
    if not pid:
        raise RuntimeError(f"no prompt_id in response: {json.dumps(res)[:800]}")
    return pid


def wait(server: str, pid: str, timeout: float) -> dict:
    deadline = time.time() + timeout
    last = ""
    while time.time() < deadline:
        hist = _json(f"{server}/history/{pid}")
        entry = hist.get(pid)
        if entry:
            status = entry.get("status", {})
            if status.get("status_str") == "error" or status.get("completed") is False:
                msgs = status.get("messages", [])
                raise RuntimeError(f"workflow failed: {json.dumps(msgs)[:1500]}")
            if entry.get("outputs"):
                return entry
            last = json.dumps(status)[:300]
        time.sleep(2.0)
    raise TimeoutError(f"no result after {timeout:.0f}s (last status: {last or 'pending'})")


def download(server: str, item: dict, out_dir: Path) -> Path:
    q = urlencode(
        {
            "filename": item["filename"],
            "subfolder": item.get("subfolder", ""),
            "type": item.get("type", "output"),
        }
    )
    data = _request(f"{server}/view?{q}", timeout=300)
    target = out_dir / Path(item["filename"]).name
    target.write_bytes(data)
    return target


def alpha_stats(path: Path) -> dict:
    try:
        from PIL import Image
    except ImportError:
        return {"error": "Pillow not installed"}
    import numpy as np

    with Image.open(path) as im:
        rgba = im.convert("RGBA")
        a = np.asarray(rgba)[..., 3].astype("float32")
        return {
            "width": rgba.width,
            "height": rgba.height,
            "has_alpha": bool(im.mode in ("RGBA", "LA")),
            "transparent_rate": round(float((a < 50).mean()), 4),
            "opaque_rate": round(float((a > 245).mean()), 4),
            "min_alpha": int(a.min()),
            "max_alpha": int(a.max()),
            "mean_alpha": round(float(a.mean()) / 255.0, 4),
        }


def _thumb_mad(a: Path, b: Path) -> float:
    """Mean |diff| of two 256x256 LANCZOS thumbnails, used to spot the composite."""
    from PIL import Image
    import numpy as np

    with Image.open(a) as ia, Image.open(b) as ib:
        ta = ia.convert("RGB").resize((256, 256), Image.LANCZOS)
        tb = ib.convert("RGB").resize((256, 256), Image.LANCZOS)
        return float(np.abs(np.asarray(ta, "int16") - np.asarray(tb, "int16")).mean())


def classify(files: list[Path], layers: int, reference: Path | None = None) -> list[tuple[Path, str]]:
    """Name outputs by measured alpha; node order is not a reliable role signal."""
    stats = [(p, alpha_stats(p)) for p in files]
    out: list[tuple[Path, str]] = []
    subjects = [(p, s) for p, s in stats if s.get("transparent_rate", 0) > 0.25]
    for i, (p, _s) in enumerate(subjects, 1):
        out.append((p, f"subject_{i}"))
    rest = [p for p, s in stats if s.get("transparent_rate", 0) <= 0.25]
    if rest:
        if reference is not None and len(rest) > 1:
            scored = sorted(rest, key=lambda p: _thumb_mad(p, reference))
            composite, backgrounds = scored[0], scored[1:]
        else:
            composite, backgrounds = rest[0], rest[1:]
        out.append((composite, "composite"))
        for i, p in enumerate(backgrounds, 1):
            out.append((p, f"background_{i}"))
    return out


def dry_run(graph: dict, values: dict, template: str) -> dict:
    resolved = substitute(graph, values)
    text = json.dumps(resolved, ensure_ascii=False, indent=2)
    return {
        "command": "run-layered-workflow",
        "mode": "dry-run",
        "template": template,
        "placeholders": values,
        "nodes": len(graph),
        "graph_chars": len(text),
        "unresolved": [p for p in PLACEHOLDERS if "{{" + p + "}}" in text],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Run a ComfyUI layered-decomposition workflow")
    ap.add_argument("--image", help="input image (uploaded as-is)")
    ap.add_argument("--prompt", help="layering prompt")
    ap.add_argument("--layers", type=int, default=2)
    ap.add_argument("--prefix", default="layered")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--output-dir", default=".")
    ap.add_argument("--server", help="http://host:port (overrides COMFYUI_URL)")
    ap.add_argument("--timeout", type=float, default=600.0)
    ap.add_argument("--workflow", help="API-format graph JSON with placeholders")
    ap.add_argument("--check", action="store_true", help="preflight only")
    ap.add_argument("--install-mode", action="store_true", help="check dependencies and reachability only")
    ap.add_argument("--restore-size", action="store_true", help="also write subject layers at the source size")
    ap.add_argument("--dry-run", action="store_true", help="resolve the graph, touch nothing")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    server = None
    if args.install_mode or args.check:
        try:
            server = server_url(args.server)
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        try:
            info = check(server)
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(info, ensure_ascii=False, indent=2))
        print("preflight ok: dependencies importable, server reachable")
        return 0

    graph, template = load_template(args.workflow)

    if not args.image or not args.prompt:
        print("error: --image and --prompt are required unless --check is used", file=sys.stderr)
        return 2

    values = {
        "IMAGE": Path(args.image).name,
        "PROMPT": args.prompt,
        "LAYERS": args.layers,
        "SEED": args.seed,
        "PREFIX": args.prefix,
    }

    if args.dry_run:
        info = dry_run(graph, values, template)
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        server = server_url(args.server)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        pre = check(server)  # fail before uploading anything
        up = upload(server, Path(args.image), Path(args.image).name)
        values["IMAGE"] = up.get("name", values["IMAGE"])
        resolved = substitute(graph, values)
        pid = submit(server, resolved, uuid.uuid4().hex)
        entry = wait(server, pid, args.timeout)

        files: list[Path] = []
        for node in entry.get("outputs", {}).values():
            for item in node.get("images", []) or []:
                files.append(download(server, item, out_dir))
        if not files:
            raise RuntimeError("workflow finished but produced no images")
        named = classify(files, args.layers, Path(args.image))
        renamed: list[tuple[Path, str]] = []
        for path, role in named:
            target = path.with_name(f"{args.prefix}_{role}{path.suffix}")
            path.rename(target)
            renamed.append((target, role))
            if args.restore_size and role.startswith("subject"):
                from PIL import Image

                with Image.open(args.image) as src, Image.open(target) as lay:
                    full = lay.resize(src.size, Image.LANCZOS)
                    full.save(target.with_name(f"{target.stem}_full{target.suffix}"))
        summary = {
            "status": "ok",
            "command": "run-layered-workflow",
            "server": server,
            "devices": pre["devices"],
            "prompt_id": pid,
            "prefix": args.prefix,
            "outputs": [
                {
                    "path": str(p),
                    "role": r,
                    "transparent_rate": alpha_stats(p).get("transparent_rate"),
                }
                for p, r in renamed
            ],
        }
    except (RuntimeError, TimeoutError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print("RESULT_JSON: " + json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())