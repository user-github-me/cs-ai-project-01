"""Small deterministic Markdown-to-PDF renderer used by Stage 2 snapshots."""
from pathlib import Path
from html import escape
import re
from markdown_it import MarkdownIt
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Preformatted,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from fontTools.ttLib import TTCollection

FONT_TMP=Path('/private/tmp/blue-impulse-stage2-fonts');FONT_TMP.mkdir(exist_ok=True)
fonts=TTCollection('/System/Library/Fonts/Avenir.ttc')
for name,index in [('StageBody',0),('StageBold',4),('StageItalic',1)]:
 path=FONT_TMP/(name+'.ttf');fonts.fonts[index].save(path);pdfmetrics.registerFont(TTFont(name,str(path)))
pdfmetrics.registerFontFamily('StageBody',normal='StageBody',bold='StageBold',italic='StageItalic')
pdfmetrics.registerFont(TTFont('StageSymbols','/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
INK='#162144';ACC='#BD2D70';LIGHT='#F3F5FA'
styles={
 'body':ParagraphStyle('body',fontName='StageBody',fontSize=10.3,leading=14.8,spaceAfter=7,textColor=HexColor(INK),splitLongWords=True),
 'h1':ParagraphStyle('h1',fontName='StageBold',fontSize=24,leading=29,spaceAfter=16,textColor=HexColor(INK),keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='StageBold',fontSize=16,leading=21,spaceBefore=14,spaceAfter=9,textColor=HexColor(ACC),keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='StageBold',fontSize=12,leading=16,spaceBefore=10,spaceAfter=6,textColor=HexColor(INK),keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='StageBody',fontSize=9,leading=12,spaceAfter=0,textColor=HexColor(INK),splitLongWords=True),
 'small':ParagraphStyle('small',fontName='StageBody',fontSize=8.5,leading=11,spaceAfter=5,textColor=HexColor(INK)),
 'code':ParagraphStyle('code',fontName='Courier',fontSize=8,leading=11,spaceAfter=9,textColor=HexColor(INK)),
}
md=MarkdownIt('commonmark').enable('table')

def inline(s):
 out=md.renderInline(s)
 out=re.sub(r'<a href="([^"]*)">',lambda m:'<link href="'+escape(m[1],quote=True)+'">',out).replace('</a>','</link>')
 out=out.replace('<strong>','<b>').replace('</strong>','</b>').replace('<em>','<i>').replace('</em>','</i>')
 out=out.replace('<code>','<font name="Courier">').replace('</code>','</font>')
 out=out.replace('→','<font name="StageSymbols">→</font>')
 return out.replace('<br />','<br/>').replace('\n',' ')

class Document(SimpleDocTemplate):
 def afterFlowable(self,flowable):
  if isinstance(flowable,Paragraph) and getattr(flowable,'stage_heading',None):
   level,title=flowable.stage_heading
   key='s'+str(self.seq.nextf('section'))
   self.canv.bookmarkPage(key)
   # All source sections are siblings to avoid invalid skipped PDF-outline levels.
   self.canv.addOutlineEntry(title,key,level=0,closed=False)

def render_markdown(text,path,title,subtitle='',page_offset=0):
 tokens=md.parse(text);story=[];i=0;first=True;in_list=0;list_count=[]
 while i<len(tokens):
  t=tokens[i]
  if t.type=='heading_open':
   level=int(t.tag[1:]);val=tokens[i+1].content
   if level==1 and not first:story.append(PageBreak())
   p=Paragraph(inline(val),styles.get('h'+str(min(level,3))))
   p.stage_heading=(level,val);story.append(p);first=False;i+=3;continue
  if t.type in ('bullet_list_open','ordered_list_open'):in_list+=1;list_count.append(0 if t.type=='bullet_list_open' else int(t.attrGet('start') or 1));i+=1;continue
  if t.type in ('bullet_list_close','ordered_list_close'):in_list-=1;list_count.pop();i+=1;continue
  if t.type=='paragraph_open':
   val=tokens[i+1].content;prefix=''
   if in_list:
    prefix='• ' if list_count[-1]==0 else str(list_count[-1])+'. '
    if list_count[-1]>0:list_count[-1]+=1
   story.append(Paragraph(escape(prefix)+inline(val),styles['body']));i+=3;continue
  if t.type in ('fence','code_block'):
   # Wrap code for a readable print copy; the exact code remains in source files.
   lines=[]
   for l in t.content.splitlines():
    while len(l)>89:lines.append(l[:89]);l='  '+l[89:]
    lines.append(l)
   story.append(Preformatted('\n'.join(lines),styles['code']));i+=1;continue
  if t.type=='table_open':
   rows=[];row=[];i+=1
   while tokens[i].type!='table_close':
    tt=tokens[i]
    if tt.type=='tr_open':row=[]
    if tt.type=='inline':row.append(Paragraph(inline(tt.content),styles['cell']))
    if tt.type=='tr_close':rows.append(row)
    i+=1
   if rows:
    n=len(rows[0]);width=499
    colw=[width/n]*n
    if n==2:colw=[width*.30,width*.70]
    table=Table(rows,colWidths=colw,repeatRows=1,hAlign='LEFT')
    table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),HexColor('#E8EAF4')),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#FFFFFF'),HexColor(LIGHT)]),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),.6,HexColor(ACC))]))
    story.extend([table,Spacer(1,10)])
   i+=1;continue
  if t.type=='hr':story.append(Spacer(1,9))
  i+=1
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 def page(c,doc):
  c.setFillColor(HexColor(INK));c.rect(0,810,595.28,31,fill=1,stroke=0)
  c.setFillColor(HexColor('#FFFFFF'));c.setFont('StageBold',8.5);c.drawString(48,822,'BLUE IMPULSE  /  STAGE 2')
  c.setFillColor(HexColor(INK));c.setFont('StageBody',8)
  c.drawString(48,27,subtitle[:85] or title[:85]);c.drawRightString(547,27,str(doc.page+page_offset))
 doc=Document(str(path),pagesize=(595.28,841.89),rightMargin=48,leftMargin=48,topMargin=54,bottomMargin=49,title=title,author='Blue Impulse',pageCompression=1)
 doc.build(story,onFirstPage=page,onLaterPages=page)
 return path
