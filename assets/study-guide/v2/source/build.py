"""Blue Impulse Study Guide V2 — builder.

  python build.py                 full book -> assets/study-guide/v2/BlueImpulse_Study_Guide_V2.pdf
  python build.py --only ch3      just chapter 3's generated pages (fast check) -> build/only-ch3.pdf
  python build.py --only ch3 --preview   also writes PNG contact sheets of those pages to build/preview/

Content lives in content/*.sg (one file per chapter, plus front.sg and appendix.sg).
Every @page is exactly one printed page; the audit reports any page whose content does not fit.

Markup (one directive per line; markdown everywhere else):
  @page Heading text            new page; "@page -" for no heading; "@page! Heading" for an extra-large heading
  @section 1.1 Name             this page starts subtopic 1.1 (contents, bookmarks, running label)
  @label TEXT                   small label above the heading (defaults to the current subtopic)
  @plane climb|side|top|none [tl|tr|bl|br]   airliner decoration (default: automatic)
  @box light|dark|alt [w=60] [right|center] [small] | Title      ...markdown...  @end
  @image FILE [w=45] [right|center] | caption        folder image box (page level)  — inside a @box it floats right
  @flow A > B > C               horizontal pills;  "A :: small text" adds a second line
  @stack A > B > C              vertical pills with arrows
  @cycle A > B > C              pills in a loop (shows a return note)
  @row ... @endrow              put the blocks between them side by side
  @video Title | URL            tutorial link callout
  @try ... @end                 Pause & Try exercise (sticks to the bottom of the page; no solutions)
  @goals ... @end               learning goals box (markdown list)
  @terms ... @end               key terms: one "Term: definition" per line, two columns
  @practice ... @end            end-of-chapter practice: markdown ordered list in one box
  @h2 Text                      small DIN heading outside boxes
  @space N                      vertical gap of N px
"""
from __future__ import annotations
import argparse, html, json, re, shutil, sys
from pathlib import Path
from markdown_it import MarkdownIt

SRC = Path(__file__).resolve().parent
V2 = SRC.parent
ROOT = V2.parents[2]
ART = V2 / "art"
IMG = ART / "images"
BUILD = V2 / "build"
CONTENT = SRC / "content"
TEMP = ROOT / "temp contents/ai proj stage2"
ART_PDF = TEMP / "study guide art.pdf"
TEAM_PDF = TEMP / "meet the team.pdf"
OUT_PDF = V2 / "BlueImpulse_Study_Guide_V2.pdf"
CHROME = Path.home() / "Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"

CHAPTERS = {
    1: ("Dawn", "The Fundamentals"),
    2: ("Morning", "Behaviorism & Behaviorist AI"),
    3: ("Midday", "Hardware"),
    4: ("Afternoon", "Networking"),
    5: ("Dusk", "Applications"),
    6: ("Midnight", "Strengths & Limitations"),
}
DIVIDER_PAGE = {1: 17, 2: 18, 3: 19, 4: 20, 5: 21, 6: 22}  # 1-based pages in study guide art.pdf (printed labels)
COVER_PAGE = 16

md = MarkdownIt("commonmark", {"html": True, "typographer": True}).enable(["table", "strikethrough", "smartquotes"])
# "replacements" stays off: it turns "(c)" sub-question labels into a copyright sign.


def mdr(text: str) -> str:
    return md.render(text.strip()) if text.strip() else ""


def inline(text: str) -> str:
    return md.renderInline(text.strip())


# ---------------------------------------------------------------- images
def image_index():
    """Supplied PNGs are copied once as JPEGs with clean names; lookups accept the original file name."""
    IMG.mkdir(parents=True, exist_ok=True)
    idx = {}
    from PIL import Image
    for f in sorted(TEMP.glob("*.PNG")) + sorted(TEMP.glob("*.png")) + sorted((SRC / "images").glob("*.*")):
        key = re.sub(r"[^a-z0-9.]+", "", f.stem.lower())
        dest = IMG / (re.sub(r"[^a-z0-9]+", "-", f.stem.lower()).strip("-") + (".png" if f.suffix.lower() == ".png" and f.parent == SRC / "images" else ".jpg"))
        if not dest.exists() or dest.stat().st_mtime < f.stat().st_mtime:
            im = Image.open(f)
            if dest.suffix == ".jpg":
                im.convert("RGB").save(dest, quality=88)
            else:
                im.save(dest)
        idx[key] = dest
    return idx


