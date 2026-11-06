# Blue Impulse video tutorials

Five lessons taught directly from the 96-page Blue Impulse study guide. Each MP4 includes English narration, burned-in subtitles, book screenshots, page citations, demonstrations, thinking pauses, and the original book-cover credit.

| Video | Topic | Duration | Guide pages |
|---|---|---|---|
| 01 | Basic reinforcement learning | 08:35 | 24, 25, 26, 27, 28, 31 |
| 02 | How hardware enables AI | 09:04 | 35, 36, 39, 44, 46, 86 |
| 03 | Network challenges | 09:14 | 56, 59, 61, 62, 63, 74, 88 |
| 04 | Networking for behaviorist AI | 09:38 | 24, 25, 72, 74, 75, 77, 78, 89 |
| 05 | Program execution | 09:32 | 12, 13, 14, 15, 39 |

## Inside the ZIP

- `Videos/`: the five 1920 × 1080, 30 fps H.264/AAC MP4 tutorials.
- `Tutorial_PDFs/`: one written tutorial per video, plus the combined 65-page edition.
- `Study_Guide/`: the finished 96-page study guide used on screen.
- `Scripts/`: complete timed narration and teaching outlines.
- `Subtitles/`: editable SRT and WebVTT captions; the MP4s also have visible subtitles.
- `Supporting_Files/`: runnable Python demonstrations, expected results, and instructions.
- `Editable_Project/`: the HyperFrames scenes, illustrations, book excerpts, fonts, audio, and build scripts.
- `Verification/`: file hashes, technical checks, and representative frames.

Start with a video and keep the study guide open. The PDF viewer page number is the cited book page. Use the written tutorial to review a step or find its timestamp. Run `python3 Supporting_Files/BlueImpulse_Demonstrations.py --topic all` to reproduce all five demonstrations without installing extra packages.

Narration uses the local Kokoro English voice `am_michael`; it is synthesized speech. The quiet musical bed and entry tones were generated for these lessons. The original study-guide cover, chapter colors, and excerpts retain their source appearance. Third-party social-video references are credited as inspiration and are not included.

Guide SHA-256: `2af7695b50de6d32cdc3254b1a702b1ec09701c90677bc758d956f9476b7d3e4`.
