# Blue Impulse — Stage 2 PPT V1.0

This is the complete six-chapter classroom teaching deck for **Hardware, Networking and Behaviorist AI**. The earlier Sojourner presentation is preserved in its existing directory as a separate artifact.

- `BlueImpulse_Stage2_PPT_V1.pptx`: 63 editable slides with native presenter notes and embedded Inter fonts.
- `BlueImpulse_Stage2_PPT_V1.pdf`: supplementary slide copy exported from the actual PPTX through Keynote.
- `BlueImpulse_Stage2_PPT_V1_Presenter_Notes.pdf`: slide images and the complete teaching notes, activities and expected answers.
- `BlueImpulse_Stage2_PPT_V1_Readiness_Report.pdf`: rubric-aligned review evidence, limitations and remaining human checks.
- `Teaching_Content.md`: complete medium-specific Markdown foundation for the deck.
- `supporting/`: offline demonstrations, default outputs, chapter/subtopic resource map, references and significant AI-use evidence.
- `source/`, `fonts/`, `review/`: reproducible builders, licensed fonts, automated checks and rendered review evidence.

The submission package is `submissions/stage2/slides/BlueImpulse_Stage2_PPT_V1.zip` at the repository root. It includes the actual editable deck, supplementary PDFs and all necessary supporting files. External reference links are supplementary.

## Teach the sequence

1. **Session A — Information becomes action**, slides 1–25: representation, execution, operating systems, reactive behavior and reinforcement learning.
2. **Session B — Hardware and communication**, slides 26–45: memory, pipelines, interfaces, networks, delay, security and meaning.
3. **Session C — Integrate and evaluate**, slides 46–63: real-time applications, message validation, human oversight and edge/cloud tradeoffs.

The notes allocate approximately 78.5 minutes in total, including 15 brief audience tasks. These are planning estimates, not measured rehearsal results. Adjust session length after a teammate rehearses a representative section. Activities use a show of hands, a neighbor discussion or paper; no audience device or internet account is needed.

The opening follows **Pip**, a fictional campus delivery rover. The final design challenge resolves the same problem by connecting all six chapters. The technical packet ID remains `robot-7` to match the checked demonstrations.

## Verification and remaining human checks

The report records numerical verification, package inspection, native application export, font/notes checks and visual review of all 63 rendered slides. A teammate rehearsal, content discussion and actual classroom projector test **remain pending**. Automated checks must not be recorded as those human activities.

## Rebuild

Python 3.9+, ReportLab, PyMuPDF, Pillow and fontTools are used for review and supplementary documents. Node.js uses `pptxgenjs` 4.0.1 and `fontkit`; configure `BLUE_IMPULSE_TOOLS` to a directory whose `package.json` resolves those dependencies.

Install dependencies with `npm install --prefix source` and `python3 -m pip install -r source/requirements.txt` in a suitable Python environment. Then run:

```sh
python3 source/teaching_content.py
node source/build_deck.cjs
python3 source/embed_fonts.py
python3 source/export_keynote.py
python3 source/verify_and_document.py
python3 source/package_submission.py
```

The native PDF export requires macOS and Keynote. It opens the PPTX, exports a PDF and closes without saving changes to the editable deck. Inter’s permitted regular/bold font files are included and installed for that export if missing.
