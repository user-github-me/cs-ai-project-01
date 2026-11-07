"""Verify the concrete deck, then create self-contained teaching documentation."""
from pathlib import Path
from zipfile import ZipFile
import json, re, importlib.util, hashlib, math, shutil, xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
import fitz
from PIL import Image, ImageDraw
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];REV=B/'review';SUP=B/'supporting'
S=json.loads((B/'source/slides.json').read_text());LAY=json.loads((REV/'layout-audit.json').read_text())
topic_path=ROOT/'content/topic-map.json'
if not topic_path.exists():topic_path=B/'source/module-topic-map.json'
TOPICS=json.loads(topic_path.read_text())
if topic_path.resolve()!=(B/'source/module-topic-map.json').resolve():shutil.copy2(topic_path,B/'source/module-topic-map.json')
lookup={(d['chapter'],d['title']):d for d in TOPICS['topics']}
CH=TOPICS['chapters'];PPT=B/'BlueImpulse_Stage2_PPT_V1.pptx';PDF=B/'BlueImpulse_Stage2_PPT_V1.pdf'
def norm(s):return re.sub(r'\s+','',str(s)).casefold()
def lum(h):
    a=[int(h[i:i+2],16)/255 for i in (0,2,4)];a=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in a];return sum(x*y for x,y in zip(a,[.2126,.7152,.0722]))
def ratio(a,b):x,y=sorted([lum(a),lum(b)]);return (y+.05)/(x+.05)
assert len(S)==63
assert all((d['chapter'],d['subtopic']) in lookup for d in S[:-1])
with ZipFile(PPT) as z:
    assert z.testzip() is None
    slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
    notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)]
    assert len(slides)==len(notes)==63
    ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
    note_words=[]
    for n in notes:
        t=' '.join(ET.fromstring(z.read(n)).itertext());assert 'TEACHING GUIDANCE' in t and 'Subtopic:' in t;assert len(t)>650;note_words.append(len(t.split()))
    embedded=[n for n in z.namelist() if n.endswith('.fntdata')];assert len(embedded)==2
    slide_runs=sum(len(ET.fromstring(z.read(n)).findall('.//a:t',ns)) for n in slides)
    pictures=sum(len(ET.fromstring(z.read(n)).findall('.//p:pic',ns)) for n in slides);assert pictures==0
doc=fitz.open(PDF);assert len(doc)==63
miss=[];bounds=[];fonts=set();sizes=[]
for i,p in enumerate(doc):
    rendered=norm(p.get_text())
    for item in LAY[i]['shapes']:
        if item['kind']=='text' and norm(item['text']) not in rendered:miss.append((i+1,item['text']))
    for block in p.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for sp in line['spans']:
                if not sp['text'].strip():continue
                fonts.add(sp['font']);sizes.append(sp['size']);r=fitz.Rect(sp['bbox'])
                if not p.rect.contains(r):bounds.append((i+1,sp['text']))
