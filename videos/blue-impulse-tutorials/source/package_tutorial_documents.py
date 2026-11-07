"""Collect the five tutorials and their teaching documents into a compact ZIP."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parents[1]
PDFS = REPO / 'assets/tutorials'


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=REPO / 'deliverables/BlueImpulse_Tutorial_Documents.zip')
    args = parser.parse_args()
    lessons = json.loads((PDFS / 'manifest.json').read_text())
    assert [lesson['number'] for lesson in lessons] == list(range(1, 6))
    files = {}
    rows = []
    for lesson in lessons:
        base = lesson['file'].removesuffix('_Tutorial.pdf')
        folder = base.removeprefix('BlueImpulse_')
        topic = base.split('_', 2)[2].replace('_', ' ')
        sources = [
            PDFS / lesson['file'],
            PDFS / 'scripts' / (base + '_Script_and_Teaching_Outline.pdf'),
            PROJECT / 'scripts' / (base + '_Narration.md'),
            PROJECT / 'scripts' / (base + '_Teaching_Outline.md'),
        ]
        for path in sources:
            assert path.is_file(), f'Missing teaching document: {path}'
            files[folder + '/' + path.name] = path
        rows.append(f'| {lesson["number"]:02} | {topic} | [{folder}/]({folder}/) |')
    combined = PDFS / 'BlueImpulse_All_Video_Tutorials.pdf'
    assert combined.is_file()
    files[combined.name] = combined
    readme = '\n'.join([
        '# Blue Impulse tutorial PDFs, scripts, and teaching outlines', '',
        'Each video folder contains its 13-page tutorial PDF, a printable PDF '
        'of the complete script and teaching outline, and editable Markdown '
        'copies of the narration and outline.', '',
        '| Video | Topic | Folder |', '|---|---|---|', *rows, '',
        'The combined tutorial PDF contains all five written tutorials in 65 pages. '
        'Section timestamps and guide-page references match the tutorial videos. '
        'The script PDFs include the complete narration and teaching steps.', '',
        'Study guide, videos, and supporting examples: '
        'https://github.com/user-github-me/cs-ai-project-01/tree/main/assets/tutorials', '',
        'MANIFEST.json and SHA256SUMS.txt record the size and checksum of every document.', '',
    ])
    manifest = [dict(path=name, bytes=path.stat().st_size, sha256=digest(path))
                for name, path in sorted(files.items())]
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    prefix = 'BlueImpulse_Tutorial_Documents/'
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, path in sorted(files.items()):
            archive.write(path, prefix + name)
        archive.writestr(prefix + 'README.md', readme)
        archive.writestr(prefix + 'MANIFEST.json', json.dumps(manifest, indent=2) + '\n')
        archive.writestr(prefix + 'SHA256SUMS.txt', ''.join(
            f'{item["sha256"]}  {item["path"]}\n' for item in manifest))
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(set(archive.namelist())) == 24
        for item in manifest:
            assert hashlib.sha256(archive.read(prefix + item['path'])).hexdigest() == item['sha256']
    checksum = digest(output)
    output.with_suffix('.sha256').write_text(checksum + '  ' + output.name + '\n')
    print(json.dumps(dict(file=str(output), bytes=output.stat().st_size,
                          sha256=checksum, tutorial_pdfs=6, script_outline_pdfs=5,
                          editable_scripts_and_outlines=10, crc_errors=0,
                          sha256_mismatches=0), indent=2))


if __name__ == '__main__':
    main()