IMAGES: dict = {}


def find_image(name: str) -> Path:
    name = name.strip()
    if re.search(r"\.(png|jpe?g)$", name, re.I):
        name = name[:name.rfind(".")]
    key = re.sub(r"[^a-z0-9.]+", "", name.lower())
    if key in IMAGES:
        return IMAGES[key]
    raise SystemExit(f"image not found: {name!r}")


# ---------------------------------------------------------------- parsing
class Page:
    def __init__(self, heading, chapter, src):
        self.heading = heading
        self.chapter = chapter
        self.src = src
        self.section = None
        self.label = None
        self.plane = None
        self.blocks = []  # list of (kind, data)
        self.number = None
        self.big = False


def opts_and_title(rest: str):
    if "|" in rest:
        a, t = rest.split("|", 1)
    else:
        a, t = rest, ""
    toks = a.split()
    o = {"variant": "light", "w": None, "align": None, "small": False}
    for tok in toks:
        if tok in ("light", "dark", "alt"):
            o["variant"] = tok
        elif tok.startswith("w="):
            o["w"] = int(tok[2:])
        elif tok in ("right", "center", "left"):
            o["align"] = tok
        elif tok == "small":
            o["small"] = True
    return o, t.strip()


def parse(path: Path, chapter: int):
    pages, cur = [], None
    stack = []  # open containers: list of ("row", list) / ("block", kind, opts, title, lines)
    text_buf: list[str] = []

    def target():
        for s in reversed(stack):
            if s[0] == "row":
                return s[1]
        return cur.blocks

    def flush_text():
        nonlocal text_buf
        if cur is not None and "".join(text_buf).strip():
            target().append(("text", "\n".join(text_buf)))
        text_buf = []

    lines = path.read_text().splitlines()
    for ln_no, raw in enumerate(lines, 1):
        line = raw.rstrip()
        s = line.strip()
        # inside a text block (box/try/goals/terms/practice): collect until @end
        if stack and stack[-1][0] == "block":
            if s == "@end":
                _, kind, o, title, buf = stack.pop()
                target().append((kind, {"opts": o, "title": title, "body": "\n".join(buf)}))
            else:
                stack[-1][4].append(line)
            continue
        if s.startswith("@"):
            flush_text()
            cmd, _, rest = s.partition(" ")
            rest = rest.strip()
            if cmd in ("@page", "@page!"):
                if stack:
                    raise SystemExit(f"{path.name}:{ln_no}: unclosed block before @page")
                cur = Page(None if rest in ("", "-") else rest, chapter, f"{path.name}:{ln_no}")
                cur.big = cmd == "@page!"
                pages.append(cur)
            elif cur is None:
                raise SystemExit(f"{path.name}:{ln_no}: directive before the first @page")
            elif cmd == "@section":
                cur.section = rest
            elif cmd == "@label":
                cur.label = rest
            elif cmd == "@plane":
                cur.plane = rest.split()
            elif cmd in ("@box", "@try", "@goals", "@terms", "@practice"):
                o, title = opts_and_title(rest)
                stack.append(("block", cmd[1:], o, title, []))
            elif cmd == "@row":
                stack.append(("row", []))
            elif cmd == "@endrow":
                if not stack or stack[-1][0] != "row":
                    raise SystemExit(f"{path.name}:{ln_no}: @endrow without @row")
                _, items = stack.pop()
                target().append(("row", items))
            elif cmd == "@image":
                o, cap = opts_and_title(rest)
                name = rest.split("|")[0]
                name = re.sub(r"\s(w=\d+|right|center|left)\b", "", " " + name).strip()
                target().append(("image", {"file": name, "opts": o, "caption": cap}))
            elif cmd in ("@flow", "@stack", "@cycle"):
                target().append((cmd[1:], [x.strip() for x in rest.split(" > ")]))
            elif cmd == "@video":
                t, _, u = rest.partition("|")
                target().append(("video", {"title": t.strip(), "url": u.strip()}))
            elif cmd == "@h2":
                target().append(("h2", rest))
            elif cmd == "@space":
                target().append(("space", int(rest or 10)))
            else:
                raise SystemExit(f"{path.name}:{ln_no}: unknown directive {cmd}")
        else:
            if cur is None:
                if s:
                    raise SystemExit(f"{path.name}:{ln_no}: text before the first @page")
                continue
            text_buf.append(line)
    flush_text()
    if stack:
        raise SystemExit(f"{path.name}: unclosed block at end of file")
    return pages


