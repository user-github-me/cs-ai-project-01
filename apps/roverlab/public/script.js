/* ROVERLAB interface. Classic scripts deliberately support opening index.html directly. */
(function () {
  'use strict';
  // WebKit blocks local font requests from file://. System fonts keep that mode self-contained.
  if (location.protocol === 'http:' || location.protocol === 'https:') document.documentElement.classList.add('hosted-fonts');
  const E = window.RoverLabEngine;
  const app = document.getElementById('app');
  if (!E) {
    app.innerHTML = '<main class="modal" style="display:block;margin:10vh auto"><h1>The lab could not load.</h1><p>Keep index.html, style.css, script.js, and engine.js together, then reload.</p></main>';
    return;
  }
  const STORAGE_KEY = 'roverlab.save.v2';
  const STAGES = ['Machine', 'Hardware', 'Network', 'Training', 'Mission', 'Simulation', 'Results'];
  const TITLES = ['Every mission starts with a machine.', 'A little hardware. A lot of possibility.', 'Give your robot a connection.', 'Teach it how to react.', 'Time for a real-world challenge.', 'Your robot. Out in the world.', 'Every mission teaches you something.'];
  const DESCRIPTIONS = ['Choose a robot to make your own. Each one has a different job — and a different set of tools.', 'Pick the parts, learn what they do, and watch your robot take shape.', 'Choose a communication module, connect a node, and put the link to the test.', 'Build IF → THEN rules. Test a stimulus, observe the response, and give feedback.', 'Choose your environment. Check your build, connections, and training before you head out.', 'Watch sensors, rules, and hardware work together. Your choices decide what happens.', 'Review the evidence, understand the outcome, and take a better idea back to the workbench.'];
  const MACHINE_COPY = {
    exploration: { label: 'Exploration rover', description: 'Navigate rough terrain, avoid obstacles, and explore a new world.', tag: 'THE EXPLORER', number: 'RV–01', icon: 'rover' },
    service: { label: 'Service robot', description: 'Find people, move safely, and lend a helping hand.', tag: 'THE HELPER', number: 'SR–02', icon: 'service' },
    industrial: { label: 'Industrial machine', description: 'Inspect a worksite, monitor heat, and report what matters.', tag: 'THE SPECIALIST', number: 'IM–03', icon: 'industry' }
  };
  const CHAPTERS = { 2: 'Behaviorism & behaviorist AI', 3: 'Robotics hardware', 4: 'Networks & communication', 5: 'AI in the real world' };
  const SYMBOLS = { microcontroller:'▦',sbc:'▤',memory:'▥',wheels:'◉',tracks:'▰',motors:'↻',servos:'↺',ultrasonic:'◔',infrared:'⌁',camera:'▣',temp:'♧',light:'☼',gps:'⌖',battery:'▰',solar:'▥',power:'ϟ',chassis:'⬡',arm:'⌁',casing:'▱' };
  let catalogCategory = 'all';
  let inspected = 'microcontroller';
  let networkResult = null;
  let ruleTest = null;
  let editingRule = null;
  let selectedNode = 'base';
  let sim = null;
  let playing = false;
  let speed = 1;
  let timer = null;
  let toastTimer = null;
  let lastEventId = '';
  let renderNumber = 0;
  let storageAvailable = true;
  let resetIntent = 'reset';
  let state = freshState();
  const saved = readSave();
  const hasSave = !!saved;
  let canContinue = hasSave;
  if (saved) state = saved;
  state.screen = 'landing';
  selectedNode = {exploration:'base',service:'controlComputer',industrial:'server'}[state.config.machineId];

  function freshState() {
    return { version: 2, screen: 'landing', currentStage: 0, machineChosen: false, config: E.createConfig('exploration'), networkTestedFingerprint: '', missionId: 'explore', missionAccepted: false, report: null, unlockedStage: 0 };
  }
  function clone(value) { return JSON.parse(JSON.stringify(value)); }
  function esc(value) { return String(value == null ? '' : value).replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c])); }
  function find(collection, id) { return (E.catalogs[collection] || []).find(item => item.id === id); }
  function label(collection, id) { const item = find(collection, id); return item ? item.label || item.name || id : id; }
  function textIssue(value) { return typeof value === 'string' ? value : value.message || value.description || value.label || JSON.stringify(value); }
  function listIssues(check) { return (check && Array.isArray(check.issues) ? check.issues : []).map(textIssue); }
  function machineInfo() { return MACHINE_COPY[state.config.machineId] || MACHINE_COPY.exploration; }
  function recommended() { return E.getRecommendedConfig(state.config.machineId); }
  function networkFingerprint() { return JSON.stringify({ machineId: state.config.machineId, components: state.config.components.slice().sort(), network: state.config.network }); }
  function hardwareCheck() { return E.checkHardware(state.config); }
  function networkCheck() { return E.checkNetwork(state.config); }
  function rulesCheck() { return E.checkRules(state.config); }
  function networkReady() { return networkCheck().ready && state.networkTestedFingerprint === networkFingerprint(); }
  function readiness() { return E.checkReadiness(state.config, state.missionId); }
  function gate(stage) {
    if (stage === 0) return true;
    if (!state.machineChosen) return false;
    if (stage === 1) return true;
    if (!hardwareCheck().ready) return false;
    if (stage === 2) return true;
    if (!networkReady()) return false;
    if (stage === 3) return true;
    if (!rulesCheck().ready) return false;
    if (stage === 4) return true;
    if (!state.missionAccepted || !readiness().ready) return false;
    if (stage === 5) return true;
    return !!state.report;
  }
  function maxStage() { let max = 0; for (let n = 1; n < 7; n++) { if (gate(n)) max = n; else break; } return max; }
  function readSave() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (parsed.version !== 2 || !parsed.config) return null;
      const clean = freshState();
      clean.config = E.validateConfig(parsed.config);
      clean.machineChosen = !!parsed.machineChosen;
      clean.currentStage = Number.isInteger(parsed.currentStage) ? Math.min(6, Math.max(0, parsed.currentStage)) : 0;
      clean.networkTestedFingerprint = typeof parsed.networkTestedFingerprint === 'string' ? parsed.networkTestedFingerprint : '';
      clean.missionId = find('missions', parsed.missionId) ? parsed.missionId : 'explore';
      clean.missionAccepted = !!parsed.missionAccepted;
      clean.report = parsed.report && parsed.report.scores && typeof parsed.report.overall === 'number' ? parsed.report : null;
      return clean;
    } catch (_) { storageAvailable = false; return null; }
  }
  function save() {
    state.unlockedStage = maxStage();
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); canContinue = true; }
    catch (_) { storageAvailable = false; }
  }
  function invalidate(kind) {
    pauseSimulation(); sim = null; state.report = null; state.missionAccepted = false;
    if (kind === 'hardware' || kind === 'network') { state.networkTestedFingerprint = ''; networkResult = null; }
    if (kind !== 'mission') ruleTest = null;
    save();
  }
  function announce(message) { document.getElementById('announcements').textContent = message; }
  function toast(message) {
    const element = document.getElementById('toast');
    element.textContent = message; element.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(() => { element.hidden = true; }, 3300);
  }
  function brand() { return '<button class="brand" data-action="home" aria-label="ROVERLAB home"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i><i></i></span>ROVERLAB<span style="color:#7f9ba9;font-size:8px;margin-left:2px;letter-spacing:.08em">/</span></button>'; }
  function pill(text, color, dot) { return '<span class="pill ' + (color || '') + '">' + (dot ? '<i class="dot" aria-hidden="true"></i>' : '') + esc(text) + '</span>'; }
  function info(text) { return '<div class="info-strip"><span class="info-icon" aria-hidden="true">i</span><p>' + text + '</p></div>'; }
  function chapter(number, explanation) {
    return '<div class="panel"><div class="panel-title"><h3>From the textbook, to your robot.</h3>' + pill('CH ' + String(number).padStart(2, '0'), 'cyan') + '</div><div class="panel-body"><p class="inspect-description">' + explanation + '</p><a class="button text small" href="https://github.com/user-github-me/cs-ai-project-01/blob/main/content/chapter-0' + number + '/README.md" target="_blank" rel="noopener">' + CHAPTERS[number] + ' <span aria-hidden="true">↗</span></a></div></div>';
  }
  function checkList(check, success) {
    const issues = listIssues(check);
    const warnings = (check.warnings || []).map(textIssue);
    return '<ul class="status-list">' + (issues.length ? issues.slice(0, 7).map(message => '<li class="bad"><span class="status-symbol" aria-hidden="true">○</span>' + esc(message) + '</li>').join('') : '<li><span class="status-symbol" aria-hidden="true">✓</span>' + esc(success || check.summary || 'Everything is ready.') + '</li>') + warnings.slice(0, 2).map(message => '<li class="bad"><span class="status-symbol" aria-hidden="true">△</span>' + esc(message) + '</li>').join('') + '</ul>';
  }
  function icon(type) {
    const common = 'viewBox="0 0 40 40" width="30" height="30" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"';
    if (type === 'service') return '<svg ' + common + '><rect x="11" y="5" width="18" height="13" rx="5"/><path d="M17 10h1m5 0h1M10 23h20l-2 9H12zM15 35h-3m16 0h-3M6 24v6m28-6v6M20 18v5"/></svg>';
    if (type === 'industry') return '<svg ' + common + '><path d="M9 34h22M14 33v-5l8-10-5-7M11 8h10l2 5-9 4zM21 18l8 3 5-9-5-3-5 6M31 9l1-4m3 8 3-1"/><circle cx="22" cy="18" r="3"/></svg>';
    return '<svg ' + common + '><rect x="8" y="17" width="25" height="13" rx="3"/><path d="M16 17v-6h12v6m-9-6V5m-4 17h3m7 0h3M5 23v5m31-5v5"/><circle cx="12" cy="31" r="4"/><circle cx="29" cy="31" r="4"/></svg>';
  }

  /* A small, layered SVG illustration doubles as the interactive assembly view. */
  function robotSVG(config, hero) {
    const parts = new Set(hero ? ['chassis','wheels','motors','battery','power','microcontroller','ultrasonic','camera','gps','solar','casing'] : config.components);
    const body = parts.has('chassis') || parts.has('casing');
    const machine = config.machineId;
    const uid = 'robot-' + (++renderNumber);
    function part(id, content) {
      return '<g class="' + (hero ? '' : 'assembly-part') + '"' + (hero ? '' : ' data-action="inspect" data-id="' + id + '" role="button" tabindex="0" aria-label="Inspect ' + esc(label('components', id)) + '"') + '>' + content + '</g>';
    }
    function wheel(x, y, scale) {
      return '<g transform="translate(' + x + ' ' + y + ') scale(' + (scale || 1) + ')"><path d="M-17-33C-2-45 24-28 29-3L24 24C13 41-13 25-21 6Z" fill="#142a39"/><ellipse cx="-7" cy="0" rx="24" ry="34" transform="rotate(-20)" fill="#233f4f"/><ellipse cx="-7" cy="0" rx="15" ry="24" transform="rotate(-20)" fill="#41616b" stroke="#496d77" stroke-width="2"/><ellipse cx="-7" cy="0" rx="8" ry="14" transform="rotate(-20)" fill="#9cc8c9"/><path d="M-27-17l8 2m-10 10 8 2m-7 10 8 2m-4 10 7-1M0-33l3 9m10-4 2 8" stroke="#56717a" stroke-width="2"/></g>';
    }
    let svg = '<svg viewBox="0 0 600 480" role="img" aria-label="' + (hero ? 'Illustrated exploration rover with a camera, antenna and rugged wheels' : esc(machineInfo().label) + ', ' + parts.size + ' installed components; activate a part to inspect it') + '"><defs><linearGradient id="' + uid + '-body" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f9fffb"/><stop offset="1" stop-color="#c4deda"/></linearGradient><linearGradient id="' + uid + '-side" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#80b9bb"/><stop offset="1" stop-color="#568b99"/></linearGradient><filter id="' + uid + '-shadow"><feGaussianBlur stdDeviation="12"/></filter></defs><ellipse cx="304" cy="373" rx="162" ry="36" fill="#356977" opacity=".16" filter="url(#' + uid + '-shadow)"/><g class="assembly-orbit" stroke="#83abb1" stroke-width="1" fill="none" stroke-dasharray="4 7"><ellipse cx="300" cy="306" rx="227" ry="96"/><path d="M60 307h25m430 0h25M300 196v-20m0 245v17"/></g>';
    if (parts.has('wheels') || parts.has('tracks')) {
      svg += part(parts.has('tracks') ? 'tracks' : 'wheels', wheel(164, 250, .95) + wheel(386, 270, .96));
      if (parts.has('tracks')) svg += '<path d="M146 257L239 322L257 371L157 308Z" fill="#203e4d" stroke="#53747a" stroke-width="8"/>';
    }
    if (body) svg += part('chassis', '<path d="M156 250L276 189L443 278L325 343Z" fill="#2c5667"/><path d="M156 240L323 330L324 363L157 270Z" fill="url(#' + uid + '-side)"/><path d="M323 330L444 271L442 306L324 363Z" fill="#487c8c"/><path d="M152 223Q151 214 162 208L264 156Q273 151 284 157L443 240Q453 246 448 258L440 278L325 337L158 247Z" fill="url(#' + uid + '-body)"/><path d="M152 223L325 314L448 252M325 314v22" fill="none" stroke="#a1c6c4" stroke-width="2"/><path d="M165 239L315 318" stroke="#edf9f2" stroke-width="5"/><path d="M182 226L327 300L416 255" fill="none" stroke="#b4d5d0" stroke-width="1.5"/><path d="M205 262l63 34v15l-63-34Z" fill="#314e5b"/><path d="M214 272l47 25m-44-17 41 22" stroke="#82b3b5" stroke-width="1.4"/><path d="M352 315l63-32v13l-63 32Z" fill="#eaa16b"/><path d="M163 222l19 10m229 29 20-10" stroke="#ffffff" stroke-width="4"/><circle cx="170" cy="233" r="3" fill="#87aead"/><circle cx="315" cy="311" r="3" fill="#87aead"/><path d="M328 287l35-18 21 11-35 18Z" fill="#d2e7df"/><text x="329" y="282" font-family="Arial,sans-serif" font-size="9" fill="#4c777c" transform="rotate(-27 329 282)">ROVERLAB</text>');
    else svg += '<path d="M156 232L275 170L445 259L325 325Z" fill="#e6f1ed" fill-opacity=".5" stroke="#96b8b8" stroke-width="2" stroke-dasharray="8 7"/><text x="298" y="265" text-anchor="middle" fill="#749da3" font-size="12" font-family="Arial,sans-serif">Your robot starts here</text>';
    if (parts.has('wheels') || parts.has('tracks')) svg += part(parts.has('tracks') ? 'tracks' : 'wheels', wheel(201, 299, 1.05) + wheel(356, 349, 1.05));
    if (parts.has('battery')) svg += part('battery', '<path d="M259 225L310 198L367 228L314 256Z" fill="#244b59"/><path d="M259 225v18l55 29v-16Z" fill="#1e3e4e"/><path d="M314 256l53-28v18l-53 26Z" fill="#416c76"/><path d="M279 222l8 5-6 5 18 8-4-9 7-5Z" fill="#9be2d7"/>');
    if (parts.has('microcontroller') || parts.has('sbc')) svg += part(parts.has('microcontroller') ? 'microcontroller' : 'sbc', '<path d="M203 217L245 195L281 214L238 237Z" fill="#326a65" stroke="#89b9a4" stroke-width="2"/><path d="M224 216l19-10 15 8-18 10Z" fill="#203f43"/><path d="M217 216l-9-4m14 10-9-4m15 9-9-4m25-20-7-4m16 0-7-4" stroke="#b8d5b4" stroke-width="2"/>');
    if (parts.has('solar')) svg += part('solar', '<path d="M278 218L329 191L386 222L335 249Z" fill="#244e69" stroke="#6a9fac" stroke-width="3"/><path d="M291 211l58 30m-45-37 58 30m-45-37 58 30M291 226l50-27m-35 35 50-27m-35 35 50-27" stroke="#8bbac5" stroke-width="1"/>');
    if (parts.has('camera')) svg += part('camera', '<path d="M313 208v-48l10-5v48Z" fill="#6c969e"/><path d="M306 160L327 149L342 157L321 169Z" fill="#9ec5c5"/><path d="M284 118L318 100L357 121L323 140Z" fill="#f0f8f0"/><path d="M284 118v39l39 21v-38Z" fill="#74aab2"/><path d="M323 140l34-19v39l-34 18Z" fill="#517b8c"/><ellipse cx="339" cy="146" rx="12" ry="15" fill="#234452" transform="rotate(22 339 146)"/><ellipse cx="340" cy="145" rx="7" ry="10" fill="#122d42" transform="rotate(22 340 145)"/><ellipse cx="342" cy="142" rx="3" ry="4" fill="#79d6db"/><path d="M291 138v11l11 6v-11Z" fill="#aed1d0"/>');
    if (parts.has('ultrasonic') || parts.has('infrared')) svg += part(parts.has('ultrasonic') ? 'ultrasonic' : 'infrared', '<path d="M375 277l39-20v18l-39 20Z" fill="#2b5c6b"/><ellipse cx="385" cy="280" rx="5" ry="7" transform="rotate(28 385 280)" fill="#b7e6df"/><ellipse cx="403" cy="271" rx="5" ry="7" transform="rotate(28 403 271)" fill="#b7e6df"/><ellipse cx="385" cy="280" rx="2" ry="4" transform="rotate(28 385 280)" fill="#416f77"/><ellipse cx="403" cy="271" rx="2" ry="4" transform="rotate(28 403 271)" fill="#416f77"/>');
    if (parts.has('gps') || (hero && machine !== 'industrial')) svg += part('gps', '<path d="M227 183v-76" stroke="#2a596b" stroke-width="4"/><path d="M219 186l9-5 10 5-9 5Z" fill="#527f85"/><path d="M227 111l-9-6" stroke="#2a596b" stroke-width="3"/><circle cx="227" cy="104" r="5" fill="#edab74"/><g fill="none" stroke="#5f979d" stroke-width="1.5" opacity=".6"><path d="M214 96q-8 9 0 18m26-18q8 9 0 18M207 90q-14 15 0 29m40-29q14 15 0 29"/></g>');
    if (parts.has('arm') || machine === 'industrial' && hero) svg += part('arm', '<path d="M271 225L262 160L214 116L235 87" fill="none" stroke="#345d6b" stroke-width="20" stroke-linejoin="round"/><path d="M271 225L262 160L214 116L235 87" fill="none" stroke="#e6a06e" stroke-width="12" stroke-linejoin="round"/><circle cx="262" cy="160" r="11" fill="#577b81" stroke="#bdcfc8" stroke-width="3"/><circle cx="214" cy="116" r="9" fill="#577b81"/><path d="M232 82l20-10 12 9m-28 7 17 7 14-8" fill="none" stroke="#244b5a" stroke-width="7"/>');
    if (parts.has('temp')) svg += part('temp', '<path d="M292 283v-27" stroke="#cf9d78" stroke-width="6"/><circle cx="292" cy="285" r="5" fill="#ebae7d"/>');
    if (parts.has('light')) svg += part('light', '<circle cx="177" cy="230" r="6" fill="#f7d798" stroke="#81afb1" stroke-width="2"/>');
    if (parts.has('memory')) svg += part('memory', '<path d="M245 251l22-12 16 9-22 12Z" fill="#405e64" stroke="#92b3a0" stroke-width="2"/>');
    if (parts.has('power')) svg += part('power', '<path d="M285 278l19-10 10 5-19 11Z" fill="#dfa673"/><path d="M289 277l7-4" stroke="#fff1d9" stroke-width="2"/>');
    if (parts.has('motors') || parts.has('servos')) svg += part(parts.has('motors') ? 'motors' : 'servos', '<path d="M262 317l17 9v17l-17-9Z" fill="#c2d5cf"/><path d="M265 320l10 5v10l-10-5Z" fill="#688b94"/>');
    return svg + '</svg>';
  }

  function renderLanding() {
    const config = E.createConfig('exploration');
    app.innerHTML = '<div class="landing"><header class="topbar">' + brand() + '<nav class="top-links" aria-label="About the lab"><button data-action="howto">How it works</button><button data-action="objectives">Learning objectives <span aria-hidden="true">↗</span></button></nav><div class="top-status"><span class="dot"></span> An interactive learning lab</div></header><main id="main"><section class="hero"><div class="hero-copy"><div class="eyebrow"><span class="dot" style="color:#87cdd0"></span> Big ideas start on a small workbench</div><h1>Your ideas.<br><em>In motion.</em></h1><p class="hero-description">Meet your next hands-on experiment. Turn a collection of parts into a robot that senses, responds, and finds its way.</p><p class="hero-tagline">Build it. Connect it. Train it. Send it on a mission.</p><div class="hero-actions"><button class="button cyan" data-action="start">Start new mission <span aria-hidden="true">↗</span></button>' + (canContinue ? '<button class="button ghost" data-action="continue">Continue building <span aria-hidden="true">→</span></button>' : '<button class="button ghost" data-action="howto">Take a quick look <span aria-hidden="true">▷</span></button>') + '</div><div class="hero-meta"><span>5–10 minutes</span><span>No experience needed</span><span>Built for curious minds</span></div></div><div class="hero-art"><div class="canvas-label"><span class="dot"></span> Prototype / RV–01</div><div class="corner-coordinates">35.68° N &nbsp; 139.76° E</div>' + robotSVG(config, true) + '<div class="float-label one"><i></i> Sensors ready to explore</div><div class="float-label two"><span aria-hidden="true">⌁</span> A little code. A lot of curiosity.</div><div class="art-footer"><span>Designed by you. Driven by logic.</span><strong>01 / 03</strong></div></div></section><section class="landing-path" aria-label="Your learning journey"><div class="path-intro"><h3>From parts to purpose.</h3><p>One experiment. Four big ideas.</p></div>' + [['01','Make it yours','Choose a machine. Give it the right tools.'],['02','Get connected','Build a network that goes the distance.'],['03','Teach a response','Turn observations into actions.'],['04','See what happens','Run a mission. Learn from the outcome.']].map(item => '<div class="path-step"><span class="step-num">' + item[0] + '</span><div><h4>' + item[1] + '</h4><p>' + item[2] + '</p></div></div>').join('') + '</section></main><footer class="landing-bottom"><span>ROVERLAB &nbsp; / &nbsp; A playground for robotics & artificial intelligence</span><button data-action="reset">Reset saved progress</button></footer></div>';
  }
  function render() {
    if (state.screen === 'landing') { renderLanding(); return; }
    const n = state.currentStage;
    app.innerHTML = '<div class="app-shell"><header class="app-topbar"><div class="app-topbar-left">' + brand() + '<div class="project-breadcrumb">Your workspace <span>/ &nbsp; ' + machineInfo().number + '</span></div></div><div class="app-topbar-right"><span class="save-state"><i class="dot"></i>' + (storageAvailable ? 'Saved on this device' : 'Session only') + '</span><button data-action="howto">Lab guide <span aria-hidden="true">↗</span></button><span class="avatar" aria-hidden="true">RL</span></div></header><div class="app-layout"><aside class="sidebar"><span class="eyebrow">Your experiment</span><nav class="stage-nav" aria-label="Build stages">' + STAGES.map((name, index) => '<button class="stage-button ' + (index === n ? 'active' : index < n && gate(index + 1) ? 'done' : '') + '" data-action="stage" data-stage="' + index + '"' + (gate(index) ? '' : ' disabled') + (index === n ? ' aria-current="step"' : '') + '><span class="stage-index" aria-hidden="true">' + (index < n && gate(index + 1) ? '✓' : String(index + 1).padStart(2, '0')) + '</span><span class="stage-label">' + name + '</span></button>').join('') + '</nav><div class="sidebar-foot"><span class="eyebrow">Curiosity is the engine.</span><p>Try an idea. Test it.<br>See what you can learn.</p><button data-action="objectives">Learning objectives ↗</button><button data-action="reset">Start a fresh experiment</button></div></aside><main id="main" class="workspace" tabindex="-1"><div class="page-head"><div><span class="eyebrow">Experiment ' + machineInfo().number + ' &nbsp; / &nbsp; Step ' + String(n + 1).padStart(2, '0') + ' of 07</span><h1>' + TITLES[n] + '</h1><p>' + DESCRIPTIONS[n] + '</p></div><div class="head-meta">' + pill(n === 5 ? 'Live simulation' : n === 6 ? 'Mission report' : 'Your workbench', n === 5 ? 'orange' : 'cyan', true) + '</div></div>' + (storageAvailable ? '' : '<div class="banner">Your browser blocked storage. The lab still works, but progress will last only until this page closes.</div>') + stageContent(n) + footer(n) + '</main></div></div>';
    const active = app.querySelector('.stage-button.active');
    if (active && window.innerWidth < 960) active.scrollIntoView({ block: 'nearest', inline: 'center' });
    if (n === 5 && sim) updateSimFrame();
  }
  function stageContent(n) { return [renderMachine, renderHardware, renderNetwork, renderTraining, renderMission, renderSimulation, renderResults][n](); }
  function footer(n) {
    let nextAction = 'next';
    let nextText = ['Build this machine', 'Connect your robot', 'Train your robot', 'Choose a mission', 'Launch mission', 'View mission report', 'Build another robot'][n];
    let enabled = n === 0 || gate(n + 1);
    let note = ['Three machines. A different way to put your ideas to work.', 'A processor, movement, sensors, and power: every part has a purpose.', 'A connection is ready only after a successful network test.', 'At least 3 compatible rules. Good hardware still needs good decisions.', 'Check every system before you send your robot into the field.', 'Pause, step through a decision, or speed things up. Stay curious.', 'Change one thing, run it again, and compare what happens.'][n];
    if (n === 1 && !hardwareCheck().ready) note = listIssues(hardwareCheck())[0] || note;
    if (n === 2 && !networkReady()) note = 'Connect at least one reachable node and run a successful network test.';
    if (n === 3 && !rulesCheck().ready) note = listIssues(rulesCheck())[0] || note;
    if (n === 4) { nextAction = 'launch'; enabled = readiness().ready && networkReady(); if (!enabled) note = listIssues(readiness())[0] || 'Return to a previous step to finish your setup.'; }
    if (n === 5) { nextAction = 'results'; enabled = !!state.report; }
    if (n === 6) { nextAction = 'new-build'; enabled = true; }
    return '<footer class="work-footer"><div class="work-footer-left"><div class="check-summary ' + (enabled ? 'ready' : '') + '"><i class="dot"></i><p>' + esc(note) + '</p></div></div><div class="work-footer-actions">' + (n > 0 ? '<button class="button secondary" data-action="back"><span aria-hidden="true">←</span> Back</button>' : '<button class="button text" data-action="howto">Need a hand?</button>') + '<button class="button primary" data-action="' + nextAction + '"' + (enabled ? '' : ' disabled') + '>' + nextText + ' <span aria-hidden="true">→</span></button></div></footer>';
  }
  function renderMachine() {
    return '<div class="workbench two"><div class="stack"><div class="machine-list" role="group" aria-label="Choose your machine">' + Object.keys(MACHINE_COPY).map(id => { const item = MACHINE_COPY[id]; return '<button class="machine-choice ' + (state.config.machineId === id ? 'selected' : '') + '" data-action="machine" data-id="' + id + '" aria-pressed="' + (state.config.machineId === id) + '"><span class="machine-icon">' + icon(item.icon) + '</span><span><h3>' + item.label + '</h3><p>' + item.description + '</p></span><span class="choice-radio" aria-hidden="true"></span></button>'; }).join('') + '</div>' + info('Start with what sparks your curiosity. You can experiment with another machine after your mission.') + '</div><div class="stack"><div class="robot-canvas"><div class="canvas-label"><i class="dot"></i> Meet your next prototype</div><span class="canvas-badge">' + pill(machineInfo().tag, 'cyan') + '</span>' + robotSVG(state.config, true) + '<div class="canvas-footer"><strong>' + machineInfo().label + ' / ' + machineInfo().number + '</strong><span>Preview build</span></div></div><div class="stat-row"><div class="stat-card"><label>Your mission</label><strong style="font-size:16px">' + ({exploration:'Explore',service:'Assist',industrial:'Monitor'}[state.config.machineId]) + '</strong></div><div class="stat-card"><label>Learning style</label><strong style="font-size:16px">Hands-on</strong></div><div class="stat-card"><label>Experience</label><strong style="font-size:16px">Curious</strong></div></div></div></div>';
  }
  function renderHardware() {
    const config = state.config;
    const check = hardwareCheck();
    const categories = [...new Set(E.catalogs.components.map(component => component.category))];
    const items = E.catalogs.components.filter(component => catalogCategory === 'all' || component.category === catalogCategory);
    const item = find('components', inspected) || E.catalogs.components[0];
    const installed = config.components.includes(item.id);
    const load = check.power.demand;
    return '<div class="workbench hardware-bench"><section class="panel catalog"><div class="panel-title"><h2>Component library</h2><small>' + E.catalogs.components.length + ' parts</small></div><div class="category-tabs" role="group" aria-label="Component categories"><button data-action="category" data-id="all" class="' + (catalogCategory === 'all' ? 'active' : '') + '" aria-pressed="' + (catalogCategory === 'all') + '">All parts</button>' + categories.map(category => '<button data-action="category" data-id="' + esc(category) + '" class="' + (catalogCategory === category ? 'active' : '') + '" aria-pressed="' + (catalogCategory === category) + '">' + esc(category) + '</button>').join('') + '</div><div class="component-list">' + items.map(component => {
      const on = config.components.includes(component.id);
      const compatible = !component.compatible || component.compatible.includes(config.machineId);
      return '<div class="component-card ' + (compatible ? '' : 'incompatible') + '"><span class="component-symbol" aria-hidden="true">' + (SYMBOLS[component.id] || '◇') + '</span><button class="component-text" data-action="inspect" data-id="' + component.id + '"><strong>' + esc(component.label) + '</strong><small>' + (compatible ? (component.power || 0) + ' units · ' + (on ? 'Installed' : 'Available') : 'Different machine') + '</small></button><button class="component-toggle" data-action="component" data-id="' + component.id + '" aria-label="' + (on ? 'Remove ' : 'Add ') + esc(component.label) + '" aria-pressed="' + on + '"' + (compatible ? '' : ' disabled') + '>' + (on ? '✓' : '+') + '</button></div>';
    }).join('') + '</div><div class="catalog-footer"><button class="button secondary full" data-action="starter-hardware"><span aria-hidden="true">✧</span> Try a starter build <span aria-hidden="true">↗</span></button></div></section><div class="assembly"><div class="robot-canvas"><div class="canvas-label"><i class="dot"></i> Assembly view / ' + machineInfo().number + '</div><span class="canvas-badge">' + pill(check.ready ? 'Systems ready' : 'In progress', check.ready ? 'green' : 'orange', true) + '</span>' + robotSVG(config, false) + '<div class="canvas-footer"><strong>' + machineInfo().label + '</strong><span class="canvas-tip">Select a part to inspect</span></div></div><div class="stat-row"><div class="stat-card"><label>Parts installed</label><strong>' + config.components.length + '<small>components</small></strong><div class="mini-bar"><i style="width:' + Math.min(100, config.components.length / 12 * 100) + '%"></i></div></div><div class="stat-card"><label>Power budget</label><strong>' + Math.round(load * 10) / 10 + '<small>units</small></strong><div class="mini-bar"><i style="width:' + Math.min(100, load * 2) + '%;background:#d4ae80"></i></div></div><div class="stat-card"><label>Build check</label><strong>' + (check.ready ? 'Ready' : listIssues(check).length) + '<small>' + (check.ready ? 'to connect' : 'to resolve') + '</small></strong><div class="mini-bar"><i style="width:' + (check.ready ? 100 : Math.max(5, 100 - listIssues(check).length * 13)) + '%"></i></div></div></div></div><aside class="stack inspector"><section class="panel"><div class="panel-title"><h2>Under the hood</h2>' + pill(installed ? 'Installed' : 'Explore', installed ? 'green' : '') + '</div><div class="panel-body"><div class="inspect-icon" aria-hidden="true">' + (SYMBOLS[item.id] || '◇') + '</div><h3 class="inspect-title">' + esc(item.label) + '</h3><p class="inspect-description">' + esc(item.description) + '</p><dl class="detail-pairs"><div class="detail-pair"><dt>System</dt><dd>' + esc(item.category) + '</dd></div><div class="detail-pair"><dt>Power draw</dt><dd>' + (item.power || 0) + ' units</dd></div><div class="detail-pair"><dt>Role</dt><dd>' + esc((item.capabilities || []).slice(0, 2).join(' · ') || 'Structure') + '</dd></div></dl><button class="button secondary small full" data-action="component" data-id="' + item.id + '"' + (item.compatible && !item.compatible.includes(config.machineId) ? ' disabled' : '') + '>' + (installed ? '− Remove component' : '+ Add to your robot') + '</button></div></section><section class="panel"><div class="panel-title"><h3>Pre-flight build check</h3></div><div class="panel-body">' + checkList(check, 'Processor, power, movement, and sensing are ready. Power values are simplified teaching units.') + '<div class="divider"></div><p class="small-note">Removing an essential part pauses your progress until you replace it. Your hardware also decides which rules you can train.</p></div></section></aside></div><div style="margin-top:16px">' + chapter(3, 'Sensors are your robot’s inputs. A processor interprets those signals, and actuators turn instructions into movement. Power brings every part to life.') + '</div>';
  }

  function renderNetwork() {
    const network = state.config.network;
    const selectedModules = network.modules;
    const tested = networkReady();
    const moduleOptions = selectedModules.map(id => '<option value="' + esc(id) + '">' + esc(label('modules', id)) + '</option>').join('');
    return '<div class="workbench even network-bench"><div class="stack"><section class="panel"><div class="panel-title"><h2>01 / Choose your communication</h2><small>Mix & match</small></div><div class="panel-body"><div class="selection-grid">' + E.catalogs.modules.map(item => '<button class="module-option ' + (selectedModules.includes(item.id) ? 'selected' : '') + '" data-action="module" data-id="' + item.id + '" aria-pressed="' + selectedModules.includes(item.id) + '"><span class="module-icon" aria-hidden="true">' + ({wifi:'◔',bluetooth:'ᛒ',radio:'⌁',ethernet:'⊞',cellular:'▥'}[item.id]) + '</span><span><strong>' + esc(item.label) + '</strong><small>' + esc(item.description || 'Range ' + item.range) + '</small></span></button>').join('') + '</div><div class="divider"></div><h3 class="panel-subheading">02 / Make a connection</h3><div class="field"><label for="link-source">From node</label><select id="link-source"><option value="robot">Your robot</option>' + E.catalogs.nodes.map(node => '<option value="' + node.id + '">' + esc(node.label) + '</option>').join('') + '</select></div><div class="form-row"><div class="field"><label for="link-target">To node</label><select id="link-target">' + E.catalogs.nodes.map(node => '<option value="' + node.id + '"' + (node.id === selectedNode ? ' selected' : '') + '>' + esc(node.label) + '</option>').join('') + '</select></div><div class="field"><label for="link-module">Using this module</label><select id="link-module"' + (selectedModules.length ? '' : ' disabled') + '>' + (moduleOptions || '<option value="">Choose a module first</option>') + '</select></div></div><button class="button primary small full" data-action="add-link"' + (selectedModules.length ? '' : ' disabled') + '>+ Connect nodes</button><p class="small-note" style="margin-top:11px">You can also select a destination directly on the network map. Short-range links may drop when your robot moves.</p></div></section>' + chapter(4, 'A module is the communication technology. A node is a device on the network. A link joins them. Range and reliability decide whether a message gets through.') + '</div><div class="stack"><div class="network-canvas"><div class="canvas-label"><i class="dot"></i> Network map / select a node</div>' + networkSVG() + '</div><section class="panel"><div class="panel-title"><h3>Your connections</h3>' + pill(network.links.length + ' links', tested ? 'green' : '') + '</div><div class="panel-body">' + (network.links.length ? '<ul class="link-list">' + network.links.map(link => '<li class="link-item"><div><strong>' + esc(link.from === 'robot' ? 'Robot' : label('nodes', link.from)) + ' <span aria-hidden="true">↔</span> ' + esc(label('nodes', link.to)) + '</strong><small>' + esc(label('modules', link.module)) + ' · ' + (tested ? 'Tested connection' : 'Awaiting test') + '</small></div><button class="icon-button" data-action="remove-link" data-id="' + esc(link.id) + '" aria-label="Remove link to ' + esc(label('nodes', link.to)) + '">×</button></li>').join('') + '</ul>' : '<div class="empty-state">No connections yet.<br>Choose a module and connect your first node.</div>') + '<button class="button ' + (tested ? 'secondary' : 'primary') + ' full" style="margin-top:13px" data-action="test-network">' + (tested ? '✓ Test the network again' : 'Test network connection') + ' <span aria-hidden="true">↗</span></button>' + (networkResult ? '<div class="test-result ' + (networkResult.ready ? '' : 'bad') + '"><strong>' + (networkResult.ready ? 'Route available. Your connection works.' : 'This connection needs a little work.') + '</strong>' + esc(networkResult.ready ? networkResult.summary || 'The robot can reach a useful network node.' : listIssues(networkResult).join(' ')) + (networkResult.warnings && networkResult.warnings.length ? '<br>' + esc(networkResult.warnings.map(textIssue).join(' ')) : '') + '</div>' : tested ? '<div class="test-result"><strong>Network test passed.</strong>Your current hardware and connections have been checked.</div>' : '') + '</div></section></div></div>';
  }
  function networkSVG() {
    const positions = { robot: [300,163],gateway:[133,85],server:[465,75],base:[112,260],otherRobot:[459,263],controlComputer:[304,307] };
    let svg = '<svg viewBox="0 0 600 370" role="img" aria-label="Robot network map. Select a node, then use Connect nodes."><defs><pattern id="network-grid" width="23" height="23" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#adc6c1" opacity=".45"/></pattern></defs><rect width="600" height="370" fill="url(#network-grid)"/>';
    state.config.network.links.forEach(link => {
      const a = positions[link.from] || positions.robot; const b = positions[link.to];
      if (b) svg += '<path class="network-line ' + (networkResult && !networkResult.ready ? 'bad' : '') + '" d="M' + a[0] + ' ' + a[1] + 'L' + b[0] + ' ' + b[1] + '"/><rect x="' + ((a[0]+b[0])/2-26) + '" y="' + ((a[1]+b[1])/2-9) + '" width="52" height="18" rx="4" fill="#f8fcf9"/><text x="' + ((a[0]+b[0])/2) + '" y="' + ((a[1]+b[1])/2+3) + '" font-size="8" fill="#6a9397" text-anchor="middle">' + esc(label('modules', link.module)) + '</text>';
    });
    svg += '<circle cx="300" cy="163" r="54" fill="#deeddf" stroke="#c8dfd3" stroke-dasharray="4 5"/><rect x="268" y="132" width="64" height="61" rx="13" fill="#214f60"/><path d="M285 153h31v23h-31zM290 147h21v6m-31 6v13m41-13v13M291 180h5m10 0h5" fill="none" stroke="#b8e7dc" stroke-width="2.5"/><circle cx="295" cy="163" r="2" fill="#e6b580"/><circle cx="308" cy="163" r="2" fill="#e6b580"/><text x="300" y="216" text-anchor="middle" font-size="10" fill="#3b6670">Your robot</text>';
    E.catalogs.nodes.forEach(node => {
      const pos = positions[node.id]; if (!pos) return;
      const connected = state.config.network.links.some(link => link.to === node.id);
      svg += '<g class="network-node ' + (selectedNode === node.id ? 'selected' : '') + '" data-action="node" data-id="' + node.id + '" role="button" tabindex="0" aria-label="Select ' + esc(node.label) + '"><circle cx="' + pos[0] + '" cy="' + pos[1] + '" r="42" fill="transparent" pointer-events="all"/><rect x="' + (pos[0]-28) + '" y="' + (pos[1]-27) + '" width="56" height="50" rx="11" fill="' + (connected ? '#e0efea' : '#f9fcf9') + '" stroke="' + (connected ? '#a1c4b9' : '#d5e1dc') + '"/><text x="' + pos[0] + '" y="' + (pos[1]+5) + '" text-anchor="middle" font-size="24" fill="#6d959d" aria-hidden="true">' + ({gateway:'⌁',server:'▤',base:'⌂',otherRobot:'▣',controlComputer:'▱'}[node.id]) + '</text><text x="' + pos[0] + '" y="' + (pos[1]+42) + '" text-anchor="middle" font-size="9" fill="#6e8b91">' + esc(node.label) + '</text>' + (connected ? '<circle cx="' + (pos[0]+23) + '" cy="' + (pos[1]-22) + '" r="5" fill="#72a894" stroke="#f4faf6" stroke-width="2"/>' : '') + '</g>';
    });
    return svg + '</svg>';
  }

  function renderTraining() {
    const rules = state.config.rules;
    const check = rulesCheck();
    const recommendation = recommended();
    const suggested = recommendation.rules.find(rule => !rules.some(existing => existing.stimulus === rule.stimulus)) || recommendation.rules[0];
    const edit = rules.find(rule => rule.id === editingRule);
    const currentStimulus = edit ? edit.stimulus : suggested ? suggested.stimulus : E.catalogs.stimuli[0].id;
    const currentResponse = edit ? edit.response : suggested ? suggested.response : E.catalogs.responses[0].id;
    return '<div class="workbench even"><div class="stack"><section class="panel"><div class="training-intro"><div><h3>Your robot’s playbook</h3><p>Stronger associations run first. Ties follow the rule order.</p></div>' + pill(rules.length + ' / 3 minimum', check.ready ? 'green' : 'orange') + '</div><div class="rule-list-area"><div class="training-board">' + (rules.length ? rules.map((rule, index) => '<article class="rule-card"><span class="rule-order">' + String(index + 1).padStart(2, '0') + '</span><div class="rule-body"><div class="rule-expression"><span class="rule-word">IF</span><span>' + esc(label('stimuli', rule.stimulus)) + '</span><span class="rule-word then">THEN</span><span>' + esc(label('responses', rule.response)) + '</span></div><div class="rule-strength"><span>Association ' + (rule.strength > 0 ? '+' : '') + rule.strength + '</span><span class="strength-track" aria-hidden="true">' + Array.from({length:10}, (_, i) => '<i class="' + (i < Number(rule.strength) + 5 ? 'on' : '') + '"></i>').join('') + '</span></div></div><div class="rule-actions"><button data-action="rule-up" data-id="' + rule.id + '" aria-label="Move rule ' + (index+1) + ' up"' + (index === 0 ? ' disabled' : '') + '>↑</button><button data-action="rule-down" data-id="' + rule.id + '" aria-label="Move rule ' + (index+1) + ' down"' + (index === rules.length-1 ? ' disabled' : '') + '>↓</button><button data-action="rule-edit" data-id="' + rule.id + '" aria-label="Edit rule ' + (index+1) + '">✎</button><button data-action="rule-delete" data-id="' + rule.id + '" aria-label="Delete rule ' + (index+1) + '">×</button></div></article>').join('') : '<div class="empty-state">A sensor detects something. Your robot needs a response.<br>Add your first rule below to make that connection.</div>') + '</div></div><div class="panel-body" style="border-top:1px solid var(--line)"><h3 class="panel-subheading">' + (edit ? 'Edit this association' : 'Add an association') + '</h3><div class="form-row"><div class="field"><label for="rule-stimulus">IF the robot detects…</label><select id="rule-stimulus">' + E.catalogs.stimuli.map(item => '<option value="' + item.id + '"' + (item.id === currentStimulus ? ' selected' : '') + '>' + esc(item.label) + '</option>').join('') + '</select></div><div class="field"><label for="rule-response">THEN it should…</label><select id="rule-response">' + E.catalogs.responses.map(item => '<option value="' + item.id + '"' + (item.id === currentResponse ? ' selected' : '') + '>' + esc(item.label) + '</option>').join('') + '</select></div></div><button class="button primary full small" data-action="add-rule">' + (edit ? 'Save rule changes' : '+ Add training rule') + '</button>' + (edit ? '<button class="button text small full" data-action="cancel-rule">Cancel edit</button>' : '<p class="learning-note">The form suggests a useful next rule. You can change it. A compatible response may still be a poor choice for the mission.</p>') + '</div><div class="rule-help">' + (check.ready ? '✓ Your hardware supports at least 3 active rules. Test them before you head out.' : esc(listIssues(check).join(' '))) + '</div></section>' + chapter(2, 'An IF–THEN rule associates a stimulus with a response. Your feedback strengthens or weakens that association. This is a simplified, hand-authored behaviorist model — not a self-learning neural network.') + '</div><div class="stack"><section class="panel"><div class="panel-title"><h2>The training ground</h2>' + pill('Try → Observe → Respond', 'cyan') + '</div><div class="panel-body"><p class="inspect-description" style="margin-bottom:18px">Give your robot a stimulus and see which rule wins. Reward a useful response, or weaken an unhelpful one.</p><div class="field"><label for="test-stimulus">Simulate a stimulus</label><select id="test-stimulus">' + E.catalogs.stimuli.map(item => '<option value="' + item.id + '"' + ((ruleTest ? ruleTest.stimulus : currentStimulus) === item.id ? ' selected' : '') + '>' + esc(item.label) + '</option>').join('') + '</select></div><button class="button secondary full" data-action="test-rule">Test stimulus & response <span aria-hidden="true">↗</span></button>' + renderRuleTest() + '</div></section><div class="robot-canvas" style="min-height:260px"><div class="canvas-label"><i class="dot"></i> Learning by association</div>' + robotSVG(state.config, false).replace('<svg viewBox=', '<svg style="height:225px;margin-top:10px" viewBox=') + '<div class="canvas-footer"><span>Sensor</span><span aria-hidden="true">→</span><span>Processor + rule</span><span aria-hidden="true">→</span><span>Actuator</span></div></div>' + info('Want to explore a bad decision? Try “obstacle → move forward.” The hardware supports it — but the mission will show why it is risky.') + '</div></div>';
  }
  function renderRuleTest() {
    if (!ruleTest) return '<div class="empty-state" style="margin-top:17px">Your experiment will appear here.<br>Test a rule, then tell the robot how it did.</div>';
    if (!ruleTest.ruleId) return '<div class="test-result bad"><strong>No matching, compatible response.</strong>' + esc(ruleTest.explanation || 'Add a rule for this stimulus, and make sure the required sensor and actuator are installed.') + '</div>';
    const rule = state.config.rules.find(item => item.id === ruleTest.ruleId);
    if (!rule) return '';
    return '<div class="test-result"><strong>Stimulus detected → ' + esc(label('responses', rule.response)) + '</strong><div class="test-sequence"><span>' + esc(label('stimuli', rule.stimulus)) + '</span><span aria-hidden="true">→</span><span>Rule ' + (state.config.rules.indexOf(rule)+1) + '</span><span aria-hidden="true">→</span><span>' + esc(label('responses', rule.response)) + '</span></div>' + esc(ruleTest.explanation || 'The processor selected the strongest matching association. The actuator follows the rule you wrote.') + '<div class="feedback-row"><button class="button secondary" data-action="feedback" data-delta="1">＋ Useful response</button><button class="button secondary" data-action="feedback" data-delta="-1">− Needs work</button></div><p class="learning-note">Association strength: <strong>' + (rule.strength > 0 ? '+' : '') + rule.strength + '</strong>. Feedback changes which matching rule is preferred; it does not rewrite the action.</p></div>';
  }

  function missionInfo(id) {
    return {
      explore: { title: 'Into the unknown', caption: 'EXPLORATION', description: 'Cross a rocky landscape, avoid obstacles, and reach the marked destination.', machine: 'exploration', stats:['Rough terrain','Remote base'], color:'#dce8de' },
      search: { title: 'A helping hand', caption: 'SEARCH & ASSIST', description: 'Find a person in the search area, stop safely, and send their location to base.', machine:'service', stats:['Human detection','Safe approach'], color:'#e2ebef' },
      monitor: { title: 'Eyes on the operation', caption: 'INDUSTRIAL MONITORING', description: 'Inspect the worksite, detect rising temperatures, and report a hazard.', machine:'industrial', stats:['Thermal sensing','Hazard reporting'], color:'#eae5dc' }
    }[id];
  }
  function renderMission() {
    const checks = [{title:'Hardware',check:hardwareCheck(),stage:1},{title:'Network',check:networkReady() ? networkCheck() : {ready:false,issues:['Run a network test for this configuration.']},stage:2},{title:'Behavior',check:readiness().behaviour || rulesCheck(),stage:3}];
    const selected = missionInfo(state.missionId);
    return '<div class="mission-grid">' + ['explore','search','monitor'].map(id => {
      const item = missionInfo(id); const active = id === state.missionId;
      return '<article class="mission-card ' + (active ? 'selected' : '') + '"><div class="mission-image" style="background:' + item.color + '">' + missionIllustration(id) + pill(item.caption, '') + '</div><div class="mission-card-body"><h3>' + item.title + '</h3><p>' + item.description + '</p><div class="mission-specs"><span>⌁ ' + item.stats[0] + '</span><span>↗ ' + item.stats[1] + '</span></div><button class="button ' + (active ? 'primary' : 'secondary') + ' full" data-action="mission" data-id="' + id + '" aria-pressed="' + active + '">' + (active ? '✓ Mission selected' : 'Select mission') + '</button></div></article>';
    }).join('') + '</div><div class="mission-select-head"><h2>Before you head out</h2>' + pill(readiness().ready && networkReady() ? 'All systems ready' : 'Preparation needed', readiness().ready && networkReady() ? 'green' : 'orange', true) + '</div><div class="scenario-callout"><strong>' + esc(selected.title) + ':</strong> ' + esc((find('missions', state.missionId) || {}).description || selected.description) + ' The mission uses your installed hardware, actual links, and learned rule priorities.</div><div class="readiness-grid">' + checks.map(item => '<section class="readiness-card"><div class="readiness-top"><h3>' + item.title + '</h3>' + pill(item.check.ready ? 'Ready' : 'Review', item.check.ready ? 'green' : 'orange') + '</div><p>' + esc(item.check.ready ? item.check.summary || 'Ready for this mission.' : listIssues(item.check).join(' ') || 'Review this system.') + '</p><button class="button text" data-action="stage" data-stage="' + item.stage + '">' + (item.check.ready ? 'Review setup' : 'Back to fix') + ' ↗</button></section>').join('') + '</div>' + (!readiness().ready ? '<p class="inline-warning">' + esc(listIssues(readiness()).join(' ')) + '</p>' : '') + '<div style="margin-top:17px">' + chapter(5, 'Robotics combines hardware, networking, and decision rules into a system with a real purpose. A working individual part does not guarantee a successful mission: the whole system must work together.') + '</div>';
  }
  function missionIllustration(id) {
    let svg = '<svg viewBox="0 0 340 160" aria-hidden="true"><path d="M-10 105L83 71L167 98L247 57L350 98V170H-10Z" fill="' + ({explore:'#baccc0',search:'#c3d3d9',monitor:'#d4cbbb'}[id]) + '" opacity=".5"/><path d="M-10 147L108 95L171 112L265 84L350 117" fill="none" stroke="#fbfff8" stroke-width="32" opacity=".5"/>';
    if (id === 'explore') svg += '<path d="M71 113l17-23 27 10 7 17-25 10Z" fill="#9cac9f"/><path d="M215 131l14-13 19 9-4 13Z" fill="#94a99b"/><path d="M260 86V43m0 0 29 8-29 12" stroke="#718f80" stroke-width="2" fill="#e4a775"/><circle cx="181" cy="97" r="20" fill="none" stroke="#92aa9b" stroke-dasharray="3 4"/>';
    if (id === 'search') svg += '<rect x="45" y="57" width="51" height="47" rx="6" fill="#a7bdc8"/><rect x="250" y="70" width="39" height="30" rx="4" fill="#bacbd0"/><circle cx="232" cy="114" r="6" fill="#b18e73"/><path d="M227 122h11l4 20h-20Z" fill="#d49c77"/><path d="M224 145v10m14-10v10" stroke="#66828d" stroke-width="4"/>';
    if (id === 'monitor') svg += '<path d="M66 100V62l38 20v33Z" fill="#a7aba5"/><path d="M104 82l35-20v34l-35 20Z" fill="#b9bcb2"/><path d="M66 62l35-18 38 18-35 20Z" fill="#cdd0c6"/><path d="M237 122V80l36-18v42Z" fill="#aaa99e"/><path d="M249 97v-21" stroke="#e19d6c" stroke-width="5"/><circle cx="249" cy="98" r="6" fill="#e19d6c"/>';
    return svg + '<g transform="translate(159 108) rotate(-16)"><rect x="-20" y="-11" width="40" height="24" rx="6" fill="#5e8790"/><rect x="-24" y="-14" width="9" height="10" rx="3" fill="#2f4d5c"/><rect x="15" y="-14" width="9" height="10" rx="3" fill="#2f4d5c"/><rect x="-24" y="6" width="9" height="10" rx="3" fill="#2f4d5c"/><rect x="15" y="6" width="9" height="10" rx="3" fill="#2f4d5c"/><rect x="-11" y="-7" width="23" height="12" rx="3" fill="#d9eee4"/><circle cx="13" cy="0" r="3" fill="#e2ae7a"/></g></svg>';
  }

  function renderSimulation() {
    if (!sim) sim = E.createSimulation(state.config, state.missionId);
    return '<div class="simulation-layout"><div><section class="mission-scene"><div class="scene-label"><i class="dot"></i>' + missionInfo(state.missionId).caption + ' / Live field view</div><div class="scene-live" id="sim-status">' + pill('Ready to run', 'cyan') + '</div><svg id="mission-svg" viewBox="0 0 800 480" role="img" aria-label="Live top-down robot mission. Robot movement, obstacles, and targets."></svg><div class="timeline" aria-hidden="true"><i id="sim-progress" style="width:0%"></i></div><div class="playback-controls"><div class="playback-buttons"><button class="button primary" data-action="' + (playing ? 'pause' : 'play') + '" id="play-button">' + (playing ? 'Ⅱ Pause' : '▷ Play') + '</button><button class="icon-button" data-action="step" aria-label="Step simulation forward one second" title="Step one second">▹|</button><button class="icon-button" data-action="restart-sim" aria-label="Restart mission" title="Restart mission">↺</button></div><span class="time-display" id="sim-time">00:00 / 00:55</span><label class="sr-only" for="sim-speed">Playback speed</label><select id="sim-speed"><option value="0.5"' + (speed === .5 ? ' selected' : '') + '>0.5× speed</option><option value="1"' + (speed === 1 ? ' selected' : '') + '>1× speed</option><option value="2"' + (speed === 2 ? ' selected' : '') + '>2× speed</option><option value="5"' + (speed === 5 ? ' selected' : '') + '>5× speed</option></select></div></section><div class="simulation-stats"><div class="stat-card"><label>Battery</label><strong id="stat-battery">100<small>%</small></strong></div><div class="stat-card"><label>Temperature</label><strong id="stat-temperature">24<small>°C</small></strong></div><div class="stat-card"><label>Current action</label><strong id="stat-action" style="font-size:13px">Ready</strong></div><div class="stat-card"><label>Network</label><strong id="stat-network" style="font-size:13px">Connected</strong></div></div><section class="panel" style="margin-top:15px"><div class="panel-title"><h3>Mission event log</h3><small>Decisions leave a trail.</small></div><div class="event-log" id="event-log" tabindex="0" aria-label="Mission event log"></div></section></div><aside class="stack"><section class="panel"><div class="panel-title"><h3>Mission objectives</h3>' + pill('LIVE', 'cyan') + '</div><div class="panel-body"><ul class="objective-list" id="live-objectives"></ul></div></section><section class="panel"><div class="panel-title"><h3>Inside this decision</h3></div><div class="panel-body"><div class="trace-list" id="decision-trace"></div></div></section><div class="info-strip"><span class="info-icon" aria-hidden="true">i</span><p>The robot follows your strongest matching rule. Pause and step to see the chain from input to action.</p></div></aside></div>';
  }
  function timeString(seconds) { return String(Math.floor(seconds / 60)).padStart(2, '0') + ':' + String(Math.floor(seconds % 60)).padStart(2, '0'); }
  function simulationSVG() {
    const world = sim.world || {}; const robot = sim.robot || {x:90,y:240};
    const w = world.width || 800; const h = world.height || 480;
    const color = state.missionId === 'monitor' ? '#e9e7de' : state.missionId === 'search' ? '#e3eceb' : '#e8eee1';
    let svg = '<defs><pattern id="field-grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#587963" opacity=".07"/></pattern><filter id="robot-shadow"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#274936" flood-opacity=".2"/></filter></defs><rect width="800" height="480" fill="' + color + '"/><rect width="800" height="480" fill="url(#field-grid)"/><path d="M-30 406C130 327 125 122 303 168S515 366 832 101" stroke="#f5f8ed" stroke-width="74" fill="none" opacity=".65"/><path d="M-30 406C130 327 125 122 303 168S515 366 832 101" stroke="#cbd7c1" stroke-width="1.5" stroke-dasharray="5 10" fill="none" opacity=".8"/>';
    const home = world.home || {x:80,y:240};
    svg += '<g transform="translate(' + home.x + ' ' + home.y + ')"><circle r="36" fill="#d8e9d9" stroke="#a3c3ae" stroke-dasharray="4 5"/><path d="M-18 4l18-17 18 17v17h-36Z" fill="#b8d1bb" stroke="#91b29a"/><path d="M-7 20V5H7v15" fill="#ecf5e8"/><text y="55" text-anchor="middle" font-size="9" fill="#78927e">BASE STATION</text></g>';
    (world.obstacles || []).forEach((obstacle, index) => {
      const x = obstacle.x || 0; const y = obstacle.y || 0; const r = obstacle.radius || obstacle.r || 24;
      const ow = obstacle.width || obstacle.w || r*2; const oh = obstacle.height || obstacle.h || r*2;
      if (state.missionId === 'monitor' || obstacle.type === 'wall') svg += '<g transform="translate(' + x + ' ' + y + ')"><rect x="' + (-ow/2) + '" y="' + (-oh/2+5) + '" width="' + ow + '" height="' + oh + '" rx="5" fill="#b1b3a7"/><rect x="' + (-ow/2) + '" y="' + (-oh/2) + '" width="' + ow + '" height="' + oh + '" rx="5" fill="#ced0c2" stroke="#b0b5a6"/><path d="M-10-10H10M-10-3H10" stroke="#aeb8a5" stroke-width="3"/></g>';
      else svg += '<g transform="translate(' + x + ' ' + y + ')"><ellipse cy="8" rx="' + (r+4) + '" ry="' + (r*.7) + '" fill="#738b7418"/><path d="M' + (-r) + ' 3L' + (-r*.65) + ' ' + (-r*.65) + 'L' + (r*.3) + ' ' + (-r*.85) + 'L' + r + ' ' + (-r*.05) + 'L' + (r*.5) + ' ' + (r*.7) + 'L' + (-r*.55) + ' ' + (r*.6) + 'Z" fill="' + (index%2 ? '#aebfa7' : '#a3b59c') + '" stroke="#91a38b"/><path d="M' + (-r*.65) + ' ' + (-r*.65) + 'L0 0L' + r + ' ' + (-r*.05) + 'M0 0L' + (r*.5) + ' ' + (r*.7) + '" fill="none" stroke="#bdcbb6"/></g>';
    });
    (world.targets || []).forEach((target, index) => {
      const x = target.x || 0; const y = target.y || 0; const done = !!target.done || !!target.found || !!target.visited;
      const type = target.type || target.id || '';
      svg += '<g transform="translate(' + x + ' ' + y + ')"><circle r="28" fill="' + (done ? '#bcd9bd' : '#e5dbc0') + '" opacity=".65"/><circle r="39" fill="none" stroke="' + (done ? '#8db593' : '#c0ad83') + '" stroke-dasharray="3 5"/>';
      if (state.missionId === 'search' || /person/.test(type)) svg += '<circle cy="-8" r="7" fill="#b3957a"/><path d="M-8 3h16l3 20h-22Z" fill="#cf9d70"/><path d="M-6 22v10m12-10v10" stroke="#567985" stroke-width="4"/>';
      else if (state.missionId === 'monitor' || /temp|heat/.test(type)) svg += '<rect x="-16" y="-16" width="32" height="32" rx="5" fill="#a8b5a3"/><path d="M0-9v15" stroke="#ecae77" stroke-width="5"/><circle cy="8" r="6" fill="#ecae77"/>';
      else svg += '<path d="M0 15V-20m0 0 24 7-24 10" stroke="#718c78" stroke-width="2" fill="#deaa76"/>';
      svg += '<text y="54" font-size="8" text-anchor="middle" fill="#819174">' + esc(target.label || (state.missionId === 'search' ? 'PERSON' : state.missionId === 'monitor' ? 'CHECKPOINT' : 'DESTINATION')) + '</text></g>';
    });
    const heading = robot.heading || 0;
    svg += '<g transform="translate(' + robot.x + ' ' + robot.y + ') rotate(' + heading + ')"><path d="M14-12L93-46A100 100 0 0 1 93 46L14 12Z" fill="#75b0a514" stroke="#7baca530" stroke-dasharray="4 7"/><circle r="32" fill="none" stroke="#81ada7" stroke-dasharray="3 5" opacity=".65"/><g filter="url(#robot-shadow)"><rect x="-20" y="-17" width="39" height="34" rx="8" fill="#487680"/><rect x="-19" y="-22" width="12" height="10" rx="3" fill="#244452"/><rect x="7" y="-22" width="12" height="10" rx="3" fill="#244452"/><rect x="-19" y="12" width="12" height="10" rx="3" fill="#244452"/><rect x="7" y="12" width="12" height="10" rx="3" fill="#244452"/><rect x="-13" y="-11" width="26" height="22" rx="5" fill="#d6e9dd"/><rect x="-8" y="-6" width="12" height="12" rx="2" fill="#386474"/><rect x="15" y="-9" width="7" height="18" rx="2" fill="#dfaa77"/><circle cx="20" cy="-5" r="2" fill="#fff0c5"/><circle cx="20" cy="5" r="2" fill="#fff0c5"/></g></g><text x="22" y="456" font-size="8" fill="#91a38b">SIMULATED MAP UNITS</text><g transform="translate(760 421)" fill="#82977c"><path d="M0-16l6 16-6-4-6 4Z"/><text y="15" font-size="8" text-anchor="middle">N</text></g>';
    return svg;
  }
  function updateSimFrame() {
    if (!sim || state.currentStage !== 5 || state.screen !== 'lab') return;
    const scene = document.getElementById('mission-svg'); if (!scene) return;
    scene.innerHTML = simulationSVG();
    const ended = sim.status !== 'running';
    document.getElementById('sim-status').innerHTML = pill(ended ? (sim.status === 'success' ? 'Mission complete' : 'Mission ended') : playing ? 'Running' : 'Paused', ended && sim.status !== 'success' ? 'orange' : playing ? 'green' : 'cyan', true);
    document.getElementById('sim-progress').style.width = Math.min(100, sim.time / sim.duration * 100) + '%';
    document.getElementById('sim-time').textContent = timeString(sim.time) + ' / ' + timeString(sim.duration);
    document.getElementById('stat-battery').innerHTML = Math.max(0, Math.round(sim.robot.battery)) + '<small>%</small>';
    document.getElementById('stat-temperature').innerHTML = Math.round(sim.robot.temperature || 24) + '<small>°C</small>';
    document.getElementById('stat-action').textContent = label('responses', sim.robot.action) || 'Waiting';
    document.getElementById('stat-network').textContent = sim.network && (sim.network.ready || sim.network.connected) ? 'Connected' : 'Out of range';
    document.getElementById('live-objectives').innerHTML = (sim.objectives || []).map(objective => '<li class="' + (objective.done ? 'complete' : '') + '"><span class="objective-box" aria-hidden="true">' + (objective.done ? '✓' : '') + '</span><span>' + esc(objective.label) + '</span></li>').join('');
    document.getElementById('decision-trace').innerHTML = (sim.trace && sim.trace.length ? sim.trace.slice(-5) : [{stage:'sensor',label:'Waiting for a stimulus',detail:'Press play or step to follow the first decision.'}]).map((step, index) => '<div class="trace-item"><span class="trace-mark" aria-hidden="true">' + String(index+1).padStart(2,'0') + '</span><div><h4>' + esc(step.label || step.stage) + '</h4><p>' + esc(step.detail) + '</p></div></div>').join('');
    const events = sim.events || [];
    const last = events[events.length-1];
    if ((last && last.id !== lastEventId) || !document.getElementById('event-log').children.length) {
      const log = document.getElementById('event-log');
      log.innerHTML = events.length ? events.slice(-40).map(event => '<div class="event-entry ' + esc(event.type) + '"><time>' + timeString(event.time || 0) + '</time><span>' + esc(event.message) + '</span></div>').join('') : '<div class="empty-state">Your mission’s decisions will appear here.</div>';
      log.scrollTop = log.scrollHeight;
      if (last && last.id !== lastEventId) { lastEventId = last.id; announce(last.message); }
    }
    const play = document.getElementById('play-button');
    if (play) { play.dataset.action = playing ? 'pause' : 'play'; play.textContent = playing ? 'Ⅱ Pause' : '▷ Play'; play.disabled = ended; }
    const step = app.querySelector('[data-action="step"]'); if (step) step.disabled = ended;
  }
  function startSimulation() {
    if (!sim) sim = E.createSimulation(state.config, state.missionId);
    if (sim.status !== 'running') return;
    playing = true;
    if (!timer) timer = setInterval(() => {
      if (!playing || !sim) return;
      E.tick(sim, .1 * speed);
      if (sim.status !== 'running') completeSimulation();
      else updateSimFrame();
    }, 100);
    updateSimFrame();
  }
  function pauseSimulation() { playing = false; if (timer) clearInterval(timer); timer = null; }
  function completeSimulation() {
    pauseSimulation(); state.report = sim.report || E.buildReport(sim); save();
    announce('Mission ended. Your report is ready.');
    render();
  }
  function renderResults() {
    const report = state.report;
    if (!report) return info('Finish the mission to see what your robot learned.');
    const names = {hardware:'Hardware integrity',network:'Network reliability',behaviour:'Behavior performance',completion:'Mission completion'};
    const descriptions = {hardware:'Did your components support the work?',network:'Did messages reach a useful node?',behaviour:'Did trained responses help the mission?',completion:'How many objectives did you complete?'};
    const reasons = (report.reasons || []).map(textIssue);
    return '<section class="results-hero"><div><span class="eyebrow">Experiment ' + machineInfo().number + ' / Mission debrief</span><h2>' + (report.overall >= 75 ? 'Look what your ideas can do.' : 'A useful result. A new direction.') + '</h2><p>' + esc(report.summary) + '</p></div><div class="overall-score"><strong>' + Math.round(report.overall) + '</strong><span>Overall score</span></div></section><div class="score-grid">' + ['hardware','network','behaviour','completion'].map(key => '<section class="score-card"><div class="score-label">' + names[key] + '</div><div class="score-value"><strong>' + Math.round(report.scores[key] || 0) + '</strong><span>/ 100</span></div><div class="mini-bar"><i style="width:' + Math.max(0, Math.min(100, report.scores[key] || 0)) + '%;background:' + ((report.scores[key] || 0) < 60 ? '#d8a57c' : '#74a994') + '"></i></div><p>' + descriptions[key] + '</p></section>').join('') + '</div><div class="workbench even"><section class="panel"><div class="panel-title"><h2>What happened — and why</h2>' + pill('Evidence', 'cyan') + '</div><div class="panel-body"><ul class="reason-list">' + (reasons.length ? reasons.map(reason => '<li>' + esc(reason) + '</li>').join('') : '<li>Your robot’s outcome came from the hardware, network, and responses you selected.</li>') + '</ul><div class="divider"></div><ul class="objective-list">' + (report.objectives || []).map(objective => '<li class="' + (objective.done ? 'complete' : '') + '"><span class="objective-box" aria-hidden="true">' + (objective.done ? '✓' : '–') + '</span>' + esc(objective.label) + '</li>').join('') + '</ul></div></section><section class="panel"><div class="panel-title"><h2>Take this back to the workbench</h2></div><div class="panel-body"><div class="learning-cards"><div class="learning-card"><h4>Hardware makes a response possible.</h4><p>Sensors supply inputs; processors select rules; actuators turn the output into action. Missing one link changes the whole system.</p></div><div class="learning-card"><h4>A connection depends on the environment.</h4><p>A short-range link can work at base and disappear in the field. Match the network to the mission.</p></div><div class="learning-card"><h4>A learned response is only as useful as its rule.</h4><p>Feedback changes priority. It cannot turn an unsafe action into a safe one. Edit the rule, test again, and compare.</p></div></div><button class="button secondary full" style="margin-top:19px" data-action="stage" data-stage="3">Refine your training <span aria-hidden="true">↗</span></button></div></section></div>';
  }

  function goStage(index) {
    if (!gate(index)) { toast('Finish the previous checks to unlock this step.'); return; }
    if (index !== 5) pauseSimulation();
    state.screen = 'lab'; state.currentStage = index; save(); render();
    window.scrollTo({top:0, behavior:'instant'});
    const main = document.getElementById('main'); if (main) main.focus({preventScroll:true});
  }
  function showInfo(kind) {
    const content = document.getElementById('dialog-content');
    if (kind === 'objectives') content.innerHTML = '<span class="eyebrow">A little theory. A lot of doing.</span><h2 id="dialog-title">What will you learn?</h2><p>By the end of your experiment, you will be able to:</p><ul><li>Explain how sensors, processors, actuators, and power work together in a robot.</li><li>Choose a network module based on range and reliability, and connect real network roles.</li><li>Write stimulus–response rules and explain how feedback changes an association.</li><li>Use mission evidence to understand a success or failure, then improve the design.</li></ul><p>Linked to Chapters 2–5 of your CS & AI study guide.</p><a class="button secondary small" href="https://github.com/user-github-me/cs-ai-project-01/raw/refs/heads/main/assets/study-guide/BlueImpulse_Study_Guide.pdf" target="_blank" rel="noopener">Open the Blue Impulse study guide ↗</a>';
    else content.innerHTML = '<span class="eyebrow">Welcome to your workbench</span><h2 id="dialog-title">From idea to action.</h2><p>Take 5–10 minutes to build, connect, train, and test a robot. Every choice affects the result.</p><div class="instructions-grid">' + [['Choose & build','Pick a machine, then add parts. The starter build is a useful place to begin; inspect or change any part.'],['Connect & test','Select a network module, connect a destination node, and test the connection.'],['Train a response','Write at least 3 IF–THEN rules. Test a stimulus and reward or weaken the response.'],['Run & reflect','Choose a mission, then use play, pause, step, and speed controls. Read the report and try a new idea.']].map((item,index) => '<div class="instruction-row"><span class="instruction-num">' + (index+1) + '</span><div><h3>' + item[0] + '</h3><p>' + item[1] + '</p></div></div>').join('') + '</div><p><strong>Good to know:</strong> everything is simulated locally. Your progress saves on this device when browser storage is available.</p>';
    document.getElementById('info-dialog').showModal();
  }
  function changeMachine(id) {
    if (!MACHINE_COPY[id]) return;
    if (id !== state.config.machineId) {
      state.config = E.createConfig(id); state.missionId = {exploration:'explore',service:'search',industrial:'monitor'}[id];
      selectedNode = {exploration:'base',service:'controlComputer',industrial:'server'}[id];
      invalidate('hardware'); inspected = 'microcontroller'; editingRule = null; catalogCategory = 'all';
    }
    state.machineChosen = true; save(); render();
  }
  function addLink() {
    const source = document.getElementById('link-source').value;
    const target = document.getElementById('link-target').value;
    const module = document.getElementById('link-module').value;
    if (!target || !module) return;
    if (source === target) { toast('Choose two different nodes to make a connection.'); return; }
    const network = state.config.network;
    if (network.links.some(link => link.from === source && link.to === target && link.module === module)) { toast('That connection is already on your map.'); return; }
    if (!network.nodes.includes(target)) network.nodes.push(target);
    if (source !== 'robot' && !network.nodes.includes(source)) network.nodes.push(source);
    network.links.push({id:'link-' + Date.now() + '-' + network.links.length,from:source,to:target,module,enabled:true});
    selectedNode = target; invalidate('network'); render(); announce('Connected ' + (source === 'robot' ? 'robot' : label('nodes', source)) + ' to ' + label('nodes', target) + ' with ' + label('modules', module) + '. Test the link next.');
  }
  function addRule() {
    const stimulus = document.getElementById('rule-stimulus').value;
    const response = document.getElementById('rule-response').value;
    const index = state.config.rules.findIndex(rule => rule.id === editingRule);
    const rule = {id:editingRule || 'rule-' + Date.now() + '-' + state.config.rules.length,stimulus,response,strength:0,enabled:true};
    if (index >= 0) state.config.rules[index] = rule;
    else state.config.rules.push(rule);
    editingRule = null; invalidate('training'); render(); announce('Rule saved. If ' + label('stimuli', stimulus) + ', then ' + label('responses', response) + '.');
  }
  function testRule() {
    const stimulus = document.getElementById('test-stimulus').value;
    const result = typeof E.testRule === 'function' ? E.testRule(state.config, stimulus) : null;
    const match = result && (result.rule || result.matchedRule) || E.findMatchingRule(state.config, [stimulus]);
    ruleTest = {stimulus,ruleId:match && match.id || null,explanation:result && (result.explanation || result.message) || ''};
    render(); announce(match ? 'Response: ' + label('responses', match.response) + '. Give feedback to change this association.' : 'No compatible rule matched this stimulus.');
  }
  function feedback(delta) {
    if (!ruleTest || !ruleTest.ruleId) return;
    const rememberedTest = clone(ruleTest);
    const updated = E.applyFeedback(state.config, ruleTest.ruleId, delta);
    if (updated && updated.rules) state.config = updated;
    invalidate('training'); ruleTest = rememberedTest; render();
    const rule = state.config.rules.find(item => item.id === ruleTest.ruleId);
    announce('Association ' + (delta > 0 ? 'strengthened' : 'weakened') + '. Strength is now ' + rule.strength + '.');
    toast(delta > 0 ? 'Useful response reinforced.' : 'Association weakened. You can edit the response.');
  }
  function resetLab() {
    pauseSimulation(); sim = null; state = freshState(); networkResult = null; ruleTest = null; editingRule = null; canContinue = false;
    try { localStorage.removeItem(STORAGE_KEY); } catch (_) { storageAvailable = false; }
    document.getElementById('reset-dialog').close(); render(); announce('Saved progress cleared. Your workbench is ready.');
  }
  function confirmStart(kind) {
    resetIntent = kind;
    document.getElementById('reset-title').textContent = kind === 'new' ? 'Start a new mission?' : 'Start over?';
    document.getElementById('reset-description').textContent = kind === 'new' ? 'This replaces your saved robot, training rules, and mission progress with a fresh experiment. Your current build stays safe if you cancel.' : 'This clears the saved robot, training rules, and mission progress on this device.';
    document.querySelector('[data-action="confirm-reset"]').textContent = kind === 'new' ? 'Start new mission' : 'Reset the lab';
    document.getElementById('reset-dialog').showModal();
  }
  function beginNewMission() {
    pauseSimulation(); sim = null; state = freshState(); state.screen = 'lab'; state.machineChosen = true;
    networkResult = null; ruleTest = null; editingRule = null; catalogCategory = 'all'; inspected = 'microcontroller'; selectedNode = 'base';
    document.getElementById('reset-dialog').close(); save(); render(); window.scrollTo(0,0);
    announce('A new mission is ready. Choose your machine.');
  }
  function launch() {
    if (!readiness().ready || !networkReady()) { toast('Finish your readiness checks before launch.'); return; }
    state.missionAccepted = true; state.report = null; sim = E.createSimulation(state.config, state.missionId); lastEventId = '';
    state.currentStage = 5; save(); render(); startSimulation();
    window.scrollTo({top:0,behavior:'instant'}); announce('Mission launched. Your robot is following its trained rules.');
  }

  document.addEventListener('click', event => {
    const button = event.target.closest('[data-action]');
    if (!button || button.disabled) return;
    const action = button.dataset.action; const id = button.dataset.id;
    if (action === 'home') { pauseSimulation(); state.screen = 'landing'; render(); return; }
    if (action === 'howto' || action === 'objectives') { showInfo(action); return; }
    if (action === 'reset') { confirmStart('reset'); return; }
    if (action === 'cancel-reset') { document.getElementById('reset-dialog').close(); return; }
    if (action === 'confirm-reset') { if (resetIntent === 'new') beginNewMission(); else resetLab(); return; }
    if (action === 'start') { if (canContinue) confirmStart('new'); else beginNewMission(); return; }
    if (action === 'continue') { state.screen = 'lab'; state.currentStage = Math.min(state.currentStage, maxStage()); if (state.currentStage === 5 && !sim) sim = E.createSimulation(state.config, state.missionId); render(); window.scrollTo(0,0); return; }
    if (action === 'stage') { goStage(Number(button.dataset.stage)); return; }
    if (action === 'next') { if (state.currentStage === 0) state.machineChosen = true; goStage(state.currentStage+1); return; }
    if (action === 'back') { goStage(Math.max(0,state.currentStage-1)); return; }
    if (action === 'machine') { changeMachine(id); return; }
    if (action === 'category') { catalogCategory = id; render(); return; }
    if (action === 'inspect') { inspected = id; if (state.currentStage === 1) render(); else toast(label('components', id) + ': ' + (find('components', id)?.description || '')); return; }
    if (action === 'component') {
      const component = find('components', id); if (!component || component.compatible && !component.compatible.includes(state.config.machineId)) return;
      const index = state.config.components.indexOf(id);
      if (index >= 0) state.config.components.splice(index,1); else state.config.components.push(id);
      inspected = id; invalidate('hardware'); render(); announce(component.label + (index >= 0 ? ' removed.' : ' installed.')); return;
    }
    if (action === 'starter-hardware') {
      state.config.components = recommended().components.slice(); invalidate('hardware'); render();
      toast('Starter hardware installed. Inspect a part to discover its role.'); announce('Starter hardware installed. Network and training are yours to build.'); return;
    }
    if (action === 'module') {
      const modules = state.config.network.modules; const index = modules.indexOf(id);
      if (index >= 0) modules.splice(index,1); else modules.push(id);
      invalidate('network'); render(); return;
    }
    if (action === 'node') { selectedNode = id; render(); return; }
    if (action === 'add-link') { addLink(); return; }
    if (action === 'remove-link') { state.config.network.links = state.config.network.links.filter(link => link.id !== id); invalidate('network'); render(); return; }
    if (action === 'test-network') {
      networkResult = networkCheck(); state.networkTestedFingerprint = networkResult.ready ? networkFingerprint() : ''; save(); render();
      announce(networkResult.ready ? 'Network test passed. You can continue to training.' : 'Network test failed. ' + listIssues(networkResult).join(' ')); return;
    }
    if (action === 'add-rule') { addRule(); return; }
    if (action === 'cancel-rule') { editingRule = null; render(); return; }
    if (action === 'rule-edit') { editingRule = id; render(); document.getElementById('rule-stimulus').focus(); return; }
    if (action === 'rule-delete') { state.config.rules = state.config.rules.filter(rule => rule.id !== id); invalidate('training'); render(); return; }
    if (action === 'rule-up' || action === 'rule-down') {
      const index = state.config.rules.findIndex(rule => rule.id === id); const destination = index + (action === 'rule-up' ? -1 : 1);
      if (index >= 0 && destination >= 0 && destination < state.config.rules.length) { const rule = state.config.rules.splice(index,1)[0]; state.config.rules.splice(destination,0,rule); invalidate('training'); render(); }
      return;
    }
    if (action === 'test-rule') { testRule(); return; }
    if (action === 'feedback') { feedback(Number(button.dataset.delta)); return; }
    if (action === 'mission') { state.missionId = id; invalidate('mission'); render(); return; }
    if (action === 'launch') { launch(); return; }
    if (action === 'play') { startSimulation(); return; }
    if (action === 'pause') { pauseSimulation(); updateSimFrame(); return; }
    if (action === 'step') { pauseSimulation(); if (sim && sim.status === 'running') E.tick(sim,1); if (sim.status !== 'running') completeSimulation(); else updateSimFrame(); return; }
    if (action === 'restart-sim') { pauseSimulation(); sim = E.createSimulation(state.config,state.missionId); state.report = null; lastEventId = ''; save(); render(); announce('Mission restarted and paused.'); return; }
    if (action === 'results') { if (state.report) goStage(6); return; }
    if (action === 'new-build') { beginNewMission(); return; }
  });
  document.addEventListener('change', event => {
    if (event.target.id === 'sim-speed') { speed = Number(event.target.value); announce('Playback speed ' + speed + ' times.'); }
    if (event.target.id === 'link-target') selectedNode = event.target.value;
  });
  document.addEventListener('keydown', event => {
    const target = event.target.closest('g[role="button"]');
    if (target && (event.key === 'Enter' || event.key === ' ')) { event.preventDefault(); target.dispatchEvent(new MouseEvent('click',{bubbles:true})); }
  });
  document.addEventListener('visibilitychange', () => { if (document.hidden && playing) { pauseSimulation(); updateSimFrame(); } });
  window.addEventListener('beforeunload', () => { if (state.screen === 'lab') save(); });
  window.RoverLabApp = Object.freeze({ getState: () => clone(Object.assign({},state,{simulation:sim,playing,speed,unlockedStage:maxStage()})), storageKey: STORAGE_KEY });
  render();
})();
