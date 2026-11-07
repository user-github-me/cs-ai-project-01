"""Blue Impulse Study Guide V2 — extract supplied artwork and compose chapter backgrounds.

Inputs (not committed): temp contents/ai proj stage2/study guide art.pdf
Outputs: assets/study-guide/v2/art/
  sky-N.jpg        page-28 photos, mapped as the brief orders (TL->ch4, TR->ch3, ML->ch5 ...)
  blob-*.png       page-12 depth shapes
  plane-*.png      page-11 commercial airliners as white line art on transparency
  sparkle.png      page-9 four-point star
  bg-N.jpg         per-chapter page background (theme colour + sky at ~30% + tinted blobs + header band)
  bg-intro.jpg     front-matter background
"""
from pathlib import Path
import io
import numpy as np
import pymupdf as fitz
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[4]
ART_PDF = ROOT / "temp contents/ai proj stage2/study guide art.pdf"
OUT = ROOT / "assets/study-guide/v2/art"
OUT.mkdir(parents=True, exist_ok=True)
doc = fitz.open(ART_PDF)


def xref_image(page, xref, smask=0):
    pix = fitz.Pixmap(doc, xref)
    if smask:
        pix = fitz.Pixmap(pix, fitz.Pixmap(doc, smask))
    return Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")


# ---- page 28: sky photos. Brief: top-left -> ch4, top-right -> ch3, middle-left -> ch5 (more purple).
# Remaining: middle-right -> ch2 (bright morning), bottom-left -> ch1 (soft dawn), bottom-right -> ch6 (night).
SKY = {4: 1146, 3: 1148, 5: 1147, 2: 1149, 1: 1150, 6: 1151}
for ch, xref in SKY.items():
    xref_image(doc[27], xref).convert("RGB").save(OUT / f"sky-{ch}.jpg", quality=95)

# ---- page 12: depth blobs (with soft masks)
p12 = doc[11]
masks = {img[0]: img[1] for img in p12.get_images(full=True)}
for xref in (885, 889, 893, 897, 899, 888, 890):
    xref_image(p12, xref, masks[xref]).save(OUT / f"blob-{xref}.png")

# ---- page 9: the white four-point sparkle used beside headings in the format examples
p9 = doc[8]
m9 = {img[0]: img[1] for img in p9.get_images(full=True)}
sp = xref_image(p9, 842, m9[842])
a = np.asarray(sp).astype(float)
alpha = np.clip(a[..., 3] * 1.6, 0, 255)
white = np.dstack([np.full(alpha.shape, 255.0)] * 3 + [alpha]).astype(np.uint8)
Image.fromarray(white).save(OUT / "sparkle.png")

# ---- page 11: commercial airliners, vector line art on navy -> white lines on transparency
p11 = doc[10]
PLANES = {  # clip rectangles in PDF points
    "climb": (0, 140, 236, 240),
    "side": (232, 130, 451, 251),
    "top": (33, 546, 198, 704),
}
for name, clip in PLANES.items():
    pix = p11.get_pixmap(matrix=fitz.Matrix(6, 6), clip=fitz.Rect(clip), alpha=False)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3).astype(float)
    lum = a.max(axis=2)
    alpha = np.clip((lum - 70) / 150, 0, 1) * 255
    rgba = np.zeros((pix.height, pix.width, 4), dtype=np.uint8)
    rgba[..., :3] = 255
    rgba[..., 3] = alpha.astype(np.uint8)
    im = Image.fromarray(rgba)
    im = im.crop(im.getbbox())
    im.save(OUT / f"plane-{name}.png")

