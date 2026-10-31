---
name: server-ops
description: >-
  Triage and operate a remote Linux service without a GUI: tell whether a
  failure is the app, the proxy or the network; release a port safely after
  pkill; keep reverse-proxy headers as lists instead of collapsed strings;
  drain a node before restarting it; keep SSE streams open through proxies; size
  a GPU/LLM process before launching it; and avoid the Windows tool-machine
  traps when the only shell is PowerShell. Use when asked to deploy, restart or
  debug a remote service, write a restart or recovery script, investigate 502 /
  404 / SSE disconnects, or check a health endpoint. Keywords — 运维, 部署,
  重启, 排障, pkill, 端口释放, 反向代理, 502, drain, SSE, GPU 显存, 探针,
  nohup, 恢复脚本, server ops.
metadata:
  version: "1.0.0"
---

# Server Ops

Remote triage is mostly a question of **which layer answered**. Every item below
exists because it misleads you if you assume the wrong layer.

## The probe first, the logs second

`scripts/probe.py` reports what a client actually receives:

```bash
python scripts/probe.py --url http://host:8000/health
python scripts/probe.py --url http://host/api --method POST --data '{"ping":1}'
```

It prints status, HTTP version, **every header as a list** (duplicates
preserved), content type and charset, the body prefix, and a `patterns` list that
names the usual suspects:

| Pattern | What it means |
| --- | --- |
| duplicate headers | a proxy collapsed a list into a comma string |
| `text/*` without charset | the client guesses the encoding; Chinese becomes mojibake |
| 5xx with a JSON body | the app is alive and the proxy is passing it through |
| HTML content-type with a JSON body | something is rewriting responses |

If `probe` shows a 502 in 3 ms, the app never saw the request — go to the proxy,
not the logs. If it takes 30 s, you have a queue or a drain problem.

## pkill and port release

- `pkill -f name` matches the **full command line**, including the `ssh` command
  that is running it. You can kill your own session. Anchor the pattern or use a
  pid file.
- After the process dies, the port can stay in `TIME_WAIT`. "Address already in
  use" is not a stuck process; it is a socket in teardown. Check with `ss -ltnp`
  before killing anything twice.
- Restart windows: stop accepting, let in-flight requests finish, then restart.
  A hard kill during a write is how you get a half-written file nobody can
  explain later.

## Reverse proxy rules

1. **Headers with several values must stay lists.** Collapsing `Set-Cookie` into
   one comma-joined string logs the user out in ways that look random. If your
   proxy config joins values, that is the bug.
2. **Drain before removal.** Take the node out of rotation, wait for open
   connections to close, then stop it. Deleting a node mid-request turns a
   deploy into a wave of 502s.
3. **404 locally, not upstream.** When a route disappears, answer from the proxy
   so the error is fast and consistent instead of timing out against a dead
   backend.
4. **SSE needs the buffering turned off** and a long read timeout, or events
   arrive in bursts minutes late — which looks exactly like "the model is slow".

## GPU and LLM processes

- Check what is already resident before launching: a second model that does not
  fit does not fail cleanly, it OOMs at the first long request.
- Size by weights plus KV cache, not weights alone. A 7B model that "fits" in
  8 GB fails on a 4k-token prompt.
- Set an explicit request timeout and a queue limit; an unbounded queue converts
  a slow model into a dead service.

## Deploy from a git checkout

```bash
git fetch --all && git reset --hard origin/main   # only on a deploy box, never a work tree
# scan for secrets before starting
# run the selftest / health check, then flip traffic
```

`reset --hard` on a deploy box is correct because that box should own no local
commits. On a machine where a human also edits files, it destroys work — that is
why the two are different skills.

## Windows tool machine

When the only shell is PowerShell talking to Linux over SSH:

- Quote remote commands through a here-string, not nested quotes; three levels of
  quoting is where commands silently lose an argument.
- `$LASTEXITCODE` is the remote exit code; a successful `ssh` that ran a failing
  command returns 0 in `$?` and non-zero only here.
- Do not pipe remote stderr through `2>&1` with `$ErrorActionPreference='Stop'`;
  a warning line becomes a terminating error (see the `powershell` skill).

## Verification

```bash
python -X utf8 tests/run_tests.py     # 16 assertions against a local server
```

The tests stand up a server that returns duplicate `Set-Cookie` headers, missing
charset, a 500 with JSON, HTML content type with a JSON body, a 404, a POST echo
and a hang, then assert the probe reports each one and maps timeout/connect/
usage errors to exit 5/4/2.

The operational advice above (pkill, drain, GPU sizing) is **not** verified by
those tests — it is knowledge, not code. Treat it as a checklist to reason with,
not as proof that your service is healthy.