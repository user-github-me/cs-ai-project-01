# ROVERLAB browser QA

Run: 2026-11-07T09:13:07.169Z. Browser: chromium. URL: http://127.0.0.1:8791.

| Check | Result |
| --- | --- |
| Desktop exploration: all seven stages, gating, feedback, playback controls | PASSED |
| Mobile service/search: complete touch-sized journey with no horizontal overflow | PASSED |
| Desktop industrial/monitor: complete mission with correct rules | PASSED |
| Wrong compatible rule changes monitoring outcome | PASSED |
| Keyboard focus and Enter activate game controls | PASSED |
| Saved build survives reload, continues, and resets | PASSED |
| Rule editing, ordering, deletion, and hardware changes preserve valid gates | PASSED |
| Start new mission confirms replacement while Continue preserves the saved build | PASSED |
| Relay links connect distinct nodes and reject a self-link | PASSED |
| Direct file URL runs without network access | PASSED |
| Hosted game reloads offline and restores progress from the local cache | PASSED |
| No browser exceptions or failed app resource requests | PASSED |

Browser errors: 0. Failed resource requests: 0.

The suite uses public controls for setup, training, and playback. It checks chromium at desktop and mobile viewports. Automated WebKit checks do not establish compatibility with every Safari version.

Reproduce with `node tests/browser.mjs` from `apps/roverlab`. The runner starts a local static server unless `ROVERLAB_URL` is supplied.
