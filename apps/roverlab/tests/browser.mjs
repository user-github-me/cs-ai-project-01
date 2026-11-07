/**
 * ROVERLAB browser journeys.
 * Run: node tests/browser.mjs
 * Optional: ROVERLAB_URL=http://localhost:8791 PLAYWRIGHT_CHROMIUM_EXECUTABLE=/path/to/chromium
 */
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { access, mkdir, writeFile } from 'node:fs/promises';
import { homedir } from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const project = fileURLToPath(new URL('../', import.meta.url));
const webroot = path.join(project, 'public');
const review = path.join(project, 'review');
const port = process.env.ROVERLAB_PORT || '8791';
const baseURL = process.env.ROVERLAB_URL || `http://127.0.0.1:${port}`;
const browserName = process.env.ROVERLAB_BROWSER || 'chromium';
const reportName = process.env.ROVERLAB_REPORT_NAME || (browserName === 'chromium' ? 'qa' : `qa-${browserName}`);
const outcomes = [];
const browserErrors = [];
const failedRequests = [];
let server;
let browser;

async function loadPlaywright() {
  if (process.env.PLAYWRIGHT_MODULE) return import(process.env.PLAYWRIGHT_MODULE);
  try {
    return await import('playwright');
  } catch {
    throw new Error('Install Playwright with npm install --no-save playwright, or set PLAYWRIGHT_MODULE to its absolute module path.');
  }
}

async function executablePath() {
  if (process.env.PLAYWRIGHT_EXECUTABLE) return process.env.PLAYWRIGHT_EXECUTABLE;
  if (browserName === 'chromium' && process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE) return process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
  const relative = browserName === 'webkit' ? 'webkit-2359/pw_run.sh' : 'chromium_headless_shell-1248/chrome-headless-shell-mac-arm64/chrome-headless-shell';
  const local = path.join(homedir(), 'Library/Caches/ms-playwright', relative);
  try {
    await access(local);
    return local;
  } catch {
    return undefined;
  }
}

async function startServer() {
  if (process.env.ROVERLAB_URL) return;
  server = spawn('python3', ['-m', 'http.server', port, '--bind', '127.0.0.1', '--directory', webroot], { stdio: 'ignore' });
  for (let attempt = 0; attempt < 80; attempt++) {
    if (server.exitCode !== null) throw new Error(`Static server exited with ${server.exitCode}.`);
    try {
      const response = await fetch(baseURL);
      if (response.ok) return;
    } catch {}
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  throw new Error('Static server did not start within 8 seconds.');
}

async function context(options = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 }, ...options });
  ctx.on('page', page => {
    page.on('pageerror', error => browserErrors.push({ url: page.url(), message: error.message }));
    page.on('console', message => {
      if (message.type() === 'error') browserErrors.push({ url: page.url(), message: message.text() });
    });
    page.on('requestfailed', request => failedRequests.push({ url: request.url(), error: request.failure()?.errorText }));
  });
  return ctx;
}

async function noOverflow(page, label) {
  const sizes = await page.evaluate(() => ({ viewport: innerWidth, document: document.documentElement.scrollWidth, body: document.body.scrollWidth }));
  assert.ok(sizes.document <= sizes.viewport + 1 && sizes.body <= sizes.viewport + 1, `${label}: horizontal overflow ${JSON.stringify(sizes)}`);
}

async function screenshot(page, name) {
  if (process.env.ROVERLAB_SCREENSHOTS === '0' || browserName !== 'chromium') return;
  await page.evaluate(() => window.scrollTo({ top: 0, left: 0, behavior: 'instant' }));
  await page.screenshot({ path: path.join(review, `${name}.png`), fullPage: true, animations: 'disabled' });
}

async function check(name, callback) {
  const started = Date.now();
  try {
    const details = await callback();
    outcomes.push({ name, status: 'passed', durationMs: Date.now() - started, ...(details ? { details } : {}) });
    console.log(`PASS ${name}`);
  } catch (error) {
    if (error.skip) {
      outcomes.push({ name, status: 'skipped', durationMs: Date.now() - started, reason: error.message });
      console.log(`SKIP ${name}: ${error.message}`);
      return;
    }
    outcomes.push({ name, status: 'failed', durationMs: Date.now() - started, error: error.stack || String(error) });
    console.error(`FAIL ${name}: ${error.message}`);
  }
}

