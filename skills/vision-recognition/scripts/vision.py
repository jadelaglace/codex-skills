#!/usr/bin/env python3
"""Call a vision model for image understanding when the host model cannot see images.

Two providers are supported and selected explicitly or by `auto`:

  openai  Any OpenAI-compatible /chat/completions endpoint. Configure with
          VISION_BASE_URL, VISION_MODEL, VISION_API_KEY (or the matching flags).
  bl      The local Bailian CLI (`bl vision describe`). Useful on machines that
          already have Bailian configured but no directly exported API key.

The script never stores or prints credentials. It prints the model's text answer
to stdout; diagnostics go to stderr.
"""

from __future__ import annotations

import argparse
import base64
import json
import locale
import mimetypes
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

DEFAULT_BL_MODEL = "qwen3-vl-plus"


def _fail(message: str, code: int = 2) -> "NoReturn":
    sys.stderr.write(message.rstrip() + "\n")
    raise SystemExit(code)


def _data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _verify_images(paths: list[str]) -> list[Path]:
    result = []
    for raw in paths:
        path = Path(raw)
        if not path.is_file():
            _fail(f"image not found: {raw}")
        try:
            with Image.open(path) as im:
                im.verify()
        except Exception as exc:  # noqa: BLE001 - surface decoder reason
            _fail(f"cannot decode image {raw}: {exc}")
        result.append(path)
    return result


def _compose(paths: list[Path]) -> Path:
    """Place images side by side with A/B labels for single-image providers."""
    images = []
    for path in paths:
        im = Image.open(path)
        im.load()
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        images.append(im)
    height = max(im.height for im in images)
    gap = 28
    width = sum(im.width for im in images) + gap * (len(images) - 1)
    canvas = Image.new("RGB", (width, height + 28), "white")
    draw = ImageDraw.Draw(canvas)
    x = 0
    for index, im in enumerate(images):
        if im.height != height:
            scale = height / im.height
            im = im.resize((max(1, round(im.width * scale)), height), Image.Resampling.LANCZOS)
        canvas.paste(im, (x, 28))
        draw.text((x + 6, 6), chr(ord("A") + index), fill="black")
        x += im.width + gap
    handle = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    handle.close()
    out = Path(handle.name)
    canvas.save(out)
    return out


def _openai_request(
    base_url: str,
    model: str,
    api_key: str,
    prompt: str,
    images: list[Path],
    max_tokens: int,
    timeout: int,
) -> dict:
    content: list[dict] = [{"type": "text", "text": prompt}]
    for path in images:
        content.append({"type": "image_url", "image_url": {"url": _data_uri(path)}})
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": content}],
    }
    request = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:800]
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"network error: {exc.reason}") from exc


def _message_text(message: dict) -> str:
    content = message.get("content")
    if isinstance(content, str) and content.strip():
        return content.strip()
    if isinstance(content, list):
        parts = [p.get("text", "") for p in content if isinstance(p, dict) and p.get("type") == "text"]
        text = "\n".join(part for part in parts if part.strip())
        if text.strip():
            return text.strip()
    reasoning = message.get("reasoning_content")
    if isinstance(reasoning, str) and reasoning.strip():
        raise RuntimeError(
            "model returned only reasoning_content; increase --max-tokens or simplify the question"
        )
    raise RuntimeError("model returned empty content")


