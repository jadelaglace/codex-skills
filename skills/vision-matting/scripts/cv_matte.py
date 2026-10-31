#!/usr/bin/env python3
"""Deterministic matting utilities for still images (PIL + numpy, no GPU).

Subcommands:
  key-white      white/photo-studio background removal (level/soft ramp + white un-blend)
  key-chroma     green/blue screen keying (chroma dominance + soft gate + despill)
  shadow-extract lift an AO shadow layer (97th-percentile white reference + calibrated scale)
  merge-over     straight-alpha "over" compositing, first argument is the TOP layer
  resize         LANCZOS resize that keeps the alpha channel

Every subcommand accepts --json for a machine-readable summary. Numbers come from
the pixels written by this run, never from assumptions.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------- helpers


def load_rgba(path: str) -> Image.Image:
    with Image.open(path) as im:
        return im.convert("RGBA")


def save(im: Image.Image, path: str) -> None:
    target = Path(path)
    if target.parent and not target.parent.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
    im.save(target)


def _ccl(mask: np.ndarray, conn: int = 8):
    """Run-length connected components (8-connectivity by default).

    Returns (rows, find, totals): rows[y] lists (start, end, label) runs, totals
    maps root -> pixel count. One pass per row with union-find over touching
    runs; no scipy, so multi-megapixel masks stay fast.
    """
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

    rows: list[list[tuple[int, int, int]]] = []
    prev: list[tuple[int, int, int]] = []
    for y in range(h):
        row = mask[y]
        if not row.any():
            prev = []
            rows.append([])
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
            # 8-connectivity: runs touching at a corner still belong together
            if conn == 8:
                while j < len(prev) and prev[j][1] < s:
                    j += 1
                k = j
                while k < len(prev) and prev[k][0] <= e:
                    union(label, prev[k][2])
                    k += 1
            else:
                while j < len(prev) and prev[j][1] <= s:
                    j += 1
                k = j
                while k < len(prev) and prev[k][0] < e:
                    union(label, prev[k][2])
                    k += 1
        prev = cur
        rows.append(cur)

    totals = {i: size[i] for i in range(len(parent)) if find(i) == i}
    return rows, find, totals


def _components(mask: np.ndarray) -> list[int]:
    _, _, totals = _ccl(mask)
    return sorted(totals.values(), reverse=True)


def _keep_largest(alpha: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    """Keep only the largest 8-connected component of alpha > threshold."""
    mask = alpha > threshold
    if not mask.any():
        return alpha
    rows, find, totals = _ccl(mask)
    if len(totals) <= 1:
        return alpha
    best = max(totals, key=lambda r: totals[r])
    keep = np.zeros_like(mask)
    for y, runs in enumerate(rows):
        for s, e, label in runs:
            if find(label) == best:
                keep[y, s:e] = True
    out = alpha.copy()
    out[~keep] = 0.0
    return out


def _luma(rgb: np.ndarray) -> np.ndarray:
    return rgb.mean(axis=2)


def _unblend_white(rgb: np.ndarray, a: np.ndarray) -> np.ndarray:
    """Recover foreground colour from a white-background composite."""
    a3 = np.maximum(a[..., None], 0.02)
    out = (rgb - (1.0 - a[..., None]) * 255.0) / a3
    out = np.where(a[..., None] > 0.02, out, rgb)
    return np.clip(np.nan_to_num(out, nan=0.0), 0, 255)


def darkness_map(rgb: np.ndarray, floor: float = 0.02) -> np.ndarray:
    """Shadow darkness relative to the 97th-percentile luminance of the plate."""
    lum = rgb.mean(axis=2)
    white = float(np.percentile(lum, 97))
    if white <= 1:
        return np.zeros_like(lum)
    dark = np.clip(1.0 - lum / white - floor, 0.0, 1.0)
    dark[dark < 0.03] = 0.0
    return dark


def _stats(alpha: np.ndarray) -> dict:
    a = alpha.astype(np.float32)
    if a.max() > 1.5:
        a = a / 255.0
    return {
        "alpha_coverage": round(float((a > 0.5).mean()), 4),
        "opaque_rate": round(float((a > 0.5).mean()), 4),
        "semi_rate": round(float(((a > 0.1) & (a <= 0.5)).mean()), 4),
        "mean_alpha": round(float(a.mean()), 4),
        "max_alpha": round(float(a.max()), 4) if a.size else 0.0,
        "components": len(_components(a > 0.5)),
    }


def _suffix(args, default: str) -> str:
    if args.out:
        return args.out
    src = Path(getattr(args, "image", None) or getattr(args, "base", "out"))
    return str(src.with_name(f"{src.stem}{default}.png"))


# ---------------------------------------------------------------- subcommands


def cmd_key_white(args) -> dict:
    im = load_rgba(args.image)
    rgb = np.asarray(im, dtype=np.float32)[..., :3]
    lum = _luma(rgb)
    hi = args.level
    lo = hi - max(args.soft, 1.0)
    a = np.clip((hi - lum) / max(hi - lo, 1.0), 0.0, 1.0)
    if args.keep_largest:
        a = _keep_largest(a)
    fg = _unblend_white(rgb, a)
    out = np.dstack([fg, a * 255.0]).astype(np.uint8)
    path = _suffix(args, "_cut")
    save(Image.fromarray(out, mode="RGBA"), path)
    return {
        "command": "key-white",
        "out": path,
        "size": [im.width, im.height],
        "level": hi,
        "soft": args.soft,
        "keep_largest": bool(args.keep_largest),
        "warning": "subject areas that are near-white may be keyed out",
        **_stats(a * 255.0),
    }


def cmd_key_chroma(args) -> dict:
    im = load_rgba(args.image)
    rgb = np.asarray(im, dtype=np.float32)[..., :3]
    idx = {"green": 1, "blue": 2}[args.color]
    others = [i for i in (0, 1, 2) if i != idx]
    dom = rgb[..., idx] - np.maximum(rgb[..., others[0]], rgb[..., others[1]])
    a = np.clip(1.0 - dom / max(args.tolerance, 1.0), 0.0, 1.0)
    # soft gate: remap the ambiguous middle so the edge lands on a clean ramp
    a = np.clip((a - args.soft_lo) / max(args.soft_hi - args.soft_lo, 1e-3), 0.0, 1.0)
    if args.keep_largest:
        a = _keep_largest(a)
    if args.despill:
        # clamp the screen channel to the stronger of the other two
        clamped = np.minimum(rgb[..., idx], np.maximum(rgb[..., others[0]], rgb[..., others[1]]))
        rgb[..., idx] = np.where(a[..., ] > 0.02, clamped, rgb[..., idx])
    out = np.dstack([np.clip(rgb, 0, 255), a * 255.0]).astype(np.uint8)
    path = _suffix(args, "_cut")
    save(Image.fromarray(out, mode="RGBA"), path)
    return {
        "command": "key-chroma",
        "out": path,
        "size": [im.width, im.height],
        "color": args.color,
        "tolerance": args.tolerance,
        "soft_gate": [args.soft_lo, args.soft_hi],
        "despill": bool(args.despill),
        **_stats(a * 255.0),
    }


def cmd_shadow_extract(args) -> dict:
    bg = load_rgba(args.background)
    bg_rgb = np.asarray(bg, dtype=np.float32)[..., :3]
    dark = darkness_map(bg_rgb, args.floor)

    ref_rgb = None
    outside = None
    if args.reference:
        ref = load_rgba(args.reference)
        if ref.size != bg.size:
            ref = ref.resize(bg.size, Image.LANCZOS)
        ref_rgb = np.asarray(ref, dtype=np.float32)[..., :3]
    if args.subject:
        subj = load_rgba(args.subject)
        if subj.size != bg.size:
            subj = subj.resize(bg.size, Image.LANCZOS)
        outside = np.asarray(subj)[..., 3] < 26

    scale = 1.0
    mean_bg = float(dark[dark > 0].mean()) if (dark > 0).any() else 0.0
    if args.scale and args.scale > 0:
        scale = float(args.scale)
        mode = "manual"
    elif ref_rgb is not None and outside is not None:
        odark = darkness_map(ref_rgb, args.floor)
        om = (odark > 0) & outside
        mean_ref = float(odark[om].mean()) if om.any() else 0.0
        if mean_bg > 1e-6 and mean_ref > 0:
            scale = float(np.clip(mean_ref / mean_bg, args.scale_min, 1.0))
        mode = "auto"
    else:
        mode = "none"

    a = np.clip(dark * scale, 0.0, 1.0)
    if outside is not None:
        a[~outside] = 0.0
    if args.far_factor != 1.0 and outside is not None:
        near = _dilate(outside, max(2, int(min(bg.size) * 0.02)))
        a[(~near) & outside] *= args.far_factor

    out = np.dstack([np.zeros((bg.height, bg.width, 3), np.uint8),
                     (a * 255.0).astype(np.uint8)])
    path = _suffix(args, "_shadow")
    save(Image.fromarray(out, mode="RGBA"), path)
    return {
        "command": "shadow-extract",
        "out": path,
        "size": [bg.width, bg.height],
        "dark_pixels": int((dark > 0).sum()),
        "dark_ratio": round(float((dark > 0).mean()), 4),
        "mean_bg_darkness": round(mean_bg, 4),
        "scale": round(scale, 3),
        "scale_mode": mode,
        **_stats(a * 255.0),
    }


def _dilate(mask: np.ndarray, radius: int) -> np.ndarray:
    """Cheap square dilation by down/up-sampling the mask."""
    h, w = mask.shape
    f = max(2, radius)
    im = Image.fromarray((mask * 255).astype(np.uint8), mode="L")
    small = im.resize((max(1, w // f), max(1, h // f)), Image.BOX)
    small = small.point(lambda v: 255 if v > 0 else 0)
    return np.asarray(small.resize((w, h), Image.NEAREST)) > 0


def cmd_merge_over(args) -> dict:
    layers = [load_rgba(p) for p in [args.top, *args.lower]]
    top = np.asarray(layers[0], dtype=np.float32)
    for lower in layers[1:]:
        low = lower
        if low.size != layers[0].size:
            low = low.resize(layers[0].size, Image.LANCZOS)
        low_arr = np.asarray(low, dtype=np.float32)
        a1 = top[:, :, 3:4] / 255.0
        a2 = low_arr[:, :, 3:4] / 255.0
        pm = top[:, :, :3] * a1 + low_arr[:, :, :3] * a2 * (1.0 - a1)
        a_out = np.clip(a1 + a2 * (1.0 - a1), 0.0, 1.0)
        rgb = np.where(a_out > 0, pm / np.maximum(a_out, 1e-6), 0.0)
        top = np.concatenate([np.clip(rgb, 0, 255), a_out * 255.0], axis=2)
    path = _suffix(args, "_merged")
    save(Image.fromarray(top.astype(np.uint8), mode="RGBA"), path)
    return {
        "command": "merge-over",
        "out": path,
        "size": list(layers[0].size),
        "layers": len(layers),
        "order": "arg1 is top, later arguments are below",
        **_stats(top[..., 3]),
    }


def cmd_resize(args) -> dict:
    im = load_rgba(args.image)
    if args.scale and args.scale > 0:
        tw = max(1, round(im.width * args.scale))
        th = max(1, round(im.height * args.scale))
    elif args.width and args.height:
        tw, th = args.width, args.height
    else:
        raise SystemExit("resize needs --scale, or both --width and --height")
    out = im.resize((tw, th), Image.LANCZOS)
    path = _suffix(args, f"_{tw}x{th}")
    save(out, path)
    return {
        "command": "resize",
        "out": path,
        "size": list(out.size),
        "source_size": [im.width, im.height],
    }


# ---------------------------------------------------------------- cli


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Deterministic matting utilities")
    sub = p.add_subparsers(dest="cmd", required=True)

    w = sub.add_parser("key-white", help="remove a white/studio background")
    w.add_argument("image")
    w.add_argument("--out", help="output path (default: <name>_cut.png)")
    w.add_argument("--level", type=float, default=248.0, help="luminance treated as pure white")
    w.add_argument("--soft", type=float, default=28.0, help="ramp width below --level")
    w.add_argument("--keep-largest", action="store_true")
    w.add_argument("--json", action="store_true")
    w.set_defaults(func=cmd_key_white)

    c = sub.add_parser("key-chroma", help="key a green/blue screen")
    c.add_argument("image")
    c.add_argument("--color", choices=["green", "blue"], default="green")
    c.add_argument("--out", help="output path (default: <name>_cut.png)")
    c.add_argument("--tolerance", type=float, default=60.0, help="chroma dominance treated as screen")
    c.add_argument("--soft-lo", type=float, default=0.2)
    c.add_argument("--soft-hi", type=float, default=0.7)
    c.add_argument("--despill", action="store_true", default=True)
    c.add_argument("--no-despill", dest="despill", action="store_false")
    c.add_argument("--keep-largest", action="store_true")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_key_chroma)

    s = sub.add_parser("shadow-extract", help="extract an AO shadow layer")
    s.add_argument("background")
    s.add_argument("--out", help="output path (default: <name>_shadow.png)")
    s.add_argument("--reference", help="original image used to calibrate the scale")
    s.add_argument("--subject", help="subject RGBA layer; shadow is zeroed inside it")
    s.add_argument("--floor", type=float, default=0.02)
    s.add_argument("--scale", type=float, default=0.0, help="0 = auto-calibrate")
    s.add_argument("--scale-min", type=float, default=0.3)
    s.add_argument("--far-factor", type=float, default=1.0)
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_shadow_extract)

    m = sub.add_parser("merge-over", help="composite layers; the first argument is the top layer")
    m.add_argument("top")
    m.add_argument("lower", nargs="*")
    m.add_argument("--out", help="output path (default: <name>_merged.png)")
    m.add_argument("--json", action="store_true")
    m.set_defaults(func=cmd_merge_over)

    r = sub.add_parser("resize", help="LANCZOS resize preserving alpha")
    r.add_argument("image")
    r.add_argument("--out")
    r.add_argument("--scale", type=float, default=0.0)
    r.add_argument("--width", type=int, default=0)
    r.add_argument("--height", type=int, default=0)
    r.add_argument("--json", action="store_true")
    r.set_defaults(func=cmd_resize)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        summary = args.func(args)
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())