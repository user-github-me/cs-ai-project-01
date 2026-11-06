"""Write timed scripts, teaching outlines, and a portable package index."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def clock(t):
    n = int(t)
    return f'{n // 60:02}:{n % 60:02}'

def main():
    scripts = ROOT / 'scripts'
    scripts.mkdir(exist_ok=True)
    lessons = [json.loads(p.read_text()) for p in sorted(ROOT.glob('lesson-??.json'))]
    overview = ['# Blue Impulse video tutorials', '',
        'Five lessons taught directly from the 96-page Blue Impulse study guide. Each MP4 includes English narration, burned-in subtitles, book screenshots, page citations, demonstrations, thinking pauses, and the original book-cover credit.', '',
        '| Video | Topic | Duration | Guide pages |', '|---|---|---|---|']
    combined = ['# Timed narration scripts', '',
        'The section times below come from the delivered audio. Each paragraph is the actual spoken narration. Question pauses are explicit. The SRT/VTT files use measured audio-cue boundaries.', '']
    for lesson in lessons:
        n = lesson['number']
        stem = f'BlueImpulse_Video{n:02}_{lesson["slug"]}'
        overview.append(f'| {n:02} | {lesson["title"]} | {clock(lesson["duration"])} | '+', '.join(map(str,lesson['pages']))+' |')
        lines = [f'# Video {n:02}: {lesson["title"]}', '',
                 f'Duration: {clock(lesson["duration"])}. Video: `{stem}.mp4`.', '',
                 '## Learning objectives', '']
        lines.extend(f'- {s}' for s in lesson['objectives'])
        for i, scene in enumerate(lesson['scenes'], 1):
            lines += ['', f'## {clock(scene["start"])}–{clock(scene["start"]+scene["duration"])} · {scene["title"]}', '',
                      f'Study guide page {scene["page"]}. Visual: {scene["kind"]}.', '']
            for j, cue in enumerate(scene['cues']):
                lines += [cue, '']
                if 'question_pause' in scene and j == scene.get('pause_after'):
                    pause = scene['question_pause']
                    lines += [f'**[Pause for {pause["duration"]} seconds. Keep the answer hidden.]**', '']
            if scene['kind'] == 'question':
                lines += [f'On-screen question: {scene["prompt"]}', '', f'Answer after the pause: {scene["answer"]}', '']
        text = '\n'.join(lines).rstrip()+'\n'
        (scripts / f'{stem}_Narration.md').write_text(text)
        combined += lines + ['', '---', '']
        outline = [f'# Teaching outline: {lesson["title"]}', '',
            'Open the guide at the pages below. Let learners answer before continuing through a thinking pause. Use the matching Python demonstration to change an input and explain the resulting change.', '',
            '| Time | Teaching step | Guide page | What to show or ask |',
            '|---|---|---|---|']
        for scene in lesson['scenes']:
            action = scene.get('prompt') or scene.get('quote') or '; '.join(scene.get('labels', [])) or scene['title']
            outline.append(f'| {clock(scene["start"])} | {scene["title"]} | {scene["page"]} | {action.replace("|", "/")} |')
        outline += ['', 'The written tutorial PDF contains the full explanation and exact book excerpts. Numerical examples are teaching models, with assumptions stated in the guide, narration, and supporting file.', '']
        (scripts / f'{stem}_Teaching_Outline.md').write_text('\n'.join(outline))
    (ROOT / 'SCRIPT.md').write_text('\n'.join(combined))
    overview += ['', '## Inside the ZIP', '',
        '- `Videos/`: the five 1920 × 1080, 30 fps H.264/AAC MP4 tutorials.',
        '- `Tutorial_PDFs/`: one written tutorial per video, plus the combined 65-page edition.',
        '- `Study_Guide/`: the finished 96-page study guide used on screen.',
        '- `Scripts/`: complete timed narration and teaching outlines.',
        '- `Subtitles/`: editable SRT and WebVTT captions; the MP4s also have visible subtitles.',
        '- `Supporting_Files/`: runnable Python demonstrations, expected results, and instructions.',
        '- `Editable_Project/`: the HyperFrames scenes, illustrations, book excerpts, fonts, audio, and build scripts.',
        '- `Verification/`: file hashes, technical checks, and representative frames.', '',
        'Start with a video and keep the study guide open. The PDF viewer page number is the cited book page. Use the written tutorial to review a step or find its timestamp. Run `python3 Supporting_Files/BlueImpulse_Demonstrations.py --topic all` to reproduce all five demonstrations without installing extra packages.', '',
        'Narration uses the local Kokoro English voice `am_michael`; it is synthesized speech. The quiet musical bed and entry tones were generated for these lessons. The original study-guide cover, chapter colors, and excerpts retain their source appearance. Third-party social-video references are credited as inspiration and are not included.', '',
        'Guide SHA-256: `2af7695b50de6d32cdc3254b1a702b1ec09701c90677bc758d956f9476b7d3e4`.', '']
    (ROOT / 'DELIVERY_README.md').write_text('\n'.join(overview))
    print(f'Wrote {len(lessons)} timed scripts and teaching outlines.')

if __name__ == '__main__':
    main()