# ---- chapter palettes (from the brief) and page backgrounds
PAL = {
    0: dict(base="#2B5FB8", sky=4, blobA="#E15B83", blobB="#28B5F2", sky_op=.34),   # front matter (Content1.png look)
    1: dict(base="#7A99C7", sky=1, blobA="#DF8F9C", blobB="#C6CAE5", sky_op=.30),   # Dawn
    2: dict(base="#7FB6E0", sky=2, blobA="#F9E296", blobB="#6FC4FA", sky_op=.30),   # Morning
    3: dict(base="#2F93C9", sky=3, blobA="#72C7DB", blobB="#95CAEC", sky_op=.30),   # Midday
    4: dict(base="#2469D8", sky=4, blobA="#E15B83", blobB="#28B5F2", sky_op=.30),   # Afternoon
    5: dict(base="#4E4580", sky=5, blobA="#DC5983", blobB="#EC9C6B", sky_op=.30),   # Dusk
    6: dict(base="#1E2A4D", sky=6, blobA="#215096", blobB="#343C70", sky_op=.32),   # Midnight
}
W, H = 1240, 1754  # A4 at 150 dpi
HEADER = 78        # header band height (px at 150 dpi ~ 37pt)


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def feather(w, h):
    """Smooth 0..1 mask that reaches zero at every edge, so no blob can leave a rectangular seam."""
    x = np.minimum(np.arange(w), np.arange(w)[::-1]) / (w * 0.22)
    y = np.minimum(np.arange(h), np.arange(h)[::-1]) / (h * 0.22)
    m = np.clip(np.outer(np.clip(y, 0, 1), np.clip(x, 0, 1)), 0, 1)
    return m * m * (3 - 2 * m)


def tinted(blob, a, b, opacity, size):
    gray = ImageOps.grayscale(blob)
    t = ImageOps.colorize(gray, hexrgb(a), hexrgb(b)).convert("RGBA")
    al = np.asarray(blob.getchannel("A")).astype(float) * opacity * feather(blob.width, blob.height)
    t.putalpha(Image.fromarray(al.astype(np.uint8)))
    return t.resize(size, Image.Resampling.LANCZOS)


for ch, p in PAL.items():
    base = Image.new("RGB", (W, H), hexrgb(p["base"]))
    sky = Image.open(OUT / f"sky-{p['sky']}.jpg").convert("RGB")
    sky = ImageOps.fit(sky, (W, H), method=Image.Resampling.LANCZOS)
    sky = sky.filter(ImageFilter.GaussianBlur(2))
    if ch == 5:  # brief: make the chapter-5 photo more purple
        sky = ImageOps.colorize(ImageOps.grayscale(sky), (50, 40, 110), (226, 205, 240))
    if ch == 6:
        sky = ImageEnhance.Brightness(sky).enhance(0.9)
    im = Image.blend(base, sky, p["sky_op"]).convert("RGBA")
    # depth shapes from art page 12, big and soft, recoloured to the chapter palette
    for xref, box, op in [(893, (-300, -160, 980, 640), .95), (885, (700, 380, 1460, 1240), .85),
                          (897, (-420, 980, 820, 1860), .75), (899, (860, 1180, 1420, 1940), .6)]:
        blob = Image.open(OUT / f"blob-{xref}.png").convert("RGBA").filter(ImageFilter.GaussianBlur(14))
        im.alpha_composite(tinted(blob, p["blobA"], p["blobB"], op, (box[2] - box[0], box[3] - box[1])), (box[0], box[1]))
    # header band: a lighter strip of sky, as in the format examples
    band = Image.open(OUT / f"sky-{p['sky']}.jpg").convert("RGB")
    band = ImageOps.fit(band, (W, HEADER * 4), method=Image.Resampling.LANCZOS, centering=(0.5, 0.15))
    band = band.resize((W, HEADER), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(6))
    if ch == 5:
        band = ImageOps.colorize(ImageOps.grayscale(band), (110, 90, 160), (236, 222, 246))
    band = Image.blend(Image.new("RGB", (W, HEADER), hexrgb(p["base"])), band, 0.62)
    band = Image.blend(band, Image.new("RGB", (W, HEADER), (255, 255, 255)), 0.12)
    im.paste(band, (0, 0))
    name = "bg-intro.jpg" if ch == 0 else f"bg-{ch}.jpg"
    im.convert("RGB").save(OUT / name, quality=90)

print("prepared:", sorted(p.name for p in OUT.iterdir()))
