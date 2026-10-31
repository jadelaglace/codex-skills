---
name: vision-matting
description: >-
  Produce alpha-channel assets from images and video frames — cut out subjects,
  split layers, extract shadows, composite layers, and resize while keeping
  transparency. Use when asked to remove a background, key a green/blue screen,
  lift an object out of a photo, extract or restore a contact shadow, merge RGBA
  layers, or drive an AI layered decomposition (ComfyUI / Qwen-Image-Layered).
  Does not decide what the image shows (vision-recognition) and does not certify
  output quality (vision-qc). Keywords — 抠图, 去背景, 透明背景, 分层, 抠像,
  色键, 绿幕, 蓝幕, 阴影提取, 多层合成, matte, alpha, layered.
metadata:
  version: "1.0.0"
---

# Vision Matting

Turn a source image into an asset with a real alpha channel, then hand it to
`vision-qc` for acceptance. Two paths, picked by material rather than by taste:

| Material | Path | Cost |
| --- | --- | --- |
| Soft shadows, hair, glass, busy background, production quality | AI layered decomposition (`run_layered_workflow.py`) | tens of seconds to minutes, needs GPU + models |
| Flat white / studio sweep | `cv_matte.py key-white` | instant |
| Green or blue screen | `cv_matte.py key-chroma` | instant |
| Shadow landed in the background layer and must be rescued | `shadow-extract` + `merge-over` | instant |
| Existing RGBA layers to stack or resize | `merge-over` / `resize` | instant |

The fast path is a shim, not a substitute: `key-white` renders a soft shadow as
an opaque grey blob and punches holes through genuinely white subject areas.
Say so when it applies and offer the AI path.

This skill produces assets. It does not describe content, does not judge whether
the result is acceptable, and does not generate new imagery (see
`vision-recognition`, `vision-qc`, `comfyui-generate`).

## Fast path (`scripts/cv_matte.py`)

Pure PIL + numpy, no GPU, no network. Every subcommand prints a JSON summary
with `--json`, and that summary is measured from the pixels just written.

```bash
# white/studio background; --keep-largest drops specks and watermarks
python scripts/cv_matte.py key-white product.jpg --keep-largest --out cut.png --json

# green screen with despill on the retained edge
python scripts/cv_matte.py key-chroma shot.png --color green --tolerance 40 --despill 0.8 --out cut.png

# lift an AO shadow: background layer + reference photo + subject layer
python scripts/cv_matte.py shadow-extract bg_layer.png --reference orig.jpg --subject subject.png --out shadow.png --json

# stack premultiplied layers bottom-to-top, then restore the original size
python scripts/cv_matte.py merge-over subject.png shadow.png --out final.png
python scripts/cv_matte.py resize final.png --width 2752 --height 1536 --out big.png
```

### `key-white`

`alpha = clamp((level - mean(r,g,b)) / soft)` where `level` (default `248`) is
the luminance treated as pure white and `soft` (default `28`) is the ramp below
it. The colour is then un-blended against white for every pixel with `alpha >
0.02`, so semi-transparent edges keep their true colour instead of a white
fringe. Raise `--level` for a slightly grey sweep, lower `--soft` for a harder
edge. `--keep-largest` keeps only the biggest **8-connected** component, which
removes dust, watermarks and reflection specks — 8- rather than 4-connected, or
a diagonal hair line splits in two.

### `key-chroma`

Keys on chroma dominance `screen - max(other two)` (`--tolerance 60`): a pixel
whose screen channel beats both others by the tolerance is fully transparent,
one that does not is fully opaque. A soft gate then remaps the ambiguous middle
(`--soft-lo 0.2` to `--soft-hi 0.7`) so the edge lands on a clean ramp instead
of a step. `--despill` clamps the screen channel to `max(other two)` rather than
subtracting a fixed amount, which is what keeps a green fringe from turning
grey. Use `--color blue` for blue screens.

### `shadow-extract`

Recovers the ambient-occlusion shadow when the decomposition folded it into the
background layer. Darkness is measured against the **97th percentile** of the
plate's luminance:

