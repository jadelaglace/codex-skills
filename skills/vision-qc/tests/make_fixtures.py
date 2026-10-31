"""Build small synthetic fixtures for the vision-qc checks."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

def soften(im, r=1.0):
    a = im.split()[-1].filter(ImageFilter.GaussianBlur(r))
    im.putalpha(a)
    return im

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "fixtures")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 400, 300
SS = 4  # supersample factor


def aa_layer(draw_fn) -> Image.Image:
    """Draw at 4x then downsample, so edges carry a real alpha ramp."""
    big = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(big), SS)
    return big.resize((W, H), Image.LANCZOS)


def good(d, s):
    d.rounded_rectangle((120 * s, 80 * s, 280 * s, 225 * s), radius=18 * s, fill=(220, 30, 40, 255))
    d.ellipse((150 * s, 60 * s, 250 * s, 140 * s), fill=(240, 200, 60, 255))


soften(aa_layer(good)).save(OUT / "subject_aa.png")

# 3 disconnected components (two stray islands) + a soft halo
bad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(bad)
d.rounded_rectangle((120, 80, 280, 225), radius=18, fill=(220, 30, 40, 255))
d.ellipse((170, 60, 230, 120), fill=(250, 250, 250, 90))
d.rectangle((330, 240, 336, 246), fill=(220, 30, 40, 255))
d.rectangle((300, 20, 306, 26), fill=(0, 0, 0, 255))
bad.save(OUT / "bad_cutout.png")

# halo only: translucent ring around an otherwise clean subject
halo = aa_layer(good)
ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(ring).ellipse((110, 50, 290, 240), fill=(255, 255, 255, 120))
ring = ring.filter(ImageFilter.GaussianBlur(6))
halo = Image.alpha_composite(ring, halo)
halo.save(OUT / "halo.png")

# empty alpha (nothing opaque)
Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(OUT / "empty.png")

# a reference photo for annotate / multibg backgrounds
photo = Image.new("RGB", (W, H), (235, 235, 240))
ImageDraw.Draw(photo).ellipse((60, 40, 340, 260), fill=(200, 205, 215))
photo.save(OUT / "photo.jpg", quality=92)

print("fixtures:", OUT)


