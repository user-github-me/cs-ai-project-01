# ROVERLAB browser QA plan

The browser suite exercises public controls in Chromium and WebKit against a plain static server or a deployed URL. Mission setup and training use actual clicks or mobile taps rather than injected application state.

## Required journeys

- Rover, service, and industry: choose machine; install compatible hardware; connect the network; train at least three IF/THEN rules; satisfy readiness; run animated mission; reach results.
- Confirm incomplete hardware, incomplete connections, and fewer than three rules block progression with a useful explanation.
- Compare correct and deliberately incorrect compatible rules. A bad rule must alter a decision or mission result, and feedback must change the rule's association strength.
- Exercise pause, single step, resume, playback speed, and replay/restart.
- Reload a saved session, continue it, and reset it through public controls.
- Confirm Start new mission asks before replacing a saved build, cancellation preserves it, and confirmation opens an empty workbench.
- Edit, reorder, and delete rules; remove and restore required hardware; verify these changes invalidate the relevant progression gates.
- Build a robot → gateway → base relay route and reject a self-link.
- Exercise keyboard navigation and inspect visible focus and accessible control names.
- Repeat representative interactions at 1440×1000 desktop and 390×844 mobile, checking document overflow and inspecting screenshots.
- Capture browser errors and failed app resource requests. Smoke-test the direct file URL and offline behavior when technically available.

## Review artifacts

- `tests/browser.mjs`: reproducible interaction checks with an optional external static server URL.
- `review/qa-results.json`: machine-readable outcomes from the latest run.
- `review/qa-report.md`: concise human-readable findings and any remaining limitations.
- `review/*.png`: a small set of inspected representative frames.

## Run the checks

From `apps/roverlab`, install the test dependency with `npm install --no-save playwright` and make a compatible Chromium browser available, then run `node tests/browser.mjs`. The static server starts automatically on port 8791 and shuts down when the suite finishes. The game itself has no npm dependency.

Options:

- `PLAYWRIGHT_MODULE`: absolute path to an already installed Playwright module, as an alternative to a local package.
- `PLAYWRIGHT_EXECUTABLE`: browser executable override.
- `ROVERLAB_BROWSER=webkit`: run the same checks in an installed WebKit browser.
- `ROVERLAB_PORT=8792`: use a different local server port.
- `ROVERLAB_URL=https://roverlab-blue-impulse.vercel.app`: test the deployed app.
- `ROVERLAB_REPORT_NAME=qa-hosted`: keep deployment reports separate from local reports.
- `ROVERLAB_SCREENSHOTS=0`: retain existing visual artifacts instead of capturing them again.

The direct-file check blocks all HTTP/HTTPS requests while allowing local files. Hosted Chromium offline checks use the browser's offline mode after the service worker controls the page. See `webkit-offline-limitation.md` for the separately recorded WebKit limitation and its explicit opt-in skip flag.

## Scope boundaries

This suite verifies the interactive educational simulation rather than real robotics or machine-learning performance. It does not cover deployment credentials, real hardware, or external service reliability.
