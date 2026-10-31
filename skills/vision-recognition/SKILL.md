---
name: vision-recognition
description: Recognize and verify image or video-frame content with a vision model plus objective CV measurements. Use when asked what a picture shows, to transcribe text or tables from screenshots, compare two images, judge visual similarity, style, background, or color, locate changed regions, or when the host model cannot accept image input. Does not perform matting, compositing, image generation, or print/scan QC.
metadata:
  version: "1.0.0"
---

# Vision Recognition

Answer "what is this, are these alike, where do they differ" with two cooperating
layers:

- **the vision model** for meaning: content, text, layout, style, intent;
- **`scripts/cv_inspect.py`** for objective measurement: size, brightness,
  dominant colors, alpha coverage, pixel difference, change box, downscaling.

Use CV numbers to ground the model's reading. For objective questions such as
"what color is the background" or "where did it change", measure first, then ask
the model to interpret the measurement instead of guessing from pixels.

This skill is the recognition/verification member of a three-way split. Matting,
compositing, and layer extraction belong to `vision-matting`; print artifacts,
alpha/multi-background checks, and annotation/QC belong to `vision-qc`. This
skill does not generate or edit images and does not replace document OCR
pipelines.

## When the host cannot see images

If the current model rejects image input (for example `read_image` reports that
the model does not declare image input), call the bundled script instead of
claiming the image was inspected. Never describe an image you did not read.

## Backend selection

`scripts/vision.py` supports two providers and picks one with `--provider auto`:

| Provider | Use when | Required configuration |
| --- | --- | --- |
| `openai` | Any OpenAI-compatible `/chat/completions` endpoint | `VISION_BASE_URL`, `VISION_MODEL`, `VISION_API_KEY` (or flags) |
| `bl` | A local Bailian CLI is authenticated | `bl` on `PATH` |

`auto` prefers `openai` when a base URL or API key is present, otherwise falls
back to `bl`. It exits with an explicit `unavailable` error when neither exists;
report that state instead of inventing a result.

Keep endpoints, model IDs, and keys in the environment or local config. Never
write credentials, internal hostnames, or personal paths into this skill, its
outputs, or the repository. `VISION_FALLBACK_MODELS` may list comma-separated
model IDs; each is tried in order on request failure.

## Workflow

1. **Identify the inputs.** Read image paths and the actual question. For video,
   extract representative frames first, then treat them as still images.
2. **Measure before asking.** Run `cv_inspect.py info` for brightness, dominant
   colors, and alpha; `diff` for two-image comparison; `thumb` for large images.
3. **Downscale large images.** Use `thumb --max 1568` (or the provider's limit)
   before sending, and say that the model saw a downscaled copy.
4. **Ask a bounded question.** Name the region, the expected evidence, and the
   output shape. For comparison, ask for differences, not separate descriptions.
5. **Check the answer.** Confirm `finish_reason` is `stop`, the content is
   non-empty, and the answer addresses the question. Treat `length` as
   truncation, not success. For screenshots, check whether text near the edges
   may be cropped before concluding something is absent.
6. **Report what was measured and what was inferred.** Cite CV numbers
   separately from model claims.

## Commands

```bash
# objective measurements
python scripts/cv_inspect.py info screenshot.png --json
python scripts/cv_inspect.py diff before.png after.png --mark diff_box.png --json
python scripts/cv_inspect.py thumb huge.png --max 1568

# model understanding (single or multiple images)
python scripts/vision.py --image shot.png --prompt "逐字提取图中的文字与表格结构"
python scripts/vision.py --image a.png --image b.png --prompt "指出两张图的差异，按区域说明"
python scripts/vision.py --image scan.png --prompt "这张图是什么？" --provider bl --json
```

For multi-image questions with the `bl` provider, the script composes the images
side by side and labels them A/B before the call; tell the model the labels.

## Failure states

- `unavailable`: no configured backend, `bl` missing, or the endpoint cannot be
  reached. Report the missing configuration; do not fabricate a description.
- `empty content`: the model returned only reasoning or nothing. Raise
  `--max-tokens`, simplify the question, or switch models once.
- `finish_reason=length`: the answer is truncated. Narrow the request and retry.
- Size or format rejection: downscale with `thumb`, convert to PNG/JPEG, and
  retry once.
- Conflicting evidence: prefer measured CV values and say which claim is
  unverified rather than averaging the two.

## Verification

A working check is: `cv_inspect.py` reports the expected dimensions and change
box on a synthetic fixture, and `vision.py` transcribes a known string from a
real screenshot. Format validation and a successful script exit do not prove
visual accuracy; state the sample inspected and the remaining gap.