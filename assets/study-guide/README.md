# Blue Impulse study guide and Test Bank — Stage 2 V1.0

[Complete Study Guide PDF](BlueImpulse_Study_Guide.pdf) · [Editable Test Bank](BlueImpulse_Stage2_TestBank_V1.docx) · [Test Bank PDF](BlueImpulse_Stage2_TestBank_V1.pdf)

The complete guide has 121 pages: the original 96-page teaching sequence followed by six guided missions, resource introductions, and explained answers for all 65 retained exercises. The separate Test Bank contains 24 True/False questions, 24 single-answer multiple-choice questions and six substantial open tasks, with four/four/one per chapter. Questions precede the explanatory answer key. The [Stage 2 submission package](https://github.com/user-github-me/cs-ai-project-01/releases/download/blue-impulse-stage2-2026-11-07/BlueImpulse_Stage2_StudyGuide_TestBank_V1.zip) includes the complete PDF, editable DOCX, optional PDF copy and runnable activity support.

| Chapter | Theme | Core PDF pages |
| --- | --- | --- |
| 1. The Fundamentals | Dawn | 5–21 |
| 2. Behaviorism & Behaviorist AI | Morning | 22–33 |
| 3. Hardware | Midday | 34–50 |
| 4. Networking | Afternoon | 51–70 |
| 5. Applications | Dusk | 71–83 |
| 6. Strengths & Limitations | Midnight | 84–95 |

The active learning and feedback section begins on page 97. Bookmarks navigate every original topic and the new missions, resources and answers. All six missions provide a goal, preparation, steps, observations, reflection and feedback. Paper alternatives contain every required input and expected result; optional Python uses only the standard library. A fictional campus delivery rover, Pip, connects the examples. Its device identifier is `robot-7` in the packet demonstration.

The original cover and all six chapter dividers are preserved as PDF pages without overlays. The original art's printed labels identify its cover on page 16 and dividers on pages 17–22. Existing window panels, diagrams and photographs retain the supplied artwork and font brief. The user-created `BlueImpulse_Study_Guide_compressed.pdf` has not been modified by this revision.

## Source, review and remaining human evidence

[Complete Markdown V2](../../content/README.md) contains all 67 developed topics, 67 application checkpoints with feedback, six missions, 65 exercises and answers, glossaries and full resource introductions. [Review status](../../content/REVIEW.md) distinguishes completed automated/AI-assisted checks from the mandatory independent teammate attempts that are still pending. No human test, feedback, contribution or reflection has been invented.

The six supplied chapter PDFs define scope. Their notes credit *Cambridge International AS & A Level Computer Science* but do not identify a full edition or bibliography; this provenance limitation is explicit. Six traceable references and optional learning resources support the revision, including Sutton and Barto, Nand to Tetris, IETF RFCs, NIST and Unicode. Each resource has a relevant section, a task, limitations and an offline alternative. User-supplied artwork retains its own third-party rights.

The 7 November revision was assisted by Neogpt/Codex. Its important changes and actual checks are documented in the Markdown submission report and the project and personal logs. The previous guide was developed before this complete Markdown reconstruction; the report records that workflow repair honestly.

## Rebuild and verify

On macOS, with Avenir, Arial Unicode and DIN Condensed installed:

```sh
/private/tmp/blue-impulse-study-env/bin/python -m pip install -r assets/study-guide/source/requirements.txt
/private/tmp/blue-impulse-study-env/bin/python assets/study-guide/source/build_guide.py
/private/tmp/blue-impulse-study-env/bin/python assets/study-guide/source/build_stage2.py
/private/tmp/blue-impulse-study-env/bin/python assets/study-guide/source/verify_guide.py
/private/tmp/blue-impulse-study-env/bin/python assets/study-guide/source/verify_stage2.py
```

`build_guide.py` creates the original-art 96-page base. `build_stage2.py` builds the complete edition, Markdown snapshot/report, editable Test Bank and both submission ZIPs. It is safe to rerun: it retains the first 96 guide pages and replaces the generated appendix. The art extraction step in `prepare_assets.py` is only needed when rebuilding extracted artwork from the ignored original `temp contents/` files.

`manifest.json` records the complete PDF hash and stable original topic pages; `source/page-map.json` and `layout-audit.json` describe the original core pages. `source/verification.json` checks the complete guide, including the unchanged artwork and 65 answers. `source/stage2-review/` holds PDF, code, resource and package evidence. Revised video references use chapter number, chapter name and subtopic, so they do not depend on pagination.
