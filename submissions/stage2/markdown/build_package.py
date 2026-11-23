"""Build the Stage 2 Markdown V2.0 submission package.

  python build_package.py pdf      -> BlueImpulse_Stage2_Markdown_V2_Content.pdf (complete rendered content)
  python build_package.py zip      -> BlueImpulse_Stage2_Markdown_V2.zip (source snapshot + content PDF + report)
  python build_package.py check    -> extract the ZIP into a temporary folder and check files, images and links

The source snapshot is the repository's README, task list, content/ folder and the chapter outlines it cites. Relative
links that point outside the snapshot are rewritten to GitHub URLs at the snapshot commit so the extracted copy has no
broken links.
"""
from __future__ import annotations
import hashlib, json, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
from markdown_it import MarkdownIt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REPO_URL = "https://github.com/user-github-me/cs-ai-project-01"
PDF = HERE / "BlueImpulse_Stage2_Markdown_V2_Content.pdf"
ZIP = HERE / "BlueImpulse_Stage2_Markdown_V2.zip"
REPORT = [HERE / "BlueImpulse_Stage2_Markdown_Submission_Report.docx", HERE / "BlueImpulse_Stage2_Markdown_Submission_Report.pdf"]
CHROME = Path.home() / "Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
CHAPTERS = {1: "The Fundamentals", 2: "Behaviorism & Behaviorist AI", 3: "Hardware", 4: "Networking",
            5: "Applications", 6: "Strengths & Limitations"}
md = MarkdownIt("commonmark", {"html": True}).enable(["table", "strikethrough"])


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout.strip()


CSS = """
@page { size: A4; margin: 18mm 17mm 20mm 17mm; }
body { font-family: "Avenir", "Avenir Next", "Helvetica Neue", sans-serif; font-size: 10.4pt; line-height: 1.5; color: #1b2340; }
h1 { font-family: "DIN Condensed", "Avenir Next Condensed", sans-serif; font-size: 30pt; color: #1e3f7a; margin: 0 0 8pt; }
h2 { font-size: 15pt; color: #1e5baf; margin: 18pt 0 6pt; border-bottom: 1.5pt solid #c9d8ef; padding-bottom: 3pt; break-after: avoid; }
h3 { font-size: 12.5pt; color: #24426b; margin: 14pt 0 4pt; break-after: avoid; }
h4 { font-size: 10.8pt; color: #356db7; margin: 10pt 0 3pt; break-after: avoid; }
p { margin: 0 0 6pt; } ul, ol { margin: 0 0 6pt 18pt; padding: 0; } li { margin: 1.5pt 0; }
table { border-collapse: collapse; width: 100%; margin: 4pt 0 8pt; font-size: 9.4pt; break-inside: auto; }
th, td { border: 0.8pt solid #b9c6de; padding: 3pt 5pt; vertical-align: top; text-align: left; }
th { background: #e8eef9; }
tr { break-inside: avoid; }
blockquote { margin: 8pt 0; padding: 6pt 10pt; background: #fff6d8; border-left: 3.5pt solid #e0b52f; break-inside: avoid; }
blockquote p { margin: 0 0 3pt; }
img { max-width: 100%; max-height: 105mm; display: block; margin: 4pt auto 2pt; break-inside: avoid; }
p > em:only-child { display: block; text-align: center; font-size: 9pt; color: #4b5a7a; }
code { font-family: Menlo, monospace; font-size: 8.8pt; background: #eef1f7; padding: 0 2pt; border-radius: 2pt; }
pre { background: #eef1f7; padding: 6pt; font-size: 8.6pt; white-space: pre-wrap; }
a { color: #1e5baf; text-decoration: none; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: center; }
.cover .t { font-family: "DIN Condensed", sans-serif; font-size: 44pt; color: #1e3f7a; line-height: 1; }
.cover .s { font-size: 14pt; margin-top: 10pt; color: #356db7; }
.cover table { width: auto; margin-top: 24pt; font-size: 10.5pt; }
.part { font-size: 9pt; letter-spacing: .12em; text-transform: uppercase; color: #6b7a99; margin-bottom: 2pt; break-before: page; break-after: avoid; }
"""


def render_md(text: str, base: Path) -> str:
    html = md.render(text)

    def fix(m):
        src = m.group(2)
        if re.match(r"^[a-z]+:", src):
            return m.group(0)
        return f'{m.group(1)}{(base / src).resolve().as_uri()}"'
    html = re.sub(r'(<img[^>]*?src=")([^"]+)"', fix, html)
    # in-document links to other files become plain text (the PDF is one document)
    html = re.sub(r'<a href="(?!https?:)[^"]*">(.*?)</a>', r"\1", html)
    # demote the file's own H1 so the chapter title is the only H1
    return html


