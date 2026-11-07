"""Build printable, complete narration-and-teaching-outline PDFs from Markdown.

Usage: python source/build_script_pdfs.py [--output PATH]
Requires ReportLab, fontTools with WOFF2/Brotli support, and PyMuPDF.
The Markdown files remain the source of truth; no narration is regenerated.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import tempfile
import unicodedata
from pathlib import Path

import fitz
from fontTools.ttLib import TTFont as FontToolsFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 44
TEXT_WIDTH = PAGE_WIDTH - MARGIN * 2
NAVY = colors.HexColor("#212C4A")
PINK = colors.HexColor("#E15B83")
PALE = colors.HexColor("#FCF3F6")
GRAY = colors.HexColor("#586172")
RULE = colors.HexColor("#D9DEE7")


def inline_markdown(text: str) -> str:
    """Retain source characters while translating the two used inline markers."""
    result = html.escape(text)
    result = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", result)
    result = re.sub(r"`([^`]+)`", r"<font name='ScriptInter'>\1</font>", result)
    # The bundled Inter files are Latin subsets. Preserve, rather than spell out,
    # mathematical Greek and arrows using the study guide's existing font.
    result = re.sub(r"[αγ→]", r"<font name='ScriptSymbols'>\g<0></font>", result)
    return result


def plain_markdown(text: str) -> str:
    return text.replace("**", "").replace("`", "")


def normalized(text: str) -> str:
    return re.sub(r"[^\w]+", " ", unicodedata.normalize("NFKC", text).lower()).strip()


def register_fonts(cache: Path) -> None:
    for name, filename in (
        ("ScriptInter", "Inter-400.woff2"),
        ("ScriptInterBold", "Inter-700.woff2"),
    ):
        font = FontToolsFont(ROOT / "assets/fonts" / filename)
        font.flavor = None
        target = cache / f"{name}.ttf"
        font.save(target)
        pdfmetrics.registerFont(TTFont(name, str(target)))
    pdfmetrics.registerFontFamily(
        "ScriptInter",
        normal="ScriptInter",
        bold="ScriptInterBold",
        italic="ScriptInter",
        boldItalic="ScriptInterBold",
    )
    pdfmetrics.registerFont(
        TTFont("ScriptAnta", str(ROOT / "assets/fonts/Anta-Regular.ttf"))
    )
    pdfmetrics.registerFont(TTFont(
        "ScriptSymbols", str(ROOT.parents[1] / "assets/study-guide/fonts/SmileySans-Oblique.ttf")
    ))
    pdfmetrics.registerFontFamily(
        "ScriptSymbols", normal="ScriptSymbols", bold="ScriptSymbols",
        italic="ScriptSymbols", boldItalic="ScriptSymbols",
    )


def styles() -> dict[str, ParagraphStyle]:
    base = dict(fontName="ScriptInter", textColor=NAVY, alignment=TA_LEFT)
    return {
        "title": ParagraphStyle(
            "title", **{**base, "fontName": "ScriptAnta"},
            fontSize=26, leading=31, spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "subtitle", **{**base, "fontName": "ScriptInterBold"},
            fontSize=12, leading=17, spaceAfter=10,
        ),
        "heading": ParagraphStyle(
            "heading", **{**base, "fontName": "ScriptAnta"},
            fontSize=18, leading=22, spaceBefore=11, spaceAfter=9,
            keepWithNext=True,
        ),
        "section": ParagraphStyle(
            "section", **{**base, "fontName": "ScriptAnta"},
            fontSize=16, leading=20, spaceAfter=7, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "body", **base, fontSize=10.2, leading=14.6, spaceAfter=6,
        ),
        "meta": ParagraphStyle(
            "meta", **{**base, "textColor": GRAY},
            fontSize=9.3, leading=13.5, spaceAfter=9,
        ),
        "pause": ParagraphStyle(
            "pause", **base, fontSize=10.1, leading=14.4, spaceAfter=8,
            spaceBefore=2, borderColor=PINK, borderWidth=1,
            borderPadding=7, backColor=PALE,
        ),
        "cell": ParagraphStyle(
            "cell", **base, fontSize=8.8, leading=12.2,
        ),
        "tablehead": ParagraphStyle(
            "tablehead", **{**base, "fontName": "ScriptInterBold", "textColor": colors.white},
            fontSize=8.6, leading=12,
        ),
    }


class ScriptDocument(BaseDocTemplate):
    def __init__(self, filename: Path, lesson: dict):
        super().__init__(
            str(filename), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
            topMargin=69, bottomMargin=53,
            title=f"Blue Impulse Video {lesson['number']:02d}: {lesson['title']} — Script and Teaching Outline",
            author="Blue Impulse",
            subject="Complete timed narration and teaching outline for the study-guide tutorial",
            pageCompression=1,
        )
        self.lesson = lesson
        self.bookmark_number = 0
        frame = Frame(
            MARGIN, 53, TEXT_WIDTH, PAGE_HEIGHT - 122,
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
            id="content",
        )
        self.addPageTemplates(PageTemplate(id="print", frames=frame, onPage=self.page_art))

    def page_art(self, canvas, document):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.setFont("ScriptInterBold", 9)
        canvas.drawString(MARGIN, PAGE_HEIGHT - 34, f"BLUE IMPULSE  /  VIDEO {self.lesson['number']:02d}")
        canvas.setStrokeColor(PINK)
        canvas.setLineWidth(2)
        canvas.line(MARGIN, PAGE_HEIGHT - 44, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 44)
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.6)
        canvas.line(MARGIN, 40, PAGE_WIDTH - MARGIN, 40)
        canvas.setFont("ScriptInter", 8)
        canvas.setFillColor(GRAY)
        canvas.drawString(MARGIN, 25, "Script and teaching outline · Blue Impulse study guide")
        canvas.drawRightString(PAGE_WIDTH - MARGIN, 25, f"Page {document.page}")
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in {"heading", "section"}:
            self.bookmark_number += 1
            key = f"section-{self.bookmark_number}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.getPlainText(), key, 0, closed=False)


def source_parts(narration: str, outline: str):
    sections = re.split(r"(?m)^## (\d{2}:\d{2}–\d{2}:\d{2} · .+)\n", narration)
    if len(sections) != 25:
        raise ValueError("Expected exactly twelve timed narration sections")
    preamble = sections[0].strip()
    timed_sections = [(sections[i], sections[i + 1].strip()) for i in range(1, len(sections), 2)]
    outline_lines = outline.splitlines()
    table_lines = [line for line in outline_lines if line.startswith("|")]
    rows = [[cell.strip() for cell in line.strip("|").split("|")] for line in table_lines]
    if len(rows) != 14 or any(len(row) != 4 for row in rows):
        raise ValueError("Expected a four-column, twelve-step teaching outline")
    first_table = next(i for i, line in enumerate(outline_lines) if line.startswith("|"))
    last_table = max(i for i, line in enumerate(outline_lines) if line.startswith("|"))
    intro = "\n".join(outline_lines[1:first_table]).strip()
    outro = "\n".join(outline_lines[last_table + 1:]).strip()
    return preamble, timed_sections, rows[0], rows[2:], intro, outro


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(inline_markdown(text), style)


def build_pdf(lesson: dict, narration_path: Path, outline_path: Path, destination: Path) -> dict:
    narration = narration_path.read_text(encoding="utf-8")
    outline = outline_path.read_text(encoding="utf-8")
    preamble, sections, headers, rows, intro, outro = source_parts(narration, outline)
    st = styles()
    story = []

    # Preserve the title, source duration and video filename, and all objectives.
    for block in re.split(r"\n\s*\n", preamble):
        if block.startswith("# "):
            story.append(paragraph(block[2:], st["title"]))
            story.append(paragraph("Complete script and teaching outline", st["subtitle"]))
        elif block.startswith("## "):
            story.append(paragraph(block[3:], st["heading"]))
        elif block.startswith("- "):
            for index, item in enumerate(block.splitlines(), 1):
                story.append(paragraph(f"{index}. {item[2:]}", st["body"]))
        else:
            story.append(paragraph(block, st["meta"]))

    story.append(paragraph("Guide pages: " + ", ".join(map(str, lesson["pages"])) + ".", st["meta"]))
    story.append(paragraph(outline.splitlines()[0].removeprefix("# "), st["heading"]))
    story.append(paragraph(intro, st["body"]))
    story.append(Spacer(1, 5))
    cells = [[paragraph(cell, st["tablehead"]) for cell in headers]]
    cells.extend([[paragraph(cell, st["cell"]) for cell in row] for row in rows])
    table = Table(cells, colWidths=[43, 155, 44, TEXT_WIDTH - 242], repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, RULE),
    ]))
    story.append(table)
    story.append(Spacer(1, 9))
    story.append(paragraph(outro, st["body"]))
    story.append(Spacer(1, 12))
    narration_lead = [paragraph("Complete narration", st["heading"]), paragraph(
        "Read the narration verbatim. Bracketed pauses and on-screen prompts are teaching directions; "
        "keep the answer hidden until the indicated pause has finished. Timestamps match the source script.",
        st["meta"],
    )]

    # Keep each section on one page so its cue, explanation and pause remain together.
    for section_index, (heading, body) in enumerate(sections):
        content = narration_lead.copy() if section_index == 0 else []
        content.append(paragraph(heading, st["section"]))
        for index, block in enumerate(re.split(r"\n\s*\n", body)):
            style = st["meta"] if index == 0 and block.startswith("Study guide page") else st["body"]
            if block.startswith("**[Pause"):
                style = st["pause"]
            content.append(paragraph(block, style))
        content.append(Spacer(1, 12))
        story.append(KeepTogether(content))
    ScriptDocument(destination, lesson).build(story)

    # Verify every source paragraph/cell independently, including non-spoken directions.
    required = []
    for source in (narration, outline):
        for block in re.split(r"\n\s*\n", source.strip()):
            if block.startswith("|"):
                for line in block.splitlines():
                    if re.fullmatch(r"[|\-: ]+", line):
                        continue
                    required.extend(cell.strip() for cell in line.strip("|").split("|"))
            elif block.startswith("- "):
                required.extend(line[2:] for line in block.splitlines())
            else:
                required.append(re.sub(r"^#{1,2} ", "", block))
    with fitz.open(destination) as pdf:
        text = normalized("\n".join(page.get_text() for page in pdf))
        missing = [part for part in required if normalized(plain_markdown(part)) not in text]
        if missing:
            raise AssertionError(f"Missing source text in {destination.name}: {missing}")
        out_of_bounds = []
        for page_number, page in enumerate(pdf, 1):
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        x0, y0, x1, y1 = span["bbox"]
                        if x0 < MARGIN - 2 or x1 > PAGE_WIDTH - MARGIN + 2 or y0 < 16 or y1 > PAGE_HEIGHT - 16:
                            out_of_bounds.append((page_number, span["text"], span["bbox"]))
        if out_of_bounds:
            raise AssertionError(f"Out-of-bounds text in {destination.name}: {out_of_bounds}")
        return {
            "file": str(destination), "pages": len(pdf),
            "source_text_items_verified": len(required), "sections": len(sections),
            "teaching_steps": len(rows), "missing_text": 0, "out_of_bounds": 0,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT.parents[1] / "assets/tutorials/scripts")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    reports = []
    with tempfile.TemporaryDirectory(prefix="blue-impulse-script-fonts-") as temporary:
        register_fonts(Path(temporary))
        for lesson_path in sorted(ROOT.glob("lesson-??.json")):
            lesson = json.loads(lesson_path.read_text(encoding="utf-8"))
            stem = f"BlueImpulse_Video{lesson['number']:02d}_{lesson['slug']}"
            reports.append(build_pdf(
                lesson,
                ROOT / "scripts" / f"{stem}_Narration.md",
                ROOT / "scripts" / f"{stem}_Teaching_Outline.md",
                output / f"{stem}_Script_and_Teaching_Outline.pdf",
            ))
    print(json.dumps(reports, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
