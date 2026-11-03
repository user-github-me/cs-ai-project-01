"""Prepare the original graphic treatments and the NASA photographs for Stage 2."""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import math
import struct
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
from fontTools.ttLib import TTFont
from fontTools import subset

BASE = Path(__file__).resolve().parents[1]
ART = BASE / 'art'
WORK = Path('/private/tmp/blue-impulse-stage2')
WORK.mkdir(parents=True, exist_ok=True)
W, H = 1920, 1080
RESAMPLE = Image.Resampling.LANCZOS
rng = np.random.default_rng(1997)


def save_jpg(image, name, quality=91):
    image.convert('RGB').save(ART / name, quality=quality, optimize=True)


def grain(image, strength=2.5):
    array = np.asarray(image.convert('RGB')).astype(np.float32)
    noise = rng.normal(0, strength, (image.height, image.width, 1))
    return Image.fromarray(np.uint8(np.clip(array + noise, 0, 255)))


def stars():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    glow = np.exp(-((xx-W*.86)/(W*.48))**2-((yy-H*.84)/(H*.75))**2)
    arr = np.zeros((H, W, 3), dtype=np.float32) + np.array([19, 10, 21])
    arr += glow[..., None] * np.array([35, 9, 22])
    im = grain(Image.fromarray(np.uint8(arr)), 1.7)
    draw = ImageDraw.Draw(im)
    for i in range(190):
        x, y = int(rng.integers(0, W)), int(rng.integers(0, H))
        radius = 1 if i < 178 else 2
        shade = int(rng.integers(65, 160))
        draw.ellipse((x-radius,y-radius,x+radius,y+radius), fill=(shade, int(shade*.83), int(shade*.76)))
    return im


starfield = stars()
save_jpg(starfield, 'starfield.jpg')

# Original liquid-ink texture: a deterministic, warped band field, not AI output.
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
x, y = xx/W, yy/H
u = x + .19*np.sin(5.6*y+1.9*np.sin(3.7*x))
v = y + .18*np.sin(4.7*x-2.6*y)
field = 2.6*u + .53*np.sin(6.1*v) + .28*np.sin(5.3*u+3*v)
t = np.mod(field, 1.0)
stops = np.array([0,.12,.17,.23,.28,.39,.45,.48,.54,.62,.69,.78,.82,.93,1])
cols = np.array([[24,8,24],[49,14,28],[104,36,55],[179,69,102],
                 [199,97,96],[233,78,0],[251,179,42],[249,221,177],
                 [73,25,22],[24,8,24],[65,14,79],[179,69,102],
                 [233,78,0],[251,179,42],[24,8,24]],dtype=np.float32)
rgb = np.stack([np.interp(t,stops,cols[:,i]) for i in range(3)],axis=-1)
quiet = np.clip((x-.22)/.55,0,1)**1.5
rgb = rgb*quiet[...,None] + np.array([24,8,24])*(1-quiet[...,None])
save_jpg(grain(Image.fromarray(np.uint8(rgb)),3.1), 'molten-ribbons.jpg',93)

# Use genuine Martian terrain from the NASA Sojourner photograph at the foot of a starfield.
terrain = Image.open(ART/'sojourner-on-mars.jpg').convert('RGB').crop((0,0,1276,365)).resize((W,400),RESAMPLE)
terrain = ImageOps.colorize(ImageOps.grayscale(terrain), '#522013', '#EFAC76')
mask = Image.new('L',(W,H),0)
d = ImageDraw.Draw(mask)
points = [(0,H),(0,858),(180,824),(395,858),(610,810),(825,833),(1040,783),(1270,810),(1490,745),(1720,780),(1920,751),(W,H)]
d.polygon(points,fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(.65))
terrain_full = Image.new('RGB',(W,H),'#AD582F')
terrain_full.paste(terrain,(0,680))
landscape = Image.composite(terrain_full,starfield,mask)
save_jpg(grain(landscape,1.4),'mars-landscape.jpg')


def disc(source, output):
    im = Image.open(ART/source).convert('RGB')
    # NASA sources have a dark surround. Derive the disc's bounding square from brightness.
    a = np.asarray(im)
    bright = (a.max(axis=2)>38)
    ys,xs = np.where(bright)
    left,top,right,bottom = xs.min(),ys.min(),xs.max()+1,ys.max()+1
    side = max(right-left,bottom-top)
    cx,cy = (left+right)/2,(top+bottom)/2
    im = im.crop((round(cx-side/2),round(cy-side/2),round(cx+side/2),round(cy+side/2))).resize((1600,1600),RESAMPLE)
    mask = Image.new('L',im.size)
    ImageDraw.Draw(mask).ellipse((4,4,1596,1596),fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1))
    im.putalpha(mask)
    im.save(ART/output,optimize=True)


disc('mars-source.jpg','mars.png')
disc('earth-source.jpg','earth.png')

# Carefully traced cutout from the existing NASA surface photograph; retain the real antenna.
rover = Image.open(ART/'sojourner-on-mars.jpg').convert('RGBA')
mask = Image.new('L',rover.size,0)
d = ImageDraw.Draw(mask)
outline = [(227,580),(518,417),(557,425),(584,437),(650,451),(771,475),(872,500),
           (909,512),(882,529),(1000,552),(1009,561),(1057,568),(1065,584),(1035,602),
           (1019,626),(1029,648),(1010,661),(1038,681),(1049,718),(1079,724),(1103,753),
           (1122,818),(1117,846),(1094,879),(1071,897),(1002,901),(984,889),(940,937),
           (884,973),(869,1028),(846,1061),(814,1086),(784,1096),(741,1083),(704,1057),
           (682,1022),(640,1024),(597,1007),(562,1015),(513,1000),(466,974),(439,942),
           (421,903),(393,946),(359,959),(311,953),(273,937),(244,908),(231,877),
           (231,850),(252,823),(279,819),(298,802),(276,788),(251,777),(252,763),
           (280,748),(262,720),(241,684),(255,650),(289,634),(262,603),(227,593)]