def build_pdf(snapshot_label: str):
    from playwright.sync_api import sync_playwright
    content = ROOT / "content"
    parts = []
    commit = git("rev-parse", "--short", "HEAD")
    parts.append(f"""<div class="cover"><div class="t">Hardware, Networks &amp; Behaviorist AI</div>
<div class="s">Stage 2 · Markdown content V2.0 — complete rendered copy</div>
<table><tr><th>Team</th><td>Blue Impulse</td></tr><tr><th>Module</th><td>Hardware, Networks and Behaviorist AI</td></tr>
<tr><th>Repository</th><td>{REPO_URL}</td></tr><tr><th>Snapshot</th><td>{snapshot_label}</td></tr>
<tr><th>Contents</th><td>Module overview · six chapters (explanations, worked examples, diagrams, activities, practice) · checked answers · references</td></tr></table></div>""")
    readme = (content / "README.md").read_text()
    parts.append('<div class="part">Module overview</div>' + render_md(readme, content).replace("<h1>", '<h1 class="first">', 1))
    for ch, name in CHAPTERS.items():
        d = content / f"chapter-{ch:02d}"
        parts.append(f'<div class="part">Chapter {ch}</div>' + render_md((d / "draft.md").read_text(), d))
        sol = d / "solutions.md"
        if sol.exists():
            parts.append(f'<div class="part">Chapter {ch} · answers</div>' + render_md(sol.read_text(), d))
    parts.append('<div class="part">References</div>' + render_md((content / "references.md").read_text(), content))
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(parts)}</body></html>'
    tmp = HERE / "_content.html"
    tmp.write_text(html)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=str(CHROME))
        pg = b.new_page()
        pg.goto(tmp.as_uri(), wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=str(PDF), format="A4", print_background=True, outline=True, tagged=True,
               display_header_footer=True, header_template="<span></span>",
               footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#6b7a99;font-family:Avenir">'
                               'Blue Impulse · Markdown V2.0 · page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
               margin={"top": "18mm", "bottom": "20mm", "left": "17mm", "right": "17mm"})
        b.close()
    tmp.unlink()
    import pymupdf as fitz
    d = fitz.open(PDF)
    print(f"content PDF: {d.page_count} pages, {PDF.stat().st_size/1e6:.1f} MB, commit {commit}")


SNAPSHOT_ITEMS = ["README.md", "task.md", "content", "drafts/stage 2/Bone Structures"]


def rewrite_links(text: str, rel_dir: str, commit: str, included) -> str:
    def fix(m):
        label, target = m.group(1), m.group(2)
        if re.match(r"^([a-z]+:|#)", target):
            return m.group(0)
        path, _, frag = target.partition("#")
        norm = (Path(rel_dir) / path).as_posix()
        parts = []
        for p in norm.split("/"):
            if p == "..":
                if parts:
                    parts.pop()
            elif p not in ("", "."):
                parts.append(p)
        norm = "/".join(parts)
        if any(norm == i or norm.startswith(i + "/") for i in included):
            return m.group(0)
        url = f"{REPO_URL}/blob/{commit}/{norm}".replace(" ", "%20") + (f"#{frag}" if frag else "")
        return f"[{label}]({url})"
    return re.sub(r"\[([^\]]*)\]\(([^)\s]+)\)", fix, text)


def build_zip():
    commit = git("rev-parse", "HEAD")
    top = "BlueImpulse_Stage2_Markdown_V2"
    manifest = {"repository": REPO_URL, "snapshot_commit": commit, "files": {}}
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for item in SNAPSHOT_ITEMS:
            src = ROOT / item
            files = [src] if src.is_file() else sorted(p for p in src.rglob("*") if p.is_file() and p.name != ".DS_Store")
            for f in files:
                rel = f.relative_to(ROOT).as_posix()
                data = f.read_bytes()
                if f.suffix == ".md":
                    data = rewrite_links(data.decode(), str(Path(rel).parent), commit, SNAPSHOT_ITEMS).encode()
                z.writestr(f"{top}/source-snapshot/{rel}", data)
                manifest["files"][f"source-snapshot/{rel}"] = hashlib.sha256(data).hexdigest()
        for f in [PDF] + [r for r in REPORT if r.exists()]:
            z.write(f, f"{top}/{f.name}")
            manifest["files"][f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
        z.writestr(f"{top}/MANIFEST.json", json.dumps(manifest, indent=1))
    print(f"ZIP: {ZIP.name} {ZIP.stat().st_size/1e6:.1f} MB, {len(manifest['files'])} files, snapshot {commit[:7]}")


def check():
    out = Path(tempfile.mkdtemp(prefix="bi_zip_check_"))
    with zipfile.ZipFile(ZIP) as z:
        bad = z.testzip()
        z.extractall(out)
    problems = []
    root = out / "BlueImpulse_Stage2_Markdown_V2"
    for f in root.rglob("*.md"):
        text = f.read_text()
        for m in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)\)", text):
            t = m.group(1)
            if re.match(r"^([a-z]+:|#)", t):
                continue
            p = (f.parent / t.split("#")[0]).resolve()
            if not p.exists():
                problems.append(f"{f.relative_to(root)} -> {t}")
    import pymupdf as fitz
    for pdf in root.glob("*.pdf"):
        fitz.open(pdf).page_count
    print(json.dumps({"extracted_to": str(out), "zip_test": bad, "broken_local_links": problems[:30],
                      "n_broken": len(problems)}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "pdf"
    if cmd == "pdf":
        build_pdf(sys.argv[2] if len(sys.argv) > 2 else git("log", "-1", "--format=%h, %ad", "--date=format:%d %B %Y"))
    elif cmd == "zip":
        build_zip()
    elif cmd == "check":
        check()