assert not miss,miss
assert not bounds,bounds
assert all('Inter' in n for n in fonts),fonts
assert min(sizes)>=27.9,min(sizes)
spec=importlib.util.spec_from_file_location('demo',SUP/'BlueImpulse_Demonstrations.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
assert M.q_update()['new']==3.3 and M.q_update()['target']==4.6 and M.q_update(terminal=True)['new']==1.5
assert [r['completes_at_cycle'] for r in M.pipeline()['rows']]==[4,5,6]
assert [x['distance_metres'] for x in M.delay_distances()]==[15,1.5,.15,6]
assert [r['result'] for r in M.packet_examples()['messages']]==['ACCEPT','STALE','DUPLICATE / OLD SEQUENCE']
assert M.execute_program()['result']==7 and M.execute_program(9)['result']==12
assert int('11111101',2)==253 and int('11111101',2)-256==-3
assert 100*100*24//8==30000
test_packet=dict(device='robot-7',units='m',policy_version=3,authenticated=True,sequence=42,timestamp_ms=800)
assert M.accept_message(test_packet,41)[0]=='ACCEPT'
test_packet['timestamp_ms']=799;assert M.accept_message(test_packet,41)[0]=='STALE'
for a in [0,1]:
    for b in [0,1]:assert (a&b)==int(bool(a) and bool(b))
stats=dict(slides=63,chapters=6,native_notes=63,notes_words=sum(note_words),audience_tasks=sum(bool(d['activity']) for d in S),
    approximate_teaching_minutes=sum(d['minutes'] for d in S),editable_text_runs=slide_runs,raster_slide_pictures=pictures,embedded_font_weights=2,
    native_pdf_pages=63,min_native_font_pt=round(min(sizes),2),font_families=sorted(fonts),missing_rendered_text=miss,outside_page_text=bounds,
    contrast_white_on_navy=round(ratio('FFF6FA','111936'),2),contrast_pink_on_navy=round(ratio('FF4385','111936'),2),
    example_checks='passed: signed byte, raw image size, Q update and terminal state, pipeline, delay, packet order and freshness boundary, program and modified ADD, AND truth table',
    keynote_import_pdf_export='passed on 7 November 2026',keynote_slideshow='automated start/stop at slide 29 passed; not human rehearsal',
    human_teammate_review='pending',human_rehearsal='pending',classroom_projector_check='pending',
    pptx_sha256=hashlib.sha256(PPT.read_bytes()).hexdigest(),pdf_sha256=hashlib.sha256(PDF.read_bytes()).hexdigest())
assert stats['contrast_pink_on_navy']>=4.5
(REV/'verification.json').write_text(json.dumps(stats,indent=2)+'\n')
for start in range(0,len(doc),9):
    out=Image.new('RGB',(1920,1080),(255,255,255))
    for i in range(start,min(start+9,len(doc))):
        p=doc[i];pix=p.get_pixmap(matrix=fitz.Matrix(640/p.rect.width,640/p.rect.width));im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples).resize((640,360));out.paste(im,((i-start)%3*640,(i-start)//3*360))
    out.save(REV/f'contact-{start//9+1:02d}.jpg',quality=90)
for i in [7,16,28,40,49,59]:doc[i].get_pixmap(matrix=fitz.Matrix(2,2)).save(REV/f'slide-{i+1:02d}.png')

# Exact source-to-teaching map. It deliberately names chapters/subtopics, not book pages.
rows=['# Learning resource map — Blue Impulse\n','The 63-slide classroom deck shares the following exact chapter/subtopic titles with the checked Markdown and study guide. The actual explanation and activity are included in the deck and notes. These references are for continuation and practice.\n','| Slides | Chapter and subtopic | Chapter practice ID |','| --- | --- | --- |']
for d in S[:-1]:
    t=lookup[(d['chapter'],d['subtopic'])];rows.append(f"| {d['number']} | Chapter {d['chapter']} — {CH[str(d['chapter'])]}: **{d['subtopic']}** | {t['exercise']} |")
rows+=['\n## Focused video tutorials\n','| Video | Exact filename | Matching slide sequence |','| --- | --- | --- |',
'| 01 | `BlueImpulse_Video01_Basic_Reinforcement_Learning.mp4` | 17–24 |',
'| 02 | `BlueImpulse_Video02_How_Hardware_Enables_AI.mp4` | 26–32 |',
'| 03 | `BlueImpulse_Video03_Network_Challenges.mp4` | 37–41, 48 |',
'| 04 | `BlueImpulse_Video04_Networking_for_Behaviorist_AI.mp4` | 49–52 |',
'| 05 | `BlueImpulse_Video05_Program_Execution.mp4` | 8–11 |',
'\nVideos are a separate Stage 2 submission and are not needed to teach this self-contained deck. The offline commands and all expected results are included in `Demonstration_Guide.md` and `expected-results.json`.\n',
'## Independent practice\n','Use the chapter exercises and checked solutions after attempting the classroom tasks. Chapter mission activities ACT-01 through ACT-06 and the Stage 2 test bank provide additional practice. The test bank uses TF01–TF24, MC01–MC24 and OE01–OE06, with four true/false items, four multiple-choice items and one open-ended item per chapter. The test bank is submitted with the study guide.\n']
(SUP/'Learning_Resource_Map.md').write_text('\n'.join(rows))
md=['# Blue Impulse — Stage 2 classroom teaching content V1.0\n','Module: Hardware, Networking and Behaviorist AI. This checked medium-specific Markdown is the content source for the editable slides and native presenter notes. All figures are original diagrams and all activities have a debrief below or on a later slide.\n']
for d in S:
    md.extend([f"\n## Slide {d['number']}: {d['title']}\n",f"Chapter {d['chapter']} — {CH[str(d['chapter'])]}; subtopic: **{d['subtopic']}**. Planned time: {d['minutes']} minute(s).\n",'Audience-facing content:\n'])
    for t in d['items']:md.append('- '+(' / '.join(map(str,t)) if isinstance(t,list) else str(t)).replace('\n',' · '))
    md.extend(['\nTeaching notes:\n',d['notes']])
    if d['activity']:md.extend(['\nActivity: '+d['activity']])
    if d['answer']:md.extend(['\nExpected answer / debrief: '+d['answer']])
    md.extend(['\nReference: '+d['source']+'. Full attribution is in `supporting/Sources.md`.'])
(B/'Teaching_Content.md').write_text('\n'.join(md)+'\n')
ai=f'''# Significant AI-use evidence — teaching slides

Date: 7 November 2026. Tool: NeoGPT/Codex in the local repository. The user requested the work for Blue Impulse; this record does not invent an individual student role or reflection.

## Important request

User excerpt: “rules/Stage2_All_Instructions.md follow this. and make whole repo follow this. make it it ready. log everything in my personal log.”

The applicable slide instructions require a complete module teaching story, large-room readability, visual explanations, meaningful audience activity, presenter notes, a self-contained editable PowerPoint package and authentic evidence. The separate Sojourner presentation did not by itself cover the full six-chapter module.

## Output and decisions

- Generated a new 63-slide module deck in a separate directory and preserved the earlier Sojourner artifacts.
- Used Pip, a fictional campus delivery rover, as an opening problem and final integrated design challenge; kept `robot-7` for the shared packet example.
- Selected a three-session structure and 15 short audience tasks. Moved detailed explanations, assumptions, expected answers and sources into substantive native notes.
- Used editable text, shapes, tables and arrows with one Inter typeface; vivid pink, deep navy and near-white form the three-color palette.
- Kept every technical demonstration local and reproducible. The deck does not need an online platform, a robot or a video service.

## Verification and revisions actually performed

- Font metrics rejected text that was too wide or tall; the affected diagram labels and boxes were revised before export.
- The first native export revealed a fallback typeface for Unicode arrow glyphs. Audience text was changed to the word “to”; explanatory arrows remain editable shapes. The current native PDF uses Inter only.
- Added the initial sequence and freshness threshold to the packet challenge slide so the audience can solve it without relying on hidden information.
- Added both read and write directions between CPU and memory in the architecture diagram.
- Checked the signed-byte and raw-image arithmetic, Q-learning and terminal alternative, pipeline schedule, network delay, packet sequence/freshness boundary, toy program and AND table independently with Python assertions.
- Opened and exported the actual PPTX through Keynote; an automated slideshow start/stop on slide 29 succeeded. Compared every authored audience text item with extracted text in the native PDF, checked all text bounds and font sizes, and inspected rendered slide contact sheets.

Current evidence: {stats['slides']} slides, {stats['native_notes']} native notes, {stats['audience_tasks']} audience tasks, minimum visible native text {stats['min_native_font_pt']} pt, no missing rendered text, no text outside the page. Exact data and file hashes are in `review/verification.json`.

## Human work still needed

A teammate review, rehearsal, actual classroom projector check, and individual student explanation/reflection are not evidenced in this session. They remain pending. Automated generation, inspection or application launch must not be recorded as those human activities. No teacher feedback, participant response, rehearsal timing, student contribution or learning outcome has been fabricated.
'''
(SUP/'AI_Use_Evidence.md').write_text(ai)

pdfmetrics.registerFont(TTFont('Inter',str(B/'fonts/Inter-Regular.ttf')));pdfmetrics.registerFont(TTFont('Inter-Bold',str(B/'fonts/Inter-Bold.ttf')))
NAVY=HexColor('#111936');PINK=HexColor('#FF4385')
styles={
 'title':ParagraphStyle('title',fontName='Inter-Bold',fontSize=20,leading=25,textColor=NAVY,spaceAfter=12),
 'h2':ParagraphStyle('h2',fontName='Inter-Bold',fontSize=12,leading=16,textColor=NAVY,spaceBefore=9,spaceAfter=5),
 'body':ParagraphStyle('body',fontName='Inter',fontSize=10.2,leading=14,textColor=NAVY,spaceAfter=6),
 'small':ParagraphStyle('small',fontName='Inter',fontSize=8.8,leading=12,textColor=NAVY,spaceAfter=5)}
def para(t,style='body'):return Paragraph(escape(str(t).replace('→','to')).replace('\n','<br/>'),styles[style])
def foot(c,d):
 c.setStrokeColor(PINK);c.line(42,34,A4[0]-42,34);c.setFont('Inter',8);c.setFillColor(NAVY);c.drawString(42,22,'BLUE IMPULSE · STAGE 2 PPT V1.0');c.drawRightString(A4[0]-42,22,str(d.page))
notes_story=[];thumbs=REV/'notes-thumbnails';thumbs.mkdir(exist_ok=True)
for i,d in enumerate(S):
    if i:notes_story.append(PageBreak())
    notes_story.extend([para(f"{d['number']:02d} · {d['title']}",'title'),para(f"Chapter {d['chapter']} — {CH[str(d['chapter'])]} / {d['subtopic']}",'small')])
    p=doc[i];pix=p.get_pixmap(matrix=fitz.Matrix(1.1,1.1));f=thumbs/f'{i+1:02d}.jpg';pix.pil_save(str(f),quality=90);notes_story.append(RLImage(str(f),width=500,height=281.25))
    notes_story.extend([Spacer(1,8),para(f"Planned time: {d['minutes']} minute(s). Human rehearsal remains pending.",'small'),para(d['notes'])])
    if d['activity']:notes_story.extend([para('Audience task','h2'),para(d['activity'])])
    if d['answer']:notes_story.extend([para('Expected answer / debrief','h2'),para(d['answer'])])
    notes_story.append(para('Source: '+d['source']+'. Full citations: supporting/Sources.md. Continuation: supporting/Learning_Resource_Map.md.','small'))
SimpleDocTemplate(str(B/'BlueImpulse_Stage2_PPT_V1_Presenter_Notes.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=45,title='Blue Impulse Stage 2 PPT V1.0 Presenter Notes',author='Blue Impulse').build(notes_story,onFirstPage=foot,onLaterPages=foot)

report=[para('Stage 2 PPT V1.0 — Readiness report','title'),para('Blue Impulse · Hardware, Networking and Behaviorist AI · 7 November 2026'),
para('Concrete deliverable','h2'),para('63 editable PowerPoint slides cover all six chapters in three sessions. Native presenter notes, 15 timed audience tasks, checked answers, a native slide PDF, a complete notes PDF, offline Python demonstrations, reference maps, fonts and source files are included.'),
para('Rubric-aligned evidence','h2')]
for title,body in [
('Essential coverage and teaching story','Slides 1–25 establish representation, execution and behavior; 26–45 connect hardware and communication; 46–63 integrate applications and constraints. Pip’s delayed response opens the lesson; the final architecture challenge resolves it.'),
('Accuracy and explanatory quality','Worked examples and visual models explain state changes, reinforcement learning, pipelining, delays and message handling. Notes disclose assumptions and common misconceptions. Checked arithmetic and outputs are preserved in the supporting files.'),
('Visual design and readability',f"The native PDF uses only Inter, with minimum visible text {stats['min_native_font_pt']} pt. White/navy contrast is {stats['contrast_white_on_navy']}:1 and pink/navy is {stats['contrast_pink_on_navy']}:1. Every authored text element was found in the native export; all extracted text lies within the page. Actual projector readability still needs a human check."),
('Audience engagement','15 brief tasks ask learners to calculate, predict, compare, justify or diagnose. Prompts include realistic thinking time and notes include debriefs. Main numerical challenges have later answer slides; discussions explicitly allow justified alternatives.'),
('Notes and teaching readiness','All 63 slides have native notes, approximate timing, exact subtopic references and source guidance. Optional demonstrations need only Python 3.9 and include complete expected output; the slide tables are the offline fallback.'),
('Learning-system coherence','The deck uses the same six chapters, Pip example and checked numerical cases as the Markdown, guide and focused videos. The local resource map gives specific subtopics, exercise IDs and all five tutorial filenames.')]:report.extend([para(title,'h2'),para(body)])
report.extend([PageBreak(),para('Verification evidence and limitations','title'),para('Checks actually completed','h2'),para(f"PPTX archive opened successfully; {len(slides)} slide parts and {len(notes)} native note parts are present. Both Inter weights are embedded. All explanatory audience objects are editable text/shapes; the slides do not contain rasterized pages. The actual deck opened and exported through Keynote, and an automated slideshow start/stop succeeded at slide 29."),para('All 63 native slide renders were inspected via contact sheets, with representative diagram/table slides inspected at full size. Font-metric checks were followed by native text-presence, font and bounds checks. This is software-assisted review, not evidence of a classroom presentation.'),para(stats['example_checks']),para('Evidence files','h2'),para('review/verification.json; review/layout-audit.json; review/contact-01.jpg through contact-07.jpg; review/slide-08.png, 17, 29, 41, 50 and 60; supporting/expected-results.json; supporting/AI_Use_Evidence.md; review/source-link-check.json.'),para('Significant AI use','h2'),para('NeoGPT/Codex generated substantial content, diagrams, notes and builder code under the user’s instruction to apply the Stage 2 rules. The AI-use evidence file contains the relevant request, concrete outputs, decisions, corrections and verification. No individual student mastery, unobserved contribution, teacher feedback or audience response is inferred.'),para('Human checks still pending','h2'),para('Another team member must review the slides and rehearse a representative section using these notes. Check actual classroom projection from the back, refine planned activity timing and confirm that the presenter can explain the models and assumptions. These checklist items are intentionally not marked complete.'),para('Submission format and accessibility','h2'),para('Submit BlueImpulse_Stage2_PPT_V1.zip because it contains multiple required files. It includes the editable PPTX, actual notes, supplementary PDFs and all needed supporting files. The PDF does not replace the PowerPoint. External sources and related video links are optional continuation material, not missing required explanations.')])
SimpleDocTemplate(str(B/'BlueImpulse_Stage2_PPT_V1_Readiness_Report.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=45,title='Blue Impulse Stage 2 PPT V1.0 Readiness Report',author='Blue Impulse').build(report,onFirstPage=foot,onLaterPages=foot)
notes_pdf=fitz.open(B/'BlueImpulse_Stage2_PPT_V1_Presenter_Notes.pdf');assert len(notes_pdf)==63,len(notes_pdf)
for i,d in enumerate(S):assert norm(d['title']) in norm(notes_pdf[i].get_text())
stats['presenter_notes_pdf_pages']=len(notes_pdf);stats['readiness_report_pdf_pages']=len(fitz.open(B/'BlueImpulse_Stage2_PPT_V1_Readiness_Report.pdf'))
(REV/'verification.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats,indent=2))
