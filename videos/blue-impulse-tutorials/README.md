# Blue Impulse book tutorials

Five narrated tutorials accompany the six-chapter study guide. See [the package index](DELIVERY_README.md) for topics, durations, and contents, and [the timed narration](SCRIPT.md) for every spoken section.

The films use the original book's midnight background `#212C4A`, pink accent `#E15B83`, and neutral text `#E6E4E5`. Screenshots retain the book's own colors. Each moving teaching object anticipates its main movement for three frames at 30 fps. Captions remain still and follow measured speech.

## Preview or render

The audio, fonts, screenshots, and generated HTML are included. Rendering existing lessons does not require the speech model or original temporary source files.

Install Node.js, FFmpeg, Python 3.9+, and HyperFrames 0.9.4. In this directory:

```sh
python3 source/select_lesson.py 1
hyperframes preview
```

Choose a lesson number from 1 through 5. Only `index.html` is a root composition; templates for the other lessons are under `entries/`. Select lessons sequentially and wait for a render or check to finish before selecting another.

```sh
hyperframes check --json
HF_STATIC_DEDUP=false hyperframes render --fps 30 --workers 4 --gpu --no-browser-gpu --output renders/tutorial.mp4
```

The reference render uses screenshot capture and H.264/AAC output. Static-frame deduplication is disabled because this CLI version incorrectly classified a changing question countdown as static. This preserves every rendered frame. Hardware encoding can be omitted on machines that do not support it.

For all five films, `source/render_lessons.py` renders and decodes every frame. `source/optimize_delivery.py` then makes smaller H.264 CRF 18 copies, verifies image similarity, and checks that decoded audio is unchanged. `source/review_final_media.py` checks actual caption frames and creates overview images. In the repository, `source/package_delivery.py` assembles the verified ZIP and copies the final MP4s into `assets/tutorials/videos/`.

## Edit or rebuild

- Change narration and lesson content in `source/lesson_content.py`.
- Change common layouts in `source/build_video.py`; change the five demonstrations in `compositions/frames/`.
- `lesson-01.json` through `lesson-05.json` contain the delivered narration's measured timing. They are the timing source for scenes and subtitles.
- `python3 source/build_video.py` regenerates the HTML from the measured lesson data.
- `python3 source/build_delivery_docs.py` regenerates timed scripts and outlines.
- `python3 source/check_lessons.py` checks and captures all five lessons sequentially.

To change the spoken audio, use Python 3.12 with `kokoro-onnx==0.6.1`, `soundfile`, NumPy, and FFmpeg. Download `kokoro-v1.0.onnx` and `voices-v1.0.bin` from the public [Kokoro ONNX model release](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0). Run:

```sh
python3 source/build_audio.py --models /path/to/downloaded-models
python3 source/build_video.py
python3 source/build_delivery_docs.py
```

Rebuild and recheck the films after changing narration; new speech changes timings. The delivered M4A stems and mix files can be used directly without regenerating speech. WAV cue caches and speech-model binaries are excluded from the package.

The tutorial PDFs are built with `source/build_tutorial_pdfs.py` using ReportLab, PyMuPDF, FontTools, Brotli, and Pillow. In the repository they are saved in `assets/tutorials/`. The main study guide's source and original artwork references are in `assets/study-guide/`; input files under `temp contents/` remain ignored by Git.

The PDF builder accepts `--output /path/to/folder`; outside the repository its default is `generated-tutorials/` inside this project. Book references and measured narration must be checked again after changing the teaching content.

## Sources and teaching limits

All book excerpts are exact raster crops of the finished study guide. `assets/book/provenance.json` records their origin and frozen PDF hash. File paths are relative to this project. The original cover and full guide retain the attribution in the book.

The rover example is a simulation. The pipeline assumes four one-cycle stages without stalls. Delay distances exclude braking. The networking example consumes an externally supplied authentication result and does not implement cryptography. The CPU uses an invented teaching instruction set. These limits are stated in the lessons and supporting material.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for fonts, audio tools, animation software, and style references.