async function writeReport() {
  const report = { generatedAt: new Date().toISOString(), browser: browserName, baseURL, outcomes, browserErrors, failedRequests };
  await writeFile(path.join(review, `${reportName}-results.json`), `${JSON.stringify(report, null, 2)}\n`);
  const lines = [
    '# ROVERLAB browser QA',
    '',
    `Run: ${report.generatedAt}. Browser: ${browserName}. URL: ${baseURL}.`,
    '',
    '| Check | Result |',
    '| --- | --- |',
    ...outcomes.map(result => `| ${result.name} | ${result.status.toUpperCase()}${result.error || result.reason ? ` — ${(result.error || result.reason).split('\n')[0].replaceAll('|', '\\|')}` : ''} |`),
    '',
    `Browser errors: ${browserErrors.length}. Failed resource requests: ${failedRequests.length}.`,
    '',
    `The suite uses public controls for setup, training, and playback. It checks ${browserName} at desktop and mobile viewports. Automated WebKit checks do not establish compatibility with every Safari version.`,
    '',
    'Reproduce with `node tests/browser.mjs` from `apps/roverlab`. The runner starts a local static server unless `ROVERLAB_URL` is supplied.',
    '',
  ];
  await writeFile(path.join(review, `${reportName}-report.md`), lines.join('\n'));
}

function action(page, name, extra = '') {
  return page.locator(`[data-action="${name}"]${extra}`);
}

async function click(page, name, extra = '') {
  const target = action(page, name, extra);
  if (page.__roverlabTouch) await target.tap();
  else await target.click();
}

async function state(page) {
  return page.evaluate(() => window.RoverLabApp.getState());
}

async function freshPage(options = {}) {
  const ctx = await context(options);
  const page = await ctx.newPage();
  page.__roverlabTouch = Boolean(options.hasTouch);
  await page.goto(baseURL);
  await action(page, 'start').waitFor();
  return { ctx, page };
}

async function selectRule(page, stimulus, response) {
  await page.locator('#rule-stimulus').selectOption(stimulus);
  await page.locator('#rule-response').selectOption(response);
  await click(page, 'add-rule');
}

async function gateDoesNotAdvance(page, readStage, label) {
  const before = await readStage();
  const next = action(page, 'next');
  if (!(await next.isDisabled())) await next.click();
  assert.equal(await readStage(), before, `${label} should block progression`);
}

async function keyboardFocus(page) {
  await page.keyboard.press('Tab');
  if (browserName === 'webkit' && await page.evaluate(() => document.activeElement === document.body)) await page.keyboard.press('Alt+Tab');
  const focus = await page.evaluate(() => {
    const node = document.activeElement;
    const style = getComputedStyle(node);
    return {
      tag: node.tagName,
      text: node.getAttribute('aria-label') || node.textContent.trim(),
      outline: style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) > 0,
      shadow: style.boxShadow !== 'none',
    };
  });
  assert.notEqual(focus.tag, 'BODY', 'Tab should reach an interactive element');
  assert.ok(focus.text, 'Focused control should have an accessible name');
  assert.ok(focus.outline || focus.shadow, 'Keyboard focus should have a visible indicator');
  return focus;
}

async function stageIs(page, expected) {
  await page.waitForFunction(stage => window.RoverLabApp.getState().currentStage === stage, expected);
  await noOverflow(page, `stage ${expected}`);
}

