"""Sequential runtime checks and representative frame captures for all five lessons."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=5)
    args = parser.parse_args()
    reports = []
    env = dict(os.environ, PRODUCER_BROWSER_GPU_MODE='hardware')
    try:
        for n in range(args.start, args.end + 1):
            lesson = json.loads((ROOT / f'lesson-{n:02}.json').read_text())
            shutil.copyfile(ROOT / f'entries/video-{n:02}.html.in', ROOT / 'index.html')
            times = [round(s['start'] + s['duration'] * .70, 3) for s in lesson['scenes']]
            for scene in lesson['scenes']:
                if scene['kind'].endswith('-demo'):
                    times.extend(round(scene['start'] + b['start'] + 1, 3)
                                 for b in scene['beats'][1::2])
                if 'question_pause' in scene:
                    p = scene['question_pause']
                    times.append(round(scene['start'] + p['start'] + p['duration'] - .3, 3))
            times.append(round(lesson['duration'] - .3, 3))
            at = ','.join(str(t) for t in sorted(set(times)))
            with (ROOT / f'build/check-{n:02}.json').open('w') as out, (ROOT / f'build/check-{n:02}.log').open('w') as err:
                result = subprocess.run(['hyperframes', 'check', '--json', '--samples', '12',
                    '--at', at, '--at-transitions', '--max-transition-samples', '36',
                    '--max-issues', '100', '--browser-gpu'], cwd=ROOT, env=env, stdout=out, stderr=err)
            report = json.loads((ROOT / f'build/check-{n:02}.json').read_text())
            print(f'Video {n:02}: check exit {result.returncode}; ok={report.get("ok")}', flush=True)
            with (ROOT / f'build/snapshot-{n:02}.json').open('w') as out, (ROOT / f'build/snapshot-{n:02}.log').open('w') as err:
                snap = subprocess.run(['hyperframes', 'snapshot', '--json', '--at', at,
                    '--output', f'build/review-{n:02}', '--browser-gpu'], cwd=ROOT, env=env, stdout=out, stderr=err)
            reports.append({'video': n, 'check_exit': result.returncode,
                            'check_ok': report.get('ok'), 'snapshot_exit': snap.returncode,
                            'timestamps': sorted(set(times))})
            (ROOT / 'build/preflight-summary.json').write_text(json.dumps(reports, indent=2) + '\n')
            if result.returncode or snap.returncode:
                raise RuntimeError(f'Review video {n:02} before continuing.')
    finally:
        shutil.copyfile(ROOT / 'entries/video-01.html.in', ROOT / 'index.html')
        all_reports=[]
        for n in range(1,6):
            path=ROOT/f'build/check-{n:02}.json'
            if not path.exists() or not path.stat().st_size:
                continue
            report=json.loads(path.read_text())
            row=dict(video=n,ok=report['ok'])
            for key in ['lint','runtime','layout','contrast','craft','motion','audio']:
                row[key]={field:report[key][field] for field in
                          ['errorCount','warningCount','checked','passed','enabled']
                          if field in report[key]}
            all_reports.append(row)
        (ROOT/'build/all-checks-summary.json').write_text(json.dumps(all_reports,indent=2)+'\n')

if __name__ == '__main__':
    run()