# ---------------------------------------------------------------- rendering
def box_style(o):
    st = []
    if o.get("w"):
        st.append(f"width:{o['w']}%")
    return f' style="{";".join(st)}"' if st else ""


def align_cls(o):
    return {"right": " right", "center": " center"}.get(o.get("align") or "", "")


def pill(text):
    if "::" in text:
        a, b = text.split("::", 1)
        return f'<div class="pill">{inline(a)}<small>{inline(b)}</small></div>'
    return f'<div class="pill">{inline(text)}</div>'


def render_body(body: str) -> str:
    """Markdown body of a box; @image lines inside a box float right; @flow/@stack lines also allowed."""
    out, buf = [], []

    def flush():
        if buf:
            out.append(mdr("\n".join(buf)))
            buf.clear()
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("@image "):
            flush()
            rest = s[len("@image "):]
            name, _, cap = rest.partition("|")
            name = re.sub(r"\s(w=\d+|right|center|left)\b", "", " " + name).strip()
            m = re.search(r"w=(\d+)", rest.split("|")[0])
            w = f' style="width:{m.group(1)}%"' if m else ""
            src = find_image(name).relative_to(BUILD.parent).as_posix()
            out.append(f'<figure class="inimg"{w}><img src="../{src}">' + (f"<figcaption>{inline(cap)}</figcaption>" if cap.strip() else "") + "</figure>")
        elif s.startswith("@flow ") or s.startswith("@stack ") or s.startswith("@cycle "):
            flush()
            kind, rest = s[1:].split(" ", 1)
            out.append(render_block((kind, [x.strip() for x in rest.split(" > ")])))
        elif s == "@clear":
            flush()
            out.append('<div class="clear"></div>')
        else:
            buf.append(line)
    flush()
    return "\n".join(out)


def win(variant, title, body_html, extra_cls="", style=""):
    head = f"<h3>{inline(title)}</h3>" if title else ""
    return (f'<div class="win {variant}{extra_cls}"{style}><div class="tb"><i></i><i></i><i></i><b></b></div>'
            f'<div class="wb">{head}{body_html}</div></div>')


def render_block(b):
    kind, data = b
    if kind == "text":
        return f'<div class="out">{mdr(data)}</div>'
    if kind == "h2":
        return f'<div class="h2">{inline(data)}</div>'
    if kind == "space":
        return f'<div class="spacer" style="height:{data}px"></div>'
    if kind == "row":
        return '<div class="row">' + "".join(render_block(x) for x in data) + "</div>"
    if kind == "box":
        o = data["opts"]
        cls = align_cls(o) + (" small" if o["small"] else "")
        return win(o["variant"], data["title"], render_body(data["body"]), cls, box_style(o))
    if kind == "try":
        o = data["opts"]
        return win(o["variant"], data["title"] or "Pause &amp; Try", render_body(data["body"]), " try small", box_style(o))
    if kind == "goals":
        o = data["opts"]
        return win(o["variant"], data["title"] or "Learning goals", render_body(data["body"]), " goals", box_style(o))
    if kind == "practice":
        o = data["opts"]
        body = re.sub(r"\[(\d+) marks?\]", lambda m: f'<span class="marks">[{m.group(1)}]</span>', data["body"])
        return win(o["variant"], data["title"] or "Practice", render_body(body), " practice", box_style(o))
    if kind == "terms":
        o = data["opts"]
        items = []
        for ln in data["body"].splitlines():
            if ":" in ln and ln.strip():
                t, d = ln.split(":", 1)
                items.append(f"<div><b>{inline(t)}:</b> {inline(d)}</div>")
        return win(o["variant"], data["title"] or "Key terms", '<div class="terms">' + "".join(items) + "</div>", " small", box_style(o))
    if kind == "image":
        o = data["opts"]
        src = find_image(data["file"]).relative_to(BUILD.parent).as_posix()
        cap = f"<figcaption>{inline(data['caption'])}</figcaption>" if data["caption"] else ""
        return (f'<figure class="folder{align_cls(o)}"{box_style(o)}><div class="tab"></div>'
                f'<div class="fb"><img src="../{src}">{cap}</div></figure>')
    if kind == "flow":
        parts = []
        for i, x in enumerate(data):
            if i:
                parts.append('<span class="arr">&rarr;</span>')
            parts.append(pill(x))
        return '<div class="flow">' + "".join(parts) + "</div>"
    if kind == "cycle":
        parts = []
        for i, x in enumerate(data):
            if i:
                parts.append('<span class="arr">&rarr;</span>')
            parts.append(pill(x))
        return ('<div class="cycle">' + "".join(parts) + '<span class="arr">&#8635;</span></div>')
    if kind == "stack":
        parts = []
        for i, x in enumerate(data):
            if i:
                parts.append('<div class="down">&darr;</div>')
            parts.append(pill(x))
        return '<div class="stack">' + "".join(parts) + "</div>"
    if kind == "video":
        return (f'<div class="video"><span class="play"></span><span><b>{inline(data["title"])}</b>'
                f'<a href="{html.escape(data["url"])}">{html.escape(data["url"])}</a></span></div>')
    raise SystemExit(f"cannot render {kind}")


