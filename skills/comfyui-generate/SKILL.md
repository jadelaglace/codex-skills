---
name: comfyui-generate
description: >-
  Drive any ComfyUI server from the command line: upload inputs, submit an
  API-format workflow, poll the queue, download every output, and classify the
  failure when something goes wrong. Use when asked to run a ComfyUI workflow,
  generate or edit images on a local or remote ComfyUI, batch a graph over many
  seeds, inspect which node classes a server actually has, or debug why a submit
  was rejected. Carries no server address, model name or private graph — you
  supply the workflow. Does not cut out or composite alpha assets
  (vision-matting) and does not certify output quality (vision-qc).
  Keywords — ComfyUI, workflow, API format, queue, prompt_id, generate,
  txt2img, img2img, batch, KSampler, object_info, 出图, 跑工作流.
metadata:
  version: "1.0.0"
---

# ComfyUI Generate

A thin, honest client. It knows the HTTP contract, not your models: the graph,
the server and every value you want driven come from the outside.

## Why the workflow is an argument

A ComfyUI graph encodes the exact `class_type` names and model files of one
installation. Shipping a "working" graph with a Skill means shipping something
that breaks on the next server upgrade, and it leaks private asset pipelines.
So the rule here is: **the graph is data**. You export it, this tool runs it.

## Quick start

```bash
# 1. what is this server, and do I have Pillow for alpha stats?
python scripts/comfy.py --server http://host:port check

# 2. which node classes does it actually have? (catches "missing custom node")
python scripts/comfy.py --server http://host:port nodes --filter KSampler

# 3. resolve the graph offline — no server, nothing uploaded
python scripts/comfy.py run --workflow wf.json --prompt "a red ball" --dry-run

# 4. run it
python scripts/comfy.py --server http://host:port run \
  --workflow wf.json --prompt "a red ball" --seed 42 \
  --output-dir out --prefix ball
```

`--server` overrides `COMFYUI_URL`; there is no built-in address and the tool
refuses to guess. Every command exits with a code that identifies the failure,
and the last line of a successful run is machine-readable:

```
RESULT_JSON: {"status":"ok","prompt_id":"…","seed":42,"outputs":[{"path":"out/ball_9_1.png","node":"9","alpha":{…}}]}
```

`transparent_rate` / `opaque_rate` appear only for RGBA outputs, so you can tell
a subject layer from a background without opening the file.

## Placeholders

The graph carries `{{NAME}}` tokens; unknown names are left alone and reported,
never silently blanked.

| Placeholder | Comes from | Notes |
| --- | --- | --- |
| `{{PROMPT}}` / `{{NEGATIVE}}` | `--prompt` / `--negative` | |
| `{{SEED}}` | `--seed` | random 48-bit when omitted, printed in the result |
| `{{WIDTH}}` / `{{HEIGHT}}` | `--width` / `--height` | default 1024 |
| `{{STEPS}}` / `{{CFG}}` | `--steps` / `--cfg` | default 20 / 7.0 |
| `{{PREFIX}}` | `--prefix` | also the local filename prefix |
| `{{MODEL}}` | `--model` | passed through as `ckpt_name` style string |
| `{{IMAGE}}`, `{{IMAGE_1}}`, `{{IMAGE_2}}`… | `--image` (repeatable) | **the server-side name**, not your local path |

Two details that cause most of the silent breakage:

- A whole-string placeholder keeps its native type (`{{SEED}}` becomes a number,
  not `"42"`), because ComfyUI validates ints strictly.
- When a server renames a colliding upload, the graph is written with the new
  name. Using the local filename here is the classic "works once" bug.

For anything the flags do not cover, override by path — applied after
substitution:

```bash
--set 3.inputs.denoise=0.55 --set 12.inputs.image=ref.png
```

## Exported graph, not the UI file

`Save` gives the UI format (`{"nodes": [...], "links": [...]}`), which `/prompt`
rejects. Use **Save (API format)**. The client detects the UI shape and says so
instead of submitting garbage.

## Failure taxonomy

Exit codes are the contract; the message names the node or URL.

| Exit | Meaning | First move |
| --- | --- | --- |
| 2 | usage: bad `--set`, missing file, UI-format graph | fix the argument; the message names it |
| 3 | no server configured | pass `--server` or set `COMFYUI_URL` |
| 4 | cannot reach / non-200 outside the graph | check host, port, firewall |
| 5 | 401/403 | the server wants auth; this client sends none by design |
| 6 | graph rejected (`node_errors`) | the node list names the missing model or node |
| 7 | execution failed (`status_str: error`) | read `messages`; OOM and missing files look different |
| 8 | completed but no images | the graph has no `SaveImage`, or it saved nothing |
| 9 | timeout | raise `--timeout`; a saturated GPU is not a prompt problem |

Exit 6 prints one line per rejected node. Do not "fix" a `value_not_in_list`
by editing the graph blindly: it means the file is not on that server.

## Batch and repeatability

`--seed` is printed in `RESULT_JSON`, so a run is reproducible without trusting
logs. For a sweep, loop in the shell and keep `--prefix` unique per iteration;
the client is stateless between runs and never reuses a `prompt_id`.

## Testing this Skill

```bash
python -X utf8 tests/run_tests.py     # 25 assertions, no GPU, no network
```

`tests/stub_server.py` implements `/system_stats`, `/upload/image`, `/prompt`,
`/history/<id>`, `/view` and `/object_info`, with scenarios for auth,
`node_errors`, execution error, empty output, timeout and server-side rename.
That is how the happy path and all six failure paths are proven here; a real
server is not required to know the client works.

## Boundaries

- No addresses, keys, model names or private graphs in the repository — a graph
  exports from your installation and stays with your project.
- This Skill does not judge the picture: hand outputs to `vision-qc`, and cut
  alpha assets with `vision-matting`.
- One graph per file; if a task needs several stages, chain them in the caller
  rather than inventing a meta-workflow here.