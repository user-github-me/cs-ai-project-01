"""Build the searchable study guide, fixed page map and visual proofs.

Requires PyMuPDF, ReportLab, Pillow, NumPy and fontTools. Run prepare_assets.py
first. macOS supplies Avenir and DIN; only their permitted PDF subsets are embedded.
"""
from pathlib import Path
from functools import lru_cache
from html import escape
import hashlib, io, json, math, re, sys
import fitz
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from fontTools.ttLib import TTCollection, TTFont as FontToolsFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.utils import ImageReader
from guide_content import PAGES, B, T
from exercises import EXERCISES, source_path, label
from reference_content import TITLES, GOALS, TERMS

ROOT=Path(__file__).resolve().parents[3]
DEST=ROOT/'assets/study-guide'
ART=DEST/'art'
TMP=Path('/private/tmp/blue-impulse-study-review')
TMP.mkdir(exist_ok=True)
W,H=595.5,842.25
M=35.0
BW=W-2*M-5
PALETTES={int(k):v for k,v in json.loads((ART/'palette.json').read_text()).items()}

def register_fonts():
    collection=TTCollection('/System/Library/Fonts/Avenir.ttc')
    for name,index in [('Avenir',0),('AvenirBold',4),('AvenirOblique',1)]:
        path=TMP/f'{name}.ttf'
        collection.fonts[index].save(path)
        pdfmetrics.registerFont(TTFont(name,str(path)))
    pdfmetrics.registerFontFamily('Avenir',normal='Avenir',bold='AvenirBold',italic='AvenirOblique')
    pdfmetrics.registerFont(TTFont('DIN','/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Anta',str(DEST/'fonts/Anta-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('Smiley',str(DEST/'fonts/SmileySans-Oblique.ttf')))

def para(text, width, size=11.2, color='#212C4A', font='Avenir', leading=None):
    style=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.36,
                         textColor=HexColor(color),spaceBefore=0,spaceAfter=0,
                         allowWidows=0,allowOrphans=0,splitLongWords=True)
    p=Paragraph(escape(str(text)).replace('\n','<br/>'),style)
    _,height=p.wrap(width,10000)
    return p,height

def draw_p(c,text,x,top,width,size=11.2,color='#212C4A',font='Avenir',leading=None):
    p,height=para(text,width,size,color,font,leading)
    p.drawOn(c,x,top-height)
    return height

@lru_cache(maxsize=800)
def skin(ch,variant,width,height,folder=False):
    density=2
    original=Image.open(ART/('folder-base.png' if folder else f'window-{ch}-{variant}.png')).convert('RGBA')
    # Shrink the original chrome before stretching the interior. Dots, rounded
    # corners, folder tabs and the original offset shadow retain their shape.
    original=original.resize((round(original.width*.40),round(original.height*.40)),Image.Resampling.LANCZOS)
    if folder:
        a=np.array(original).astype(float)
        target=np.array(tuple(int(PALETTES[ch]['light'][i:i+2],16) for i in (1,3,5)))
        a[:,:,:3]=np.clip(a[:,:,:3]/np.array([194,218,229])*target,0,255)
        original=Image.fromarray(a.astype(np.uint8))
    ow,oh=original.size
    left=min(76,ow//3);right=min(16,ow//5)
    top=min(34 if not folder else 42,oh//3);bottom=min(17,oh//5)
    dw,dh=max(round(width*density),left+right+1),max(round(height*density),top+bottom+1)
    out=Image.new('RGBA',(dw,dh))
    sx=[0,left,ow-right,ow];sy=[0,top,oh-bottom,oh]
    dx=[0,left,dw-right,dw];dy=[0,top,dh-bottom,dh]
    for yi in range(3):
        for xi in range(3):
            tile=original.crop((sx[xi],sy[yi],sx[xi+1],sy[yi+1]))
            tile=tile.resize((dx[xi+1]-dx[xi],dy[yi+1]-dy[yi]),Image.Resampling.LANCZOS)
            out.paste(tile,(dx[xi],dy[yi]))
    return ImageReader(out)

def table_object(block,width,ch,size):
    count=len(block['headers'])
    if count>=5:
        colw=[width*.21]+[width*.79/(count-1)]*(count-1)
        fs=min(size,9.0)
    elif count==3:
        colw=[width*.24,width*.36,width*.40];fs=min(size,10.1)
    else:
        colw=[width*.35,width*.65] if count==2 else [width/count]*count
        fs=min(size,10.4)
    data=[]
    for idx,row in enumerate([block['headers']]+block['rows']):
        data.append([para(v,colw[j]-12,fs,'#FFFFFF' if idx==0 else PALETTES[ch]['ink'],
                          'AvenirBold' if idx==0 else 'Avenir',fs*1.27)[0] for j,v in enumerate(row)])
    t=Table(data,colWidths=colw,hAlign='LEFT')
    t.setStyle(TableStyle([
      ('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),HexColor(PALETTES[ch]['deep'])),
      ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
      ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ]))
    _,height=t.wrap(width,10000)
    return t,height

def block_height(block,width,ch,size):
    if block['kind']=='text':
        _,h=para(block['text'],width-31,size)
        _,th=para(block['title'],width-31,15,font='Smiley',leading=20)
        return 26+th+6+h+15
    if block['kind']=='table':
        _,h=table_object(block,width-31,ch,size)
        return 25+22+6+h+15
    if block['kind']=='diagram':
        _,cap=para(block.get('caption',''),width-31,10.1)
        return 25+22+(111 if block.get('diagram')=='branch' else 71)+cap+14
    raise ValueError(block['kind'])

def arrow(c,x1,y1,x2,y2,col,width=1.3):
    c.setStrokeColor(HexColor(col));c.setLineWidth(width)
    c.line(x1,y1,x2,y2)
    angle=math.atan2(y2-y1,x2-x1)
    p=c.beginPath();p.moveTo(x2,y2)
    for offset in [-.5,.5]:
        p.lineTo(x2-6*math.cos(angle+offset),y2-6*math.sin(angle+offset))
    p.close();c.setFillColor(HexColor(col));c.drawPath(p,fill=1,stroke=0)

def node(c,ch,text,x,top,width,height=43):
    c.drawImage(str(ART/f'node-{ch}.png'),x,top-height,width,height,mask='auto')
    color=PALETTES[ch]['ink'] if ch in [1,2,3] else '#FFFFFF'
    p,h=para(text,width-14,10.0,color,'AvenirBold',11.7)
    p.drawOn(c,x+6,top-(height-5-h)/2-h-1)

def draw_diagram(c,b,x,top,width,ch):
    start=top-46
    labels=b['labels'];col=PALETTES[ch]['deep']
    if b.get('diagram')=='branch':
        node(c,ch,labels[0],x+16,start-25,width*.36,46)
        for k,text in enumerate(labels[1:]):
            ntop=start-k*53
            node(c,ch,text,x+width*.57,ntop,width*.37,43)
            arrow(c,x+width*.40,start-48,x+width*.56,ntop-22,col)
        cap_top=start-110
    else:
        gap=17;inner=width-32;n=len(labels);nw=(inner-gap*(n-1))/n
        for j,text in enumerate(labels):
            nx=x+16+j*(nw+gap)
            node(c,ch,text,nx,start,nw,44)
            if j<n-1 and b.get('diagram')!='tiles':
                if b.get('diagram')=='bidirectional':
                    arrow(c,nx+nw+2,start-18,nx+nw+gap-3,start-18,col)
                    arrow(c,nx+nw+gap-3,start-26,nx+nw+2,start-26,col)
                else:
                    arrow(c,nx+nw+2,start-21,nx+nw+gap-3,start-21,col)
        if b.get('diagram')=='loop':
            y=start-54
            c.setStrokeColor(HexColor(col));c.setLineWidth(1)
            c.line(x+width-25,start-45,x+width-25,y)
            c.line(x+width-25,y,x+25,y)
            arrow(c,x+25,y,x+25,start-45,col,1)
        cap_top=start-70
    draw_p(c,b.get('caption',''),x+16,cap_top,width-32,10.1,PALETTES[ch]['ink'])

def draw_block(c,b,x,top,width,height,ch,variant,size):
    folder=b['kind'] in ['diagram','table']
    c.drawImage(skin(ch,variant,round(width,2),round(height,2),folder),x,top-height,width,height,mask='auto')
    dark=variant=='dark' and ch in [1,4,5,6] and not folder
    color='#FFFFFF' if dark else PALETTES[ch]['ink']
    if b['kind']=='text':
        title_h=draw_p(c,b['title'],x+15,top-24,width-31,15,color,'Smiley',20)
        draw_p(c,b['text'],x+15,top-24-title_h-6,width-31,size,color)
    elif b['kind']=='table':
        draw_p(c,b['title'],x+15,top-24,width-31,17,color,'DIN',20)
        table,th=table_object(b,width-31,ch,size)
        table.drawOn(c,x+15,top-25-22-6-th)
    else:
        draw_p(c,b['title'],x+15,top-24,width-31,17,color,'DIN',20)
        draw_diagram(c,b,x,top,width,ch)

def front_pages():
    return [
      dict(kind='fixed',fixed=0,key='cover',title='Cover',chapter=0),
      dict(kind='toc',key='contents',chapter=4,title='Your route through the guide',exercise='5.1',blocks=[]),
      dict(kind='content',key='learning-goals-1',chapter=4,title='What you will learn',exercise='1.5',source='Team learning-outcomes files',blocks=[B(f'0{i} · {TITLES[i]}',GOALS[i]) for i in [1,2,3]]),
      dict(kind='content',key='learning-goals-2',chapter=4,title='From concepts to decisions',exercise='6.5',source='Team learning-outcomes files',blocks=[B(f'0{i} · {TITLES[i]}',GOALS[i]) for i in [4,5,6]]),
    ]

def make_schedule():
    pages=front_pages()
    used={p['exercise'] for p in PAGES}
    for ch in range(1,7):
        pages.append(dict(kind='fixed',fixed=ch,key=f'chapter-{ch}',title=TITLES[ch],chapter=ch))
        pages.extend(dict(p,kind='content') for p in PAGES if p['chapter']==ch)
        terms=TERMS[ch]
        for j in range(0,len(terms),9):
            k=j//9+1
            pages.append(dict(kind='content',key=f'key-terms-{ch}-{k}',title=f'Key terms · {ch:02d}',chapter=ch,
                              exercise={1:'1.1c',2:'2.2',3:'3.1a',4:'4.6a',5:'5.1',6:'6.3'}[ch],source='Team key-terms files; definitions clarified',
                              blocks=[T('Build your vocabulary',['Term','Meaning'],terms[j:j+9]),
                                      B('Use the terms in an explanation','Choose two terms and connect them in a sentence about a working system. A definition is useful when it helps you explain a mechanism, compare alternatives or justify a decision. Return to the relevant teaching page if you cannot yet give an example.')] ))
        remaining=[key for key in EXERCISES if key.startswith(f'{ch}.') and key not in used]
        for j in range(0,len(remaining),4):
            batch=remaining[j:j+4]
            if not batch:continue
            pages.append(dict(kind='content',key=f'practice-{ch}-{j//4+1}',title=f'Practice · Chapter {ch}',chapter=ch,
                              exercise=batch[-1],source='Team GitHub exercises',
                              blocks=[B('Try first, then check feedback','Write your reasoning before opening the explained answers after the six chapter missions. Show units and intermediate steps for calculations. For comparisons, use the same criteria on both sides. Match the question number with the answer key in this complete edition.')]+[B(label(k),EXERCISES[k]) for k in batch[:-1]]))
    pages.append(dict(kind='content',key='sources',chapter=6,title='Sources & acknowledgements',exercise='6.7',source='Blue Impulse project materials',blocks=[
      B('Learning materials','This guide is an edited synthesis of the six chapter PDFs supplied by Blue Impulse, with learning outcomes, key terms and exercises from the project repository at revision 9a645d0. The team’s source notes credit Cambridge International AS & A Level Computer Science and disclose use of Gemini, Claude and ChatGPT. The supplied files do not identify a complete textbook edition or bibliography.'),
      B('Artwork and production','The unchanged cover and six labelled dividers come from study guide art.pdf. Its window boxes, folder panels, diagram shapes, aircraft and sky images are reused throughout; the supplementary art PDF guides the layouts. Anta, DIN Condensed, Smiley Sans and Avenir follow the written font brief. Neogpt assisted with editing, diagrams, layout and PDF production.'),
      B('How to read this edition','Page numbers refer to physical PDF pages, including the cover and dividers. Each teaching or reference page ends with a question from the team’s exercise files. The complete Stage 2 edition includes six missions, resources and explained answers after the core chapters. Wording is lightly edited for clarity and technical accuracy. Worked examples teach methods using separate examples. The original art’s printed chapter labels determine the divider order.')
    ]))
    for idx,p in enumerate(pages):p['page']=idx+1
    return pages

LAYOUT=[]

def render_content(c,p):
    ch=p['chapter'];palette=PALETTES[ch]
    c.drawImage(str(ART/f'background-{ch}.jpg'),0,0,W,H)
    c.saveState();c.setFillColor(HexColor(palette['deep']));c.setFillAlpha(.7);c.rect(0,H-30,W,30,stroke=0,fill=1);c.restoreState()
    c.setFillColor(HexColor('#FFFFFF'));c.setFont('DIN',10)
    c.drawString(M,H-19,'BLUE IMPULSE  /  STUDY GUIDE')
    c.drawRightString(W-M,H-19,f'{palette["name"].upper()}  ·  {TITLES[ch]}')
    title=p['title'].replace('→','/')
    title_h=draw_p(c,title,M,H-48,BW,28,'#FFFFFF','Anta',34)
    content_top=H-48-title_h-20
    key=p['exercise'];question=EXERCISES[key]
    _,qh=para(question,BW-31,10.6,leading=14.3)
    ex_height=max(101,57+qh+12)
    ex_top=50+ex_height
    blocks=p['blocks']
    chosen=None
    for fs in [11.2,10.8,10.4]:
        heights=[block_height(b,BW,ch,fs) for b in blocks]
        total=sum(heights)+9*max(0,len(blocks)-1)
        if total<=content_top-ex_top-17:
            chosen=fs,heights,total;break
    if chosen is None:
        raise RuntimeError(f'Page {p["page"]} {p["key"]} needs {total:.1f} pt; available {content_top-ex_top-17:.1f}')
    fs,heights,total=chosen
    y=content_top
    for i,(b,bh) in enumerate(zip(blocks,heights)):
        variant='dark' if i%3==1 else 'light'
        draw_block(c,b,M,y,BW,bh,ch,variant,fs)
        LAYOUT.append(dict(page=p['page'],role='content',kind=b['kind'],title=b['title'],x=M,y_top=y,width=BW,height=bh,font_size=fs))
        y-=bh+9
    # All teaching, reference, contents and learning-goal pages end with a question.
    c.drawImage(skin(ch,'light',BW,ex_height),M,50,BW,ex_height,mask='auto')
    draw_p(c,'PAUSE & TRY',M+15,ex_top-24,BW-31,17,palette['ink'],'DIN',19)
    draw_p(c,question,M+15,ex_top-46,BW-31,10.6,palette['ink'],leading=14.3)
    c.setFillColor(HexColor(palette['ink']));c.setFont('Avenir',7.7)
    c.drawString(M+15,60,f'{label(key)}  ·  Adapted from GitHub exercises')
    c.linkURL('https://github.com/user-github-me/cs-ai-project-01/blob/main/'+source_path(key),(M+12,55,M+BW-12,72),relative=0,thickness=0)
    LAYOUT.append(dict(page=p['page'],role='exercise',key=key,x=M,y_top=ex_top,width=BW,height=ex_height,font_size=10.6))
    footer='#FFFFFF' if ch in [4,5,6] else '#212C4A'
    c.setFillColor(HexColor(footer));c.setFont('Avenir',8.4)
    c.drawString(M,28,'How machines sense, connect, and act')
    c.setFont('AvenirBold',10);c.drawRightString(W-M,28,str(p['page']))
    c.showPage()

def main():
    register_fonts()
    schedule=make_schedule()
    starts={p['chapter']:p['page'] for p in schedule if p['kind']=='fixed' and p['chapter']}
    ends={ch:max(p['page'] for p in schedule if p['chapter']==ch and p['key']!='sources' and p['key'] not in ['contents','learning-goals-1','learning-goals-2']) for ch in range(1,7)}
    schedule[1]['blocks']=[
      T('Six chapters, one connected story',['Chapter','Read'],[[f'{i:02d} · {TITLES[i]}',f'Pages {starts[i]}–{ends[i]} · {PALETTES[i]["name"]}'] for i in range(1,7)]),
      B('How to study','Start with a chapter’s learning goals, then read one teaching page at a time. Follow the diagram or worked example. Pause at the question before moving on, and write an answer in your own notes. Then try the matching chapter mission in the activity section beginning on page 97. Explained answers follow the six missions.'),
      B('Find a page quickly','This PDF has bookmarks for every chapter and teaching page. Page numbers match the PDF viewer, including the unchanged cover and chapter dividers. The learning goals are on pages 3–4. Missions, optional resources and the complete answer key follow page 96; their bookmarks provide direct navigation. GitHub links are supplementary.')
    ]
    raw=TMP/'generated-guide-pages.pdf'
    c=canvas.Canvas(str(raw),pagesize=(W,H),pageCompression=1)
    c.setTitle('Blue Impulse Study Guide — How Machines Sense, Connect, and Act')
    for p in schedule:
        if p['kind']=='fixed':c.showPage()
        else:render_content(c,p)
    c.save()
    generated=fitz.open(raw);fixed=fitz.open(ART/'cover-and-dividers.pdf');final=fitz.open()
    for i,p in enumerate(schedule):
        if p['kind']=='fixed':final.insert_pdf(fixed,from_page=p['fixed'],to_page=p['fixed'])
        else:final.insert_pdf(generated,from_page=i,to_page=i)
    final.set_metadata(dict(title='Blue Impulse Study Guide: How Machines Sense, Connect, and Act',author='Blue Impulse',subject='Hardware, networking and behaviourist AI',keywords='study guide, hardware, networks, reinforcement learning, Blue Impulse',creator='Blue Impulse / Neogpt; ReportLab and PyMuPDF'))
    toc=[]
    for p in schedule:
        level=1 if p['kind']=='fixed' or p['key'] in ['contents','learning-goals-1','learning-goals-2','sources'] else 2
        toc.append([level,p['title'],p['page']])
    final.set_toc(toc)
    final.set_page_labels([dict(startpage=0,prefix='',style='D',firstpagenum=1)])
    # Link each contents chapter row to its actual divider page.
    toc_page=final[1]
    for ch in range(1,7):
        matches=toc_page.search_for(f'{ch:02d} · {TITLES[ch]}')
        for rect in matches:
            toc_page.insert_link({'kind':fitz.LINK_GOTO,'from':rect,'page':starts[ch]-1})
    output=DEST/'BlueImpulse_Study_Guide.pdf'
    final.subset_fonts()
    final.save(output,garbage=4,deflate=True)
    (DEST/'source/page-map.json').write_text(json.dumps(schedule,ensure_ascii=False,indent=2))
    (DEST/'source/layout-audit.json').write_text(json.dumps(LAYOUT,ensure_ascii=False,indent=2))
    (DEST/'source/exercise-map.json').write_text(json.dumps({k:{'text':v,'source':source_path(k),'pages':[p['page'] for p in schedule if p.get('exercise')==k or any(b.get('text')==v for b in p.get('blocks',[]))]} for k,v in EXERCISES.items()},ensure_ascii=False,indent=2))
    manifest=dict(file=output.name,pages=len(schedule),chapters={str(ch):{'start':starts[ch],'end':ends[ch]} for ch in starts},topic_pages={p['key']:p['page'] for p in schedule},sha256=hashlib.sha256(output.read_bytes()).hexdigest())
    (DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    proof=fitz.open(output)
    thumbs=[]
    preview_dir=TMP/'guide-previews';preview_dir.mkdir(exist_ok=True)
    for i,page in enumerate(proof):
        pix=page.get_pixmap(matrix=fitz.Matrix(.30,.30),alpha=False)
        im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        tile=Image.new('RGB',(200,284),'#dadde5');tile.paste(im,((200-im.width)//2,7))
        ImageDraw.Draw(tile).text((10,267),str(i+1),fill='#212C4A');thumbs.append(tile)
    for group in range(0,len(thumbs),24):
        take=thumbs[group:group+24]
        sheet=Image.new('RGB',(1200,284*math.ceil(len(take)/6)),'#dadde5')
        for k,im in enumerate(take):sheet.paste(im,((k%6)*200,(k//6)*284))
        sheet.save(preview_dir/f'overview-{group//24+1}.jpg',quality=90)
    overview=Image.new('RGB',(1200,284*math.ceil(len(thumbs)/6)),'#dadde5')
    for k,im in enumerate(thumbs):overview.paste(im,((k%6)*200,(k//6)*284))
    overview.save(DEST/'BlueImpulse_Study_Guide_Overview.jpg',quality=93)
    for key in ['cover','bits-bytes','fetch-execute','rl-loop','q-learning','hardware-roles','pipeline','tcp-ip','network-challenges','networked-ai','real-time','hardware-limits','sources']:
        page=proof[manifest['topic_pages'][key]-1]
        page.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(preview_dir/f'{key}.png')
    print(json.dumps({'pdf':str(output),'pages':len(schedule),'chapter_pages':manifest['chapters'],'minimum_prose_font':min(e['font_size'] for e in LAYOUT if e['role']=='content'),'proofs':str(preview_dir)},indent=2))

if __name__=='__main__':main()
