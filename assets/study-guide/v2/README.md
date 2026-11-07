# Blue Impulse Study Guide — V2

**[BlueImpulse_Study_Guide_V2.pdf](BlueImpulse_Study_Guide_V2.pdf)** — 209 pages, A4, with bookmarks for every chapter and subtopic.

| Part | Pages |
| --- | --- |
| Cover · Meet the team (supplied, unchanged) | 1–5 |
| About this guide · Contents | 6–8 |
| Ch. 1 The Fundamentals (Dawn) | 9–41 |
| Ch. 2 Behaviorism & Behaviorist AI (Morning) | 42–71 |
| Ch. 3 Hardware (Midday) | 72–106 |
| Ch. 4 Networking (Afternoon) | 107–153 |
| Ch. 5 Applications (Dusk) | 154–176 |
| Ch. 6 Strengths & Limitations (Midnight) | 177–204 |
| Appendix · RoverLab: Build, Connect, Train | 205–209 |

Each chapter: supplied divider → learning goals (verbatim) → key terms → numbered subtopics, every content page ending with a Pause & Try (no solutions printed) → Practice. The design follows the team's art brief: chapter palettes, window boxes / folder boxes / diagram pills recreated with colours sampled from `study guide art.pdf` pages 4–8, page backgrounds from the page-28 photos at ~30% over the chapter colour with page-12 depth shapes and page-11 airliners, DIN Condensed headings, Smiley Sans box headings and Avenir text. The content applies the team's revision notes (`STUDY GUIDE FIX FIX.md`, `Chapter3Improvements.docx`).

## Rebuild

Needs macOS (DIN Condensed and Avenir are system fonts), Python 3.12 with `PyMuPDF Pillow numpy markdown-it-py playwright qrcode`, a Playwright Chromium, and the supplied inputs in `temp contents/ai proj stage2/` (not in Git).

```sh
cd assets/study-guide/v2/source
python prepare_assets.py          # backgrounds, airliners, sparkle, sky photos -> ../art/
python build.py                   # full book -> ../BlueImpulse_Study_Guide_V2.pdf (prints layout problems; must be [])
python build.py --only ch3 --preview   # one chapter, with contact sheets in ../build/preview/
```

Content lives in `source/content/*.sg` (one file per chapter, plus `front.sg` and `appendix.sg`); the markup is documented at the top of `source/build.py`, and `source/WRITING_BRIEF.md` holds the rules every chapter follows. `build/` holds intermediates and is ignored.

Video links point to the tutorial MP4s in `assets/tutorials/stage2/videos/`; Video 02 links to the version 2 film in `assets/tutorials/v2/`. RoverLab screenshots were captured from the game in `apps/roverlab/`.
