#!/usr/bin/env python3
"""Quality checks for matte/render products (PIL + numpy, no GPU).

Subcommands:
  analyze   quantified verdict for a cutout: components, stray pixels, mid-band
            (halo) ratio, edge transition width
  multibg   composite the product over six backgrounds plus a 4x zoom strip, so
            white/black fringes, colour spill and semi-transparent patches show
  annotate  draw boxes, arrows, circles and labels on a copy for review

Thresholds follow the documented reference band; every number is measured from
the file, never assumed. Exit code is 0 for pass, 3 for a failed verdict, and 2
for a usage or input error, so callers can gate on it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]

PALETTE = [
    (220, 40, 40),
    (240, 140, 20),
    (30, 110, 220),
    (20, 160, 80),
    (140, 60, 200),
    (0, 170, 170),
]

DEFAULTS = {
    "max_mid_band": 0.05,      # 32 <= alpha <= 224, reference gate
    "min_edge_width": 1.7,     # px, measured on real accepted assets
    "max_edge_width": 3.2,
    "stray_max_px": 50,
    "component_thresholds": [50, 96, 128],
}


def load_rgba(path: str) -> Image.Image:
    with Image.open(path) as im:
        return im.convert("RGBA")


def font(size: int) -> ImageFont.ImageFont:
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def _neighbors(a: np.ndarray) -> np.ndarray:
    """4-neighbour minimum, so boundary pixels can be found by comparison."""
    out = a.copy()
    out[1:, :] = np.minimum(out[1:, :], a[:-1, :])
    out[:-1, :] = np.minimum(out[:-1, :], a[1:, :])
    out[:, 1:] = np.minimum(out[:, 1:], a[:, :-1])
    out[:, :-1] = np.minimum(out[:, :-1], a[:, 1:])
    return out


def measure(im: Image.Image) -> dict:
    rgba = np.asarray(im, dtype=np.uint8)
    alpha = rgba[..., 3].astype(np.float32) / 255.0
    total = alpha.size

    mask = alpha >= 0.5
    opaque = alpha >= 0.98
    clear = alpha <= 0.02
    mid = (alpha > 0.125) & (alpha <= 0.878)

    # boundary pixels: inside the mask but with at least one outside neighbour
    inner = mask & (_neighbors(np.where(mask, 1.0, 0.0)) < 0.5)
    band = int(mid.sum())
    edge_len = int(inner.sum())
    width = round(band / edge_len, 3) if edge_len else 0.0

    comps = _components(mask)
    largest = comps[0] if comps else 0
    strays = [c for c in comps[1:] if c < DEFAULTS["stray_max_px"]]
    small_total = int(sum(c for c in comps[1:] if c < DEFAULTS["stray_max_px"]))

    # the same gate at three thresholds: a mask that is clean at 128 but split at
    # 50 has faint ghosting around the subject
    by_threshold = {}
    for t in DEFAULTS["component_thresholds"]:
        m = alpha * 255.0 >= t
        cs = _components(m)
        by_threshold[str(t)] = {
            "components": len(cs),
            "largest_share": round((cs[0] / max(int(m.sum()), 1)) if cs else 0.0, 4),
            "stray_pixels": int(sum(c for c in cs[1:] if c < DEFAULTS["stray_max_px"])),
        }

    edges = [0.0, 32.0, 128.0, 224.0, 255.0]
    histogram = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        bucket = (alpha * 255.0 >= lo) & (alpha * 255.0 < hi if hi < 255 else alpha * 255.0 <= hi)
        histogram.append([int(lo), int(hi), round(float(bucket.mean()), 4)])

    return {
        "size": [im.width, im.height],
        "alpha_coverage": round(float(mask.mean()), 4),
        "alpha_opaque": round(float(opaque.mean()), 4),
        "alpha_clear": round(float(clear.mean()), 4),
        "alpha_histogram": histogram,
        "mid_band_ratio": round(band / total, 4),
        "components": len(comps),
        "component_sizes": comps[:8],
        "largest_component_share": round(largest / max(int(mask.sum()), 1), 4),
        "stray_components": len(strays),
        "stray_pixels": small_total,
        "by_threshold": by_threshold,
        "edge_length": edge_len,
        "edge_transition_px": width,
        "mean_alpha": round(float(alpha.mean()), 4),
    }


def _components(mask: np.ndarray) -> list[int]:
    """Connected-component sizes (4-connectivity) via run-length union-find."""
    h, w = mask.shape
    parent: list[int] = []
    size: list[int] = []

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    prev: list[tuple[int, int, int]] = []
    for y in range(h):
        row = mask[y]
        if not row.any():
            prev = []
            continue
        padded = np.concatenate(([False], row, [False]))
        diff = np.diff(padded.astype(np.int8))
        starts = np.flatnonzero(diff == 1).tolist()
        ends = np.flatnonzero(diff == -1).tolist()
        cur: list[tuple[int, int, int]] = []
        j = 0
        for s, e in zip(starts, ends):
            label = len(parent)
            parent.append(label)
            size.append(e - s)
            cur.append((s, e, label))
            while j < len(prev) and prev[j][1] <= s:
                j += 1
            k = j
            while k < len(prev) and prev[k][0] < e:
                union(label, prev[k][2])
                k += 1
        prev = cur

    totals: dict[int, int] = {}
    for i in range(len(parent)):
        if find(i) == i:
            totals[i] = size[i]
    return sorted(totals.values(), reverse=True)


def verdict(m: dict) -> tuple[str, list[str]]:
    issues: list[str] = []
    if m["components"] == 0:
        issues.append("empty alpha: nothing is opaque")
    elif m["components"] > 1:
        issues.append(f"{m['components']} disconnected components")
    if m["stray_pixels"] > 0:
        issues.append(f"{m['stray_pixels']} stray pixels in {m['stray_components']} small islands")
    if m["mid_band_ratio"] > DEFAULTS["max_mid_band"]:
        issues.append(
            f"mid-band {m['mid_band_ratio']:.1%} > {DEFAULTS['max_mid_band']:.0%} (halo or blurred edge)"
        )
    w = m["edge_transition_px"]
    if m["components"] and w <= 0:
        issues.append("edge transition unmeasurable: alpha is binary, expect jagged edges")
    elif 0 < w < DEFAULTS["min_edge_width"]:
        issues.append(f"edge transition {w}px < {DEFAULTS['min_edge_width']} (aliased stairs)")
    if w > DEFAULTS["max_edge_width"]:
        issues.append(f"edge transition {w}px > {DEFAULTS['max_edge_width']} (soft/blurred edge)")
    for t, info in m.get("by_threshold", {}).items():
        if info["components"] > 1:
            issues.append(f"threshold {t}: {info['components']} components")
        if info["stray_pixels"] > 0:
            issues.append(f"threshold {t}: {info['stray_pixels']} stray pixels")
    if m["components"] == 1 and not issues:
        return "pass", issues
    return "fail", issues


def cmd_analyze(args) -> tuple[dict, int]:
    im = load_rgba(args.image)
    m = measure(im)
    m["command"] = "analyze"
    m["image"] = args.image
    m["thresholds"] = dict(DEFAULTS)
    v, issues = verdict(m)
    m["verdict"] = v
    m["issues"] = issues
    return m, (0 if v == "pass" else 3)


# ---------------------------------------------------------------- multibg


def _checker(w: int, h: int, cell: int = 16) -> Image.Image:
    im = Image.new("RGB", (w, h), (210, 210, 210))
    d = ImageDraw.Draw(im)
    for y in range(0, h, cell):
        for x in range(0, w, cell):
            if ((x // cell) + (y // cell)) % 2:
                d.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(150, 150, 150))
    return im


def _bgs(w: int, h: int) -> list[tuple[str, Image.Image]]:
    return [
        ("white", Image.new("RGB", (w, h), (255, 255, 255))),
        ("black", Image.new("RGB", (w, h), (0, 0, 0))),
        ("checker", _checker(w, h)),
        ("gray", Image.new("RGB", (w, h), (128, 128, 128))),
        ("green", Image.new("RGB", (w, h), (0, 200, 80))),
        ("magenta", Image.new("RGB", (w, h), (220, 0, 200))),
    ]


def _auto_zoom(im: Image.Image, alpha: np.ndarray) -> tuple[int, int, int, int]:
    """Crop around the busiest edge region, centred on that edge's centroid."""
    h, w = alpha.shape
    mask = alpha >= 0.5
    edge = mask & (_neighbors(np.where(mask, 1.0, 0.0)) < 0.5)
    gy, gx = 4, 4
    best, best_cell = -1, None
    for j in range(gy):
        for i in range(gx):
            y0, y1 = j * h // gy, (j + 1) * h // gy
            x0, x1 = i * w // gx, (i + 1) * w // gx
            score = int(edge[y0:y1, x0:x1].sum())
            if score > best:
                best, best_cell = score, (x0, y0, x1, y1)

    if best_cell is None or best <= 0:
        cx, cy = w // 2, h // 2
    else:
        x0, y0, x1, y1 = best_cell
        ys, xs = np.nonzero(edge[y0:y1, x0:x1])
        cx = x0 + int(xs.mean()) if xs.size else (x0 + x1) // 2
        cy = y0 + int(ys.mean()) if ys.size else (y0 + y1) // 2

    half_w, half_h = max(24, w // 8), max(18, h // 8)
    return (
        max(0, cx - half_w),
        max(0, cy - half_h),
        min(w, cx + half_w),
        min(h, cy + half_h),
    )


def cmd_multibg(args) -> tuple[dict, int]:
    im = load_rgba(args.image)
    scale = min(1.0, args.tile_size / max(im.width, im.height))
    if scale < 1.0:
        im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
    w, h = im.size

    if args.zoom:
        zx = [int(v) for v in args.zoom.split(",")]
        box = tuple(zx) if len(zx) == 4 else _auto_zoom(im, np.asarray(im)[..., 3] / 255.0)
    else:
        box = _auto_zoom(im, np.asarray(im)[..., 3] / 255.0)

    label_h = 26
    tiles = _bgs(w, h)
    crop = im.crop(box)
    zf = 4
    tw, th = crop.width * zf, crop.height * zf
    canvas = Image.new("RGB", (max(w * 3, tw * 3), (h + label_h) * 2 + th + label_h), (32, 32, 32))
    d = ImageDraw.Draw(canvas)
    f = font(16)

    for idx, (name, bg) in enumerate(tiles):
        comp = Image.alpha_composite(bg.convert("RGBA"), im).convert("RGB")
        col, row = idx % 3, idx // 3
        x, y = col * w, row * (h + label_h)
        canvas.paste(comp, (x, y + label_h))
        d.text((x + 8, y + 4), name, fill=(240, 240, 240), font=f)

    # 4x pixel zoom of the busiest edge region, over the first three backgrounds
    zoom = crop.resize((tw, th), Image.NEAREST)
    zy = (h + label_h) * 2
    d.text((8, zy + 4), f"zoom {zf}x {box}", fill=(240, 240, 240), font=f)
    for idx, (name, bg) in enumerate(tiles[:3]):
        tile_bg = bg.crop(box).resize((tw, th), Image.NEAREST).convert("RGBA")
        tile = Image.alpha_composite(tile_bg, zoom)
        canvas.paste(tile.convert("RGB"), (idx * tw, zy + label_h))

    out = Path(args.out)
    if out.parent and not out.parent.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    return {
        "command": "multibg",
        "out": args.out,
        "tiles": [n for n, _ in tiles],
        "zoom": list(box),
        "zoom_factor": 4,
        "size": list(canvas.size),
        "source_size": [im.width, im.height],
    }, 0


# ---------------------------------------------------------------- annotate


def _parse_box(s: str) -> tuple[tuple[int, int, int, int], str]:
    parts = s.split(",")
    if len(parts) < 4:
        raise argparse.ArgumentTypeError("box needs x0,y0,x1,y1[,label]")
    return tuple(int(v) for v in parts[:4]), ",".join(parts[4:])


def cmd_annotate(args) -> tuple[dict, int]:
    base = load_rgba(args.image)
    canvas = base.convert("RGB")
    d = ImageDraw.Draw(canvas)
    f = font(max(16, canvas.width // 40))
    drawn = 0

    for s in args.box or []:
        box, label = _parse_box(s)
        color = PALETTE[drawn % len(PALETTE)]
        d.rectangle(box, outline=color, width=max(2, canvas.width // 300))
        if label:
            d.text((box[0] + 4, max(0, box[1] - f.size - 4)), label, fill=color, font=f)
        drawn += 1

    for s in args.circle or []:
        parts = s.split(",")
        if len(parts) < 3:
            raise SystemExit("circle needs cx,cy,r")
        cx, cy, r = (int(v) for v in parts[:3])
        color = PALETTE[drawn % len(PALETTE)]
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=max(2, canvas.width // 300))
        drawn += 1

    for s in args.arrow or []:
        parts = s.split(",")
        if len(parts) < 4:
            raise SystemExit("arrow needs x0,y0,x1,y1[,label]")
        x0, y0, x1, y1 = (int(v) for v in parts[:4])
        label = ",".join(parts[4:])
        color = PALETTE[drawn % len(PALETTE)]
        d.line((x0, y0, x1, y1), fill=color, width=max(2, canvas.width // 300))
        ang = np.arctan2(y1 - y0, x1 - x0)
        for da in (2.6, -2.6):
            d.line((x1, y1, x1 + 18 * np.cos(ang + da), y1 + 18 * np.sin(ang + da)), fill=color, width=3)
        if label:
            d.text((x1 + 6, y1 - 10), label, fill=color, font=f)
        drawn += 1

    for s in args.text or []:
        parts = s.split(",")
        if len(parts) < 3:
            raise SystemExit("text needs x,y,label")
        d.text((int(parts[0]), int(parts[1])), ",".join(parts[2:]), fill=(255, 40, 40), font=f)
        drawn += 1

    out = Path(args.out)
    if out.parent and not out.parent.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    return {
        "command": "annotate",
        "out": args.out,
        "size": list(canvas.size),
        "shapes": drawn,
        "note": "annotations are review aids on a new file; the source image is untouched",
    }, 0


# ---------------------------------------------------------------- cli


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="QC checks for matte/render products")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyze", help="quantified verdict on a cutout")
    a.add_argument("image")
    a.add_argument("--json", action="store_true")
    a.set_defaults(func=cmd_analyze)

    m = sub.add_parser("multibg", help="six-background exposure sheet")
    m.add_argument("image")
    m.add_argument("--out", required=True)
    m.add_argument("--zoom", help="x0,y0,x1,y1 crop for the 4x strip")
    m.add_argument("--tile-size", type=int, default=520)
    m.add_argument("--json", action="store_true")
    m.set_defaults(func=cmd_multibg)

    n = sub.add_parser("annotate", help="draw review marks on a copy")
    n.add_argument("image")
    n.add_argument("--out", required=True)
    n.add_argument("--box", action="append", metavar="X0,Y0,X1,Y1[,LABEL]")
    n.add_argument("--arrow", action="append", metavar="X0,Y0,X1,Y1[,LABEL]")
    n.add_argument("--circle", action="append", metavar="CX,CY,R[,LABEL]")
    n.add_argument("--text", action="append", metavar="X,Y,LABEL")
    n.add_argument("--json", action="store_true")
    n.set_defaults(func=cmd_annotate)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        summary, code = args.func(args)
    except FileNotFoundError as exc:
        print(f"error: input not found: {exc.filename}", file=sys.stderr)
        return 2
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 - single CLI boundary
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        for k, v in summary.items():
            print(f"{k}: {v}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())