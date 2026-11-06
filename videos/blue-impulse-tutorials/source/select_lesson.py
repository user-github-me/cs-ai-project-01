"""Select the root film before previewing, checking, or rendering it."""
from pathlib import Path
import argparse
import json

p=argparse.ArgumentParser();p.add_argument('number',type=int,choices=range(1,6));a=p.parse_args()
root=Path(__file__).resolve().parents[1]
source=root/'entries'/f'video-{a.number:02}.html.in'
assert source.exists(),f'Build lesson {a.number} first.'
(root/'index.html').write_text(source.read_text())
lesson=json.loads((root/f'lesson-{a.number:02}.json').read_text())
print(f'Selected video {a.number:02}: {lesson["title"]} ({lesson["duration"]:.2f} seconds)')
