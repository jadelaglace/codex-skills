#!/usr/bin/env python3
"""Generic Gitea API client: one `api` command, no hardcoded instance.

    python scripts/gitea.py api GET /repos/me/proj/issues
    python scripts/gitea.py api POST /repos/me/proj/issues --data '{"title":"x"}'
    python scripts/gitea.py pr-merge --owner me --repo proj --number 7 --style squash
    python scripts/gitea.py issue-close --owner me --repo proj --number 12

Base URL comes from --base-url or GITEA_URL; the token from --token or
GITEA_TOKEN. Nothing is baked in, because the same API serves every instance.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_CONFIG = 3
EXIT_CONNECT = 4
EXIT_AUTH = 5
EXIT_API = 6


class GiteaError(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code


def config(args) -> tuple[str, str]:
    base = (args.base_url or os.environ.get("GITEA_URL") or "").rstrip("/")
    if not base:
        raise GiteaError("no base URL: pass --base-url https://git.example.com/api/v1 or set GITEA_URL", EXIT_CONFIG)
    if not base.endswith("/api/v1"):
        base += "/api/v1"
    token = args.token or os.environ.get("GITEA_TOKEN") or ""
    if not token:
        raise GiteaError("no token: pass --token or set GITEA_TOKEN", EXIT_CONFIG)
    return base, token


def api(base: str, token: str, method: str, path: str, data: dict | None, timeout: float) -> tuple[int, object]:
    url = base + path
    body = json.dumps(data, ensure_ascii=False).encode("utf-8") if data is not None else None
    headers = {"Authorization": f"token {token}", "Accept": "application/json"}
    if body:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            status = resp.status
    except urllib.error.HTTPError as exc:
        detail = exc.read()[:400].decode("utf-8", "replace")
        if exc.code in (401, 403):
            raise GiteaError(f"{method} {path} -> {exc.code}: token rejected or lacks scope ({detail})", EXIT_AUTH) from exc
        raise GiteaError(f"{method} {path} -> {exc.code}: {detail}", EXIT_API) from exc
    except urllib.error.URLError as exc:
        raise GiteaError(f"cannot reach {url}: {exc.reason}", EXIT_CONNECT) from exc
    try:
        return status, json.loads(raw.decode("utf-8")) if raw else {}
    except (UnicodeDecodeError, json.JSONDecodeError):
        return status, {"raw": raw[:400].decode("utf-8", "replace")}


def repo_path(owner: str, repo: str) -> str:
    return f"/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}"


def cmd_api(args) -> int:
    data = None
    if args.data:
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as exc:
            raise GiteaError(f"--data is not JSON: {exc}", EXIT_USAGE) from exc
    base, token = config(args)
    status, payload = api(base, token, args.method, args.path, data, args.timeout)
    print(json.dumps({"status": status, "body": payload}, ensure_ascii=False, indent=2))
    return EXIT_OK


def cmd_pr_merge(args) -> int:
    base, token = config(args)
    path = repo_path(args.owner, args.repo) + f"/pulls/{args.number}/merge"
    payload = {"Do": args.style, "delete_branch_after_merge": args.delete_branch}
    status, response = api(base, token, "POST", path, payload, args.timeout)
    print(json.dumps({"status": status, "merge": response}, ensure_ascii=False, indent=2))
    return EXIT_OK


def cmd_issue_close(args) -> int:
    base, token = config(args)
    path = repo_path(args.owner, args.repo) + f"/issues/{args.number}"
    status, response = api(base, token, "PATCH", path, {"state": "closed"}, args.timeout)
    print(json.dumps({"status": status, "issue": response.get("number") if isinstance(response, dict) else None}, ensure_ascii=False))
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Gitea API client")
    ap.add_argument("--base-url", help="https://host (or GITEA_URL); /api/v1 is appended")
    ap.add_argument("--token", help="access token (or GITEA_TOKEN)")
    ap.add_argument("--timeout", type=float, default=60.0)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("api", help="call any endpoint")
    a.add_argument("method")
    a.add_argument("path", help="e.g. /repos/owner/repo/issues (the /api/v1 prefix is added for you)")
    a.add_argument("--data", help="JSON request body")
    a.set_defaults(func=cmd_api)

    m = sub.add_parser("pr-merge", help="merge a pull request")
    m.add_argument("--owner", required=True)
    m.add_argument("--repo", required=True)
    m.add_argument("--number", type=int, required=True)
    m.add_argument("--style", choices=["merge", "rebase", "rebase-merge", "squash", "fast-forward-only"], default="squash")
    m.add_argument("--delete-branch", action="store_true")
    m.set_defaults(func=cmd_pr_merge)

    c = sub.add_parser("issue-close", help="close an issue")
    c.add_argument("--owner", required=True)
    c.add_argument("--repo", required=True)
    c.add_argument("--number", type=int, required=True)
    c.set_defaults(func=cmd_issue_close)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except GiteaError as exc:
        print("error: " + json.dumps({"error": str(exc), "code": exc.code}, ensure_ascii=False), file=sys.stderr)
        return exc.code


if __name__ == "__main__":
    raise SystemExit(main())