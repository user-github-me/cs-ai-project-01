# Final tutorial video verification

Status: **pass**. 5 of 5 delivery files passed the machine checks; 10 encoded proof frames were inspected by AI.

| Video | MB (decimal) | Seconds | Decoded frames | LUFS | True peak (dBTP) | Endpoint SSIM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 01 | 47.43 | 600 | 36,000 | -16.13 | -1.95 | 0.997273 |
| 02 | 48.16 | 600 | 36,000 | -16.12 | -2.04 | 0.997548 |
| 03 | 48.90 | 600 | 36,000 | -16.12 | -1.72 | 0.997499 |
| 04 | 50.06 | 600 | 36,000 | -16.12 | -1.61 | 0.997488 |
| 05 | 45.85 | 600 | 36,000 | -16.12 | -2.03 | 0.997459 |

Each completed file was checked for 1920×1080 resolution, constant 60 fps, 36,000 frames, 600 seconds and a size below 250 MB. A full sequential decode used one decoder/filter thread and treated decoder errors as failures. The H.264 video uses 8-bit YUV 4:2:0; the delivered full-range `yuvj420p` alias and color-range metadata are recorded in the JSON.

The AAC packet payloads and timestamps match the verified source mix exactly. Encoded-mix loudness and true-peak measurements are carried forward only after source-file and packet identity checks. SRT caption text and millisecond timestamps match the measured JSON and the frozen rendered captions; cues remain within their scenes and outside thinking pauses.

Lossy encoding introduces small endpoint pixel differences. SSIM above measures the first and last decoded MP4 frames, before JPEG proof conversion. It is a loop-seam measurement, not a whole-film perceptual-quality score. Four compact JPEG proofs are retained per video: first, last, one worked demonstration and one two-line caption. Only the latter two are visually inspected.

This is AI-assisted verification. It does not claim a human full viewing, listening test, peer-feedback session or rehearsal. Machine decoding and selected stills cannot establish full-motion pacing or educational effectiveness. The voice is disclosed synthetic Kokoro narration.

Detailed checks, hashes, exact proof-frame times and visual observations: [final-video-checks.json](final-video-checks.json). Compact proofs: [encoded/](encoded/).
