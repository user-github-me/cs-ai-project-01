"""Produce written versions of the actual videos, with timestamps and original book excerpts."""
from pathlib import Path
import argparse
import json
import html
from fontTools.ttLib import TTFont as FontToolsFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
import fitz

ROOT=Path(__file__).resolve().parents[1]
W,H=595.28,841.89
BG=HexColor('#212C4A');INK=HexColor('#E6E4E5');ACCENT=HexColor('#E15B83')
OUT=ROOT.parents[1]/'assets/tutorials'
AUDIT=[]

def clean(s):
    return html.escape(str(s).replace('α','alpha').replace('γ','gamma').replace('→',' to ').replace('−','-'))

def para(c,text,x,top,width,size=11.8,color=INK,face='Inter',leading=None,max_height=None):
    style=ParagraphStyle('text',fontName=face,fontSize=size,leading=leading or size*1.38,textColor=color,spaceAfter=0)
    p=Paragraph(text,style)
    _,height=p.wrap(width,1000)
    if max_height is not None and height>max_height:
        raise ValueError(f'Text overflow: {height:.1f}>{max_height:.1f}: {text[:90]}')
    p.drawOn(c,x,top-height)
    AUDIT.append(dict(page=c.getPageNumber(),x=x,top=top,width=width,height=height,text=text))
    return top-height

def page_base(c,lesson,section,number):
    c.setFillColor(BG);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(ACCENT);c.setFont('InterBold',10)
    c.drawString(42,H-42,f'BLUE IMPULSE  /  VIDEO TUTORIAL {lesson["number"]:02}')
    c.setStrokeColor(ACCENT);c.setLineWidth(1.2);c.line(42,46,W-42,46)
    c.setFont('Inter',9);c.setFillColor(INK)
    c.drawString(42,29,section);c.drawRightString(W-42,29,str(number))

def fit_image(c,path,x,y,width,height):
    image=ImageReader(str(path));iw,ih=image.getSize();scale=min(width/iw,height/ih)
    fw,fh=iw*scale,ih*scale
    c.drawImage(image,x,y+height-fh,width=fw,height=fh,mask='auto')
    return fh

def clock(seconds):
    return f'{int(seconds)//60:02}:{int(seconds)%60:02}'