async function buildThroughNetwork(page, machine, { gates = false, shots = false } = {}) {
  await click(page, 'start');
  await click(page, 'machine', `[data-id="${machine}"]`);
  await click(page, 'next');
  await stageIs(page, 1);
  if (gates) await gateDoesNotAdvance(page, async () => (await state(page)).currentStage, 'Incomplete hardware');
  await click(page, 'starter-hardware');
  if (shots) await screenshot(page, '02-hardware-desktop');
  await click(page, 'next');
  await stageIs(page, 2);
  if (gates) await gateDoesNotAdvance(page, async () => (await state(page)).currentStage, 'Incomplete network');
  const moduleId = machine === 'industrial' ? 'ethernet' : 'radio';
  const targetId = { exploration: 'base', service: 'controlComputer', industrial: 'server' }[machine];
  const moduleButton = action(page, 'module', `[data-id="${moduleId}"]`);
  if (await moduleButton.getAttribute('aria-pressed') !== 'true') await click(page, 'module', `[data-id="${moduleId}"]`);
  await page.locator('#link-target').selectOption(targetId);
  await page.locator('#link-module').selectOption(moduleId);
  await click(page, 'add-link');
  await click(page, 'test-network');
  await click(page, 'next');
  await stageIs(page, 3);
  if (gates) await gateDoesNotAdvance(page, async () => (await state(page)).currentStage, 'Missing training');
}

async function train(page, rules, { feedback = false, shots = false, gates = false } = {}) {
  for (const [index, [stimulus, response]] of rules.entries()) {
    await selectRule(page, stimulus, response);
    if (gates && index === 1) await gateDoesNotAdvance(page, async () => (await state(page)).currentStage, 'Only two trained rules');
  }
  const trained = await state(page);
  assert.ok(trained.config.rules.length >= 3, 'At least three associations should be saved');
  await noOverflow(page, 'trained rule table');
  if (feedback) {
    await page.locator('#test-stimulus').selectOption(rules[0][0]);
    await click(page, 'test-rule');
    const before = (await state(page)).config.rules.find(rule => rule.stimulus === rules[0][0]);
    await click(page, 'feedback', '[data-delta="1"]');
    const rewarded = (await state(page)).config.rules.find(rule => rule.stimulus === rules[0][0]);
    assert.ok(rewarded.strength > before.strength, 'Positive feedback should strengthen the association');
    await click(page, 'test-rule');
    await click(page, 'feedback', '[data-delta="-1"]');
    const corrected = (await state(page)).config.rules.find(rule => rule.stimulus === rules[0][0]);
    assert.ok(corrected.strength < rewarded.strength, 'Negative feedback should weaken the association');
  }
  if (shots) await screenshot(page, '03-training-desktop');
  await click(page, 'next');
  await stageIs(page, 4);
}

const journeys = [
  { machine: 'exploration', mission: 'explore', rules: [['obstacle', 'stopTurn'], ['destination', 'return'], ['batteryLow', 'return']] },
  { machine: 'service', mission: 'search', rules: [['person', 'stopReport'], ['destination', 'return'], ['batteryLow', 'return'], ['obstacle', 'stopTurn']] },
  { machine: 'industrial', mission: 'monitor', rules: [['tempHigh', 'stopReport'], ['safeTemp', 'move'], ['networkLost', 'indicator']] },
];

async function runMission(page, mission, { controls = false, shots = false } = {}) {
  await click(page, 'mission', `[data-id="${mission}"]`);
  await click(page, 'launch');
  await stageIs(page, 5);
  if (controls) {
    if ((await state(page)).playing) await click(page, 'pause');
    const paused = (await state(page)).simulation.time;
    await page.waitForTimeout(400);
    assert.equal((await state(page)).simulation.time, paused, 'Pause should stop the simulation clock');
    await click(page, 'step');
    assert.ok((await state(page)).simulation.time > paused, 'Step should advance the simulation');
    await click(page, 'play');
    const resumed = (await state(page)).simulation.time;
    await page.waitForFunction(time => window.RoverLabApp.getState().simulation.time > time, resumed);
    await click(page, 'pause');
    await click(page, 'restart-sim');
    if ((await state(page)).playing) await click(page, 'pause');
    assert.ok((await state(page)).simulation.time < 0.3, 'Restart should reset the simulation clock');
  }
  const speed = page.locator('#sim-speed');
  const fastest = await speed.locator('option').evaluateAll(options => options.map(option => option.value).sort((a, b) => Number(b) - Number(a))[0]);
  await speed.selectOption(fastest);
  assert.equal(Number((await state(page)).speed), Number(fastest), 'Selected playback speed should reach state');
  if (!(await state(page)).playing) await click(page, 'play');
  if (shots) {
    await page.waitForTimeout(800);
    await screenshot(page, '04-simulation-desktop');
  }
  await page.waitForFunction(() => {
    const current = window.RoverLabApp.getState();
    return current.report || current.simulation?.status !== 'running';
  }, null, { timeout: 45000 });
  const completed = await state(page);
  assert.ok(completed.simulation.time > 0, 'A mission should simulate elapsed time');
  if (completed.currentStage !== 6) await click(page, 'results');
  await stageIs(page, 6);
  const finished = await state(page);
  assert.ok(finished.report, 'The results screen should contain a mission report');
  assert.ok(Number.isFinite(finished.report.overall), 'Mission score should be a finite number');
  if (shots) await screenshot(page, '05-results-desktop');
  return finished;
}