PLANE_SPOTS = {  # (name, css) defaults cycle through these; low opacity line art like the format examples
    "br": "right:-30px;bottom:30px;width:300px;opacity:.28",
    "bl": "left:-40px;bottom:70px;width:280px;opacity:.24;transform:scaleX(-1)",
    "tr": "right:-30px;top:60px;width:250px;opacity:.22",
    "tl": "left:-30px;top:120px;width:240px;opacity:.20;transform:scaleX(-1)",
}


def page_html(p: Page, idx: int, chapter_label: str | None, cur_section: str | None):
    ch = p.chapter
    bg = f"../art/bg-{'intro' if ch == 0 else ch}.jpg"
    out = [f'<section class="page ch{ch}" data-src="{html.escape(p.src)}" data-n="{p.number}">',
           f'<img class="bg" src="{bg}">']
    if chapter_label:
        out.append(f'<div class="hdr">{html.escape(chapter_label)}</div>')
    plane = p.plane or [("climb", "side", "top")[idx % 3], ("br", "bl", "br", "tr")[idx % 4]]
    if plane[0] != "none":
        spot = plane[1] if len(plane) > 1 else "br"
        out.append(f'<img class="deco" src="../art/plane-{plane[0]}.png" style="{PLANE_SPOTS[spot]}">')
    out.append('<div class="content">')
    label = p.label if p.label is not None else cur_section
    if label:
        out.append(f'<div class="sec">{html.escape(label)}</div>')
    if p.heading:
        spark = '<img class="spark" src="../art/sparkle.png">'
        out.append(f'<div class="ph{" big" if p.big else ""}">{inline(p.heading)}{spark}</div>')
    for b in p.blocks:
        out.append(render_block(b))
    out.append("</div>")
    if p.number:
        out.append(f'<div class="pn">{p.number}</div>')
    out.append("</section>")
    return "\n".join(out)


def toc_pages(toc, start_number):
    """Full-page contents in the Content1.png format, split over as many pages as needed."""
    per_page = [[1, 2, 3, 4], [5, 6]]
    pages = []
    for k, chs in enumerate(per_page):
        out = [f'<section class="page ch0 toc" data-n="{start_number + k}"><img class="bg" src="../art/bg-intro.jpg">',
               '<img class="deco" src="../art/plane-climb.png" style="right:-30px;bottom:40px;width:300px;opacity:.25">',
               '<div class="content" style="gap:6px">']
        out.append('<div class="ph big">Contents</div>' if k == 0 else '<div class="ph big">Contents</div>')
        for ch in chs:
            name = CHAPTERS[ch][1]
            first = toc["chapters"].get(ch, "")
            out.append(f'<div class="toc-ch"><div class="n">{ch}</div><div class="t">{html.escape(name)}</div><div class="p">{first}</div></div>')
            out.append('<div class="toc-sub">' + "".join(
                f"<div><span>{html.escape(s)}</span><span>{n}</span></div>" for s, n in toc["sections"].get(ch, [])) + "</div>")
        if k == 1:
            extra = toc.get("extra", [])
            if extra:
                out.append('<div class="toc-ch"><div class="n">A</div><div class="t">Appendix</div><div class="p">' + str(extra[0][1]) + "</div></div>")
                out.append('<div class="toc-sub">' + "".join(f"<div><span>{html.escape(s)}</span><span>{n}</span></div>" for s, n in extra) + "</div>")
        out.append(f'</div><div class="pn">{start_number + k}</div></section>')
        pages.append("\n".join(out))
    return pages


