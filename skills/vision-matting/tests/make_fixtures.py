"""Build small synthetic fixtures for vision-matting / vision-qc checks."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "fixtures")
OUT.mkdir(parents=True, exist_ok=True)

# 1) white studio background, subject + soft contact shadow
W, H = 400, 300
img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)
shadow = Image.new("L", (W, H), 0)
ds = ImageDraw.Draw(shadow)
ds.ellipse((90, 210, 310, 250), fill=90)
shadow = shadow.filter(ImageFilter.GaussianBlur(12))
img = Image.composite(Image.new("RGB", (W, H), (90, 90, 90)), img, shadow)
d = ImageDraw.Draw(img)
d.rounded_rectangle((120, 80, 280, 225), radius=18, fill=(220, 30, 40))
d.rectangle((150, 60, 250, 90), fill=(210, 25, 35))
img.save(OUT / "white_product.jpg", quality=95)

# 2) clean RGBA subject (rect + circle) for analysis / multibg
subj = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ds2 = ImageDraw.Draw(subj)
ds2.rounded_rectangle((120, 80, 280, 225), radius=18, fill=(220, 30, 40, 255))
ds2.ellipse((150, 60, 250, 140), fill=(240, 200, 60, 255))
subj.save(OUT / "subject.png")

# 3) green screen with spill on the subject edge
g = Image.new("RGB", (320, 240), (0, 177, 64))
dg = ImageDraw.Draw(g)
dg.ellipse((80, 40, 240, 200), fill=(30, 80, 220))
dg.ellipse((80, 40, 240, 200), outline=(0, 150, 90), width=3)
g.save(OUT / "greenscreen.png")

# 4) background layer holding the shadow, subject layer, and the reference
bg = Image.new("RGB", (W, H), (250, 250, 250))
dbg = ImageDraw.Draw(bg)
sh = Image.new("L", (W, H), 0)
ImageDraw.Draw(sh).ellipse((100, 200, 300, 250), fill=120)
sh = sh.filter(ImageFilter.GaussianBlur(10))
bg = Image.composite(Image.new("RGB", (W, H), (120, 120, 120)), bg, sh)
bg.save(OUT / "bg_with_shadow.png")

ref = bg.copy()
ref.paste(subj, (0, 0), subj)
ref.save(OUT / "reference.png")

# 5) bad cutout: halo + stray island + ragged edge
bad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
db = ImageDraw.Draw(bad)
db.rounded_rectangle((120, 80, 280, 225), radius=18, fill=(220, 30, 40, 255))
db.ellipse((170, 60, 230, 120), fill=(250, 250, 250, 90))       # translucent halo
db.rectangle((330, 240, 336, 246), fill=(220, 30, 40, 255))     # stray island
db.rectangle((300, 20, 306, 26), fill=(0, 0, 0, 255))           # stray island
bad.save(OUT / "bad_cutout.png")

print("fixtures:", OUT)