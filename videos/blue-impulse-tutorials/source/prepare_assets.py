"""Create exact page images and excerpt crops from the finished, frozen study guide."""
from pathlib import Path
import hashlib
import json
import shutil
import fitz

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parents[1]
GUIDE = REPO / "assets/study-guide"
EXPECTED_SHA = "2af7695b50de6d32cdc3254b1a702b1ec09701c90677bc758d956f9476b7d3e4"
PAGES = [1,12,13,14,15,24,25,26,27,28,31,35,36,39,44,46,56,59,61,62,63,65,72,74,75,77,78,86,88,89]

def main():
    pdf = GUIDE / "BlueImpulse_Study_Guide.pdf"
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == EXPECTED_SHA, "Book changed: review every citation before rebuilding."
    target = PROJECT / "assets/book"
    target.mkdir(parents=True, exist_ok=True)
    fonts = PROJECT / "assets/fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    for name in ["Anta-Regular.ttf", "Anta-OFL.txt"]:
        shutil.copy2(GUIDE / "fonts" / name, fonts / name)
    doc = fitz.open(pdf)
    layouts = json.loads((GUIDE / "source/layout-audit.json").read_text())
    result = {"source": "BlueImpulse_Study_Guide.pdf", "sha256": EXPECTED_SHA, "pages": {}}
    for p in PAGES:
        page = doc[p-1]
        dest = target / f"page-{p:03}.jpg"
        page.get_pixmap(matrix=fitz.Matrix(1.7,1.7),alpha=False).pil_save(str(dest),format="JPEG",quality=94)
        record = {"full": f"assets/book/{dest.name}", "excerpts": []}
        for n, box in enumerate(b for b in layouts if b["page"] == p and b["role"] == "content"):
            rect = fitz.Rect(box["x"], page.rect.height-box["y_top"], box["x"]+box["width"], page.rect.height-box["y_top"]+box["height"])
            out = target / f"page-{p:03}-block-{n}.png"
            page.get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=rect,alpha=False).save(out)
            record["excerpts"].append({"title":box["title"],"path":f"assets/book/{out.name}","rect":list(rect)})
        result["pages"][str(p)] = record
    shutil.copy2(GUIDE / "art/book-cover.png", target / "cover.png")
    (target / "provenance.json").write_text(json.dumps(result,indent=2)+"\n")
    (PROJECT / "capture/extracted").mkdir(parents=True, exist_ok=True)
    shutil.copy2(GUIDE / "source/page-map.json", PROJECT / "capture/extracted/guide-page-map.json")
    tokens = dict(title="Blue Impulse book tutorials",description="Five lessons taught from the finished study guide",colors=["#212C4A","#E15B83","#E6E4E5"],fonts=["Anta","Inter"])
    (PROJECT / "capture/extracted/tokens.json").write_text(json.dumps(tokens,indent=2)+"\n")
    print(f"Created exact page images and excerpt crops for {len(PAGES)} guide pages.")

if __name__ == "__main__":
    main()
