# Rendering specification

GOAL: teach five topics by guiding a first-semester learner through the actual Blue Impulse book and a checkable example.
OUTPUT: five 1920×1080 H.264 MP4 files, 30 fps, each 300–600 seconds; one ZIP containing PDFs, scripts, subtitles, and supporting code.
TIME: measured narration is the timing source. Each question holds for 5–6 seconds before the answer. Each final cover holds for the credit narration plus 1.6 seconds.
LOOK: uniform #212C4A ground; #E15B83 active accents; #E6E4E5 neutral text; original-color book excerpts. Anta64–88 display; Inter36–44 body; JetBrainsMono34–40 code. No decorative shadows or textures.
MOTION: 0.1-second opposite-direction anticipation, then 0.4–0.6-second power3.out arrival, 0.1-second staggers. Teaching graphics progress on measured cues. Captions change on actual audio boundaries with no spatial motion.
SHOTS: the ordered scene list is in STORYBOARD.md; exact beats are in lesson-01.json through lesson-05.json after narration. One semantic scene per sub-composition.
BANNED: unreferenced factual claims, tiny demo labels, giant empty backgrounds, gradients, decorative glow/particles, simultaneous reveal of all answers, screenshots used as unreadable wallpaper, moving subtitles, hallucinated page numbers.
QA: verify all page references and numeric results, inspect every scene, inspect each answer reveal and ending, require 300–600 seconds, 1920×1080, 30 fps, audio, burned-in captions plus sidecars; decode final files and check archive integrity.

Reference inspection: both supplied TikTok clips were accessible. They show product motion with large objects, strong scale changes, spring/anticipation, staggered reveals and typography. Our tutorial adapts that movement to educational diagrams while retaining the book palette and longer reading holds. Third-party reference videos are not redistributed.
