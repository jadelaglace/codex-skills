#!/usr/bin/env python3
"""Minimal OpenAI-compatible chat client with honest failure reporting.

Talks to any server that implements `POST {base}/chat/completions`: vLLM, SGLang,
LM Studio, Ollama's OpenAI endpoint, or a hosted gateway. No endpoint, key or
model name is built in.

    python scripts/llm.py --prompt "..." --model my-model
    echo "long text" | python scripts/llm.py --system "summarise" --stdin
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_CONFIG = 3
EXIT_CONNECT = 4
EXIT_AUTH = 5
EXIT_API = 6
EXIT_EMPTY = 7


class LLMError(Exception):
    def __init__(self, message: str, code: int, detail: dict | None = None):
        super().__init__(message)
        self.code = code
        self.detail = detail or {}


def base_url(arg: str | None) -> str:
    raw = (arg or os.environ.get("LLM_BASE_URL") or "").rstrip("/")
    if not raw:
        raise LLMError(
            "no base URL: pass --base-url https://host/v1 or set LLM_BASE_URL", EXIT_CONFIG
        )
    return raw


def payload_for(args, prompt: str) -> dict:
    body: dict = {
        "model": args.model,
        "messages": [],
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
    }
    if args.system:
        body["messages"].append({"role": "system", "content": args.system})
    body["messages"].append({"role": "user", "content": prompt})
    if args.json_mode:
        body["response_format"] = {"type": "json_object"}
    if args.think:
        if args.think_style == "template":
            body["chat_template_kwargs"] = {"enable_thinking": args.think == "on"}
        elif args.think == "off":
            body["reasoning_effort"] = "none"
        else:
            body["reasoning_effort"] = args.think
    if args.stop:
        body["stop"] = args.stop
    return body


def call(url: str, key: str | None, body: dict, timeout: float) -> dict:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read()[:400].decode("utf-8", "replace")
        if exc.code in (401, 403):
            raise LLMError(f"server rejected the key ({exc.code}): {detail}", EXIT_AUTH) from exc
        raise LLMError(f"HTTP {exc.code}: {detail}", EXIT_API) from exc
    except urllib.error.URLError as exc:
        raise LLMError(f"cannot reach {url}: {exc.reason}", EXIT_CONNECT) from exc
    except TimeoutError as exc:
        raise LLMError(f"timed out after {timeout:.0f}s", EXIT_CONNECT) from exc
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LLMError(f"response is not JSON: {raw[:200]!r}", EXIT_API) from exc


def extract(reply: dict) -> tuple[str, str, dict]:
    """Return (text, reasoning, usage) and refuse to guess when both are empty."""
    choices = reply.get("choices") or []
    if not choices:
        raise LLMError(f"no choices in response: {json.dumps(reply)[:300]}", EXIT_EMPTY)
    choice = choices[0]
    message = choice.get("message") or {}
    text = (message.get("content") or "").strip()
    reasoning = (message.get("reasoning_content") or "").strip()
    usage = reply.get("usage") or {}
    finish = choice.get("finish_reason")
    if finish and finish != "stop":
        print(
            f"warning: finish_reason={finish} — the reply may be truncated; raise --max-tokens "
            "or shorten the prompt",
            file=sys.stderr,
        )
    if not text and reasoning:
        print(
            "warning: content is empty but reasoning_content is not — the thinking phase "
            "consumed the budget; raise --max-tokens or turn thinking off",
            file=sys.stderr,
        )
        return reasoning, reasoning, usage
    if not text:
        raise LLMError("empty reply: both content and reasoning_content are blank", EXIT_EMPTY)
    return text, reasoning, usage


def run(args) -> int:
    prompt = args.prompt
    if args.stdin:
        prompt = sys.stdin.read()
    if not prompt or not prompt.strip():
        raise LLMError("no prompt: pass --prompt or --stdin", EXIT_USAGE)

    body = payload_for(args, prompt)
    if args.dry_run:
        raw_base = (args.base_url or os.environ.get("LLM_BASE_URL") or "").rstrip("/")
        url = (raw_base or "<unset: LLM_BASE_URL>") + "/chat/completions"
        print(json.dumps({"url": url, "body": body}, ensure_ascii=False, indent=2))
        return EXIT_OK

    url = base_url(args.base_url) + "/chat/completions"
    key = args.api_key or os.environ.get("LLM_API_KEY")
    attempts = 2 if args.retry else 1
    last: LLMError | None = None
    for attempt in range(1, attempts + 1):
        try:
            reply = call(url, key, body, args.timeout)
            break
        except LLMError as exc:
            last = exc
            if attempt == attempts or exc.code not in (EXIT_CONNECT, EXIT_API):
                raise
            print(f"warning: attempt {attempt} failed ({exc}); retrying once", file=sys.stderr)
            time.sleep(args.retry_delay)
    else:  # pragma: no cover - loop always breaks or raises
        raise last or LLMError("unknown failure", EXIT_API)

    text, reasoning, usage = extract(reply)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {len(text)} chars to {args.out}", file=sys.stderr)
    if args.json:
        print(
            json.dumps(
                {
                    "status": "ok",
                    "model": reply.get("model") or args.model,
                    "text": text,
                    "chars": len(text),
                    "reasoning_chars": len(reasoning),
                    "usage": usage,
                },
                ensure_ascii=False,
            )
        )
    elif not args.out:
        print(text)
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="OpenAI-compatible chat client")
    ap.add_argument("--base-url", help="e.g. http://host:8000/v1 (or LLM_BASE_URL)")
    ap.add_argument("--api-key", help="bearer token (or LLM_API_KEY)")
    ap.add_argument("--model", required=False, default=os.environ.get("LLM_MODEL", ""))
    ap.add_argument("--prompt")
    ap.add_argument("--stdin", action="store_true", help="read the prompt from stdin")
    ap.add_argument("--system")
    ap.add_argument("--max-tokens", type=int, default=1024)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--stop", action="append")
    ap.add_argument("--think", choices=["on", "off", "low", "medium", "high"])
    ap.add_argument(
        "--think-style",
        choices=["effort", "template"],
        default="effort",
        help="effort: reasoning_effort (OpenAI/gateway); template: chat_template_kwargs (vLLM/Qwen)",
    )
    ap.add_argument("--json-mode", action="store_true")
    ap.add_argument("--json", action="store_true", help="print a machine-readable envelope")
    ap.add_argument("--out", help="write the text to a file instead of stdout")
    ap.add_argument("--timeout", type=float, default=120.0)
    ap.add_argument("--retry", action="store_true", help="retry once on connect/5xx")
    ap.add_argument("--retry-delay", type=float, default=2.0)
    ap.add_argument("--dry-run", action="store_true", help="print the request and stop")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.model:
        args.model = "default"
    try:
        return run(args)
    except LLMError as exc:
        payload = {"error": str(exc), "code": exc.code}
        print("error: " + json.dumps(payload, ensure_ascii=False), file=sys.stderr)
        return exc.code
    except KeyboardInterrupt:
        return EXIT_API


if __name__ == "__main__":
    raise SystemExit(main())