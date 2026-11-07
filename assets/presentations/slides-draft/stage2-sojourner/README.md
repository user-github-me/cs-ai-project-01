# Blue Impulse — Sojourner / Stage 2

> **Historical visual draft.** The 37-slide Sojourner design and its original scope are preserved here. The [current Stage 2 teaching deck](../../stage2-teaching/README.md) contains 63 editable slides, complete presenter notes, six-chapter teaching content, and classroom activities.

A 37-slide, widescreen visual draft built from the team's [Stage 2 outline](../stage2-slide-outline.md) and the four supplied style references. It uses a retro Mars palette, photographic rover cutouts, flowing ink textures, large titles, and a symbolic rocket journey.

- [Editable PowerPoint](../BlueImpulse_Stage2_Sojourner.pptx)
- [PDF preview](../BlueImpulse_Stage2_Sojourner.pdf)
- [All-slide overview](../BlueImpulse_Stage2_Overview.jpg)

This is the **visual structure only**, as requested in the outline. Detailed explanations, Safa and Nazif's claims, the rover video, and the game remain empty. Empty text boxes are named in PowerPoint's Selection Pane, and speaker notes describe what each slide is intended to hold.

## Design

The title font is Horizon, recovered from the team's existing Stage 1 presentation and packaged as **Horizon Presentation** for compatibility. Its letter shapes are unchanged. Body text is Quicksand Medium. Both fonts are embedded in the PowerPoint, and every visible text run is at least **28 pt**. Main titles range from approximately 50 to 150 pt, with larger decorative chapter numerals.

| Colour | Hex |
| --- | --- |
| Deep aubergine | `#180818` |
| Plum | `#632644` |
| Dusty magenta | `#B34566` |
| Coral | `#C76160` |
| Burnt orange | `#E94E00` |
| Amber | `#FBB32A` |
| Warm cream | `#F9DEB5` |

The deck uses 24 native PowerPoint Morph transitions, with a Fade fallback for applications that do not support Morph. Open the `.pptx` in desktop PowerPoint and advance through the slides to play the rocket and signal-path movements. The PDF is a static preview. The PowerPoint can be imported into Canva, but native PowerPoint Morph transitions do not transfer as equivalent Canva animations.

The PDF and overview were checked from an actual 37-slide Keynote export. Keynote needs the fonts installed locally; the requested fonts have been installed on Nazif's Mac. On another Mac, run the preparation script to recover `/private/tmp/blue-impulse-stage2/Horizon.ttf`, then install that file and `fonts/Quicksand-Medium.ttf` with Font Book before editing in Keynote. The PDF displays the intended typography without font installation.

## Slide map

| Slides | Section |
| --- | --- |
| 1–5 | Blue Impulse, Sojourner introduction, Earth-to-Mars journey |
| 6–14 | Hardware: body, information collection, lander, instruments, cameras, APXS, wheels, antenna and UHF |
| 15–25 | Networks: path, outbound/inbound sequences, UHF, half-duplex, heartbeat, limits and decisions |
| 26–32 | Behaviorist AI: question, Safa vs Nazif, stimulus/response, video placeholder and rover comparison |
| 33–37 | Integration, blank game, return journey and thank you |

The returning rocket is a storytelling device, not a claim about the Pathfinder mission: Sojourner remained on Mars. The behaviorist-AI discussion is framed as a question; no reinforcement-learning claim has been added.

## Artwork and credits

NASA images retain their source identities in the files and notes. The small surface-camera images are archival material; their original resolution is limited.

| Asset | Source |
| --- | --- |
| Sojourner surface photograph and traced rover cutout | [NASA/JPL — PIA01122](https://images.nasa.gov/details/PIA01122) |
| Rover rear / APXS view | [NASA/JPL — PIA00614](https://images.nasa.gov/details/PIA00614) |
| Pathfinder lander view | [NASA/JPL — PIA01121](https://images.nasa.gov/details/PIA01121) |
| Additional APXS reference | [NASA/JPL — PIA00966](https://images.nasa.gov/details/PIA00966) |
| Additional wheel-track reference | [NASA/JPL — PIA01137](https://images.nasa.gov/details/PIA01137) |
| Mars globe | [NASA/JPL/USGS — PIA00407](https://images.nasa.gov/details/PIA00407) |
| Earth / Blue Marble | [NASA — Apollo 17, AS17-148-22727](https://images.nasa.gov/details/as17-148-22727) |
| Curiosity and Perseverance engineering models | [NASA/JPL-Caltech — PIA24525](https://images.nasa.gov/details/PIA24525) |
| Quicksand font | [SIL Open Font License](fonts/Quicksand-OFL.txt) |

The rocket, starfield, liquid-ink texture, and terrain composition are original graphics created for this draft. The rover is a manually traced cutout of the NASA photograph, not a generated replacement rover. The colour palette and composition were guided by the supplied references; their collage photographs were not copied into the deck.

Image generation was attempted through `neoimg`, but all requests returned an Azure authorization error and produced no images. The attempted [art prompts](source/art-prompts.json) are retained for future use. The finished artwork comes from the sources and original graphics listed above.

## Editable source

- [prepare_art.py](source/prepare_art.py): deterministic textures, the rocket SVG, NASA image treatments and font preparation.
- [build_deck.cjs](source/build_deck.cjs): editable slide layout, empty content boxes, speaker notes and design previews.
- [finish_deck.py](source/finish_deck.py): font embedding, Morph transitions, media deduplication and package validation.
- [slides.json](source/slides.json): slide-by-slide topic, notes and transition map.
- [render_keynote.swift](source/render_keynote.swift): optional macOS Keynote PDF export and native render review.

To rebuild from the repository root, install Python's `Pillow`, `numpy` and `fonttools`, plus Node dependencies in a temporary directory:

```sh
npm install --prefix /private/tmp/blue-impulse-stage2-tools pptxgenjs@4.0.1 sharp @resvg/resvg-js fontkit
python3 assets/presentations/slides-draft/stage2-sojourner/source/prepare_art.py
node assets/presentations/slides-draft/stage2-sojourner/source/build_deck.cjs
python3 assets/presentations/slides-draft/stage2-sojourner/source/finish_deck.py
```

Horizon is recovered from the existing `final-presentation/BlueImpulse_Stage1_StatusReport_compressed.pptx`; its raw font file is not distributed separately here. The generator leaves intermediate files in `/private/tmp/blue-impulse-stage2/` and writes the finished deck beside this folder.
