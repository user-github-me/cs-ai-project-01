"""Export the Study Guide V2 chapter sources (content/chN.sg) to the shared Markdown chapters.

  python export_markdown.py          -> <repo>/content/chapter-0N/draft.md (+ images/, figures/)

The study guide and the Markdown chapter therefore carry the same explanations, examples,
Pause & Try activities (numbered "Pause & Try N.k" so content/chapter-0N/solutions.md can
answer them) and Practice questions. Correct an error in both places, or correct the .sg
source and re-run this export.
"""
from __future__ import annotations
import re, shutil
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parents[3]
ART_IMAGES = SRC.parent / "art" / "images"
TEMP = ROOT / "temp contents/ai proj stage2"

CHAPTERS = {1: "The Fundamentals", 2: "Behaviorism & Behaviorist AI", 3: "Hardware",
            4: "Networking", 5: "Applications", 6: "Strengths & Limitations"}
# box body colours from style.css (used as figure backgrounds so drawings stay legible on white pages)
BOX = {
    1: {"light": "#D9C9E8", "dark": "#466BAA", "alt": "#E5D9E7", "page": "#7A99C7"},
    2: {"light": "#F8EFBA", "dark": "#356DB7", "alt": "#C2DAE5", "page": "#7FB6E0"},
    3: {"light": "#77E0F5", "dark": "#2CABBE", "alt": "#C4E3F7", "page": "#2F93C9"},
    4: {"light": "#D6E8F9", "dark": "#216ABF", "alt": "#D6E8F9", "page": "#2469D8"},
    5: {"light": "#D9C9E8", "dark": "#483278", "alt": "#D6C9E5", "page": "#4E4580"},
    6: {"light": "#F6F6F5", "dark": "#042D62", "alt": "#E6E4E5", "page": "#1E2A4D"},
}


