"""Inspect actual MP4 caption bands and create scene overview images."""
from pathlib import Path
import argparse
import json
import re
import subprocess
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]

def balanced_sum(parts):
    # FFmpeg's expression parser has a recursion limit; keep long selections shallow.
    if len(parts) <= 8:
        return '+'.join(parts)
    middle=len(parts)//2
    return '('+balanced_sum(parts[:middle])+')+('+balanced_sum(parts[middle:])+')'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=5)
    args = parser.parse_args()
    review = ROOT / 'review'
    review.mkdir(exist_ok=True)
    for n in range(args.start, args.end + 1):
        report_path = review / f'video-{n:02}-media.json'
        deadline = time.monotonic() + 7200
        while not report_path.exists():
            if time.monotonic() > deadline:
                raise TimeoutError(f'Compact video {n:02} did not finish.')
            if 'Traceback' in (ROOT / 'build/optimize-run.log').read_text():
                raise RuntimeError('Inspect the failed optimization job.')
            time.sleep(2)
        lesson = json.loads((ROOT / f'lesson-{n:02}.json').read_text())
        report = json.loads(report_path.read_text())
        video = ROOT / 'renders' / report['file']
        folder = ROOT / f'build/final-review-{n:02}'
        folder.mkdir(exist_ok=True)
        cases = [dict(frame=int((c['start']+c['end'])/2*30), expected='caption', cue=c['id'])
                 for c in lesson['captions']]
        for scene in lesson['scenes']:
            if 'question_pause' in scene:
                p = scene['question_pause']
                t = scene['start'] + p['start'] + p['duration']/2
                cases.append(dict(frame=int(t*30), expected='clear', cue=scene['key']))
        cases.append(dict(frame=int((lesson['duration']-.4)*30), expected='clear', cue='final-cover'))
        cases.sort(key=lambda item: item['frame'])
        assert len({c['frame'] for c in cases}) == len(cases)
        selection = balanced_sum([f'eq(n\\,{c["frame"]})' for c in cases])
        subprocess.run(['ffmpeg', '-v', 'error', '-threads', '2', '-i', str(video),
            '-vf', f'select={selection},crop=1528:104:196:868', '-fps_mode', 'vfr',
            '-threads', '1', '-an', '-y', str(folder / 'caption-%03d.png')], check=True)
        frames = sorted(folder.glob('caption-*.png'))
        assert len(frames) == len(cases)
        for case, frame in zip(cases, frames):
            pixels = np.asarray(Image.open(frame).convert('RGB'))
            count = int(np.all(pixels > 160, axis=2).sum())
            case['light_text_pixels'] = count
            case['passed'] = count > 180 if case['expected']=='caption' else count < 40
        assert all(c['passed'] for c in cases), [c for c in cases if not c['passed']]
        normalise = lambda s: re.sub('[^a-z0-9]', '', s.lower())
        assert normalise(' '.join(c['text'] for c in lesson['captions'])) == normalise(
            ' '.join(c for scene in lesson['scenes'] for c in scene['cues']))
        stem = f'BlueImpulse_Video{n:02}_{lesson["slug"]}'
        srt = (ROOT / 'subtitles' / f'{stem}.srt').read_text()
        chunks = re.split(r'\n\s*\n', srt.strip())
        assert len(chunks) == len(lesson['captions'])
        assert all(len(c.splitlines()[2:]) <= 2 for c in chunks)
        srt_words = ' '.join(' '.join(c.splitlines()[2:]) for c in chunks)
        assert normalise(srt_words) == normalise(' '.join(c['text'] for c in lesson['captions']))
        caption_report = dict(video=n, caption_frames_checked=len(lesson['captions']),
                              silent_frames_checked=len(cases)-len(lesson['captions']),
                              all_passed=True, srt_matches_complete_narration=True,
                              srt_max_lines=2, cases=cases)
        (review / f'video-{n:02}-captions.json').write_text(json.dumps(caption_report, indent=2)+'\n')
        sheet = Image.new('RGB', (1920, 1552), '#121829')
        draw = ImageDraw.Draw(sheet)
        font_path = ROOT / 'build/pdf-fonts/Inter.ttf'
        font = ImageFont.truetype(str(font_path), 19) if font_path.exists() else ImageFont.load_default()
        for i, scene in enumerate(lesson['scenes']):
            t = scene['start'] + scene['duration']*.70
            image_path = folder / f'scene-{i:02}.jpg'
            subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(video),
                '-frames:v', '1', '-q:v', '2', '-update', '1', '-y', str(image_path)], check=True)
            image = Image.open(image_path).convert('RGB').resize((640,360),Image.Resampling.LANCZOS)
            x=(i%3)*640;y=(i//3)*388
            sheet.paste(image,(x,y+28))
            draw.text((x+9,y+4),f'{int(t)//60:02}:{int(t)%60:02}  {scene["title"]}',font=font,fill='white')
        sheet.save(review / f'BlueImpulse_Video{n:02}_Overview.jpg', quality=92)
        print(f'VIDEO {n:02}: {len(lesson["captions"])} caption frames and {len(cases)-len(lesson["captions"])} silent frames verified; overview saved', flush=True)

if __name__ == '__main__':
    main()
