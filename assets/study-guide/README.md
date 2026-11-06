# Blue Impulse study guide

[Study guide PDF](BlueImpulse_Study_Guide.pdf) · [All-page overview](BlueImpulse_Study_Guide_Overview.jpg)

The 96-page guide covers the six supplied chapters. It includes learning goals, explanations, worked examples, diagrams, key terms and the team's GitHub exercises. The PDF has selectable text, chapter and topic bookmarks, linked contents, and links to the exercise files. Page numbers match the PDF viewer, including the cover and dividers.

| Chapter | Theme | PDF pages |
| --- | --- | --- |
| 1. The Fundamentals | Dawn | 5–21 |
| 2. Behaviorism and Behaviorist AI | Morning | 22–33 |
| 3. Hardware | Midday | 34–50 |
| 4. Networking | Afternoon | 51–70 |
| 5. Applications | Dusk | 71–83 |
| 6. Strengths and Limitations | Midnight | 84–95 |

The original cover and all six chapter dividers are preserved as PDF pages, without overlays or edits. The supplied art's printed chapter labels put the cover on page 16 and the dividers on pages 17–22; these labels resolve the shifted page references in the written prompt. All other pages end with an exercise. No exercise answer key is included.

The page boxes, folder panels, diagram shapes, aircraft and photographs were extracted from `study guide art.pdf`. Background photographs are composited at 30% opacity; Chapter 5's photograph is tinted purple. The secondary template informs the layouts. Fonts follow the written brief: Anta titles, DIN Condensed headings, Smiley Sans subheadings and Avenir text. Body prose is 11.2 pt. Diagram labels, table cells, references and navigation use smaller type where appropriate.

## Content and source notes

The six supplied chapter PDFs define the content scope. Learning outcomes, key terms and questions were checked against repository revision `9a645d0`. This is an edited study guide, not a facsimile of those source PDFs. Technical clarifications address fixed rules versus reinforcement learning, exploitation and future return, CPU timing, SSD latency, current Ethernet and TLS usage, signatures, real-time deadlines, and the limits of edge computing. Unsupported performance percentages were not carried over. Exercise wording and numbering are lightly normalised, including the circuit-switching premise and the distinction between signing and encryption.

The source notes credit *Cambridge International AS & A Level Computer Science* and disclose the team's use of Gemini, Claude and ChatGPT; the supplied materials do not identify a complete textbook edition or bibliography. Neogpt assisted with editing, diagrams, layout and production of this guide. User-supplied art is retained for this project; this repository does not assert a new licence over third-party artwork.

## Rebuild

Keep the original inputs in the ignored root folder `temp contents/`. On macOS with Avenir and DIN Condensed installed:

```sh
python3 -m venv /private/tmp/blue-impulse-study-env
/private/tmp/blue-impulse-study-env/bin/python -m pip install -r assets/study-guide/source/requirements.txt
/private/tmp/blue-impulse-study-env/bin/python assets/study-guide/source/prepare_assets.py
/private/tmp/blue-impulse-study-env/bin/python assets/study-guide/source/build_guide.py
/private/tmp/blue-impulse-study-env/bin/python assets/study-guide/source/verify_guide.py
```

Anta and Smiley Sans font files and their licences are included. The macOS Avenir and DIN font files are not redistributed; the PDF embeds subsets for viewing and printing. The extracted artwork allows rebuilding the layout without re-extracting assets, while the original art PDF is needed for the unchanged-page verification.

`manifest.json` fixes the topic page numbers and PDF checksum. `source/page-map.json` contains the page content, `source/exercise-map.json` maps questions to their locations, and `source/verification.json` records the completed checks. Those page numbers are the reference for the companion tutorials.
