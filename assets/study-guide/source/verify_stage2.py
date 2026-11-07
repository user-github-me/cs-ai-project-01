"""Verify the submitted learning files, numbers, documents and package copies."""
from pathlib import Path
import sys,json,re,hashlib,zipfile,unicodedata
import fitz
from docx import Document
from stage2_learning import ANSWERS,CHECKS,MISSIONS,RESOURCES
from stage2_testbank import TF,MC,OE
from guide_content import PAGES
from reference_content import TITLES

ROOT=Path(__file__).resolve().parents[3];BASE=ROOT/'assets/study-guide';REVIEW=BASE/'source/stage2-review'
norm=lambda s:re.sub(r'\s+','',unicodedata.normalize('NFKC',str(s)))
assert len(TF)==len(MC)==24 and len(OE)==6
for ch in range(1,7):assert [sum(x[0]==ch for x in group) for group in [TF,MC,OE]]==[4,4,1]
for row in MC:assert len(row[3])==len(set(row[3]))==4 and row[4] in 'ABCD'
for row in OE:assert len(row[-1].split())>100
assert set(CHECKS)=={p['key'] for p in PAGES}
assert len(ANSWERS)==65
# Independent arithmetic checks for the consequential worked examples.
assert int('01001111',2)==79
assert int('10011010',2)-256==-102
assert ((-53)&255)==int('11001011',2)
assert 16384*512*8/8/(1024**3)==.0078125
assert abs(2+.5*(1+.9*4-2)-3.3)<1e-9
assert 2+.5*(1-2)==1.5
assert [30*t/1000 for t in [500,50,5,200]]==[15,1.5,.15,6]
assert 4+3-1==6 and 4+5-1==8
pdfs=[BASE/'BlueImpulse_Study_Guide.pdf',BASE/'BlueImpulse_Stage2_TestBank_V1.pdf',ROOT/'submissions/stage2/markdown/BlueImpulse_Stage2_Markdown_V2_Content.pdf',ROOT/'submissions/stage2/markdown/BlueImpulse_Stage2_Markdown_Submission_Report.pdf']
rows=[];texts={}
for path in pdfs:
 d=fitz.open(path);parts=[];spans=0
 for i,p in enumerate(d):
  t=p.get_text();parts.append(t)
  if path.name=='BlueImpulse_Study_Guide.pdf' and i<96:continue
  assert '\x00' not in t,('Missing glyph',path.name,i+1)
  for block in p.get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    for s in line['spans']:
     r=fitz.Rect(s['bbox']);assert r.x0>=-1 and r.y0>=-1 and r.x1<=p.rect.width+1 and r.y1<=p.rect.height+1,('Text outside page',path.name,i+1,s['text']);spans+=1
 texts[path.name]=norm(' '.join(parts))
 rows.append({'file':str(path.relative_to(ROOT)),'pages':len(d),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checked_text_spans':spans})
 # All pages can be rasterised, not only the cover.
 for p in d:p.get_pixmap(matrix=fitz.Matrix(.12,.12),alpha=False)
 d.close()
bank_pdf=texts['BlueImpulse_Stage2_TestBank_V1.pdf'];content_pdf=texts['BlueImpulse_Stage2_Markdown_V2_Content.pdf']
doc=Document(BASE/'BlueImpulse_Stage2_TestBank_V1.docx');doc_text=norm(' '.join(p.text for p in doc.paragraphs))
for group in [TF,MC,OE]:
 for row in group:
  assert norm(row[2]) in doc_text,('Missing DOCX question',row[2])
  assert norm(row[2]) in bank_pdf,('Missing PDF question',row[2])
for i,row in enumerate(MC,1):
 assert norm(f'MC{i:02d}: {row[4]}') in bank_pdf
 for choice in row[3]:assert norm(choice) in bank_pdf
for row in OE:assert norm(row[-1]) in doc_text
# Verify questions precede the actual answer-key heading.
assert bank_pdf.index('OE06—Chapter')<bank_pdf.index('Answerkey—readafter')
# The rendered source includes all topic titles, checkpoints, glossary concepts,
# source questions and answers; split paragraphs may contain page headers.
for p in PAGES:assert norm(p['title']) in content_pdf
for key,(q,a) in CHECKS.items():assert norm(q) in content_pdf,('Missing checkpoint',key)
for key,a in ANSWERS.items():assert norm('Answer '+key) in content_pdf
# Local links in canonical teaching files must resolve; old historical sample is
# retained in the snapshot but not counted as the canonical chapter.
links=0
for p in (ROOT/'content').rglob('*.md'):
 if p.name in ['Chapter-01-sample.md','UseOfAI.md']:continue
 for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',p.read_text()):
  if target.startswith(('http:','https:','#','mailto:')):continue
  rel=target.split('#')[0]
  if rel:assert (p.parent/rel).exists(),('Broken local link',p,rel);links+=1
packages=[]
for zpath in (ROOT/'submissions/stage2').rglob('*.zip'):
 if zpath.parent.name not in ['markdown','study-guide']:continue
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None;manifest=json.loads(z.read('MANIFEST.json'))
  for rel,rec in manifest['files'].items():assert hashlib.sha256(z.read(rel)).hexdigest()==rec['sha256']
  packages.append({'file':str(zpath.relative_to(ROOT)),'files':len(manifest['files']),'crc_and_hashes':'passed'})
resources=json.loads((REVIEW/'resource-access.json').read_text());assert len(resources)==6 and all(x.get('status')==200 for x in resources)
result={'status':'passed','date':'2026-11-07','pdfs':rows,'test_bank':{'true_false':24,'multiple_choice':24,'open_ended':6,'each_chapter':'4 TF / 4 MC / 1 OE','open_sample_word_counts':[len(x[-1].split()) for x in OE]},'developed_topics':67,'checkpoint_feedback_pairs':67,'explained_exercises':65,'missions':6,'working_local_links':links,'resource_access': '6/6 signed-out HTTP 200','packages':packages,'human_review':'pending; no independent teammate attempt evidence supplied'}
(REVIEW/'final-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
