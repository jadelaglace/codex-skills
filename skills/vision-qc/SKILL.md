---
name: vision-qc
description: >-
  Accept or reject matte and render products with measured evidence — alpha
  components, stray islands, mid-band halo, edge transition width,
  six-background exposure sheets, and annotation for review. Use when asked to
  check a cutout, verify a render, find white/black fringes or halo, gate a
  matting result, mark defects on an image, or QC video/PAG transparency output.
  Does not perform the matting or compositing (vision-matting) and does not
  describe image content (vision-recognition). Keywords — 质检, 自检, 验收,
  白边, 黑边, 虚边, 毛边, 游离噪点, 画框标注, matte QC, alpha, halo, PAG.
metadata:
  version: "1.0.0"
---

# Vision QC

The acceptance gate after matting or rendering. Four steps, and the order is the
point: measure, expose, look, mark.

The recurring lesson behind this skill is that a self-decoded composite is not
what the user sees. If you composite the layers yourself and then judge that
composite, you have checked your own arithmetic. Check the delivered file, on
backgrounds you did not choose, in layers you did not flatten.

This skill decides pass or fail. It does not cut the matte (`vision-matting`) and
does not read content (`vision-recognition`) — it borrows the vision model for
the final judgement step.

## 1. Measure (`scripts/cv_qc.py analyze`)

```bash
python scripts/cv_qc.py analyze subject.png --json   # exit 0 pass, 3 fail
```

| Metric | Meaning | Reference band |
| --- | --- | --- |
| `components` | 4-connected components of `alpha >= 0.5` | exactly 1 |
| `stray_pixels` | pixels in components smaller than 50 px | 0 |
| `by_threshold` | the same counts at `alpha >= 50`, `96`, `128` | 1 component and 0 stray at **all three** |
| `mid_band_ratio` | share of pixels with `0.125 < alpha <= 0.878` | <= 5% |
| `edge_transition_px` | mid-band area / boundary length, i.e. mean ramp thickness | 1.7 - 3.2 px |
| `alpha_histogram` | share per band (0–32, 32–128, 128–224, 224–255) | bimodal |
| `alpha_coverage` | share of pixels with `alpha >= 0.5` | material dependent |

A clean cutout is bimodal: background at 0, subject at 255, with a thin ramp.
A wide `edge_transition_px` is a halo or a blurred mask; `0` means the alpha is
binary and edges will be stair-stepped. The three thresholds catch what a single
one hides: a mask can look clean at 128 while faint ghosting splits it at 50.

Thresholds live in `DEFAULTS` at the top of the script so a project can tighten
them. They are gates, not proof: a pass means no measured defect, not that the
image looks right. Step 3 is still required.

## 2. Expose (`scripts/cv_qc.py multibg`)

```bash
python scripts/cv_qc.py multibg subject.png --out qc_sheet.png --json
```

Six backgrounds — white, black, checkerboard, mid grey, green, magenta — plus a
4x pixel zoom of the busiest edge region (or `--zoom x0,y0,x1,y1`). Each
background reveals a different defect:

| Background | What it exposes |
| --- | --- |
| white | black fringe, dark residue along the edge |
| black | white fringe, bright halo, semi-transparent noise |
| checkerboard | floating translucent patches, uneven density |
| mid grey | faint shadow that vanishes on white |
| green / magenta | colour spill and grey skirts at the edge |

Inspect the zoom, not just the tiles: hair tips, colour boundaries, and the
contact zone where shadow and subject overlap.

## 3. Judge with the vision model

Use `vision-recognition`'s `scripts/vision.py` on the exposure sheet. Three rules
make the difference:

1. **State where to look and what good looks like.** "On the black tile, check
   the left edge of the wheel for a white halo" beats "are there any problems".
2. **Lead with a hypothesis.** "The previous version had a grey fringe on the
   white tile; is it gone?" localises far better than an open question.
3. **Declare what is intentional.** A retained semi-transparent contact shadow
   must be named in the prompt, or the model reports it as dirt.
4. **Demand a verdict line.** Ask for a final line of `结论：过` or `结论：不过`.

If the answer is empty with `finish_reason=length`, shorten the prompt or raise
the token budget and retry once — that is truncation, not a pass.

## 4. Mark (`scripts/cv_qc.py annotate`)

```bash
python scripts/cv_qc.py annotate product.png \
  --box 100,200,500,600,边缘毛糙 \
  --arrow 900,100,820,300,偏色 \
  --circle 512,300,60 --text 60,540,未清理 \
  --out marked.png --json
```

Boxes, arrows, circles and text with an automatic palette, drawn on a copy; the
source file is never modified. Every shape can be repeated.

## Video and PAG

The five-layer self-check and the defect-to-fix table for animated transparency
products are in `references/video-qc.md`. The short version: frame-level alpha
and RGB inspection, CV metrics, multi-background overlay, re-measure after
encoding, and finally a real player screenshot. Skipping a layer means the
product was not checked.

## Failure states

| Symptom | Likely cause | Next step |
| --- | --- | --- |
| several components | specks, a watermark, or a split subject | `vision-matting key-white --keep-largest`, or cut by hand |
| wide ramp, high mid-band | blurred mask or halo | re-cut with a tighter ramp; do not "fix" it with contrast |
| binary alpha, width 0 | hard mask, no anti-aliasing | supersample the mask before export |
| fringe only on black | bright halo from un-premultiplied edges | re-composite with premultiplied alpha |
| fringe only on green | colour spill | re-run keying with despill |
| `empty alpha` | nothing opaque, or the wrong file | check the file before reporting |

## Verification

Run `analyze` on a known-good and a known-bad fixture: the good one passes with
a ramp inside the band, the bad one reports its components, strays and halo
width by number. Exit codes gate CI (0 pass, 3 fail, 2 usage). A pass from step 1
plus a deliberate look at step 2 is the minimum honest evidence; say which
images and which backgrounds you actually inspected.