def _call_openai(args: argparse.Namespace, images: list[Path]) -> dict:
    base_url = args.base_url or os.environ.get("VISION_BASE_URL", "")
    api_key = args.api_key or os.environ.get("VISION_API_KEY", "")
    model = args.model or os.environ.get("VISION_MODEL", "")
    missing = [name for name, value in (("base URL", base_url), ("API key", api_key), ("model", model)) if not value]
    if missing:
        _fail(
            "openai provider is not configured; missing " + ", ".join(missing) + ".\n"
            "Set VISION_BASE_URL / VISION_MODEL / VISION_API_KEY or pass "
            "--base-url / --model / --api-key."
        )
    models = [model]
    for extra in (os.environ.get("VISION_FALLBACK_MODELS") or "").split(","):
        extra = extra.strip()
        if extra and extra not in models:
            models.append(extra)
    last_error: Exception | None = None
    for candidate in models:
        try:
            response = _openai_request(
                base_url, candidate, api_key, args.prompt, images, args.max_tokens, args.timeout
            )
            choice = (response.get("choices") or [{}])[0]
            text = _message_text(choice.get("message") or {})
            return {
                "provider": "openai",
                "model": candidate,
                "content": text,
                "finish_reason": choice.get("finish_reason"),
                "usage": response.get("usage"),
                "warnings": _warnings(choice.get("finish_reason")),
            }
        except RuntimeError as exc:
            last_error = exc
    raise RuntimeError(f"all configured models failed: {last_error}")


def _warnings(finish_reason: str | None) -> list[str]:
    warnings = []
    if finish_reason == "length":
        warnings.append("finish_reason=length: answer may be truncated; raise --max-tokens or narrow the question")
    elif finish_reason not in (None, "stop"):
        warnings.append(f"finish_reason={finish_reason}: inspect the answer before trusting it")
    return warnings


def _decode_console(data: bytes) -> str:
    """Decode CLI output that may be UTF-8 or the Windows ANSI code page."""
    if not data:
        return ""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        pass
    for encoding in (locale.getpreferredencoding(False), "gb18030"):
        try:
            return data.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    return data.decode("utf-8", "replace")


def _call_bl(args: argparse.Namespace, images: list[Path]) -> dict:
    executable = shutil.which(args.bl_command)
    if not executable:
        _fail(f"bl provider unavailable: '{args.bl_command}' was not found on PATH")
    model = args.model or os.environ.get("VISION_MODEL") or DEFAULT_BL_MODEL
    composed: Path | None = None
    target = images[0]
    prompt = args.prompt
    if len(images) > 1:
        composed = _compose(images)
        target = composed
        prompt = (
            "图中从左到右依次为 A、B 两张图。请分别理解，再按用户问题作答。\n\n" + args.prompt
        )
    command = [
        executable,
        "vision",
        "describe",
        "--image",
        str(target),
        "--prompt",
        prompt,
        "--model",
        model,
        "--timeout",
        str(args.timeout),
    ]
    try:
        completed = subprocess.run(
            command, capture_output=True, timeout=args.timeout + 30
        )
    finally:
        if composed is not None:
            composed.unlink(missing_ok=True)
    stdout = _decode_console(completed.stdout)
    stderr = _decode_console(completed.stderr)
    if completed.returncode != 0:
        raise RuntimeError(
            f"bl exited {completed.returncode}: {(stderr or stdout).strip()[:800]}"
        )
    text = stdout.strip()
    if not text:
        raise RuntimeError("bl returned no text")
    return {
        "provider": "bl",
        "model": model,
        "content": text,
        "finish_reason": None,
        "usage": None,
        "warnings": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--image", action="append", required=True, help="image path; repeat for multi-image")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--provider", choices=["auto", "openai", "bl"], default="auto")
    parser.add_argument("--model")
    parser.add_argument("--base-url")
    parser.add_argument("--api-key")
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--bl-command", default="bl")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    images = _verify_images(args.image)
    provider = args.provider
    if provider == "auto":
        if args.base_url or args.api_key or os.environ.get("VISION_BASE_URL") or os.environ.get("VISION_API_KEY"):
            provider = "openai"
        elif shutil.which(args.bl_command):
            provider = "bl"
        else:
            _fail(
                "no vision backend is available. Configure an OpenAI-compatible endpoint with "
                "VISION_BASE_URL / VISION_MODEL / VISION_API_KEY, or install the Bailian CLI (`bl`)."
            )

    try:
        result = _call_openai(args, images) if provider == "openai" else _call_bl(args, images)
    except RuntimeError as exc:
        _fail(str(exc), 1)

    for warning in result.pop("warnings"):
        sys.stderr.write("warning: " + warning + "\n")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["content"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())