```
white = percentile(luma, 97)
dark  = clamp(1 - luma / white - floor, 0, 1)   # floor 0.02, values < 0.03 dropped
alpha = dark * scale
```

The 97th percentile makes the estimate robust to a large dark subject; a plain
min/max would read the subject itself as shadow. `--scale 0` (default)
auto-calibrates the strength from `--reference` plus `--subject`: it compares
the mean darkness outside the subject in the original against the plate, and
clamps the ratio to `[--scale-min 0.3, 1.0]`. A manual `--scale` pins it.

The layer colour is pure black, so it darkens whatever sits under it — an AO
model — instead of carrying a baked-in grey. `--subject` zeroes the shadow
inside the subject.

### `merge-over`

Straight-alpha "over" where **the first argument is the top layer**:
`merge-over subject.png shadow.png` puts the subject above the shadow, which is
the rescue order. Later arguments go underneath, in order, and are resized to
the top layer if they differ. Any number of layers is accepted.

## AI path (`scripts/run_layered_workflow.py`)

This client does not hard-code a graph. Export the API-format workflow from the
ComfyUI instance that has the layering model installed, replace the values you
want driven with the placeholders, and pass it in. See
`references/workflow.md` and `references/prompt_examples.md`.

```bash
# 1. preflight: dependencies plus reachability, nothing uploaded
python scripts/run_layered_workflow.py --server http://host:port --install-mode

# 2. resolve the graph offline and print what would be sent (no server needed)
python scripts/run_layered_workflow.py --workflow wf.json \
  --image in.png --prompt "<prompt>" --layers 2 --dry-run

# 3. submit, wait, download, classify outputs by measured alpha
python scripts/run_layered_workflow.py --server http://host:port --workflow wf.json \
  --image in.png --prompt "<prompt>" --layers 2 --prefix layered_suv --output-dir out \
  --restore-size
```

Server resolution is `--server` then `COMFYUI_URL`; there is no built-in
address. The client uploads, submits, polls `/history`, downloads from `/view`,
then names each file by its measured alpha (`subject_N`, `background_N`,
`composite`) because node order is not a reliable role signal. Classification is
`transparent_rate > 0.25` for a subject layer, and the composite is the opaque
layer with the smallest 256×256 thumbnail MAD against the source. `--restore-size`
writes an extra `_full` copy of each subject layer at source resolution (a
convenience for compositing; it adds no detail). The last line is
`RESULT_JSON: {...}` with `path`, `role` and `transparent_rate` per output. `--check`
runs before the upload in the same invocation, so a wrong host fails before any
file leaves the machine.

If the server is unreachable, the graph is rejected (`node_errors`), or the run
times out, report that state. Do not downgrade silently to the fast path and do
not claim a layered result you did not receive.

## Failure states

| Symptom | Meaning | Action |
| --- | --- | --- |
| `key-white` returns an opaque grey island where the shadow was | known limit of the fast path | use the AI path, or `shadow-extract` |
| `key-white` punches holes in the subject | subject contains near-white areas | lower `--level`, or use the AI path |
| `key-chroma` leaves a coloured fringe | spill survives the clamp despill | add `--no-despill` to see the raw key, then tighten `--tolerance` |
| shadow layer empty | prompt did not separate the shadow, or `--floor` too high | lower `--floor`, pass `--reference` and `--subject` so the scale calibrates |
| `components` > 1 in the summary | leftover specks | `--keep-largest`, or inspect before merging |
| `cannot reach ...` / `HTTP 4xx` | server or route problem | fix the host; do not retry in a loop |
| `workflow failed` with `node_errors` | server lacks a model file or a node | report the node list; do not edit the graph blindly |

## Verification

Offline path: `key-white`, `key-chroma`, `shadow-extract`, `merge-over` and
`resize` run on synthetic fixtures, and the shadow rescue is graded by
compositing the result over the reference and reporting MAD. That number is the
evidence, not the exit code.

AI path: exercised only against a live ComfyUI host. Without one, `--check`
fails cleanly and `--dry-run` proves the substitution, which is where the local
evidence stops. State that gap instead of implying an end-to-end run.