d.polygon(outline,fill=255)
d.line([(695,508),(658,170)],fill=255,width=18)
d.ellipse((646,162,671,184),fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(.6))
rover.putalpha(mask)
rover = rover.crop((205,142,1145,1115))
rover.save(ART/'sojourner-cutout.png',optimize=True)

# Original retro rocket illustration, supplied as SVG and raster for universal slide support.
rocket_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="1440" viewBox="0 0 720 1440">
<defs><linearGradient id="body"><stop stop-color="#B88062"/><stop offset=".3" stop-color="#F8DFBD"/><stop offset=".5" stop-color="#FFF0D4"/><stop offset=".72" stop-color="#E7B17C"/><stop offset="1" stop-color="#9B4C37"/></linearGradient>
<linearGradient id="fin"><stop stop-color="#F47524"/><stop offset=".5" stop-color="#D54113"/><stop offset="1" stop-color="#7D0101"/></linearGradient>
<linearGradient id="flame" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#FFF5D4"/><stop offset=".25" stop-color="#FBB32A"/><stop offset=".6" stop-color="#E94E00"/><stop offset="1" stop-color="#B34566" stop-opacity="0"/></linearGradient></defs>
<path d="M290 1002 C238 1120 305 1287 358 1422 C414 1300 486 1126 430 1002 Z" fill="url(#flame)"/>
<path d="M330 1012 C297 1125 327 1233 360 1307 C390 1215 424 1098 390 1012 Z" fill="#FFF0BE" opacity=".85"/>
<path d="M265 642 C154 746 133 874 129 1014 L283 918 Z" fill="url(#fin)" stroke="#4F1722" stroke-width="8"/>
<path d="M455 642 C566 746 587 874 591 1014 L437 918 Z" fill="url(#fin)" stroke="#4F1722" stroke-width="8"/>
<path d="M360 43 C255 204 243 351 247 673 L271 966 Q360 1007 449 966 L473 673 C477 351 465 204 360 43 Z" fill="url(#body)" stroke="#4F1722" stroke-width="8"/>
<path d="M360 43 C305 128 278 196 263 274 Q360 304 457 274 C442 196 415 128 360 43 Z" fill="url(#fin)"/>
<path d="M281 356 Q295 272 321 220" fill="none" stroke="#FFF2DA" stroke-width="12" stroke-linecap="round" opacity=".7"/>
<circle cx="360" cy="442" r="77" fill="#A9602D" stroke="#542519" stroke-width="7"/><circle cx="360" cy="442" r="59" fill="#24122F"/>
<path d="M323 438 Q328 407 355 405" stroke="#C76160" stroke-width="10" fill="none" stroke-linecap="round"/>
<path d="M262 841 Q360 871 458 841 L453 899 Q360 935 267 899 Z" fill="#B34566"/>
<path d="M278 957 Q360 983 442 957 L428 1017 Q360 1034 292 1017 Z" fill="#371525" stroke="#4F1722" stroke-width="6"/>
<path d="M350 774 L360 1130 L385 911 L368 767 Z" fill="#E94E00" stroke="#7D0101" stroke-width="5"/>
</svg>'''
(ART/'rocket.svg').write_text(rocket_svg)

# Fix the static instance's naming records after the variable-font extraction.
font_path = BASE/'fonts/Quicksand-Medium.ttf'
font = TTFont(font_path)
names = {1:'Quicksand',2:'Medium',3:'BlueImpulse:Quicksand-Medium',4:'Quicksand Medium',6:'Quicksand-Medium',16:'Quicksand',17:'Medium'}
for record in font['name'].names:
    if record.nameID in names:
        record.string = names[record.nameID].encode(record.getEncoding())
font.save(font_path)

# Horizon already belongs to the team's Stage 1 presentation; use its existing embedding.
deck = BASE.parents[1]/'final-presentation/BlueImpulse_Stage1_StatusReport_compressed.pptx'
with ZipFile(deck) as archive:
    data = archive.read('ppt/fonts/font4.fntdata')
    length = struct.unpack_from('<I',data,4)[0]
    horizon = TTFont(BytesIO(data[-length:]))
    horizon['head'].macStyle = 1
    horizon['OS/2'].fsSelection = 32
    horizon['OS/2'].usWeightClass = 700
    horizon['OS/2'].recalcUnicodeRanges(horizon)
    if 'DSIG' in horizon:
        del horizon['DSIG']
    options = subset.Options()
    options.hinting = False
    cleaner = subset.Subsetter(options=options)
    cleaner.populate(glyphs=horizon.getGlyphOrder())
    cleaner.subset(horizon)
    names = {1:'Horizon Presentation',2:'Bold',3:'BlueImpulse:Horizon-Presentation',4:'Horizon Presentation Bold',6:'HorizonPresentation-Bold',16:'Horizon Presentation',17:'Bold'}
    for record in horizon['name'].names:
        if record.nameID in names:
            record.string = names[record.nameID].encode(record.getEncoding())
    horizon.save(WORK/'Horizon.ttf')
    (WORK/'Horizon.fntdata').write_bytes(data)

print('Prepared original textures, accurate NASA cutouts, rocket source, and requested fonts.')
