"""Render final MP4s sequentially, verify their streams, and decode every frame."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=5)
    args = parser.parse_args()
    (ROOT / 'renders').mkdir(exist_ok=True)
    reports = []
    env = dict(os.environ, HF_STATIC_DEDUP='false', PRODUCER_LOW_MEMORY_MODE='false',
               PRODUCER_FORCE_SCREENSHOT='true')
    try:
        for n in range(args.start, args.end + 1):
            lesson = json.loads((ROOT / f'lesson-{n:02}.json').read_text())
            target = ROOT / 'renders' / f'BlueImpulse_Video{n:02}_{lesson["slug"]}.mp4'
            shutil.copyfile(ROOT / f'entries/video-{n:02}.html.in', ROOT / 'index.html')
            started = time.monotonic()
            print(f'RENDERING VIDEO {n:02}: {lesson["duration"]:.2f}s', flush=True)
            with (ROOT / f'build/render-{n:02}.log').open('w') as log:
                subprocess.run(['hyperframes', 'render', '--fps', '30', '--workers', '4',
                    '--gpu', '--no-browser-gpu', '--quality', 'delivery', '--output', str(target)],
                    cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
            probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
                    '-show_streams', '-show_format', '-of', 'json', str(target)], text=True))
            video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            audio = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
            duration = float(probe['format']['duration'])
            assert video['codec_name'] == 'h264'
            assert audio['codec_name'] == 'aac'
            assert (video['width'], video['height'], video['r_frame_rate']) == (1920, 1080, '30/1')
            assert 300 <= duration <= 600
            assert abs(duration - lesson['duration']) < .15
            with (ROOT / f'build/decode-{n:02}.log').open('w') as log:
                subprocess.run(['ffmpeg', '-v', 'error', '-i', str(target), '-f', 'null', '-'],
                               stdout=log, stderr=log, check=True)
            assert not (ROOT / f'build/decode-{n:02}.log').read_text().strip(), 'Decode reported errors.'
            report = {'video': n, 'file': target.name, 'duration_seconds': duration,
                      'width': video['width'], 'height': video['height'], 'fps': video['r_frame_rate'],
                      'frame_count': int(video['nb_frames']), 'video_codec': video['codec_name'],
                      'audio_codec': audio['codec_name'], 'audio_sample_rate': audio['sample_rate'],
                      'bytes': target.stat().st_size, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
                      'decode_errors': 0, 'render_and_decode_seconds': round(time.monotonic() - started, 2)}
            reports.append(report)
            (ROOT / f'build/render-result-{n:02}.json').write_text(json.dumps(report, indent=2) + '\n')
            (ROOT / 'build/render-summary.json').write_text(json.dumps(reports, indent=2) + '\n')
            print(f'FINISHED VIDEO {n:02}: {duration:.2f}s, {target.stat().st_size / 1024**2:.1f} MiB, every frame decoded', flush=True)
    finally:
        shutil.copyfile(ROOT / 'entries/video-01.html.in', ROOT / 'index.html')

if __name__ == '__main__':
    main()
