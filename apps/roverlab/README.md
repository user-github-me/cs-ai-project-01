# ROVERLAB: Build, Connect, Train

An interactive Blue Impulse study-guide companion. Build a machine from components, connect it to a network, teach stimulus–response rules, then test the actual configuration in a mission. A first experiment takes approximately 5–10 minutes.

**Play:** https://roverlab-blue-impulse.vercel.app  
**Download:** [Complete application ZIP](https://github.com/user-github-me/cs-ai-project-01/releases/download/blue-impulse-stage2-2026-11-07/BlueImpulse_ROVERLAB_Source.zip)

**Access from China:** connect to your VPN before opening the hosted game; it is needed on our university network. Start with the [brief tutorial](TUTORIAL.md) or its [one-page PDF for submission](BlueImpulse_ROVERLAB_Quick_Start.pdf).

## Play locally

Download and extract the ZIP, then open `public/index.html` in a modern browser. All game code, illustrations and the font are local. No installation, account, API key, build tool or internet connection is required for this mode. Browser support for saving progress from `file://` differs; use local HTTP for consistent saving and offline caching:

```sh
cd apps/roverlab
python3 -m http.server 8000 --directory public
```

Open http://localhost:8000. After the first complete load over HTTP/HTTPS, the service worker caches the game for offline reloads. Linked GitHub chapters and the study-guide PDF are separate online resources; download them beforehand if needed. Saved progress belongs to this browser and address, not an account. If browser storage is blocked, the game works for the current session and displays that limitation.

## Your experiment

1. Choose an exploration rover, service robot or industrial machine.
2. Add components in the hardware workshop. Inspect their functions and remove parts to compare compatibility and power demand. The starter build is optional.
3. Install a communication module, connect devices, and run a connection test. A local test does not guarantee that a moving robot remains in range.
4. Create at least three IF–THEN rules. Test a stimulus, give feedback, edit responses, and change priority. Stronger associations win between competing rules; order breaks ties.
5. Select a mission and resolve its readiness findings.
6. Play, pause, step, restart or change playback speed. Read the event log to connect sensor input, rule selection, physical action and packet delivery.
7. Inspect the four scores and explanations. Change one decision and compare the outcome.

All controls support tapping or clicking. Use Tab/Shift+Tab to move between controls, Enter/Space to activate buttons and arrow keys in native select menus. Dialogs support Escape. Reset asks for confirmation and clears this game's saved progress.

## Learning connections

| Study-guide chapter | What to investigate |
| --- | --- |
| [Chapter 2 — Behaviorism & Behaviorist AI](https://github.com/user-github-me/cs-ai-project-01/blob/main/content/chapter-02/README.md) | Stimulus–response associations; feedback changes the strength of competing associations. |
| [Chapter 3 — Hardware](https://github.com/user-github-me/cs-ai-project-01/blob/main/content/chapter-03/README.md) | Sensors, processors, memory, power and actuators have different jobs. |
| [Chapter 4 — Networking](https://github.com/user-github-me/cs-ai-project-01/blob/main/content/chapter-04/README.md) | Endpoints, routes, range, reliability and communication failures. |
| [Chapter 5 — Applications](https://github.com/user-github-me/cs-ai-project-01/blob/main/content/chapter-05/README.md) | Readiness, practical constraints and system integration. |
| [Chapter 6 — Strengths & Limitations](https://github.com/user-github-me/cs-ai-project-01/blob/main/content/chapter-06/README.md) | Why success in a simplified simulation does not establish real-world safety. |

Use the [guided activity](https://github.com/user-github-me/cs-ai-project-01/blob/main/assets/tutorials/stage2/supporting/ROVERLAB_Activity.md) alongside the [complete study guide](https://github.com/user-github-me/cs-ai-project-01/blob/main/assets/study-guide/BlueImpulse_Study_Guide.pdf) and [tutorials](https://github.com/user-github-me/cs-ai-project-01/blob/main/assets/tutorials/stage2/README.md).

This is an explicit teaching model, not a neural network or a full reinforcement-learning algorithm. Rules are authored by the player; feedback adjusts association strength. Sensing prerequisites, power units, range units, timing and reliability values are simplified, fictional game values. A missing sensor cannot detect its stimulus, a missing actuator cannot perform its action, and a missing or out-of-range network route cannot deliver a report. The mission engine uses deterministic steps so the same configuration is reproducible. A feasible but ineffective rule can still produce a partial or failed mission.

Between triggered rules, a navigation controller moves toward the current goal. The exploration sensor automatically collects a reading at the research site and attempts to transmit it over the configured route; a `destination → return` rule is needed to bring the rover home. Service person reports and industrial temperature alerts require a `message` or `stop and report` response. The industrial machine also needs a stop response to cool down and a safe-temperature response to restart.

## Files and checks

```text
apps/roverlab/
  public/
    index.html          Browser entry point
    style.css           Responsive interface
    script.js           Workshop UI, progress, playback and persistence
    engine.js           Catalogues, validation, rules and deterministic missions
    offline.js          Optional service-worker registration
    sw.js               Local game cache
    manifest.webmanifest
    assets/             Local Inter font, license and SVG icon
  tests/                Engine and browser-journey tests
  review/               Test plan and recorded results
  vercel.json           Static output and HTTP headers
  README.md
```

Engine tests require Node.js:

```sh
node --test tests/engine.test.cjs
```

Run this from `apps/roverlab`. See the [engine verification record](review/engine-report.md) for the tested mission outcomes and model boundaries.

For browser checks, install Playwright as a local development tool (`npm install --no-save playwright`, then `npx playwright install chromium`) and run `node tests/browser.mjs`. This development-only dependency is not used by the application. All 12 Chromium checks passed locally and on the [public deployment](review/qa-hosted-report.md). WebKit passed 11 checks; automated cached offline reload was not verified in that runner, as [documented](review/webkit-offline-limitation.md). See the [local QA results](review/qa-report.md) and [WebKit results](review/qa-webkit-report.md) for exact scope. Local file mode uses a system font to avoid browser restrictions; hosted pages use the bundled Inter font.

## Publishing and automatic updates

The Vercel project is `roverlab-blue-impulse` in the **Hobby** workspace `usergithubmes-projects`. It is connected to `user-github-me/cs-ai-project-01`:

- Production branch: `main`.
- Root directory: `apps/roverlab`.
- Framework preset: Other.
- Output directory: `public`.
- Build and install commands: empty; no dependencies are needed.

Push game changes to `main` to publish a new production deployment at the same shareable URL. Other branches can receive Vercel preview deployments. The root `.vercelignore` keeps course documents, videos and working files out of CLI uploads; the public deployment serves only this app's `public/` directory. Local Vercel metadata and environment files are ignored by Git.

To publish your own copy, import the GitHub repository into a Vercel Hobby project with the settings above. Alternatively upload the contents of `public/` to Netlify or another static host. For GitHub Pages, publish this directory as the site's artifact; no routing rewrite or server is necessary. Use the host's assigned HTTPS URL as the permanent link in the ebook.

The app uses no paid add-ons, server functions, databases, analytics or external runtime APIs. Vercel's normal Hobby limits still apply. The user can manage the project in their existing Vercel account.

## Attribution and authorship

ROVERLAB was produced for Blue Impulse with Neogpt/Codex assistance following Nazif's brief. Source, verification and activity notes are public with the course repository. Illustrations are original code-based SVG/CSS graphics. Inter by Rasmus Andersson is bundled under the [SIL Open Font License](public/assets/Inter-OFL.txt). Automated browser checks are recorded separately from any future student or teacher review.
