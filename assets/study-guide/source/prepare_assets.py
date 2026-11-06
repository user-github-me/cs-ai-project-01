"""Extract the supplied artwork without changing the cover or chapter dividers."""
from pathlib import Path
import io
import json
import fitz
import numpy as np
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'assets/study-guide/art'
SOURCE = ROOT / 'temp contents/study guide art.pdf'
OUT.mkdir(parents=True, exist_ok=True)
doc = fitz.open(SOURCE)

def rgba_xref(page, xref):
    smask = next((v[1] for v in page.get_images(full=True) if v[0] == xref), 0)
    pix = fitz.Pixmap(doc, xref)
    if smask:
        pix = fitz.Pixmap(pix, fitz.Pixmap(doc, smask))
    return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGBA')

def crop(page_no, box, name, remove_white=True):
    p = doc[page_no-1]
    pix = p.get_pixmap(matrix=fitz.Matrix(3, 3), clip=fitz.Rect(box), alpha=False)
    im = Image.frombytes('RGB', [pix.width, pix.height], pix.samples).convert('RGBA')
    if remove_white:
        # Only remove the exterior white canvas. White title bars stay intact.
        for x, y in [(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)]:
            if min(im.getpixel((x,y))[:3]) > 244:
                ImageDraw.floodfill(im, (x,y), (0,0,0,0), thresh=14)
    im.save(OUT/name)
    return im

# Actual printed chapter labels take precedence over the shifted page list in the prompt.
fixed = fitz.open()
fixed.insert_pdf(doc, from_page=15, to_page=21)
fixed.save(OUT/'cover-and-dividers.pdf', garbage=4, deflate=True)
doc[15].get_pixmap(matrix=fitz.Matrix(1.5,1.5), alpha=False).save(OUT/'book-cover.png')

specs = {
    1: [(5,(61,450,222,692)), (5,(248,450,537,692))],
    2: [(5,(61,257,317,407)), (5,(345,260,525,405))],
    3: [(6,(61,257,317,407)), (6,(345,260,525,405))],
    4: [(4,(248,450,537,692)), (4,(61,450,222,692))],
    5: [(4,(61,257,317,407)), (4,(338,257,502,407))],
    6: [(6,(248,450,537,692)), (6,(61,450,222,692))],
}
for ch, variants in specs.items():
    for kind, (pn,box) in zip(['light','dark'],variants):
        crop(pn,box,f'window-{ch}-{kind}.png')
crop(7,(65,246,320,405),'folder-base.png')

nodes={1:833,2:832,3:836,4:834,5:835,6:837}
for ch,xref in nodes.items():
    rgba_xref(doc[7],xref).save(OUT/f'node-{ch}.png')

# These are the six photographs identified on art page 28.
photos={1:1150,2:1149,3:1148,4:1146,5:1147,6:1151}
for ch,xref in photos.items():
    rgba_xref(doc[27],xref).convert('RGB').save(OUT/f'sky-{ch}.jpg',quality=94)

plane=crop(11,(33,546,198,704),'aircraft-crop.png',False)
arr=np.array(plane).astype(float)
alpha=np.clip((arr[:,:,:3].max(axis=2)-80)/175,0,1)*255
line=np.zeros_like(arr,dtype=np.uint8)
line[:,:,:3]=255;line[:,:,3]=alpha.astype(np.uint8)
Image.fromarray(line).save(OUT/'aircraft.png')

for xref in [885,889,893,895,897]:
    rgba_xref(doc[11],xref).save(OUT/f'depth-{xref}.png')

palettes={
 1:dict(name='Dawn',bg='#7A99C7',deep='#466BAA',light='#E5D9E7',accent='#DF8F9C',ink='#212C4A'),
 2:dict(name='Morning',bg='#8FBCDD',deep='#356DB7',light='#FAF6D3',accent='#EED583',ink='#212C4A'),
 3:dict(name='Midday',bg='#388BC5',deep='#168FCB',light='#C4E3F7',accent='#69BEC1',ink='#153756'),
 4:dict(name='Afternoon',bg='#193FA8',deep='#2469D8',light='#D5E5F5',accent='#E15B83',ink='#142B52'),
 5:dict(name='Dusk',bg='#5D6B98',deep='#463373',light='#D6C9E5',accent='#DC5983',ink='#302444'),
 6:dict(name='Midnight',bg='#212C4A',deep='#2B2E65',light='#E6E4E5',accent='#215096',ink='#212C4A'),
}
for ch,p in palettes.items():
    W,H=1191,1685
    im=Image.new('RGB',(W,H),p['bg'])
    sky=ImageOps.fit(Image.open(OUT/f'sky-{ch}.jpg'),(W,H),method=Image.Resampling.LANCZOS)
    if ch==5:
        sky=ImageOps.colorize(ImageOps.grayscale(sky),'#322F72','#D6C9E5')
    im=Image.blend(im,sky,.30).convert('RGBA')
    # Supplied blurred page-12 objects, recoloured to their chapter palette.
    for xref,box,opacity in [(893,(-200,-240,880,500),.30),(885,(780,350,1400,1100),.28),(897,(-350,950,700,1700),.22)]:
        blob=Image.open(OUT/f'depth-{xref}.png').convert('RGBA')
        gray=ImageOps.grayscale(blob)
        tinted=ImageOps.colorize(gray,p['accent'],p['light']).convert('RGBA')
        tinted.putalpha(blob.getchannel('A').point(lambda v:int(v*opacity)))
        tinted=tinted.resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
        im.alpha_composite(tinted,(box[0],box[1]))
    jet=Image.open(OUT/'aircraft.png').resize((380,365),Image.Resampling.LANCZOS)
    jet.putalpha(jet.getchannel('A').point(lambda v:int(v*.15)))
    im.alpha_composite(jet,(790,1200))
    im.convert('RGB').save(OUT/f'background-{ch}.jpg',quality=92)

(OUT/'palette.json').write_text(json.dumps(palettes,indent=2))
(OUT/'provenance.json').write_text(json.dumps({
 'source':'User-supplied study guide art.pdf',
 'cover_source_page':16,'divider_source_pages':list(range(17,23)),
 'windows_source_pages':[4,5,6],'folder_source_page':7,'diagram_nodes_source_page':8,
 'aircraft_source_page':11,'depth_source_page':12,'sky_source_page':28,
 'sky_opacity':0.30,'chapter_5_sky_recoloured_purple':True,
 'note':'Cover and dividers are imported as PDF pages without overlays or edits.'
},indent=2))
print('Prepared exact cover, six dividers, chapter boxes, diagram shapes and backgrounds.')
