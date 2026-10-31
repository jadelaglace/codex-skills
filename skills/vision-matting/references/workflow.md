# Wiring a layering workflow into `run_layered_workflow.py`

The client is deliberately graph-agnostic: it uploads, submits, polls and
downloads, but the node graph comes from your ComfyUI instance.

## 1. Export the API-format graph

In ComfyUI, enable the dev options and use **Save (API format)** — not the
regular workflow JSON. The graph must be a mapping of node id → `{class_type,
inputs}`, which is what `POST /prompt` expects.

## 2. Insert placeholders

Replace the values the client should drive with these exact strings:

| Placeholder | Replaced with | Where it usually goes |
| --- | --- | --- |
| `{{IMAGE}}` | uploaded file name returned by `/upload/image` | `LoadImage.image` |
| `{{PROMPT}}` | `--prompt` | the positive `CLIPTextEncode.text` |
| `{{LAYERS}}` | `--layers` | layer-count node input (integer) |
| `{{SEED}}` | `--seed` | sampler `seed` |
| `{{PREFIX}}` | `--prefix` | `SaveImage.filename_prefix` |

A value is replaced when the whole string equals the placeholder; inside a
longer string the placeholder is interpolated. `--dry-run` prints unresolved
placeholders, so a typo surfaces before a submit.

## 3. Make the outputs identifiable

The client classifies downloaded images by measured alpha, not by node id: files
with transparent pixels become `subject_1..N`, the rest become `background_N`
and `composite`. That heuristic is only as good as what the graph saves — save
the layered subject, the background and, if the graph produces one, the
recomposited image.

## 4. Preflight, then run

```bash
python scripts/run_layered_workflow.py --server http://host:port --install-mode
python scripts/run_layered_workflow.py --workflow wf.json \
  --image in.png --prompt "<prompt>" --layers 2 --dry-run
python scripts/run_layered_workflow.py --server http://host:port --workflow wf.json \
  --image in.png --prompt "<prompt>" --layers 2 --prefix layered_suv --output-dir out
```

`--install-mode` checks the Python dependencies and `/system_stats` and exits;
`--dry-run` needs no server at all. `--check` reports device names and free VRAM.
A run that fails while VRAM is nearly exhausted is a scheduling problem, not a
prompt problem — wait and retry rather than editing the prompt.

## Known node ids

The deployment this skill was distilled from used five fixed nodes; if you are
adapting an export from that fleet, the placeholders map like this:

| Node | Input | Placeholder |
| --- | --- | --- |
| `74` | `image` | `{{IMAGE}}` (the server-side upload name, not the local path) |
| `116` | `value` | `{{PROMPT}}` |
| `83:119` | `layers` | `{{LAYERS}}` |
| `60` | `filename_prefix` | `{{PREFIX}}` |
| `83:3` | `seed` | `{{SEED}}` |

Any other graph works too — the client only substitutes placeholders.

## Failure reading

| Message | Cause |
| --- | --- |
| `no ComfyUI server configured` | neither `--server` nor `COMFYUI_URL` set |
| `cannot reach ...` | wrong host/port, firewall, or server down |
| `template ... missing placeholders` | the export dropped a node, or the placeholder is misspelled |
| `server rejected the graph: {...node_errors...}` | a model file or custom node is missing on the server |
| `workflow failed: [...]` | execution error; the message list names the node |
| `no result after Ns` | still queued, or the server is saturated; raise `--timeout` |

## Housekeeping

- Keep host addresses, keys and model paths in the environment or local config,
  never inside the skill or the graph committed to a repository.
- A graph is only valid for the node and model versions it was exported from;
  re-export after upgrading the server.