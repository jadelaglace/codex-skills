#!/usr/bin/env python3
"""HTTP probe that reports what a browser would see, not what curl prints.

Built for remote-service triage: status, header list (duplicates preserved),
content type and charset, body prefix, and elapsed time — the four things that
decide whether a failure is the app, the proxy, or the network.

    python scripts/probe.py --url http://127.0.0.1:8000/health
    python scripts/probe.py --url http://host/api --method POST --header "X-K: v" --data '{"a":1}'
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_CONNECT = 4
EXIT_TIMEOUT = 5


def probe(url: str, method: str, headers: list[str], data: str | None, timeout: float, limit: int) -> dict:
    parsed = {}
    for raw in headers:
        if ":" not in raw:
            raise SystemExit(f"error: --header needs 'Name: value', got {raw!r}")
        name, value = raw.split(":", 1)
        parsed[name.strip()] = value.strip()

    body = data.encode("utf-8") if data is not None else None
    if body is not None and not any(k.lower() == "content-type" for k in parsed):
        parsed["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=body, headers=parsed, method=method.upper())
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw_body = response.read(limit)
            status = response.status
            version = response.version
            items = response.getheaders()
    except urllib.error.HTTPError as exc:
        raw_body = exc.read(limit)
        status = exc.code
        version = exc.version
        items = exc.headers.items()
    except urllib.error.URLError as exc:
        return {"ok": False, "error": f"cannot reach {url}: {exc.reason}", "code": EXIT_CONNECT}
    except TimeoutError:
        return {"ok": False, "error": f"no response within {timeout:.1f}s", "code": EXIT_TIMEOUT}

    elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
    pairs = [[name, value] for name, value in items]
    seen: dict[str, int] = {}
    for name, _value in pairs:
        key = name.lower()
        seen[key] = seen.get(key, 0) + 1
    duplicates = {name: count for name, count in seen.items() if count > 1}

    content_type = ""
    charset = ""
    for name, value in pairs:
        if name.lower() == "content-type":
            content_type = value
            if "charset=" in value.lower():
                charset = value.lower().split("charset=", 1)[1].split(";")[0].strip()
    text = raw_body.decode(charset or "utf-8", "replace")

    patterns: list[str] = []
    if content_type.startswith("text/") and not charset:
        patterns.append("text/* without charset: the client guesses encoding")
    if duplicates:
        patterns.append(f"duplicate headers ({', '.join(sorted(duplicates))}): a proxy may have collapsed a list into a comma string")
    if status >= 500:
        patterns.append("5xx from the app or the proxy; check which one in the body")
    if content_type.startswith("text/html") and text.lstrip()[:1] in ("{", "["):
        patterns.append("HTML content-type with a JSON body: the proxy is rewriting responses")

    return {
        "ok": True,
        "url": url,
        "method": method.upper(),
        "status": status,
        "http_version": {11: "1.1", 10: "1.0", 9: "0.9", 20: "2"}.get(version, str(version)),
        "elapsed_ms": elapsed_ms,
        "content_type": content_type,
        "charset": charset or None,
        "duplicate_headers": duplicates,
        "headers": pairs,
        "body_prefix": text[:limit],
        "body_chars": len(text),
        "patterns": patterns,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="HTTP probe for service triage")
    ap.add_argument("--url", required=True)
    ap.add_argument("--method", default="GET")
    ap.add_argument("--header", action="append", default=[])
    ap.add_argument("--data")
    ap.add_argument("--timeout", type=float, default=10.0)
    ap.add_argument("--limit", type=int, default=400)
    args = ap.parse_args(argv)

    if not args.url.startswith(("http://", "https://")):
        print("error: --url must start with http:// or https://", file=sys.stderr)
        return EXIT_USAGE

    result = probe(args.url, args.method, args.header, args.data, args.timeout, args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else result.get("code", EXIT_CONNECT)


if __name__ == "__main__":
    raise SystemExit(main())