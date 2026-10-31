---
name: gitea
description: >-
  Talk to any Gitea instance over its REST API: create and close issues, open
  and merge pull requests (squash by default), delete branches, and call any
  endpoint the client does not wrap. Use when asked to file an issue on a
  self-hosted Gitea, open or merge a PR without a browser, script a board
  update, or hit a Gitea API path directly. Keywords — Gitea, 私有 git, issue,
  PR, 合并请求, squash, API, token, delete branch, 建仓, 提 issue, 合并.
  Branch and commit conventions belong to git-workflow; this skill only moves
  API calls.
metadata:
  version: "1.0.0"
---

# Gitea

Gitea's REST API is the same everywhere: `/api/v1` plus a token. The only thing
that changes between installations is the host and the token, so neither is
compiled in here.

## Setup

```bash
export GITEA_URL=https://git.example.com     # /api/v1 is appended for you
export GITEA_TOKEN=...                        # Settings → Applications → token
```

A token needs the scopes for what you ask it to do. A token that can read issues
usually cannot create them; a 403 is a **scope** problem, not a wrong token, and
the client says so instead of guessing.

## Any endpoint

```bash
python scripts/gitea.py api GET  /version
python scripts/gitea.py api GET  /repos/me/proj/issues
python scripts/gitea.py api POST /repos/me/proj/issues --data '{"title":"board item"}'
python scripts/gitea.py api PATCH /repos/me/proj/issues/12 --data '{"state":"closed"}'
```

`api` passes the method, path and JSON body straight through, prints
`{"status":..., "body":...}` and maps failures to exit codes. That is deliberate:
a thin passthrough never goes out of date, while a client that wraps forty
endpoints goes stale on the next release.

## The wrapped flows

Only the two flows that need more than one field are wrapped:

```bash
# squash merge and drop the branch, the usual ending
python scripts/gitea.py pr-merge --owner me --repo proj --number 7 --style squash --delete-branch

# close an issue (the PR body's "Closes #n" does this for you when you merge)
python scripts/gitea.py issue-close --owner me --repo proj --number 12
```

`--style` accepts `merge`, `rebase`, `rebase-merge`, `squash`,
`fast-forward-only`. `squash` is the default because it turns a branch's trial
commits into one reviewable commit — the same reason `git-workflow` squashes.

## Exit codes

| Exit | Meaning | First move |
| --- | --- | --- |
| 2 | bad `--data` JSON, bad arguments | fix the request |
| 3 | no URL or no token | set `GITEA_URL` / `GITEA_TOKEN`; the message names which |
| 4 | cannot reach the host | check host, port, TLS |
| 5 | 401/403 | token invalid, expired, or missing a scope |
| 6 | other non-2xx | the body carries Gitea's own message (404 = wrong owner/repo/number) |

## Things that bite

- **Owner and repo are path segments.** A repo under an organisation is
  `/repos/<org>/<repo>`; the owner is not your username.
- **Deleting a branch needs the branch name URL-encoded**: `feat/a` becomes
  `feat%2Fa`. The client quotes path segments for its wrapped flows, but not for
  raw `api` paths — encode them yourself there.
- **`--data` must be JSON**, not form encoding. Gitea answers 422 on a form body
  and the message is unhelpful.
- **A merged PR keeps its branch unless you ask.** `--delete-branch` is opt-in;
  the API calls it `delete_branch_after_merge`.
- **Rate and scope limits are per token.** If a script suddenly gets 403s on
  writes that used to work, check the token's scopes before blaming the code.

## Verification

```bash
python -X utf8 tests/run_tests.py     # 20 assertions, no real instance needed
```

`tests/stub_server.py` emulates `/api/v1` routes for issues, PR merge and
version, and the tests assert the URL the client built, the `token` auth header,
the body sent, the mapped exit codes (401/404/config/connect/bad JSON), and that
a squash merge arrives as `Do: squash` with the delete flag. A real instance is
still the final word: the stub proves the protocol, not your token's scopes.