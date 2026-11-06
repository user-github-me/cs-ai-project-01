# Delivery verification

All five final videos are 1920 × 1080 H.264/AAC MP4s at 30 fps, with burned-in English subtitles. Each is between five and ten minutes.

| Video | Duration | Size | Decoded frames | Sampled SSIM |
|---|---|---|---|---|
| 01 | 8:36 | 35.6 MiB | 15,470 | 0.999032 |
| 02 | 9:05 | 36.4 MiB | 16,345 | 0.999076 |
| 03 | 9:14 | 37.6 MiB | 16,622 | 0.999088 |
| 04 | 9:38 | 40.8 MiB | 17,342 | 0.999035 |
| 05 | 9:32 | 36.9 MiB | 17,172 | 0.999155 |

Every frame of every final file decoded without errors. Compression preserved decoded audio exactly. Image similarity was measured once per second against the original renders; the scene overview images were also visually reviewed.

The final MP4s were sampled at the midpoint of all 456 spoken subtitle cues. Every sample contained visible caption text. Twelve samples during thinking pauses and final silent cover holds confirmed that the caption band was clear. SRT files contain the complete narration, in at most two lines per cue. Timing comes from measured synthesized audio chunks, without invented word timestamps.

All 60 teaching scenes were inspected in preflight and in the final scene overview images. Runtime, layout, and sampled contrast checks had no errors. The five demonstration frames were checked against their spoken sequence and supporting Python output. The expected Q values are 3.3 and 1.5; pipeline completion cycles are 4, 5, and 6; delay distances are 15, 1.5, 0.15, and 6 metres; packet results are ACCEPT, STALE, and DUPLICATE / OLD SEQUENCE; the toy program stores 7, and the changed-operand exercise stores 12.

The 96-page guide is frozen at SHA-256 2af7695b50de6d32cdc3254b1a702b1ec09701c90677bc758d956f9476b7d3e4. All 18 on-screen quotations were checked against the cited guide pages. Each tutorial PDF has 13 pages, includes every narration section, and passed text-boundary checks. The combined tutorial has 65 pages. Representative PDF pages were visually reviewed.

Known review notes: long still holds allow book reading and spoken explanation. The CLI reports those holds and dense caption tracks as warnings. It also flags initial bar states inside an already-hidden chart, and three brief formula/summary lines whose values remain in the next chart or register display. These were reviewed in context. The optional automated motion pass was disabled in this CLI; three-frame anticipation and reveal timing were checked from the source and rendered frames. Static-frame reuse was disabled to avoid an incorrect countdown-frame classification.

Voice and music levels are approximately −17 LUFS, with true peaks below 0 dBFS. The mathematical, networking, pipeline, and processor demonstrations state their teaching assumptions. The source guide and supplied artwork retain their attribution. The package includes font licenses and source credits.
