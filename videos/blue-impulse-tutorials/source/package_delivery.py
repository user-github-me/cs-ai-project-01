"""Package verified videos, PDFs, scripts, captions, examples, and editable source."""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import json
import shutil
import zipfile
import fitz

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
GUIDE_HASH = '2af7695b50de6d32cdc3254b1a702b1ec09701c90677bc758d956f9476b7d3e4'

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for data in iter(lambda: handle.read(1024*1024), b''):
            h.update(data)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=REPO/'deliverables/BlueImpulse_Tutorial_Package.zip')
    args = parser.parse_args()
    review = ROOT/'review'
    audit_names=['all-checks-summary.json','quotation-check.json','pdf-review-summary.json','audio-levels.json']
    for name in audit_names:
        if (ROOT/'build'/name).exists():
            shutil.copy2(ROOT/'build'/name,review/name)
    media = [json.loads((review/f'video-{n:02}-media.json').read_text()) for n in range(1,6)]
    captions = [json.loads((review/f'video-{n:02}-captions.json').read_text()) for n in range(1,6)]
    assert all(c['all_passed'] and c['srt_matches_complete_narration'] for c in captions)
    assert sum(c['caption_frames_checked'] for c in captions) == 456
    checks = json.loads((review/'all-checks-summary.json').read_text())
    assert len(checks) == 5 and all(c['ok'] for c in checks)
    guide = REPO/'assets/study-guide/BlueImpulse_Study_Guide.pdf'
    assert sha(guide) == GUIDE_HASH and len(fitz.open(guide)) == 96
    pdfdir = REPO/'assets/tutorials'
    pdfs = sorted(pdfdir.glob('*_Tutorial.pdf'))
    assert len(pdfs) == 5 and all(len(fitz.open(p)) == 13 for p in pdfs)
    assert len(fitz.open(pdfdir/'BlueImpulse_All_Video_Tutorials.pdf')) == 65
    files = {}
    def add(path, archive):
        assert path.is_file(), str(path)
        assert archive not in files, archive
        files[archive] = path
    add(ROOT/'DELIVERY_README.md', 'README.md')
    add(guide, 'Study_Guide/'+guide.name)
    for p in pdfs + [pdfdir/'BlueImpulse_All_Video_Tutorials.pdf']:
        add(p, 'Tutorial_PDFs/'+p.name)
    add(pdfdir/'manifest.json', 'Tutorial_PDFs/manifest.json')
    for folder, label in [('scripts','Scripts'),('subtitles','Subtitles'),('supporting','Supporting_Files')]:
        for p in sorted((ROOT/folder).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                add(p, label+'/'+p.relative_to(ROOT/folder).as_posix())
    repository_videos = pdfdir/'videos'
    repository_videos.mkdir(exist_ok=True)
    for item in media:
        path = ROOT/'renders'/item['file']
        if not path.exists():
            path = repository_videos/item['file']
        assert sha(path) == item['sha256']
        assert 300 <= item['duration_seconds'] <= 600
        assert item['width'] == 1920 and item['height'] == 1080 and item['fps'] == '30/1'
        assert item['audio_unchanged'] and item['decode_errors'] == 0
        assert path.stat().st_size < 100_000_000, 'Keep oversized media out of normal Git objects.'
        destination = repository_videos/path.name
        if path != destination:
            shutil.copy2(path, destination)
        add(path, 'Videos/'+path.name)
    # Only portable authoring inputs; no credentials, history, caches, models,
    # temporary reference downloads, raw WAVs, or duplicate rendered MP4s.
    include_dirs = ['assets','compositions','entries','source','reference','capture/extracted']
    for folder in include_dirs:
        for p in sorted((ROOT/folder).rglob('*')):
            if not p.is_file() or '__pycache__' in p.parts or p.suffix in ['.pyc','.wav']:
                continue
            if (ROOT/'assets/voice/cues') in p.parents:
                continue
            add(p, 'Editable_Project/'+p.relative_to(ROOT).as_posix())
    names = ['README.md','BRIEF.md','SPEC.md','STORYBOARD.md','SCRIPT.md','frame.md',
             'THIRD_PARTY_NOTICES.md','DELIVERY_README.md','hyperframes.json','package.json','.gitignore']
    for name in names:
        add(ROOT/name,'Editable_Project/'+name)
    # The default film in the archive is always lesson 1.
    add(ROOT/'entries/video-01.html.in','Editable_Project/index.html')
    for p in sorted(ROOT.glob('lesson-??.json')):
        add(p,'Editable_Project/'+p.name)
    for p in sorted(review.glob('*')):
        if p.is_file() and p.suffix in ['.json','.jpg','.md'] and p.name!='package-verification.json':
            add(p,'Verification/'+p.name)
    manifest = dict(created_utc=datetime.now(timezone.utc).isoformat(),
                    guide_pages=96, guide_sha256=GUIDE_HASH, videos=media,
                    tutorial_pdfs=5, pages_per_tutorial=13, combined_tutorial_pages=65,
                    subtitle_frames_verified=sum(c['caption_frames_checked'] for c in captions),
                    silent_frames_verified=sum(c['silent_frames_checked'] for c in captions),
                    files=[dict(path=name,bytes=p.stat().st_size,sha256=sha(p)) for name,p in sorted(files.items())])
    package = args.output.resolve()
    package.parent.mkdir(parents=True,exist_ok=True)
    prefix = 'BlueImpulse_Tutorial_Package/'
    with zipfile.ZipFile(package,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as archive:
        for name,p in sorted(files.items()):
            compression = zipfile.ZIP_STORED if p.suffix.lower() in ['.mp4','.m4a','.pdf','.png','.jpg','.woff2'] else zipfile.ZIP_DEFLATED
            archive.write(p,prefix+name,compress_type=compression)
        archive.writestr(prefix+'manifest.json',json.dumps(manifest,indent=2)+'\n')
        archive.writestr(prefix+'SHA256SUMS.txt',''.join(f'{r["sha256"]}  {r["path"]}\n' for r in manifest['files']))
    with zipfile.ZipFile(package) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(set(archive.namelist()))
        assert sum('/Videos/' in p and p.endswith('.mp4') for p in archive.namelist()) == 5
        for record in manifest['files']:
            h=hashlib.sha256()
            with archive.open(prefix+record['path']) as stream:
                for data in iter(lambda:stream.read(1024*1024),b''):
                    h.update(data)
            assert h.hexdigest()==record['sha256'],record['path']
    output_report = dict(zip=package.name,bytes=package.stat().st_size,sha256=sha(package),
                         files=len(files)+2,crc_errors=0,sha256_mismatches=0,videos=5,tutorial_pdfs=6)
    (package.parent/'BlueImpulse_Tutorial_Package.sha256').write_text(output_report['sha256']+'  '+package.name+'\n')
    (review/'package-verification.json').write_text(json.dumps(output_report,indent=2)+'\n')
    (pdfdir/'video-manifest.json').write_text(json.dumps(media,indent=2)+'\n')
    print(json.dumps(output_report,indent=2))

if __name__ == '__main__':
    main()