def clean_name(stem: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")


def image_file(name: str) -> Path:
    name = name.strip()
    if re.search(r"\.(png|jpe?g)$", name, re.I):
        name = name[:name.rfind(".")]
    p = ART_IMAGES / (clean_name(name) + ".jpg")
    if not p.exists():
        raise SystemExit(f"image not found for {name!r}: {p}")
    return p


def strip_styles(html: str) -> str:
    html = re.sub(r'\s+style="[^"]*"', "", html)
    return re.sub(r'\s+class="[^"]*"', "", html)


def flow_line(items, loop=False):
    parts = []
    items = [re.sub(r"<br\s*/?>", " ", it) for it in items]
    for it in items:
        if "::" in it:
            a, b = it.split("::", 1)
            parts.append(f"**{a.strip()}** ({b.strip()})")
        else:
            parts.append(f"**{it.strip()}**")
    line = " → ".join(parts)
    return line + (" → *(back to the start)*" if loop else "")


class Exporter:
    def __init__(self, ch: int, outdir: Path):
        self.ch, self.out = ch, outdir
        self.fig = 0
        self.pt = 0
        (outdir / "images").mkdir(parents=True, exist_ok=True)
        (outdir / "figures").mkdir(parents=True, exist_ok=True)
        self.used_images = set()

    def image_md(self, name, caption):
        src = image_file(name)
        dest = self.out / "images" / src.name
        shutil.copyfile(src, dest)
        self.used_images.add(src.name)
        cap = caption.strip()
        alt = re.sub(r"[*_`\[\]]", "", cap) or Path(name).stem
        return [f"![{alt}](images/{src.name})", f"*{cap}*" if cap else ""]

    def svg_md(self, svg: str, bg: str, title: str):
        self.fig += 1
        vb = re.search(r'viewBox="([\d.\s-]+)"', svg)
        w = h = None
        if vb:
            _, _, w, h = [float(x) for x in vb.group(1).split()]
        svg = re.sub(r'\s+style="[^"]*"', "", svg, count=1)
        svg = re.sub(r'(<svg\b[^>]*?)\swidth="[^"]*"', r"\1", svg, count=1)
        svg = re.sub(r'(<svg\b[^>]*?)\sheight="[^"]*"', r"\1", svg, count=1)
        attrs = ' xmlns="http://www.w3.org/2000/svg"' if "xmlns=" not in svg.split(">", 1)[0] else ""
        if w:
            attrs += f' width="{int(w)}" height="{int(h)}"'
        svg = svg.replace("<svg", "<svg" + attrs, 1)
        head, rest = svg.split(">", 1)
        svg = f'{head}><rect x="0" y="0" width="100%" height="100%" rx="10" fill="{bg}"/>{rest}'
        name = f"fig{self.ch}-{self.fig:02d}.svg"
        (self.out / "figures" / name).write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n")
        # No invented figure numbers: the chapters number their own figures in box titles, and the
        # box title is already printed as the heading just above the drawing.
        alt = re.sub(r"[*_`\[\]]", "", title) if title else "Diagram"
        return [f"![{alt}](figures/{name})"]

    def body(self, lines, variant, title):
        """Convert the inside of a block (markdown + a few directives + raw HTML/SVG)."""
        out, i = [], 0
        bg = BOX[self.ch].get(variant, BOX[self.ch]["page"])
        while i < len(lines):
            line = lines[i]
            s = line.strip()
            if "<svg" in s:
                buf = [line]
                while "</svg>" not in buf[-1] and i + 1 < len(lines):
                    i += 1
                    buf.append(lines[i])
                text = "\n".join(buf)
                pre, _, rest = text.partition("<svg")
                svg_body, _, post = rest.partition("</svg>")
                if strip_styles(pre).strip():
                    out.append(strip_styles(pre).strip())
                out += self.svg_md("<svg" + svg_body + "</svg>", bg, title)
                if strip_styles(post).strip():
                    out.append(strip_styles(post).strip())
            elif "<figure" in s and "<img" in s:
                m = re.search(r'src="[^"]*/([^/"]+)"', s)
                cap = re.search(r"<figcaption>(.*?)</figcaption>", s)
                name = m.group(1) if m else ""
                src = ART_IMAGES / name
                shutil.copyfile(src, self.out / "images" / name)
                c = re.sub(r"<[^>]+>", "", cap.group(1)) if cap else ""
                out += [f"![{c}](images/{name})", f"*{c}*" if c else ""]
            elif s.startswith("@image "):
                rest = s[len("@image "):]
                name, _, cap = rest.partition("|")
                name = re.sub(r"\s(w=\d+|right|center|left)\b", "", " " + name).strip()
                out += self.image_md(name, cap)
            elif s.startswith("@flow "):
                out += ["", flow_line(s[6:].split(" > ")), ""]
            elif s.startswith("@cycle "):
                out += ["", flow_line(s[7:].split(" > "), loop=True), ""]
            elif s.startswith("@stack "):
                items = s[7:].split(" > ")
                out.append("")
                for k, it in enumerate(items, 1):
                    it = re.sub(r"<br\s*/?>", " ", it)
                    a, _, b = it.partition("::")
                    a = re.sub(r"^\s*(step\s*)?\d+\s*[·.:—-]\s*", "", a, flags=re.I)
                    out.append(f"{k}. **{a.strip()}**" + (f" — {b.strip()}" if b.strip() else ""))
                out.append("")
            elif s.startswith("@h2 "):
                out += ["", f"#### {s[4:].strip()}", ""]
            elif s.startswith("@video "):
                t, _, u = s[7:].partition("|")
                out += ["", f"▶ **Video tutorial:** [{t.strip()}]({u.strip()})", ""]
            elif s in ("@clear",) or s.startswith("<!--"):
                pass
            elif "<" in line and ("style=" in line or "class=" in line):
                out.append(strip_styles(line))
            else:
                out.append(line)
            i += 1
        return out

    def convert(self, text: str) -> str:
        # Boolean NOT written as an overlined span must keep its meaning outside the stylesheet:
        # use a combining overline (U+0305) on every character instead of CSS.
        text = re.sub(r'<span style="text-decoration:\s*overline;?">(.*?)</span>',
                      lambda m: "".join(c + "\u0305" for c in re.sub(r"<[^>]+>", "", m.group(1))), text)
        pages, cur = [], None
        for line in text.splitlines():
            if line.startswith("@page"):
                cur = [line]
                pages.append(cur)
            elif cur is not None:
                cur.append(line)
        md = []
        self.started = False
        for page in pages:
            head = page[0].split(" ", 1)[1].strip() if " " in page[0] else ""
            section = None
            body = []
            for l in page[1:]:
                s = l.strip()
                if s.startswith("@section "):
                    section = s[len("@section "):]
                elif s.startswith(("@label", "@plane", "@space", "@row", "@endrow")):
                    continue
                else:
                    body.append(l)
            label = next((l.strip()[7:] for l in page[1:] if l.strip().startswith("@label ")), "")
            if section:
                self.started = True
                md += ["", f"## {section}", ""]
            top = (not self.started) or head.startswith("Practice") or "Practice" in label
            self.cur_head = head
            if head and head != "-":
                md += ["", f"{'##' if top else '###'} {head}", ""]
            md += self.blocks(body)
        text = "\n".join(md)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"

    def blocks(self, lines):
        out, i, chunk = [], 0, []

        def flush():
            if chunk:
                out.extend(self.body(list(chunk), "page", ""))
                chunk.clear()
        while i < len(lines):
            s = lines[i].strip()
            m = re.match(r"@(box|try|goals|terms|practice)\b(.*)$", s)
            if m:
                flush()
                kind, rest = m.group(1), m.group(2)
                opts, _, title = rest.partition("|")
                variant = next((t for t in opts.split() if t in ("light", "dark", "alt")), "light")
                buf = []
                i += 1
                while i < len(lines) and lines[i].strip() != "@end":
                    buf.append(lines[i])
                    i += 1
                out += self.block(kind, variant, title.strip(), buf)
            else:
                chunk.append(lines[i])
            i += 1
        flush()
        return out

    def block(self, kind, variant, title, buf):
        if kind == "try":
            self.pt += 1
            body = self.body(buf, variant, title)
            while body and not body[0].strip():
                body.pop(0)
            while body and not body[-1].strip():
                body.pop()
            hdr = f"> **Pause & Try {self.ch}.{self.pt}**" + (f" — {title}" if title else "")
            return ["", hdr, ">"] + [f"> {x}" if x.strip() else ">" for x in body] + [""]
        if title and title.strip().lower() == getattr(self, "cur_head", "").strip().lower():
            title = ""
        if kind == "terms":
            items = []
            for l in buf:
                if ":" in l and l.strip():
                    t, d = l.split(":", 1)
                    items.append(f"- **{t.strip()}:** {d.strip()}")
            return (["", f"#### {title}", ""] if title else [""]) + items + [""]
        if kind == "goals":
            return (["", f"#### {title}", ""] if title else [""]) + self.body(buf, variant, title) + [""]
        if kind == "practice":
            return (["", f"#### {title}", ""] if title else [""]) + self.body(buf, variant, title) + [""]
        return ["", f"#### {title}" if title else "", ""] + self.body(buf, variant, title) + [""]


def main():
    report = {}
    for ch, name in CHAPTERS.items():
        out = ROOT / "content" / f"chapter-{ch:02d}"
        if out.joinpath("images").exists():
            shutil.rmtree(out / "images")
        if out.joinpath("figures").exists():
            shutil.rmtree(out / "figures")
        ex = Exporter(ch, out)
        body = ex.convert((SRC / "content" / f"ch{ch}.sg").read_text())
        header = (f"# Chapter {ch} — {name}\n\n"
                  f"> This is the complete Stage 2 (V2.0) chapter text. It is the same content as Chapter {ch} of the "
                  f"[Blue Impulse Study Guide V2](../../assets/study-guide/v2/BlueImpulse_Study_Guide_V2.pdf), exported from "
                  f"`assets/study-guide/v2/source/content/ch{ch}.sg`. Answers to every *Pause & Try* and *Practice* question are in "
                  f"[solutions.md](solutions.md). If you correct one copy, correct the other.\n")
        (out / "draft.md").write_text(header + "\n" + body)
        report[ch] = {"pause_and_try": ex.pt, "figures": ex.fig, "images": len(ex.used_images) + len(list((out / 'images').glob('*')))}
        print(f"chapter {ch}: {ex.pt} Pause & Try, {ex.fig} figures, {len(list((out / 'images').glob('*')))} images, "
              f"{len(body.split())} words")


VIDEO = {1: ("Program execution", "1.3 (end of the topic)"), 2: ("Basic reinforcement learning", "2.3 (end of the topic)"),
         3: ("How hardware enables AI", "3.6 (end of the topic)"), 4: ("Network challenges", "4.4 (collision handling)"),
         5: ("Networking for behaviorist AI", "5.1"), 6: (None, None)}
PPT = {1: "Not a separate section (computer hardware is defined on slide 18)",
       2: "Section 3 — Behaviorist AI (slides 49–58) and \"Why Sojourner\" (slides 59–60)",
       3: "Section 1 — Hardware (slides 17–36)",
       4: "Section 2 — Networks (slides 37–48)",
       5: "Conclusion: Sojourner as one integrated system (slide 61)",
       6: "Slides 59–60: reactive behaviour compared with later rovers' autonomy"}


def anchor(h):
    h = h.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


def guide_pages():
    import pymupdf as fitz
    toc = fitz.open(SRC.parent / "BlueImpulse_Study_Guide_V2.pdf").get_toc()
    chap, sec = {}, {}
    for lvl, title, page in toc:
        m = re.match(r"Chapter (\d) ", title)
        if lvl == 1 and m:
            chap[int(m.group(1))] = page
        elif lvl == 2:
            sec[title.split(" ")[0]] = page
    return chap, sec


def intro_of(ch):
    text = (SRC / "content" / f"ch{ch}.sg").read_text().split("@page", 2)[1]
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip() and not p.strip().startswith("@") and "\n@" not in p]
    return paras[0] if paras else ""