def load_all(only=None):
    files = [("front", 0)] + [(f"ch{c}", c) for c in CHAPTERS] + [("appendix", 0)]
    data = {}
    for name, ch in files:
        f = CONTENT / f"{name}.sg"
        data[name] = parse(f, ch) if f.exists() else []
    return data


def number_pages(data):
    """Final order: cover, team (4), front pages, contents (2), [divider + chapter pages] x6, appendix."""
    import pymupdf as fitz
    team = fitz.open(TEAM_PDF).page_count
    n = 1 + team  # cover + team
    for p in data["front"]:
        n += 1
        p.number = n
    toc_start = n + 1
    n += 2
    toc = {"chapters": {}, "sections": {}, "extra": []}
    for c in CHAPTERS:
        n += 1  # divider
        toc["chapters"][c] = n
        for p in data[f"ch{c}"]:
            n += 1
            p.number = n
            if p.section:
                toc["sections"].setdefault(c, []).append((p.section, n))
    for p in data["appendix"]:
        n += 1
        p.number = n
        if p.section:
            toc["extra"].append((p.section, n))
    return toc, toc_start, n


def write_html(page_htmls, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../source/style.css"></head><body>\n'
                    + "\n".join(page_htmls) + "\n</body></html>")


AUDIT_JS = r"""
() => [...document.querySelectorAll('section.page')].map(sec => {
  const c = sec.querySelector('.content'); if (!c) return null;
  const cr = c.getBoundingClientRect(); let maxB = cr.top, maxR = cr.right, wide = [];
  for (const el of c.querySelectorAll('*')) {
    const r = el.getBoundingClientRect(); if (!r.width && !r.height) continue;
    if (r.bottom > maxB) maxB = r.bottom;
    if (r.right > cr.right + 14) wide.push(el.className || el.tagName);
  }
  const used = Math.round(maxB - cr.top), room = Math.round(cr.height);
  return {n: sec.dataset.n, src: sec.dataset.src || '', used, room, over: Math.max(0, used - room), wide: [...new Set(wide)].slice(0,4)};
}).filter(Boolean)
"""


def print_pdf(html_path: Path, pdf_path: Path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=str(CHROME))
        pg = b.new_page()
        pg.goto(html_path.as_uri(), wait_until="load")
        pg.evaluate("document.fonts.ready")
        audit = pg.evaluate(AUDIT_JS)
        pg.pdf(path=str(pdf_path), prefer_css_page_size=True, print_background=True)
        b.close()
    return audit