async function wrongMissionIsBlocked(page) {
  const incompatible = action(page, 'mission', '[data-id="monitor"]');
  if (await incompatible.isDisabled()) return;
  await incompatible.click();
  const launch = action(page, 'launch');
  if (!(await launch.isDisabled())) await launch.click();
  assert.equal((await state(page)).currentStage, 4, 'Mission requirements must block a build without temperature sensing and monitoring rules');
}

async function missionJourney(spec, options = {}) {
  const { ctx, page } = await freshPage(options.mobile ? { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true } : {});
  try {
    if (options.shots) await screenshot(page, '01-landing-desktop');
    await noOverflow(page, 'landing');
    await buildThroughNetwork(page, spec.machine, options);
    await train(page, spec.rules, options);
    if (options.gates) await wrongMissionIsBlocked(page);
    const finished = await runMission(page, spec.mission, options);
    if (options.mobile) await screenshot(page, '06-results-mobile');
    return finished;
  } finally {
    await ctx.close();
  }
}

async function finish() {
  await writeReport();
  if (browser) await browser.close();
  if (server) server.kill();
  process.exitCode = outcomes.some(result => result.status === 'failed') ? 1 : 0;
}

async function main() {
  await mkdir(review, { recursive: true });
  assert.ok(['chromium', 'webkit'].includes(browserName), 'ROVERLAB_BROWSER must be chromium or webkit');
  const playwright = await loadPlaywright();
  await startServer();
  browser = await playwright[browserName].launch({ headless: true, executablePath: await executablePath() });
  const reports = new Map();

  await check('Desktop exploration: all seven stages, gating, feedback, playback controls', async () => {
    const finished = await missionJourney(journeys[0], { gates: true, feedback: true, controls: true, shots: true });
    reports.set('explore', finished.report);
    assert.equal(finished.simulation.status, 'success', `Correct exploration rules should succeed: ${finished.report.summary}`);
    return { score: finished.report.overall, status: finished.simulation.status };
  });
  await check('Mobile service/search: complete touch-sized journey with no horizontal overflow', async () => {
    const finished = await missionJourney(journeys[1], { mobile: true });
    reports.set('search', finished.report);
    assert.equal(finished.simulation.status, 'success', `Correct service rules should succeed: ${finished.report.summary}`);
    return { score: finished.report.overall, status: finished.simulation.status };
  });
  await check('Desktop industrial/monitor: complete mission with correct rules', async () => {
    const finished = await missionJourney(journeys[2]);
    reports.set('monitor', finished.report);
    assert.equal(finished.simulation.status, 'success', `Correct monitoring rules should succeed: ${finished.report.summary}`);
    return { score: finished.report.overall, status: finished.simulation.status };
  });
  await check('Wrong compatible rule changes monitoring outcome', async () => {
    const wrong = { ...journeys[2], rules: [['tempHigh', 'move'], ['safeTemp', 'move'], ['networkLost', 'indicator']] };
    const finished = await missionJourney(wrong);
    assert.ok(reports.has('monitor'), 'The correct monitoring baseline must exist');
    assert.ok(finished.report.overall < reports.get('monitor').overall, 'A wrong temperature response should reduce the score');
    assert.notEqual(finished.simulation.status, 'success', 'A wrong critical response should affect completion');
    return { correctScore: reports.get('monitor').overall, wrongScore: finished.report.overall, wrongStatus: finished.simulation.status };
  });
  await check('Keyboard focus and Enter activate game controls', async () => {
    const { ctx, page } = await freshPage();
    try {
      const focus = await keyboardFocus(page);
      await action(page, 'start').focus();
      await page.keyboard.press('Enter');
      assert.equal((await state(page)).screen, 'lab', 'Enter should activate the start control');
      await action(page, 'next').focus();
      await page.keyboard.press('Enter');
      await stageIs(page, 1);
      return { firstFocusedControl: focus.text };
    } finally { await ctx.close(); }
  });
  await check('Saved build survives reload, continues, and resets', async () => {
    const { ctx, page } = await freshPage();
    try {
      await buildThroughNetwork(page, 'service');
      await selectRule(page, 'person', 'stopReport');
      const saved = await state(page);
      await page.reload();
      await click(page, 'continue');
      const restored = await state(page);
      assert.equal(restored.config.machineId, saved.config.machineId, 'Continue should restore the selected machine');
      assert.deepEqual(restored.config.rules, saved.config.rules, 'Continue should restore trained associations');
      assert.equal(restored.currentStage, saved.currentStage, 'Continue should restore the working stage');
      await click(page, 'reset');
      await click(page, 'cancel-reset');
      assert.deepEqual((await state(page)).config.rules, saved.config.rules, 'Cancel reset should preserve progress');
      await click(page, 'reset');
      await click(page, 'confirm-reset');
      const reset = await state(page);
      assert.equal(reset.config.rules.length, 0, 'Reset should clear trained associations');
      await page.reload();
      assert.equal((await state(page)).config.rules.length, 0, 'Reset should persist after reload');
    } finally { await ctx.close(); }
  });
  await check('Rule editing, ordering, deletion, and hardware changes preserve valid gates', async () => {
    const { ctx, page } = await freshPage();
    try {
      await buildThroughNetwork(page, 'exploration');
      await train(page, journeys[0].rules);
      await click(page, 'stage', '[data-stage="3"].stage-button');
      const initial = (await state(page)).config.rules;
      await click(page, 'rule-down', `[data-id="${initial[0].id}"]`);
      assert.equal((await state(page)).config.rules[1].id, initial[0].id, 'Move down should update rule priority order');
      await click(page, 'rule-edit', `[data-id="${initial[0].id}"]`);
      await page.locator('#rule-response').selectOption('wait');
      await click(page, 'add-rule');
      assert.equal((await state(page)).config.rules.find(rule => rule.id === initial[0].id).response, 'wait', 'Edit should save a changed response');
      await click(page, 'rule-delete', `[data-id="${initial[0].id}"]`);
      assert.equal((await state(page)).config.rules.length, 2, 'Delete should remove the selected association');
      await gateDoesNotAdvance(page, async () => (await state(page)).currentStage, 'Deleting below the three-rule minimum');
      await click(page, 'stage', '[data-stage="1"].stage-button');
      await action(page, 'component', '[data-id="memory"]').first().click();
      await gateDoesNotAdvance(page, async () => (await state(page)).currentStage, 'Removing required memory');
      await action(page, 'component', '[data-id="memory"]').first().click();
      await click(page, 'next');
      await stageIs(page, 2);
      await gateDoesNotAdvance(page, async () => (await state(page)).currentStage, 'A hardware change requires a fresh network test');
      await click(page, 'test-network');
      await click(page, 'next');
      await stageIs(page, 3);
    } finally { await ctx.close(); }
  });
  await check('Start new mission confirms replacement while Continue preserves the saved build', async () => {
    const { ctx, page } = await freshPage();
    try {
      await buildThroughNetwork(page, 'service');
      await selectRule(page, 'person', 'stopReport');
      const saved = await state(page);
      await page.reload();
      await action(page, 'start').focus();
      await page.keyboard.press('Enter');
      await page.locator('#reset-dialog[open]').waitFor();
      assert.ok(await page.evaluate(() => Boolean(document.activeElement.closest('#reset-dialog'))), 'Opening the confirmation should move keyboard focus into the dialog');
      await action(page, 'cancel-reset').focus();
      await page.keyboard.press('Enter');
      await click(page, 'continue');
      assert.deepEqual((await state(page)).config, saved.config, 'Cancel new mission and Continue should preserve the whole build');
      assert.equal((await state(page)).currentStage, saved.currentStage, 'Continue should resume the saved stage');
      await page.reload();
      await click(page, 'start');
      await action(page, 'confirm-reset').focus();
      await page.keyboard.press('Enter');
      const fresh = await state(page);
      assert.equal(fresh.screen, 'lab', 'Confirming a new mission should enter the workbench');
      assert.equal(fresh.currentStage, 0, 'A new mission should start at machine selection');
      assert.equal(fresh.config.rules.length, 0, 'A new mission should clear the previous rules');
      assert.equal(fresh.config.components.length, 0, 'A new mission should clear the previous hardware');
    } finally { await ctx.close(); }
  });
  await check('Relay links connect distinct nodes and reject a self-link', async () => {
    const { ctx, page } = await freshPage();
    try {
      await click(page, 'start');
      await click(page, 'next');
      await click(page, 'starter-hardware');
      await click(page, 'next');
      await click(page, 'module', '[data-id="radio"]');
      await page.locator('#link-target').selectOption('gateway');
      await click(page, 'add-link');
      await page.locator('#link-source').selectOption('gateway');
      await page.locator('#link-target').selectOption('gateway');
      await click(page, 'add-link');
      assert.equal((await state(page)).config.network.links.length, 1, 'A self-link should not be saved');
      await page.locator('#link-target').selectOption('base');
      await click(page, 'add-link');
      assert.ok((await state(page)).config.network.links.some(link => link.from === 'gateway' && link.to === 'base'), 'A relay connection should preserve its source');
      await click(page, 'test-network');
      await click(page, 'next');
      await stageIs(page, 3);
    } finally { await ctx.close(); }
  });
  await check('Direct file URL runs without network access', async () => {
    const ctx = await context();
    await ctx.route(/^https?:\/\//, request => request.abort());
    const page = await ctx.newPage();
    try {
      await page.goto(pathToFileURL(path.join(webroot, 'index.html')).href);
      await action(page, 'start').waitFor();
      await click(page, 'start');
      await click(page, 'machine', '[data-id="industrial"]');
      await click(page, 'next');
      await stageIs(page, 1);
      await click(page, 'starter-hardware');
      await click(page, 'next');
      await stageIs(page, 2);
    } finally { await ctx.close(); }
  });
  await check('Hosted game reloads offline and restores progress from the local cache', async () => {
    if (browserName === 'webkit' && process.env.ROVERLAB_SKIP_WEBKIT_OFFLINE === '1') {
      throw Object.assign(new Error('Not verified: this local WebKit runner reports an internal navigation error after setOffline, even with all assets cached. See webkit-offline-limitation.md.'), { skip: true });
    }
    const { ctx, page } = await freshPage();
    try {
      await page.evaluate(() => navigator.serviceWorker.ready);
      await page.waitForFunction(() => Boolean(navigator.serviceWorker.controller));
      await click(page, 'start');
      await click(page, 'machine', '[data-id="service"]');
      await click(page, 'next');
      await click(page, 'starter-hardware');
      const saved = await state(page);
      await ctx.setOffline(true);
      await page.reload();
      await click(page, 'continue');
      const restored = await state(page);
      assert.equal(restored.currentStage, saved.currentStage, 'Offline reload should preserve the stage');
      assert.deepEqual(restored.config, saved.config, 'Offline reload should preserve the build');
      await noOverflow(page, 'offline restored build');
    } finally { await ctx.close(); }
  });
  await check('No browser exceptions or failed app resource requests', async () => {
    assert.deepEqual(browserErrors, [], 'Browser console/page errors should be empty');
    assert.deepEqual(failedRequests, [], 'App resources should load successfully');
  });
}

try {
  await main();
} catch (error) {
  outcomes.push({ name: 'Browser suite setup', status: 'failed', error: error.stack || String(error) });
  console.error(error);
} finally {
  await finish();
}
