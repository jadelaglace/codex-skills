# Workflow contract

## Shape

An API-format graph is a mapping of node id → `{class_type, inputs}`:

```json
{
  "3": {"class_type": "KSampler", "inputs": {"seed": "{{SEED}}", "model": ["4", 0]}},
  "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "{{MODEL}}"}}
}
```

Links are `[node_id, output_index]`. There is no `nodes`/`links` array — that is
the UI format and `/prompt` rejects it.

## Placeholders versus overrides

| Need | Mechanism |
| --- | --- |
| A value the user changes every run | `{{PLACEHOLDER}}` |
| A one-off tweak on an existing graph | `--set 3.inputs.denoise=0.55` |
| Everything else | leave it hard-coded in *your* copy of the graph |

Substitution walks strings, lists and dicts. A string that is exactly one
placeholder is replaced by the native value (int stays int). Placeholders found
inside a longer string are interpolated as text.

Unknown placeholders are **not** blanked: they survive into the submitted graph
and the client refuses with exit 6 listing their names. That turns a typo into a
loud failure instead of a silently wrong picture.

## Upload semantics

`--image a.png --image b.png` produces:

| Token | Value |
| --- | --- |
| `{{IMAGE}}` | server-side name of the first upload |
| `{{IMAGE_1}}`, `{{IMAGE_2}}` | server-side names, in order |
| `{{IMAGE2}}` | second upload, or `""` when only one was given |

The server may rename a colliding file, so never write the local filename into
the graph. `tests/run_tests.py::case_rename` pins this behaviour.

## Choosing values at runtime

The client knows nothing about models. `--model` is just a string that lands in
`{{MODEL}}`; if your graph uses `unet_name`, `vae_name` or a LoRA stack, add
placeholders for those names in your own export.

## Versioning a graph

- Keep one graph per file, named for what it does, not for the model version.
- A graph is only valid for the node and model versions it was exported from;
  re-export after upgrading the server.
- Do not commit graphs that reference private asset paths. The repository ships
  `tests/fixtures/txt2img.json` and `img2img.json` only — synthetic graphs that
  exist to test the client, not to produce pictures.