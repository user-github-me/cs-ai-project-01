"""Make compact H.264 copies without changing duration, resolution, or audio."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda: f.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--start', type=int, default=1)
    p.add_argument('--end', type=int, default=5)
    args = p.parse_args()
    encoded = ROOT / 'build/encoded'
    originals = ROOT / 'build/render-originals'
    review = ROOT / 'review'
    for folder in [encoded, originals, review]:
        folder.mkdir(parents=True, exist_ok=True)
    for n in range(args.start, args.end + 1):
        done = ROOT / f'build/render-result-{n:02}.json'
        deadline = time.monotonic() + 7200
        while not done.exists():
            if time.monotonic() > deadline:
                raise TimeoutError(f'Video {n:02} did not finish rendering.')
            if 'Traceback' in (ROOT / 'build/final-render-run.log').read_text():
                raise RuntimeError('The render job failed; inspect its log.')
            time.sleep(2)
        source_report = json.loads(done.read_text())
        source = ROOT / 'renders' / source_report['file']
        report_path = review / f'video-{n:02}-media.json'
        if report_path.exists() and json.loads(report_path.read_text())['sha256'] == digest(source):
            print(f'VIDEO {n:02}: verified compact file already exists', flush=True)
            continue
        target = encoded / source.name
        print(f'OPTIMIZING VIDEO {n:02}', flush=True)
        with (ROOT / f'build/encode-{n:02}.log').open('w') as log:
            subprocess.run(['ffmpeg', '-hide_banner', '-i', str(source), '-map', '0:v:0',
                '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                '-threads', '2', '-g', '60', '-keyint_min', '30', '-pix_fmt', 'yuv420p',
                '-c:a', 'copy', '-movflags', '+faststart', '-y', str(target)],
                stdout=log, stderr=log, check=True)
        comparison = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(source), '-i', str(target),
            '-filter_complex', '[0:v]fps=1[a];[1:v]fps=1[b];[a][b]ssim', '-an', '-f', 'null', '-'],
            capture_output=True, text=True, check=True)
        (ROOT / f'build/ssim-{n:02}.log').write_text(comparison.stderr)
        score = float(re.findall(r'All:([0-9.]+)', comparison.stderr)[-1])
        assert score >= .99, f'Check visual quality: sampled SSIM {score}'
        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams',
                      '-show_format', '-of', 'json', str(target)], text=True))
        video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        audio = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
        assert (video['width'], video['height'], video['r_frame_rate']) == (1920, 1080, '30/1')
        assert int(video['nb_frames']) == source_report['frame_count']
        assert abs(float(probe['format']['duration']) - source_report['duration_seconds']) < .15
        hashes = []
        for file in [source, target]:
            hashes.append(subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(file),
                '-map', '0:a:0', '-f', 'hash', '-hash', 'sha256', '-'], text=True).strip())
        assert hashes[0] == hashes[1], 'Audio changed during optimization.'
        decode = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(target), '-f', 'null', '-'],
                                capture_output=True, text=True, check=True)
        assert not decode.stderr.strip(), 'Decode reported errors.'
        report = dict(source_report, duration_seconds=float(probe['format']['duration']),
                      bytes=target.stat().st_size, sha256=digest(target),
                      original_render_bytes=source.stat().st_size,
                      sampled_ssim_against_render=score, ssim_sample_rate_fps=1,
                      audio_unchanged=True, audio_pcm_hash=hashes[0],
                      compression='libx264 veryfast CRF 18; 2-second maximum GOP; AAC copied',
                      decode_errors=0)
        source.rename(originals / source.name)
        target.rename(source)
        report_path.write_text(json.dumps(report, indent=2) + '\n')
        print(f'COMPACT VIDEO {n:02}: {report["bytes"]/1024**2:.1f} MiB; SSIM {score:.6f}; audio unchanged', flush=True)

if __name__ == '__main__':
    main()