def main():
    global OUT
    parser=argparse.ArgumentParser()
    default_output=OUT if (ROOT.parents[1]/'assets/study-guide').exists() else ROOT/'generated-tutorials'
    parser.add_argument('--output',type=Path,default=default_output)
    OUT=parser.parse_args().output.resolve()
    OUT.mkdir(parents=True,exist_ok=True)
    fontdir=ROOT/'build/pdf-fonts';fontdir.mkdir(exist_ok=True)
    for name,src in [('Inter','Inter-400.woff2'),('InterBold','Inter-700.woff2')]:
        font=FontToolsFont(ROOT/'assets/fonts'/src);font.flavor=None
        target=fontdir/f'{name}.ttf';font.save(target);pdfmetrics.registerFont(TTFont(name,str(target)))
    pdfmetrics.registerFont(TTFont('Anta',str(ROOT/'assets/fonts/Anta-Regular.ttf')))
    pages=json.loads((ROOT/'assets/book/provenance.json').read_text())['pages']
    manifest=[]
    for lesson_path in sorted(ROOT.glob('lesson-??.json')):
        lesson=json.loads(lesson_path.read_text());n=lesson['number']
        out=OUT/f'BlueImpulse_Video{n:02}_{lesson["slug"]}_Tutorial.pdf'
        c=canvas.Canvas(str(out),pagesize=(W,H),pageCompression=1)
        c.setTitle(f'Blue Impulse Video {n:02} — {lesson["title"]} — Written tutorial')
        c.setAuthor('Blue Impulse');c.setSubject('Written companion to the narrated study-guide tutorial')
        page_base(c,lesson,'Written tutorial · book-based lesson',1)
        top=para(c,clean(lesson['title']),42,H-80,510,size=31,face='Anta',leading=36,max_height=120)
        para(c,f'{clock(lesson["duration"])} video · English narration · Guide-linked examples',42,top-15,510,size=12,color=ACCENT)
        para(c,'Learn with the book',42,top-67,267,size=19,face='Anta')
        y=top-105
        for i,item in enumerate(lesson['objectives'],1):
            y=para(c,f'<b>{i}.</b> {clean(item)}',42,y,267,size=12,max_height=60)-16
        para(c,'Keep the 96-page Blue Impulse study guide open. Its printed page numbers match the PDF viewer. The screenshots in this tutorial are exact crops from that book.',42,y-7,267,size=11.8,max_height=115)
        fit_image(c,ROOT/'assets/book/cover.png',348,370,180,255)
        para(c,'Guide pages: '+', '.join(map(str,lesson['pages']))+'.',42,318,510,size=12,color=ACCENT)
        para(c,'How to use this PDF',42,276,510,size=19,face='Anta')
        para(c,'Follow the timestamp at the top of each lesson page to find the matching video section. Read the book excerpt, work through the teaching text, and stop at each question before reading the answer. The complete narration is included here, with separate editable scripts and subtitle files in the package.',42,242,510,size=11.8,max_height=120)
        para(c,'Practice file: <b>BlueImpulse_Demonstrations.py</b><br/>Requires Python 3.9+ and no extra packages. The source guide, scripts, subtitle sidecars, and editable video project are included in the tutorial package.',42,140,510,size=10.8,max_height=75)
        c.bookmarkPage('start');c.addOutlineEntry('Start here','start',0)
        c.showPage()
        for i,sc in enumerate(lesson['scenes'],1):
            page_base(c,lesson,f'{clock(sc["start"])}–{clock(sc["start"]+sc["duration"])} · Guide p. {sc["page"]}',i+1)
            title_top=para(c,clean(sc['title']),42,H-78,510,size=25,face='Anta',leading=29,max_height=64)
            para(c,f'Video {clock(sc["start"])}–{clock(sc["start"]+sc["duration"])}  /  Study guide page {sc["page"]}',42,title_top-12,510,size=10.5,color=ACCENT)
            record=pages[str(sc['page'])]
            if record['excerpts']:
                default={'q-demo':2,'pipeline-demo':1,'latency-demo':1,'message-demo':2,'cpu-demo':0}.get(sc['kind'],0)
                b=min(sc.get('block',default),len(record['excerpts'])-1)
                image=ROOT/record['excerpts'][b]['path']
                fit_image(c,image,42,447,510,211)
                para(c,'Exact excerpt from the Blue Impulse study guide',42,435,510,size=9.5,color=ACCENT)
            else:
                fit_image(c,ROOT/'assets/book/cover.png',225,434,145,205)
            text='<br/><br/>'.join(clean(s) for s in sc['cues'])
            bottom=para(c,text,42,409,510,size=11.1,leading=14.4,max_height=318)
            if sc['kind']=='question':
                # The answer is in the teaching text after the pause prompt; retain the video’s full reasoning.
                para(c,f'<b>Pause first:</b> {clean(sc["prompt"])}<br/><b>Check:</b> {clean(sc["answer"])}',42,min(bottom-14,112),510,size=10.5,color=ACCENT,max_height=70)
            key=f'chapter-{i}';c.bookmarkPage(key);c.addOutlineEntry(f'{clock(sc["start"])} {sc["title"]}',key,0)
            c.linkURL('https://github.com/user-github-me/cs-ai-project-01/blob/main/assets/study-guide/BlueImpulse_Study_Guide.pdf#page='+str(sc['page']),(42,413,552,438),relative=0,thickness=0)
            c.showPage()
        c.save()
        doc=fitz.open(out)
        assert len(doc)==len(lesson['scenes'])+1
        manifest.append(dict(number=n,file=out.name,pages=len(doc),video_seconds=lesson['duration']))
        print(f'{out.name}: {len(doc)} pages')
    (ROOT/'build/pdf-layout-audit.json').write_text(json.dumps(AUDIT,indent=2,ensure_ascii=False)+'\n')
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    merged=fitz.open()
    for item in manifest:
        part=fitz.open(OUT/item['file']);merged.insert_pdf(part)
    merged.set_metadata({'title':'Blue Impulse — Five Video Tutorials','author':'Blue Impulse'})
    merged.save(OUT/'BlueImpulse_All_Video_Tutorials.pdf',garbage=4,deflate=True)

if __name__=='__main__':main()
