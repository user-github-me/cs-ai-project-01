# Blue Impulse video design

Derived from the blue-professional frame preset, with corrections required by the user's one-background/one-accent brief and book typography. The preset's automatic light/dark mapping was reversed and its body-font mapping corrected. The original generated preset is retained in reference/preset-frame.md.

- Canvas: 1920 × 1080; 30 fps.
- Background: #212C4A, uniform across all five films.
- Accent: #E15B83, used for active steps, key values, and movement.
- Text and neutral structure: #E6E4E5; neutral opacity variants allowed.
- Actual book screenshots keep their original source colors.
- Display: Anta, normal weight; 64–88 px. Body: Inter, 36–44 px. Code: JetBrains Mono, 34–40 px.
- Key content: x = 192–1728; y = 132–816. Titles at x 192, y 140, 64 px.
- Caption keep-out: y = 864–1000; captions centered in x = 196–1724, 42 px, at most two lines.
- Book citation: x 192, y 812, 28 px; original page number is the PDF viewer page.
- No additional background hues, gradients, glow, decorative particles, unrelated icons, or invented statistics.
- Objects should be large enough to explain the mechanism; educational labels are at least 30 px.
- Movement begins with 3 frames (0.10 s) travelling 8–14 px opposite the main direction. Then move over 12–18 frames using power3.out. Separate object starts by 3 frames. Hold text still while read.
- Each demonstration changes with the narration; show numerical steps only when introduced. Do not front-load the completed answer.
- Local fonts: assets/fonts/Anta-Regular.ttf; Inter-400.woff2; Inter-700.woff2; JetBrainsMono-400.woff2.
