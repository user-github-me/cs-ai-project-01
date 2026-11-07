"""Create the exact named, self-contained Stage 2 PPT submission and read it back."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json,hashlib,subprocess,tempfile,shutil
import fitz
B=Path(__file__).resolve().parents[1];ROOT=next((p for p in B.parents if (p/'rules/Stage2_All_Instructions.md').exists()),B.parent)
DEST=ROOT/'submissions/stage2/slides';DEST.mkdir(parents=True,exist_ok=True)
NAME='BlueImpulse_Stage2_PPT_V1';ZIP=DEST/(NAME+'.zip')
files=[]
for p in sorted(B.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(B)
    if '__pycache__' in rel.parts or 'notes-thumbnails' in rel.parts or p.name.startswith('.') or p.suffix=='.pyc':continue
    files.append((str(rel),p))
manifest=dict(team='Blue Impulse',assignment='Stage 2 PPT',version='V1.0',date='2026-11-07',files=[dict(path=n,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for n,p in files],human_review='Teammate rehearsal and projector review pending; no completion is inferred.')
with ZipFile(ZIP,'w',ZIP_DEFLATED,compresslevel=6) as z:
    for n,p in files:z.write(p,NAME+'/'+n)
    z.writestr(NAME+'/manifest.json',json.dumps(manifest,indent=2)+'\n')
    z.writestr(NAME+'/SHA256SUMS.txt',''.join(f"{m['sha256']}  {m['path']}\n" for m in manifest['files']))
with ZipFile(ZIP) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))
    for m in manifest['files']:assert hashlib.sha256(z.read(NAME+'/'+m['path'])).hexdigest()==m['sha256']
    with tempfile.TemporaryDirectory(prefix='blue-impulse-slide-submission-') as tmp:
        z.extractall(tmp);copy=Path(tmp)/NAME
        for file,pages in [(NAME+'.pdf',63),(NAME+'_Presenter_Notes.pdf',63),(NAME+'_Readiness_Report.pdf',2)]:assert len(fitz.open(copy/file))==pages
        with ZipFile(copy/(NAME+'.pptx')) as ppt:assert ppt.testzip() is None
        out=subprocess.check_output(['python3',str(copy/'supporting/BlueImpulse_Demonstrations.py'),'--topic','all'],text=True)
        assert json.loads(out)==json.loads((copy/'supporting/expected-results.json').read_text())
summary=dict(package=str(ZIP.relative_to(ROOT)),bytes=ZIP.stat().st_size,sha256=hashlib.sha256(ZIP.read_bytes()).hexdigest(),files=len(files),crc='passed',all_member_sha256='passed',reopened_PDFs='63 slides / 63 notes / 2 report pages',reopened_PPTX='passed',copied_demo_execution='passed',human_rehearsal='pending')
(DEST/'package-verification.json').write_text(json.dumps(summary,indent=2)+'\n')
(DEST/(NAME+'.sha256')).write_text(summary['sha256']+'  '+ZIP.name+'\n')
(DEST/'README.md').write_text('''# Blue Impulse — Stage 2 PPT V1.0 submission

Submit **BlueImpulse_Stage2_PPT_V1.zip** as the complete multiple-file teaching-slide package. It contains the editable 63-slide PPTX with native notes, slide PDF, 63-page presenter-notes PDF, readiness report, offline demonstrations and outputs, Markdown teaching source, reference map, significant AI-use evidence, fonts and reproducible builders.

`package-verification.json` records CRC/hash readback and execution of the supporting script from an extracted copy. `BlueImpulse_Stage2_PPT_V1.sha256` identifies this exact ZIP.

Human teammate review, representative rehearsal and actual classroom projector testing remain pending and are clearly labelled in the report and checklist. This package does not fabricate those records.
''')
print(json.dumps(summary,indent=2))