def write_readmes():
    chap, sec = guide_pages()
    rows = []
    for ch, name in CHAPTERS.items():
        d = ROOT / "content" / f"chapter-{ch:02d}"
        draft = (d / "draft.md").read_text()
        subs = re.findall(r"^## (\d\.\d+ .+)$", draft, re.M)
        lo = next(d.glob("Learning_Outcomes*.md")).name
        kt = next(d.glob("Key_Terms_*.md")).name
        tb = f"TF{4*ch-3:02d}–TF{4*ch:02d}, MC{4*ch-3:02d}–MC{4*ch:02d}, OE{ch:02d}"
        v, vwhere = VIDEO[ch]
        vid = f"{v} — linked at the end of {vwhere}" if v else "Not selected for a video"
        sub_lines = "\n".join(f"- [{s}](draft.md#{anchor(s)}) — Study Guide V2 p. {sec.get(s.split(' ')[0], '–')}" for s in subs)
        (d / "README.md").write_text(f"""# Chapter {ch} — {name}

{intro_of(ch)}

## Subtopics

{sub_lines}

## Files in this chapter

| File | What it contains |
| --- | --- |
| [draft.md](draft.md) | The complete V2.0 chapter: learning goals, key terms, explanations, worked examples, diagrams, *Pause & Try* activities and Practice questions |
| [solutions.md](solutions.md) | Checked answers and expected outcomes for every *Pause & Try* and Practice question |
| [{lo}]({lo}) | The team's learning outcomes for this chapter (reproduced at the start of draft.md) |
| [{kt}]({kt}) | The team's key-terms glossary |
| [exercises.md](exercises.md) | The team's original exercise set (all of it is included in the Practice section of draft.md) |
| [UseOfAI.md](UseOfAI.md) | How AI was used for this chapter |
| `images/`, `figures/` | Pictures and diagrams used by draft.md |

## Where this chapter is used

| Resource | Use |
| --- | --- |
| Study Guide V2 | Chapter {ch}, pages {chap.get(ch, '–')}–{(chap.get(ch + 1, 205) - 1) if ch < 6 else 204} ([PDF](../../assets/study-guide/v2/BlueImpulse_Study_Guide_V2.pdf)) |
| Test Bank V1 | {tb} ([Word](../../assets/study-guide/BlueImpulse_Stage2_TestBank_V1.docx)) |
| PPT (Sojourner presentation) | {PPT[ch]} |
| Video tutorial | {vid} |
""")
        rows.append((ch, name, subs, chap.get(ch)))
    return rows


if __name__ == "__main__":
    main()
    write_readmes()
