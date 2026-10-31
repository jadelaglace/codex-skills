#!/usr/bin/env python3
"""Objective image measurements for vision-recognition.

Pure Pillow + numpy; no GPU, no network, no model call.

Subcommands:
  info   dimensions, brightness distribution, dominant colors, alpha coverage
  diff   pixel difference between two same-size images, change box, optional mark
  thumb  downscale a large image before handing it to a vision model

Every subcommand supports --json for machine-readable output.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

try:
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover - environment guard
    sys.stderr.write(
        "numpy is required for cv_inspect.py diff/info.\n"
        "Install with: python -m pip install pillow numpy\n"
    )
    raise SystemExit(3)


def _fail(message: str, code: int = 2) -> "NoReturn":
    sys.stderr.write(message.rstrip() + "\n")
    raise SystemExit(code)


def _load(path: str) -> Image.Image:
    p = Path(path)
    if not p.is_file():
        _fail(f"image not found: {path}")
    try:
        im = Image.open(p)
        im.load()
        return im
    except Exception as exc:  # noqa: BLE001 - report decoder reason verbatim
        _fail(f"cannot decode image {path}: {exc}")
        raise AssertionError("unreachable")


def _rgb(im: Image.Image) -> Image.Image:
    if im.mode in ("RGBA", "LA"):
        background = Image.new("RGBA", im.size, (255, 255, 255, 255))
        background.alpha_composite(im.convert("RGBA"))
        return background.convert("RGB")
    return im.convert("RGB")


def _dominant_colors(im: Image.Image, count: int = 5) -> list[dict]:
    small = _rgb(im).resize((64, 64), Image.Resampling.BILINEAR)
    quant = small.quantize(colors=count, method=Image.Quantize.MEDIANCUT)
    palette = quant.getpalette() or []
    total = small.size[0] * small.size[1]
    counts: dict[int, int] = {}
    for value in quant.getdata():
        counts[value] = counts.get(value, 0) + 1
    result = []
    for index, pixels in sorted(counts.items(), key=lambda kv: kv[1], reverse=True):
        r, g, b = palette[index * 3 : index * 3 + 3]
        result.append(
            {
                "hex": f"#{r:02X}{g:02X}{b:02X}",
                "rgb": [r, g, b],
                "share": round(pixels / total, 4),
            }
        )
    return result


def cmd_info(args: argparse.Namespace) -> int:
    im = _load(args.image)
    rgb = np.asarray(_rgb(im), dtype=np.uint8)
    gray = rgb.mean(axis=2) if rgb.ndim == 3 else rgb.astype(np.float32)
    h, w = gray.shape
    hist, _ = np.histogram(gray, bins=10, range=(0, 255))
    alpha_ratio = None
    if im.mode in ("RGBA", "LA") and "A" in im.getbands():
        alpha = np.asarray(im.getchannel("A"), dtype=np.uint8)
        alpha_ratio = round(float((alpha > 0).mean()), 4)
    payload = {
        "path": str(Path(args.image).resolve()),
        "size": [im.width, im.height],
        "mode": im.mode,
        "aspect_ratio": round(im.width / im.height, 4),
        "brightness": {
            "mean": round(float(gray.mean()), 2),
            "median": round(float(np.median(gray)), 2),
            "overexposed_ratio": round(float((gray >= 250).mean()), 4),
            "underexposed_ratio": round(float((gray <= 5).mean()), 4),
            "histogram_bins_0_255": [int(v) for v in hist],
        },
        "dominant_colors": _dominant_colors(im),
        "alpha_coverage": alpha_ratio,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"image: {payload['path']}")
        print(f"size: {im.width}x{im.height} mode={im.mode} aspect={payload['aspect_ratio']}")
        b = payload["brightness"]
        print(
            "brightness: mean={mean} median={median} "
            "overexposed={overexposed_ratio} underexposed={underexposed_ratio}".format(**b)
        )
        print("dominant colors:")
        for color in payload["dominant_colors"]:
            print(f"  {color['hex']}  {color['share'] * 100:.1f}%")
        if alpha_ratio is not None:
            print(f"alpha coverage: {alpha_ratio}")
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    a = _load(args.image_a)
    b = _load(args.image_b)
    if a.size != b.size:
        _fail(f"size mismatch: {a.size[0]}x{a.size[1]} vs {b.size[0]}x{b.size[1]}")
    ar = np.asarray(_rgb(a), dtype=np.int16)
    br = np.asarray(_rgb(b), dtype=np.int16)
    delta = np.abs(ar - br)
    gray_delta = delta.mean(axis=2)
    mad = float(gray_delta.mean())
    mask = gray_delta > args.threshold
    changed = float(mask.mean())
    box = None
    if mask.any():
        ys, xs = np.where(mask)
        box = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    payload = {
        "image_a": str(Path(args.image_a).resolve()),
        "image_b": str(Path(args.image_b).resolve()),
        "size": [a.width, a.height],
        "threshold": args.threshold,
        "mad": round(mad, 4),
        "changed_ratio": round(changed, 6),
        "change_box": box,
        "verdict": "identical" if mad == 0 else ("minor" if changed < 0.005 else "different"),
    }
    if args.mark:
        marked = _rgb(a).copy()
        draw = ImageDraw.Draw(marked)
        if box:
            draw.rectangle(box, outline=(255, 0, 0), width=max(3, min(a.size) // 200))
        marked.save(args.mark)
        payload["mark"] = str(Path(args.mark).resolve())
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"A: {payload['image_a']}")
        print(f"B: {payload['image_b']}")
        print(f"MAD: {payload['mad']}  changed_ratio: {payload['changed_ratio']}")
        print(f"change box: {box}  verdict: {payload['verdict']}")
        if args.mark:
            print(f"marked image: {payload['mark']}")
    return 0


def cmd_thumb(args: argparse.Namespace) -> int:
    im = _load(args.image)
    long_edge = max(im.size)
    if long_edge <= args.max:
        out = Path(args.out) if args.out else Path(args.image)
        if str(out.resolve()) != str(Path(args.image).resolve()):
            im.save(out)
        print(json.dumps({"path": str(out.resolve()), "scaled": False, "size": list(im.size)}))
        return 0
    scale = args.max / long_edge
    new_size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    thumb = im.resize(new_size, Image.Resampling.LANCZOS)
    out = Path(args.out) if args.out else Path(args.image).with_name(
        Path(args.image).stem + f"_thumb{Path(args.image).suffix}"
    )
    thumb.save(out)
    print(
        json.dumps(
            {
                "path": str(out.resolve()),
                "scaled": True,
                "from_size": [im.width, im.height],
                "size": list(new_size),
            }
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    info = sub.add_parser("info", help="dimensions, brightness, dominant colors")
    info.add_argument("image")
    info.add_argument("--json", action="store_true")
    info.set_defaults(func=cmd_info)

    diff = sub.add_parser("diff", help="pixel difference between two same-size images")
    diff.add_argument("image_a")
    diff.add_argument("image_b")
    diff.add_argument("--threshold", type=int, default=8, help="per-pixel gray delta (0-255)")
    diff.add_argument("--mark", help="write A with the change box outlined in red")
    diff.add_argument("--json", action="store_true")
    diff.set_defaults(func=cmd_diff)

    thumb = sub.add_parser("thumb", help="downscale before sending to a vision model")
    thumb.add_argument("image")
    thumb.add_argument("--max", type=int, default=1568, help="maximum long edge")
    thumb.add_argument("--out")
    thumb.set_defaults(func=cmd_thumb)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())