def previews(pdf_path: Path, out_dir: Path, label: str, numbers=None):
    import pymupdf as fitz
    from PIL import Image, ImageDraw
    out_dir.mkdir(parents=True, exist_ok=True)
    d = fitz.open(pdf_path)
    ims = []
    for i, pg in enumerate(d):
        pix = pg.get_pixmap(matrix=fitz.Matrix(0.62, 0.62))
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        tag = str(numbers[i]) if numbers else str(i + 1)
        dr = ImageDraw.Draw(im)
        dr.rectangle([0, 0, 34, 16], fill="black")
        dr.text((3, 2), tag, fill="white")
        ims.append(im)
    cols, per = 4, 8
    paths = []
    for k in range(0, len(ims), per):
        chunk = ims[k:k + per]
        w, h = chunk[0].size
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (w + 8) + 8, rows * (h + 8) + 8), "#2b2b2b")
        for j, im in enumerate(chunk):
            sheet.paste(im, (8 + (j % cols) * (w + 8), 8 + (j // cols) * (h + 8)))
        p = out_dir / f"{label}-{k // per + 1:02d}.jpg"
        sheet.save(p, quality=86)
        paths.append(p)
    return paths


def assemble(gen_pdf: Path, layout, toc_data):
    """layout: list of ("art", page) | ("team", i) | ("gen", i)."""
    import pymupdf as fitz
    art, team, gen = fitz.open(ART_PDF), fitz.open(TEAM_PDF), fitz.open(gen_pdf)
    out = fitz.open()
    for kind, i in layout:
        src = {"art": art, "team": team, "gen": gen}[kind]
        out.insert_pdf(src, from_page=i, to_page=i)
    toc = [[1, "Cover", 1], [1, "Meet the team", 2]]
    for title, n in toc_data["front"]:
        toc.append([1, title, n])
    for c, (theme, name) in CHAPTERS.items():
        toc.append([1, f"Chapter {c} — {name}", toc_data["chapters"][c]])
        for s, n in toc_data["sections"].get(c, []):
            toc.append([2, s, n])
    for s, n in toc_data["extra"]:
        toc.append([1, s, n])
    out.set_toc(toc)
    out.set_metadata({"title": "Beginner's Guide: How Machines Sense, Connect, and Act — Blue Impulse Study Guide V2",
                      "author": "Blue Impulse team", "subject": "Hardware, Networks & Behaviorist AI"})
    out.save(OUT_PDF, garbage=4, deflate=True)
    return out.page_count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="ch1..ch6, front or appendix")
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    global IMAGES
    IMAGES = image_index()
    data = load_all()
    toc, toc_start, last = number_pages(data)
    BUILD.mkdir(parents=True, exist_ok=True)

    def chapter_html(name, pages):
        htmls, cur_sec = [], None
        ch = pages[0].chapter if pages else 0
        lab = f"Chapter {ch} - {CHAPTERS[ch][1]}" if ch else None
        for i, p in enumerate(pages):
            if p.section:
                cur_sec = p.section
            htmls.append(page_html(p, i, lab, cur_sec))
        return htmls

    if a.only:
        pages = data[a.only]
        htmls = chapter_html(a.only, pages)
        if a.only == "front":
            htmls += toc_pages(toc, toc_start)
        hp, pp = BUILD / f"only-{a.only}.html", BUILD / f"only-{a.only}.pdf"
        write_html(htmls, hp)
        audit = print_pdf(hp, pp)
        bad = [x for x in audit if x["over"] > 0 or x["wide"]]
        print(json.dumps({"pages": len(htmls), "pdf": str(pp), "problems": bad}, indent=1))
        if a.preview:
            nums = [p.number for p in pages] + ([toc_start, toc_start + 1] if a.only == "front" else [])
            for p in previews(pp, BUILD / "preview", a.only, nums):
                print("preview:", p)
        return

    # full book: generated pages in one HTML, then interleave with the supplied art pages
    gen_htmls, layout = [], [("art", COVER_PAGE - 1)]
    import pymupdf as fitz
    for i in range(fitz.open(TEAM_PDF).page_count):
        layout.append(("team", i))
    toc_front = []
    for h in chapter_html("front", data["front"]):
        layout.append(("gen", len(gen_htmls))); gen_htmls.append(h)
    for p in data["front"]:
        toc_front.append((p.heading or "About", p.number))
    for h in toc_pages(toc, toc_start):
        layout.append(("gen", len(gen_htmls))); gen_htmls.append(h)
    toc_front.append(("Contents", toc_start))
    for c in CHAPTERS:
        layout.append(("art", DIVIDER_PAGE[c] - 1))
        for h in chapter_html(f"ch{c}", data[f"ch{c}"]):
            layout.append(("gen", len(gen_htmls))); gen_htmls.append(h)
    for h in chapter_html("appendix", data["appendix"]):
        layout.append(("gen", len(gen_htmls))); gen_htmls.append(h)
    hp, gp = BUILD / "guide.html", BUILD / "generated.pdf"
    write_html(gen_htmls, hp)
    audit = print_pdf(hp, gp)
    toc["front"] = toc_front
    total = assemble(gp, layout, toc)
    bad = [x for x in audit if x["over"] > 0 or x["wide"]]
    (BUILD / "audit.json").write_text(json.dumps(audit, indent=1))
    print(json.dumps({"pages": total, "expected": last, "pdf": str(OUT_PDF), "problems": bad}, indent=1))
    if a.preview:
        for p in previews(OUT_PDF, BUILD / "preview", "book"):
            print("preview:", p)


if __name__ == "__main__":
    main()
