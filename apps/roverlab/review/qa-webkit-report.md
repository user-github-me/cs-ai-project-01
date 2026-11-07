# ROVERLAB browser QA

Run: 2026-11-07T09:23:52.259Z. Browser: webkit. URL: http://127.0.0.1:8792.

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
| Hosted game reloads offline and restores progress from the local cache | SKIPPED — Not verified: this local WebKit runner reports an internal navigation error after setOffline, even with all assets cached. See webkit-offline-limitation.md. |
| No browser exceptions or failed app resource requests | PASSED |

Browser errors: 0. Failed resource requests: 0.

The suite uses public controls for setup, training, and playback. It checks webkit at desktop and mobile viewports. Automated WebKit checks do not establish compatibility with every Safari version.

Reproduce with `node tests/browser.mjs` from `apps/roverlab`. The runner starts a local static server unless `ROVERLAB_URL` is supplied.
