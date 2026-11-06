"""Validate the delivered PDF against its content, artwork and page map."""
from pathlib import Path
import hashlib,json,re,unicodedata
import fitz
from fontTools.ttLib import TTCollection,TTFont
from exercises import EXERCISES

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'assets/study-guide'
pdf=fitz.open(BASE/'BlueImpulse_Study_Guide.pdf')
source=fitz.open(ROOT/'temp contents/study guide art.pdf')
pages=json.loads((BASE/'source/page-map.json').read_text())
layout=json.loads((BASE/'source/layout-audit.json').read_text())
exercise_map=json.loads((BASE/'source/exercise-map.json').read_text())
manifest=json.loads((BASE/'manifest.json').read_text())

def norm(t):
    return re.sub(r'\s+','',unicodedata.normalize('NFKC',str(t)))

assert len(pdf)==len(pages)==96
assert hashlib.sha256((BASE/'BlueImpulse_Study_Guide.pdf').read_bytes()).hexdigest()==manifest['sha256']
assert all(v['pages'] for v in exercise_map.values()),'An exercise was omitted'
fixed_checks=[]
text_checks=0
for i,p in enumerate(pages):
    page=pdf[i]
    if p['kind']=='fixed':
        original=source[15+p['fixed']]
        a=page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
        b=original.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
        assert a.width==b.width and a.height==b.height and a.samples==b.samples,('Artwork changed',i+1)
        fixed_checks.append(i+1)
        continue
    text=norm(page.get_text())
    assert norm(EXERCISES[p['exercise']]) in text,('Missing exercise',i+1)
    assert 'PAUSE&TRY' in text
    for block in p['blocks']:
        expected=[block['title']]
        if block['kind']=='text':expected.append(block['text'])
        elif block['kind']=='table':expected+=block['headers']+[v for row in block['rows'] for v in row]
        else:expected+=block['labels']+[block['caption']]
        for value in expected:
            assert norm(value) in text,('Missing text',i+1,value)
            text_checks+=1
    assert any(link.get('uri','').endswith('/exercises.md') for link in page.get_links()),('Missing exercise link',i+1)
    boxes=[fitz.Rect(e['x']-1,842.25-e['y_top']-1,e['x']+e['width']+1,842.25-e['y_top']+e['height']+1) for e in layout if e['page']==i+1]
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                r=fitz.Rect(span['bbox'])
                if r.y0<min(box.y0 for box in boxes)-2 or r.y0>795:continue  # page title, header and footer
                assert any(box.contains(r) for box in boxes),('Text outside box',i+1,span['text'],list(r))

for font,collection_index,names in [('/System/Library/Fonts/Avenir.ttc',0,['text','caption']),('/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf',None,[])]:
    f=TTCollection(font).fonts[collection_index] if collection_index is not None else TTFont(font)
    cmap=f.getBestCmap()
    if names:
        strings=list(EXERCISES.values())
        for p in pages:
            for b in p.get('blocks',[]):
                strings.extend(str(b.get(name,'')) for name in names)
                if b['kind']=='table':strings.extend(str(v) for row in b['rows'] for v in row)
        missing={c for c in ''.join(strings) if ord(c)>31 and ord(c) not in cmap}
        assert not missing,('Missing font glyphs',sorted(missing))

links=[l for l in pdf[1].get_links() if l['kind']==fitz.LINK_GOTO]
assert len(links)==6,('Contents links',len(links))
assert len(pdf.get_toc())==len(pages)
result=dict(status='passed',pages=len(pdf),unchanged_artwork_pages=fixed_checks,
            verified_text_items=text_checks,source_exercises=len(EXERCISES),
            exercise_pages=len(pages)-len(fixed_checks),contents_links=len(links),
            minimum_prose_font_pt=min(e['font_size'] for e in layout if e['role']=='content'),
            pdf_sha256=manifest['sha256'])
(BASE/'source/verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
