(function (root, factory) {
  'use strict';
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.RoverLabEngine = api;
})(typeof window !== 'undefined' ? window : globalThis, function () {
  'use strict';

  // All units and distances are teaching-scale approximations, not electrical specifications.
  var VERSION = 1;
  var ALL = ['exploration', 'service', 'industrial'];
  var machines = [
    { id: 'exploration', label: 'Exploration rover', description: 'Survey unfamiliar ground, collect a reading and bring the research home.', required: ['processor', 'memory', 'chassis', 'battery', 'power', 'mobility', 'obstacleSensor', 'navigation', 'researchSensor'], missionId: 'explore', suggestedRules: [{ stimulus: 'obstacle', response: 'stopTurn' }, { stimulus: 'destination', response: 'return' }, { stimulus: 'batteryLow', response: 'return' }] },
    { id: 'service', label: 'Service robot', description: 'Find a person, contact the control computer and return through the handoff zone.', required: ['processor', 'memory', 'chassis', 'battery', 'power', 'mobility', 'personSensor', 'navigation'], missionId: 'search', suggestedRules: [{ stimulus: 'person', response: 'stopReport' }, { stimulus: 'destination', response: 'return' }, { stimulus: 'batteryLow', response: 'return' }, { stimulus: 'obstacle', response: 'stopTurn' }] },
    { id: 'industrial', label: 'Industrial machine', description: 'Watch a powered process, stop dangerous heating and report to a server.', required: ['processor', 'memory', 'chassis', 'battery', 'power', 'actuation', 'temperature'], missionId: 'monitor', suggestedRules: [{ stimulus: 'tempHigh', response: 'stopReport' }, { stimulus: 'safeTemp', response: 'move' }, { stimulus: 'networkLost', response: 'indicator' }] }
  ];
  function part(id, label, category, power, capabilities, description, compatible, requires) {
    return { id: id, label: label, category: category, power: power, capabilities: capabilities, description: description, compatible: compatible || ALL.slice(), requires: requires || [] };
  }
  var components = [
    part('microcontroller', 'Microcontroller', 'Processing', 1, ['processor', 'indicator'], 'A low-power controller reads simple sensors and runs your rules. Camera vision needs the single-board computer.'),
    part('sbc', 'Single-board computer', 'Processing', 4, ['processor', 'visionProcessor', 'indicator'], 'More processing power enables camera-based person recognition, with a larger energy cost.'),
    part('memory', 'Memory', 'Processing', 1, ['memory'], 'Stores the rule table, sensor readings and route history. This model treats memory as an explicit module.'),
    part('wheels', 'Wheels', 'Movement', 0, ['wheels'], 'Efficient movement on firm ground. Wheels need motors and a chassis.', ['exploration', 'service'], ['motors', 'chassis']),
    part('tracks', 'Tracks', 'Movement', 0, ['tracks'], 'Slower movement with better traction around rough obstacles. The service chassis has no track mounts.', ['exploration', 'industrial'], ['motors', 'chassis']),
    part('motors', 'Motors', 'Movement', 4, ['actuation'], 'Turn wheels or tracks, or drive the stationary industrial process.'),
    part('servos', 'Servos', 'Movement', 2, ['precisionMotion'], 'Position a joint accurately. The robot arm needs servos.'),
    part('ultrasonic', 'Ultrasonic sensor', 'Sensors', 1, ['obstacleSensor', 'objectSensor'], 'Measures distance using returning sound; it detects objects but does not identify a person.'),
    part('infrared', 'Infrared sensor', 'Sensors', 1, ['obstacleSensor', 'objectSensor'], 'Detects nearby surfaces using reflected infrared light.'),
    part('camera', 'Camera', 'Sensors', 3, ['obstacleSensor', 'objectSensor', 'researchSensor', 'navigation'], 'Provides images. A single-board computer is needed here to analyse images and recognise people.', ALL.slice(), ['sbc']),
    part('temp', 'Temperature sensor', 'Sensors', 1, ['temperature', 'researchSensor'], 'Measures temperature. Its reading can trigger a rule; the sensor cannot stop a motor by itself.'),
    part('light', 'Light sensor', 'Sensors', 1, ['lightSensor', 'researchSensor'], 'Measures light intensity and can identify a dark area.'),
    part('gps', 'GPS receiver', 'Sensors', 2, ['navigation'], 'Gives a position fix so a mobile robot can locate a destination and return.', ['exploration', 'service']),
    part('battery', 'Battery', 'Energy', 0, ['battery', 'batteryMonitor'], 'Stores energy and reports its charge. This teaching battery supplies up to 24 power units.'),
    part('solar', 'Solar panel', 'Energy', 0, ['solar'], 'Replaces up to 2 energy units during daylight. It does not replace the battery or increase its peak output.', ['exploration'], ['battery']),
    part('power', 'Power distribution', 'Energy', 0.5, ['power'], 'Delivers battery power to each module. The 24-unit output limit must cover the complete design.'),
    part('chassis', 'Chassis', 'Structure', 0, ['chassis'], 'The frame supports the electronics and moving parts.'),
    part('arm', 'Robotic arm', 'Structure', 2, ['arm'], 'Manipulates a nearby object. Requires servos and a chassis.', ALL.slice(), ['servos', 'chassis']),
    part('casing', 'Protective casing', 'Structure', 0, ['protection'], 'Protects the electronics and reduces damage from a collision.')
  ];
  var modules = [
    { id: 'wifi', label: 'Wi-Fi', description: 'A fast local wireless link; walls and distance weaken it.', range: 290, reliability: 0.96, power: 2, latency: 25 },
    { id: 'bluetooth', label: 'Bluetooth', description: 'A low-power short-range link. A distant base will need a relay or a different radio.', range: 115, reliability: 0.94, power: 1, latency: 55 },
    { id: 'radio', label: 'Radio', description: 'Long-range, low-bandwidth telemetry works well for rover status and research readings.', range: 780, reliability: 0.97, power: 2, latency: 90 },
    { id: 'ethernet', label: 'Ethernet', description: 'A reliable cable within 280 map units. A travelling robot can move beyond its tether.', range: 280, reliability: 0.995, power: 1, latency: 5 },
    { id: 'cellular', label: 'Cellular', description: 'Wide-area communication with greater power use and delay.', range: 1800, reliability: 0.95, power: 4, latency: 120 }
  ];
  var nodes = [
    { id: 'gateway', label: 'Gateway', description: 'Relays packets between network links. It is not the final mission recipient.', x: 395, y: 125 },
    { id: 'server', label: 'Server', description: 'Receives and stores industrial alerts.', x: 690, y: 110 },
    { id: 'base', label: 'Base station', description: 'Receives the exploration rover’s research and status.', x: 95, y: 240 },
    { id: 'otherRobot', label: 'Another robot', description: 'A peer can relay a route, but does not replace the required base or control computer.', x: 580, y: 380 },
    { id: 'controlComputer', label: 'Control computer', description: 'Receives a service robot’s person report and coordinates assistance.', x: 120, y: 360 }
  ];
  var stimuli = [
    { id: 'obstacle', label: 'Obstacle detected', description: 'A distance or vision sensor sees an object ahead.', requires: ['obstacleSensor'] },
    { id: 'person', label: 'Person detected', description: 'The camera and computer recognise a person.', requires: ['personSensor'] },
    { id: 'batteryLow', label: 'Low battery', description: 'Charge falls below 25%.', requires: ['batteryMonitor'] },
    { id: 'tempHigh', label: 'High temperature', description: 'Temperature reaches 42 °C.', requires: ['temperature'] },
    { id: 'destination', label: 'Destination reached', description: 'Navigation confirms arrival at the mission site.', requires: ['navigation'] },
    { id: 'networkLost', label: 'Connection lost', description: 'No usable route reaches the required recipient.', requires: ['network'] },
    { id: 'lightLow', label: 'Low light', description: 'A light sensor reads less than 20%.', requires: ['lightSensor'] },
    { id: 'object', label: 'Object detected', description: 'A proximity or vision sensor detects an object.', requires: ['objectSensor'] },
    { id: 'safeTemp', label: 'Temperature safe', description: 'The stopped industrial process cools to 30 °C.', requires: ['temperature'] }
  ];
  var responses = [
    { id: 'stop', label: 'Stop', description: 'Stop movement or switch off the industrial motor.', requires: ['actuation'] },
    { id: 'move', label: 'Move / run', description: 'Move toward the current navigation goal, or run the industrial motor.', requires: ['actuation'] },
    { id: 'left', label: 'Turn left', description: 'Steer left of the current route for a short interval.', requires: ['mobility'] },
    { id: 'right', label: 'Turn right', description: 'Steer right of the current route for a short interval.', requires: ['mobility'] },
    { id: 'reverse', label: 'Reverse', description: 'Drive away from the current goal for a short interval.', requires: ['mobility'] },
    { id: 'message', label: 'Send message', description: 'Attempt a packet to the mission recipient. It can fail when the route is unavailable.', requires: ['network'] },
    { id: 'indicator', label: 'Show indicator', description: 'Light the controller’s status indicator; this does not send a packet.', requires: ['indicator'] },
    { id: 'return', label: 'Return to base', description: 'Use navigation and the drive system to change the goal to the starting base.', requires: ['mobility', 'navigation'] },
    { id: 'wait', label: 'Wait', description: 'Pause and keep observing the same stimulus.', requires: [] },
    { id: 'arm', label: 'Use arm', description: 'Operate the arm to handle a nearby object.', requires: ['arm', 'precisionMotion'] },
    { id: 'stopTurn', label: 'Stop, then turn', description: 'Brake and steer around a sensed obstacle before continuing toward the goal.', requires: ['mobility', 'obstacleSensor'] },
    { id: 'stopReport', label: 'Stop and report', description: 'Stop the motor and try to report the event through the configured network.', requires: ['actuation', 'network'] }
  ];
  var missions = [
    { id: 'explore', machineId: 'exploration', label: 'Survey & return', description: 'Reach the research site, collect a sensor reading, transmit it to the base and return safely.', targetNode: 'base', duration: 55, requiredStimuli: ['obstacle', 'destination', 'batteryLow'] },
    { id: 'search', machineId: 'service', label: 'Search & assist', description: 'Detect the person, send a report to the control computer, reach them and return to the handoff zone.', targetNode: 'controlComputer', duration: 55, requiredStimuli: ['person', 'destination', 'batteryLow'] },
    { id: 'monitor', machineId: 'industrial', label: 'Monitor & protect', description: 'Detect heating, stop the process, deliver an alert and restart only after it cools.', targetNode: 'server', duration: 50, requiredStimuli: ['tempHigh', 'safeTemp', 'networkLost'] }
  ];
  var catalogs = { machines: machines, components: components, modules: modules, nodes: nodes, stimuli: stimuli, responses: responses, missions: missions };
  function index(list) { var map = Object.create(null); list.forEach(function (item) { map[item.id] = item; }); return map; }
  var by = {}; Object.keys(catalogs).forEach(function (key) { by[key] = index(catalogs[key]); });
  function clamp(value, min, max) { return Math.min(max, Math.max(min, value)); }
  function unique(list) { return Array.from(new Set(list)); }
  function copy(value) { return JSON.parse(JSON.stringify(value)); }
  function number(value, fallback) { return typeof value === 'number' && Number.isFinite(value) ? value : fallback; }
  function distance(a, b) { return Math.hypot(a.x - b.x, a.y - b.y); }
  function label(id) { var item = by.components[id] || by.modules[id] || by.nodes[id] || by.stimuli[id] || by.responses[id]; return item ? item.label : id; }
  var capabilityLabels = { processor: 'a processor', memory: 'memory', chassis: 'a chassis', battery: 'a battery', power: 'power distribution', mobility: 'motors with wheels or tracks', actuation: 'a motor', obstacleSensor: 'an obstacle sensor', navigation: 'GPS or camera navigation', researchSensor: 'a camera, temperature sensor or light sensor', personSensor: 'a camera with a single-board computer', temperature: 'a temperature sensor', lightSensor: 'a light sensor', network: 'a communication module', precisionMotion: 'servos', batteryMonitor: 'a battery monitor', indicator: 'a processor indicator', arm: 'a robotic arm', objectSensor: 'an object sensor' };
  function createConfig(machineId) {
    var machine = by.machines[machineId] || machines[0];
    return { version: VERSION, machineId: machine.id, name: machine.label, missionId: machine.missionId, components: [], network: { modules: [], nodes: [], links: [] }, rules: [] };
  }
  function validateConfig(raw) {
    raw = raw && typeof raw === 'object' ? raw : {};
    var config = createConfig(raw.machineId);
    config.name = typeof raw.name === 'string' ? raw.name.slice(0, 60) : config.name;
    config.components = unique((Array.isArray(raw.components) ? raw.components : []).filter(function (id) { return typeof id === 'string' && Object.prototype.hasOwnProperty.call(by.components, id); }));
    var net = raw.network && typeof raw.network === 'object' ? raw.network : {};
    config.network.modules = unique((Array.isArray(net.modules) ? net.modules : []).filter(function (id) { return Object.prototype.hasOwnProperty.call(by.modules, id); }));
    config.network.nodes = unique((Array.isArray(net.nodes) ? net.nodes : []).filter(function (id) { return Object.prototype.hasOwnProperty.call(by.nodes, id); }));
    config.network.links = (Array.isArray(net.links) ? net.links : []).filter(function (link) { return link && typeof link === 'object'; }).slice(0, 40).map(function (link, i) {
      return { id: typeof link.id === 'string' ? link.id.slice(0, 80) : 'link-' + (i + 1), from: String(link.from || 'robot'), to: String(link.to || ''), module: String(link.module || ''), enabled: link.enabled !== false };
    });
    config.rules = (Array.isArray(raw.rules) ? raw.rules : []).filter(function (rule) { return rule && typeof rule === 'object'; }).slice(0, 40).map(function (rule, i) {
      return { id: typeof rule.id === 'string' ? rule.id.slice(0, 80) : 'rule-' + (i + 1), stimulus: String(rule.stimulus || ''), response: String(rule.response || ''), strength: clamp(number(rule.strength, 0), -5, 5), enabled: rule.enabled !== false };
    });
    return config;
  }
  function getCapabilities(raw) {
    var config = validateConfig(raw), caps = [];
    config.components.forEach(function (id) { var item = by.components[id]; if (item.compatible.indexOf(config.machineId) >= 0 && item.requires.every(function (dep) { return config.components.indexOf(dep) >= 0; })) caps = caps.concat(item.capabilities); });
    if (caps.indexOf('actuation') >= 0 && caps.indexOf('chassis') >= 0 && (caps.indexOf('wheels') >= 0 || caps.indexOf('tracks') >= 0)) caps.push('mobility');
    if (config.components.indexOf('camera') >= 0 && caps.indexOf('visionProcessor') >= 0) caps.push('personSensor');
    if (config.network.modules.length) caps.push('network');
    return unique(caps);
  }
  function checkHardware(raw) {
    var config = validateConfig(raw), caps = getCapabilities(config), machine = by.machines[config.machineId], issues = [], warnings = [];
    var missing = machine.required.filter(function (cap) { return caps.indexOf(cap) < 0; });
    missing.forEach(function (cap) { issues.push('Add ' + (capabilityLabels[cap] || cap) + '.'); });
    config.components.forEach(function (id) {
      var item = by.components[id];
      if (item.compatible.indexOf(config.machineId) < 0) issues.push(item.label + ' does not fit this machine’s teaching chassis.');
      item.requires.forEach(function (dep) { if (config.components.indexOf(dep) < 0) issues.push(item.label + ' needs ' + label(dep) + '.'); });
    });
    if (config.components.indexOf('wheels') >= 0 && config.components.indexOf('tracks') >= 0) issues.push('Choose wheels or tracks: this chassis supports one drive system.');
    if (config.components.indexOf('microcontroller') >= 0 && config.components.indexOf('sbc') >= 0) warnings.push('Both processors work, but the extra controller uses power; one processor is enough for this mission.');
    var demand = config.components.reduce(function (sum, id) { return sum + by.components[id].power; }, 0) + config.network.modules.reduce(function (sum, id) { return sum + by.modules[id].power; }, 0);
    var capacity = caps.indexOf('battery') >= 0 && caps.indexOf('power') >= 0 ? 24 : 0;
    if (capacity && demand > capacity) issues.push('Power demand is ' + demand + ' units, above the ' + capacity + '-unit supply. Remove a high-power module.');
    else if (capacity && demand > capacity * 0.85) warnings.push('Less than 15% power reserve: acceleration and reliable communication will be reduced.');
    if (config.network.modules.indexOf('ethernet') >= 0 && config.machineId !== 'industrial') warnings.push('Ethernet is a tether: check whether the whole mission stays within cable range.');
    if (config.components.indexOf('casing') < 0) warnings.push('A protective casing would reduce collision damage.');
    var score = clamp(Math.round(100 - issues.length * 15 - (capacity && demand / capacity > 0.85 ? 6 : 0)), 0, 100);
    return { ready: issues.length === 0, score: score, issues: unique(issues), warnings: warnings, summary: issues.length ? 'Hardware needs ' + issues.length + ' change' + (issues.length === 1 ? '' : 's') + '.' : 'Processor, sensors, actuators and energy supply are ready.', capabilities: caps, missing: missing, power: { demand: demand, capacity: capacity, reserve: capacity - demand, units: 'simplified power units', solarCredit: caps.indexOf('solar') >= 0 ? 2 : 0 } };
  }
  function startPosition(machineId) { return machineId === 'industrial' ? { x: 490, y: 245 } : { x: 95, y: 240 }; }
  function checkNetwork(raw, position, context) {
    var config = validateConfig(raw), mission = by.missions[by.machines[config.machineId].missionId], robot = position || startPosition(config.machineId), issues = [], warnings = [], graph = Object.create(null);
    graph.robot = [];
    context = context || {};
    config.network.nodes.forEach(function (id) { graph[id] = []; });
    var links = config.network.links.map(function (link) {
      var moduleInfo = by.modules[link.module], a = link.from === 'robot' ? robot : by.nodes[link.from], b = link.to === 'robot' ? robot : by.nodes[link.to];
      var result = Object.assign({}, link, { available: false, status: 'invalid', distance: a && b ? Math.round(distance(a, b)) : 0, range: moduleInfo ? moduleInfo.range : 0, reliability: 0, reason: '' });
      if (!link.enabled) { result.status = 'disabled'; result.reason = 'This link is disabled.'; }
      else if (!moduleInfo) result.reason = 'Choose a communication method.';
      else if (!graph[link.from] || !graph[link.to] || link.from === link.to) result.reason = 'Both endpoints must be present and different.';
      else if ((link.from === 'robot' || link.to === 'robot') && config.network.modules.indexOf(link.module) < 0) result.reason = 'Install the robot’s ' + moduleInfo.label + ' module.';
      else if (Array.isArray(context.blockedModules) && context.blockedModules.indexOf(link.module) >= 0) { result.status = 'interference'; result.reason = 'Local interference interrupts this radio link.'; }
      else if (result.distance > moduleInfo.range) { result.status = 'out-of-range'; result.reason = 'Distance ' + result.distance + ' exceeds the ' + moduleInfo.range + '-unit range.'; }
      else {
        result.available = true;
        result.reliability = clamp(moduleInfo.reliability - Math.pow(result.distance / moduleInfo.range, 3) * (link.module === 'ethernet' ? 0 : 0.12), 0.1, 1);
        result.status = result.reliability < 0.9 ? 'weak' : 'connected';
        result.reason = moduleInfo.label + ' link available; ' + Math.round(result.reliability * 100) + '% estimated packet reliability.';
        graph[link.from].push({ to: link.to, reliability: result.reliability, module: link.module, latency: moduleInfo.latency });
        graph[link.to].push({ to: link.from, reliability: result.reliability, module: link.module, latency: moduleInfo.latency });
      }
      return result;
    });
    function routeTo(target) {
      var best = null;
      function visit(at, path, methods, reliability, latency) {
        if (at === target) { if (!best || reliability > best.reliability) best = { target: target, available: true, path: path.slice(), modules: methods.slice(), reliability: reliability, latency: latency }; return; }
        if (path.length > 7) return;
        (graph[at] || []).forEach(function (edge) { if (path.indexOf(edge.to) < 0) visit(edge.to, path.concat(edge.to), methods.concat(edge.module), reliability * edge.reliability, latency + edge.latency); });
      }
      visit('robot', ['robot'], [], 1, 0);
      return best || { target: target, available: false, path: [], modules: [], reliability: 0, latency: 0, reason: 'No available route from the robot to ' + label(target) + '.' };
    }
    var routes = config.network.nodes.map(routeTo), route = routeTo(mission.targetNode);
    if (!config.network.modules.length) issues.push('Install at least one communication module.');
    if (config.network.nodes.indexOf(mission.targetNode) < 0) issues.push('Add the mission recipient: ' + label(mission.targetNode) + '.');
    if (!route.available) issues.push(route.reason);
    links.filter(function (link) { return link.enabled && !link.available; }).forEach(function (link) { warnings.push(label(link.from) + ' → ' + label(link.to) + ': ' + link.reason); });
    if (route.available && route.reliability < 0.9) warnings.push('The route works, but some packets may need a retry.');
    return { ready: route.available && config.network.modules.length > 0, available: route.available, score: Math.round(route.reliability * 100), issues: unique(issues), warnings: warnings, summary: route.available ? 'Robot → ' + route.path.slice(1).map(label).join(' → ') + ' (' + Math.round(route.reliability * 100) + '% estimated delivery).' : 'The required recipient cannot be reached.', requiredTarget: mission.targetNode, route: route, routes: routes, links: links, positions: Object.assign({ robot: { x: robot.x, y: robot.y } }, Object.fromEntries(nodes.map(function (node) { return [node.id, { x: node.x, y: node.y }]; }))) };
  }
  function ruleProblems(config, rule, caps) {
    var problems = [], stimulus = by.stimuli[rule.stimulus], response = by.responses[rule.response];
    if (!stimulus) problems.push('Choose a known stimulus.');
    if (!response) problems.push('Choose a known response.');
    [stimulus, response].forEach(function (item) { if (item) (item.requires || []).forEach(function (cap) { if (caps.indexOf(cap) < 0) problems.push(item.label + ' requires ' + (capabilityLabels[cap] || cap) + '.'); }); });
    return unique(problems);
  }
  function checkRules(raw, missionId) {
    var config = validateConfig(raw), mission = by.missions[missionId] || by.missions[by.machines[config.machineId].missionId], caps = getCapabilities(config), issues = [], warnings = [];
    var rules = config.rules.map(function (rule, i) { var problems = ruleProblems(config, rule, caps); return Object.assign({}, rule, { index: i, valid: problems.length === 0, issues: problems }); });
    var active = rules.filter(function (rule) { return rule.enabled; }), valid = active.filter(function (rule) { return rule.valid; });
    if (valid.length < 3) issues.push('Train at least 3 enabled rules supported by the installed hardware (' + valid.length + '/3 ready).');
    active.forEach(function (rule) { rule.issues.forEach(function (issue) { issues.push('Rule ' + (rule.index + 1) + ': ' + issue); }); });
    var missing = mission.requiredStimuli.filter(function (id) { return !valid.some(function (rule) { return rule.stimulus === id; }); });
    missing.forEach(function (id) { issues.push('This mission needs a rule for ' + label(id).toLowerCase() + '.'); });
    var duplicateStimuli = unique(active.map(function (rule) { return rule.stimulus; })).filter(function (id) { return active.filter(function (rule) { return rule.stimulus === id; }).length > 1; });
    if (duplicateStimuli.length) warnings.push('Competing rules use feedback strength first, then their displayed order.');
    return { ready: issues.length === 0, score: clamp(Math.round(100 - issues.length * 17), 0, 100), issues: unique(issues), warnings: warnings, summary: issues.length ? 'Add the missing supported associations before testing.' : 'Rule coverage is ready. The mission will test whether those responses work.', rules: rules, validCount: valid.length, missing: missing, requiredStimuli: mission.requiredStimuli.slice(), explanation: 'These are hand-authored stimulus–response associations. Positive or negative feedback changes a rule’s selection weight; this is a small reinforcement illustration, not a full reinforcement-learning system.' };
  }
  function checkReadiness(raw, missionId) {
    var config = validateConfig(raw), hardware = checkHardware(config), network = checkNetwork(config), behaviour = checkRules(config, missionId), mission = by.missions[missionId] || by.missions[by.machines[config.machineId].missionId];
    var issues = hardware.issues.concat(network.issues, behaviour.issues);
    if (mission.machineId !== config.machineId) issues.push('Choose the mission for this machine type.');
    return { ready: !issues.length, score: Math.round((hardware.score + network.score + behaviour.score) / 3), issues: issues, warnings: hardware.warnings.concat(network.warnings, behaviour.warnings), summary: !issues.length ? 'Ready for a live mission test.' : 'Complete the hardware, network and behaviour checks.', hardware: hardware, network: network, behaviour: behaviour, missionId: mission.id };
  }
  function findMatchingRule(raw, activeStimuli) {
    var config = validateConfig(raw), caps = getCapabilities(config), ids = Array.isArray(activeStimuli) ? activeStimuli : [activeStimuli], best = null;
    config.rules.forEach(function (rule) {
      if (rule.enabled && ids.indexOf(rule.stimulus) >= 0 && !ruleProblems(config, rule, caps).length && (!best || rule.strength > best.strength)) best = rule;
    });
    return best ? copy(best) : null;
  }
  function testRule(config, stimulusId) { return findMatchingRule(config, [stimulusId]); }
  function applyFeedback(config, ruleId, delta) {
    var amount = delta === 'positive' ? 1 : delta === 'negative' ? -1 : number(delta, 0);
    if (config && Array.isArray(config.rules)) config.rules.forEach(function (rule) { if (rule.id === ruleId) rule.strength = clamp(number(rule.strength, 0) + amount, -5, 5); });
    return config;
  }
  function getRecommendedConfig(machineId) {
    var config = createConfig(machineId), machine = by.machines[config.machineId];
    var shared = ['memory', 'chassis', 'battery', 'power', 'motors'];
    config.components = shared.concat(config.machineId === 'exploration' ? ['microcontroller', 'wheels', 'ultrasonic', 'temp', 'gps'] : config.machineId === 'service' ? ['sbc', 'wheels', 'camera', 'ultrasonic'] : ['microcontroller', 'temp', 'casing']);
    var method = config.machineId === 'industrial' ? 'ethernet' : 'radio', target = by.missions[machine.missionId].targetNode;
    config.network = { modules: [method], nodes: [target], links: [{ id: 'link-1', from: 'robot', to: target, module: method, enabled: true }] };
    config.rules = machine.suggestedRules.map(function (rule, i) { return { id: 'rule-' + (i + 1), stimulus: rule.stimulus, response: rule.response, strength: 0, enabled: true }; });
    return config;
  }

  function event(state, type, message, key) {
    if (key && state._eventKeys[key]) return;
    if (key) state._eventKeys[key] = true;
    state.events.push({ id: ++state._eventId, time: Math.round(state.time * 10) / 10, type: type, message: message });
    if (state.events.length > 100) state.events.shift();
  }
  function objective(state, id) { return state.objectives.find(function (item) { return item.id === id; }); }
  function complete(state, id, message) { var item = objective(state, id); if (item && !item.done) { item.done = true; item.time = state.time; event(state, 'objective', message || item.label, 'objective-' + id); } }
  function has(state, cap) { return state.capabilities.indexOf(cap) >= 0; }
  function random(state) { state.seed = (1664525 * state.seed + 1013904223) >>> 0; return state.seed / 4294967296; }
  function sendPacket(state, kind) {
    state.metrics.packetsAttempted++;
    var route = state.network.route, reserveFactor = state.readiness.hardware.power.reserve < 3.6 ? 0.85 : 1;
    var success = route.available && random(state) < route.reliability * reserveFactor;
    state.metrics.lastPacket = { time: state.time, kind: kind, delivered: success, path: route.path.slice() };
    state.trace.push({ stage: 'network', label: success ? 'Packet delivered' : 'Packet not delivered', detail: success ? route.path.map(function (id) { return id === 'robot' ? 'Robot' : label(id); }).join(' → ') : route.available ? 'A packet was lost. A later report can retry.' : 'No available route to ' + label(state.network.requiredTarget) + '.' });
    if (state.trace.length > 7) state.trace.shift();
    if (success) {
      state.metrics.packetsDelivered++;
      event(state, 'network', label(state.network.requiredTarget) + ' received ' + kind + '.', 'packet-' + kind + '-' + state.metrics.cycles);
      if (kind === 'research') complete(state, 'transmit', 'Research data reached the base station.');
      if (kind === 'person report') complete(state, 'report', 'The control computer received the person’s location.');
      if (kind === 'temperature alert') complete(state, 'alert', 'The server received the temperature alert.');
    } else { state.metrics.packetsLost++; event(state, 'network', 'Could not deliver ' + kind + ': ' + (route.available ? 'packet loss; retry needed.' : 'route unavailable.'), 'lost-' + kind + '-' + Math.floor(state.time / 3)); }
    return success;
  }
  function createSimulation(raw, missionId) {
    var config = validateConfig(raw), mission = by.missions[missionId] || by.missions[by.machines[config.machineId].missionId], readiness = checkReadiness(config, mission.id);
    if (!readiness.ready) { var error = new Error('Mission not ready: ' + readiness.issues.join(' ')); error.readiness = readiness; throw error; }
    var industry = mission.id === 'monitor', home = { x: 95, y: 240, r: 33 }, spawn = startPosition(config.machineId);
    var target = mission.id === 'search' ? { id: 'person', label: 'Person / assistance point', type: 'person', x: 647, y: 215, r: 24, found: false, collected: false } : { id: 'research', label: 'Research site', type: 'research', x: 655, y: 205, r: 26, found: false, collected: false };
    var objectives = industry ? [{ id: 'sense', label: 'Read process temperature' }, { id: 'halt', label: 'Stop at high temperature' }, { id: 'alert', label: 'Deliver an alert to the server' }, { id: 'restart', label: 'Restart after cooling safely' }, { id: 'safe', label: 'Complete a safe operating cycle' }] : mission.id === 'search' ? [{ id: 'detect', label: 'Detect the person' }, { id: 'report', label: 'Report to the control computer' }, { id: 'reach', label: 'Reach the assistance point' }, { id: 'return', label: 'Return to the handoff zone' }] : [{ id: 'survey', label: 'Collect a research reading' }, { id: 'transmit', label: 'Transmit the reading to base' }, { id: 'return', label: 'Return safely to base' }];
    var state = {
      version: VERSION, config: config, missionId: mission.id, mission: copy(mission), time: 0, duration: mission.duration, status: 'running', phase: industry ? 'monitoring' : 'outbound',
      robot: { x: spawn.x, y: spawn.y, heading: 0, battery: 100, temperature: industry ? 26 : 23, action: industry ? 'move' : 'move', indicator: false, speed: 0, integrity: 100 },
      world: { width: 800, height: 480, home: home, obstacles: industry ? [] : [{ id: 'rock-1', x: 310, y: 225, r: 34 }, { id: 'rock-2', x: 490, y: 320, r: 27 }], targets: industry ? [{ id: 'process', label: 'Monitored process', type: 'process', x: 490, y: 245, r: 48, found: true, collected: false }] : [target], nodes: copy(nodes) },
      destination: industry ? { x: spawn.x, y: spawn.y, label: 'Industrial station' } : { x: target.x, y: target.y, label: target.label },
      objectives: objectives.map(function (item) { return Object.assign(item, { done: false, time: null }); }), events: [], trace: [], path: [{ x: spawn.x, y: spawn.y }],
      network: checkNetwork(config, spawn), readiness: readiness, capabilities: getCapabilities(config),
      metrics: { distance: 0, collisions: 0, packetsAttempted: 0, packetsDelivered: 0, packetsLost: 0, decisions: 0, correctDecisions: 0, unmatchedStimuli: 0, networkAvailableTime: 0, maxTemperature: industry ? 26 : 23, cycles: 0, ruleUses: {}, ruleOutcomes: {} },
      report: null, seed: 5198, processRunning: industry, activeStimuli: [], lastRule: null, _accumulator: 0, _eventId: 0, _eventKeys: {}, _decisionAt: 0, _nextPacketAt: 0, _actionUntil: 0, _waypoint: null, _collisionAt: -10, _pathAt: 0, _hot: false, _cooled: false, _cycleStopped: false, _cycleReported: false, _wasNetworkAvailable: true, _finishReason: '', _safeRestarts: 0
    };
    event(state, 'mission', mission.label + ' started. The installed sensors and your rule table now control the machine.');
    return state;
  }
  function expectedResponse(stimulus, response, missionId) {
    var good = { obstacle: ['stopTurn', 'left', 'right', 'reverse'], person: ['stopReport', 'message'], batteryLow: ['return'], tempHigh: ['stopReport', 'stop'], destination: ['return'], networkLost: ['indicator', 'wait', 'stop'], lightLow: ['indicator', 'wait'], object: ['arm', 'stopTurn', 'stopReport'], safeTemp: ['move'] };
    return (good[stimulus] || []).indexOf(response) >= 0;
  }
  function stimuliNow(state) {
    var list = [], robot = state.robot, industry = state.missionId === 'monitor';
    if (has(state, 'batteryMonitor') && robot.battery < 25) list.push('batteryLow');
    if (!state.network.available) list.push('networkLost');
    if (industry) {
      if (robot.temperature >= 42) list.push('tempHigh');
      if (!state.processRunning && state._hot && robot.temperature <= 30) list.push('safeTemp');
    } else {
      var target = state.world.targets[0];
      var obstacle = state.world.obstacles.find(function (item) {
        var ahead = Math.cos(robot.heading * Math.PI / 180) * (item.x - robot.x) + Math.sin(robot.heading * Math.PI / 180) * (item.y - robot.y);
        return distance(robot, item) < item.r + 47 && ahead > -8;
      });
      if (obstacle && !state._waypoint) {
        if (has(state, 'obstacleSensor')) list.push('obstacle');
        if (has(state, 'objectSensor')) list.push('object');
      }
      if (state.phase === 'outbound' && distance(robot, target) < 115 && state.missionId === 'search' && has(state, 'personSensor')) {
        target.found = true;
        complete(state, 'detect', 'Camera → single-board computer: a person was recognised.');
        if (!objective(state, 'report').done) list.push('person');
      }
      if (state.phase === 'outbound' && distance(robot, target) < 30 && has(state, 'navigation')) list.push('destination');
      if (has(state, 'lightSensor') && robot.x > 425 && robot.x < 470) list.push('lightLow');
    }
    return list;
  }
  function ruleTrace(state, rule, active) {
    var stimulus = rule ? rule.stimulus : active[0], sensorLabel = stimulus ? label(stimulus) : 'Route position';
    state.trace = [{ stage: 'sensor', label: sensorLabel, detail: stimulus === 'tempHigh' || stimulus === 'safeTemp' ? state.robot.temperature.toFixed(1) + ' °C measured by the temperature sensor.' : stimulus === 'batteryLow' ? Math.round(state.robot.battery) + '% charge reported by the battery.' : 'An installed sensor produced this observation.' }, { stage: 'processor', label: state.config.components.indexOf('sbc') >= 0 ? 'Single-board computer' : 'Microcontroller', detail: 'Compare active observations with the enabled rule table in memory.' }, { stage: 'rule', label: rule ? label(rule.stimulus) + ' → ' + label(rule.response) : 'No matching rule', detail: rule ? 'Weight ' + rule.strength + '; strongest supported rule wins, then table order.' : 'No learned association handles this observation.' }, { stage: 'actuator', label: rule ? label(rule.response) : 'Continue current route', detail: rule ? by.responses[rule.response].description : 'The navigation controller continues toward its current goal.' }];
  }
  function executeRule(state, rule) {
    var response = rule.response, robot = state.robot, industry = state.missionId === 'monitor', target = state.world.targets[0];
    state.lastRule = copy(rule); state.metrics.decisions++;
    state.metrics.ruleUses[rule.id] = (state.metrics.ruleUses[rule.id] || 0) + 1;
    var useful = expectedResponse(rule.stimulus, response, state.missionId);
    if (useful) state.metrics.correctDecisions++;
    state.metrics.ruleOutcomes[rule.id] = { stimulus: rule.stimulus, response: response, useful: useful, count: state.metrics.ruleUses[rule.id] };
    event(state, 'rule', label(rule.stimulus) + ' → ' + label(response) + ' (weight ' + rule.strength + ').', 'rule-' + rule.id + '-' + Math.floor(state.time / 5));
    robot.action = response;
    if (response === 'return') {
      if (state.phase !== 'returning') event(state, 'actuator', 'The drive controller changed its goal to base.', 'return-command');
      state.phase = 'returning'; state.destination = { x: state.world.home.x, y: state.world.home.y, label: 'Base / handoff zone' }; state._waypoint = null; state._actionUntil = 0;
    } else if (response === 'stopTurn') {
      var nearest = state.world.obstacles.slice().sort(function (a, b) { return distance(robot, a) - distance(robot, b); })[0];
      if (nearest) {
        var side = robot.y < 260 ? -1 : 1;
        // A side waypoint goes around the sensed obstacle. It is created only by this rule.
        state._waypoint = { x: clamp(robot.x, 35, 765), y: clamp(nearest.y + side * (nearest.r + 83), 40, 440) };
        state._actionUntil = state.time + 0.35;
      }
    } else if (response === 'stop' || response === 'wait' || response === 'stopReport') {
      state._actionUntil = state.time + (response === 'stopReport' ? 0.8 : 1.3);
      if (industry) {
        state.processRunning = false;
        if (robot.temperature >= 42) { state._cycleStopped = true; complete(state, 'halt', 'The temperature rule stopped the industrial motor.'); }
      }
    } else if (response === 'move' && industry) {
      if (state._hot && robot.temperature <= 30 && !state.processRunning) {
        state._safeRestarts++; state.metrics.cycles++; complete(state, 'restart', 'The process restarted after cooling to a safe temperature.');
        if (state._cycleStopped && state._cycleReported) complete(state, 'safe', 'One complete cycle sensed heat, stopped, reported and restarted safely.');
        state._hot = false; state._cycleStopped = false; state._cycleReported = false;
      }
      state.processRunning = true;
    } else if (['left', 'right', 'reverse'].indexOf(response) >= 0) { state._actionUntil = state.time + 1.2; state._turnAction = response; }
    else if (response === 'indicator') { robot.indicator = true; state._actionUntil = 0; }
    else if (response === 'arm') {
      state._actionUntil = state.time + 0.8;
      if (!industry && distance(robot, target) < 60) { target.collected = true; event(state, 'actuator', 'Servos positioned the arm at the nearby target.', 'arm-target'); }
    }
    if (response === 'message' || response === 'stopReport') {
      if (state.time >= state._nextPacketAt) {
        var kind = industry && robot.temperature >= 39 ? 'temperature alert' : state.missionId === 'search' && target.found ? 'person report' : state.missionId === 'explore' && target.collected ? 'research' : 'status';
        var delivered = sendPacket(state, kind);
        if (industry && kind === 'temperature alert' && delivered) state._cycleReported = true;
        state._nextPacketAt = state.time + 1.5;
      }
    }
  }
  function moveRobot(state, dt) {
    var robot = state.robot, action = robot.action, pause = state.time < state._actionUntil && ['stop', 'wait', 'stopReport', 'stopTurn', 'arm'].indexOf(action) >= 0;
    if (pause || robot.battery <= 0) { robot.speed = 0; return; }
    var goal = state._waypoint || state.destination;
    if (state._waypoint && distance(robot, goal) < 9) { state._waypoint = null; goal = state.destination; }
    var dx = goal.x - robot.x, dy = goal.y - robot.y, length = Math.hypot(dx, dy);
    var angle = Math.atan2(dy, dx);
    if (state.time < state._actionUntil && ['left', 'right', 'reverse'].indexOf(action) >= 0) angle += action === 'left' ? -Math.PI / 2 : action === 'right' ? Math.PI / 2 : Math.PI;
    var speed = state.config.components.indexOf('tracks') >= 0 ? 26 : 32;
    if (state.readiness.hardware.power.reserve < 3.6) speed *= 0.8;
    if (robot.battery < 20) speed *= 0.55;
    speed *= Math.max(0.5, robot.integrity / 100);
    var travel = Math.min(length, speed * dt);
    var next = { x: clamp(robot.x + Math.cos(angle) * travel, 20, 780), y: clamp(robot.y + Math.sin(angle) * travel, 25, 455) };
    robot.heading = angle * 180 / Math.PI;
    var collision = state.world.obstacles.find(function (obstacle) { return distance(next, obstacle) < obstacle.r + 14; });
    if (collision) {
      robot.speed = 0;
      if (state.time - state._collisionAt >= 1.5) {
        state.metrics.collisions++; state._collisionAt = state.time; robot.integrity = Math.max(0, robot.integrity - (has(state, 'protection') ? 5 : 10));
        event(state, 'warning', 'Collision: the current response did not steer clear of the obstacle.');
      }
      return;
    }
    state.metrics.distance += distance(robot, next); robot.speed = travel / dt; robot.x = next.x; robot.y = next.y;
    if (state.time >= state._pathAt) { state.path.push({ x: robot.x, y: robot.y }); state._pathAt = state.time + 0.4; if (state.path.length > 250) state.path.shift(); }
  }
  function updateObjectives(state) {
    if (state.missionId === 'monitor') return;
    var target = state.world.targets[0], robot = state.robot;
    if (state.phase === 'outbound' && distance(robot, target) < 30) {
      target.found = true;
      if (state.missionId === 'explore' && has(state, 'researchSensor')) { target.collected = true; complete(state, 'survey', 'The research sensor collected a reading at the survey site.'); }
      if (state.missionId === 'search') complete(state, 'reach', 'The robot reached the person’s assistance point.');
    }
    // Research telemetry is a sensor-data service, and still needs a working physical route.
    if (state.missionId === 'explore' && target.collected && !objective(state, 'transmit').done && state.time >= state._nextPacketAt) { sendPacket(state, 'research'); state._nextPacketAt = state.time + 2; }
    if (state.phase === 'returning' && distance(robot, state.world.home) < 30) {
      var visited = state.missionId === 'explore' ? objective(state, 'survey').done : objective(state, 'reach').done;
      if (visited) complete(state, 'return', state.missionId === 'search' ? 'The robot returned to the handoff zone.' : 'The rover and research returned to base.');
      else event(state, 'warning', 'The robot returned before visiting the mission site.', 'early-return');
    }
  }
  function finish(state, reason) {
    if (state.status !== 'running') return;
    state._finishReason = reason || '';
    var done = state.objectives.filter(function (item) { return item.done; }).length;
    var safe = state.robot.integrity > 0 && state.robot.battery > 0 && state.metrics.maxTemperature < 65;
    state.status = done === state.objectives.length && safe ? 'success' : done > 0 && safe ? 'partial' : 'failed';
    state.robot.speed = 0;
    event(state, 'result', state.status === 'success' ? 'Mission complete: all objectives were met.' : 'Mission ended: ' + (reason || 'some objectives remain incomplete.'));
    state.report = buildReport(state);
  }
  function step(state, dt) {
    state.time = Math.round((state.time + dt) * 1000) / 1000;
    var industry = state.missionId === 'monitor', robot = state.robot;
    var interference = industry && state.time >= 22 && state.time < 26 ? ['wifi', 'bluetooth', 'radio'] : [];
    state.network = checkNetwork(state.config, robot, { blockedModules: interference });
    if (state.network.available) state.metrics.networkAvailableTime += dt;
    if (state.network.available !== state._wasNetworkAvailable) { event(state, 'network', state.network.available ? 'The route to ' + label(state.network.requiredTarget) + ' is available again.' : 'The route to ' + label(state.network.requiredTarget) + ' is unavailable.'); state._wasNetworkAvailable = state.network.available; }
    var effectiveDemand = Math.max(1, state.readiness.hardware.power.demand - state.readiness.hardware.power.solarCredit);
    robot.battery = Math.max(0, robot.battery - effectiveDemand * 0.045 * dt * (robot.speed > 0 || state.processRunning ? 1 : 0.65));
    if (industry) {
      robot.temperature = clamp(robot.temperature + (state.processRunning ? 2.3 : -2.05) * dt, 24, 90);
      state.metrics.maxTemperature = Math.max(state.metrics.maxTemperature, robot.temperature);
      complete(state, 'sense', 'Temperature sensor → processor: live process readings are available.');
      if (robot.temperature >= 42) state._hot = true;
    }
    updateObjectives(state);
    state.activeStimuli = stimuliNow(state);
    if (state.time >= state._decisionAt) {
      var rule = findMatchingRule(state.config, state.activeStimuli);
      if (state.activeStimuli.length) {
        ruleTrace(state, rule, state.activeStimuli);
        if (rule) executeRule(state, rule);
        else { state.metrics.unmatchedStimuli++; event(state, 'warning', 'No supported rule matches: ' + state.activeStimuli.map(label).join(', ') + '.', 'unmatched-' + state.activeStimuli.join('-')); }
      } else if (state.time >= state._actionUntil) {
        robot.action = industry ? state.processRunning ? 'move' : 'stop' : state.phase === 'returning' ? 'return' : 'move';
        if (!state.trace.length) state.trace = [{ stage: 'sensor', label: 'Position ready', detail: 'Navigation knows the mission goal.' }, { stage: 'processor', label: 'Route controller', detail: 'Continue moving until an observation matches a trained rule.' }, { stage: 'actuator', label: industry ? 'Process motor running' : 'Drive motors running', detail: 'Your stimulus–response rules can change this action.' }];
      }
      state._decisionAt = state.time + 0.4;
    }
    if (!industry) moveRobot(state, dt);
    updateObjectives(state);
    if (robot.battery <= 0) finish(state, 'The battery ran out.');
    else if (robot.integrity <= 0) finish(state, 'Repeated collisions disabled the machine.');
    else if (industry && robot.temperature >= 65) finish(state, 'The process overheated because a stop response did not control the motor.');
    else if (state.objectives.every(function (item) { return item.done; }) && state.time >= (industry ? 30 : 25)) finish(state);
    else if (state.time >= state.duration) finish(state, 'The test time expired with unfinished objectives.');
  }
  function tick(state, dt) {
    if (!state || state.status !== 'running') return state;
    state._accumulator += clamp(number(dt, 0), 0, 5);
    while (state._accumulator + 1e-9 >= 0.1 && state.status === 'running') { state._accumulator = Math.max(0, state._accumulator - 0.1); step(state, 0.1); }
    return state;
  }
  function buildReport(state) {
    var done = state.objectives.filter(function (item) { return item.done; }).length;
    var completion = Math.round(done / state.objectives.length * 100), metrics = state.metrics;
    var delivery = metrics.packetsAttempted ? metrics.packetsDelivered / metrics.packetsAttempted : 0;
    var uptime = state.time > 0 ? metrics.networkAvailableTime / state.time : state.network.available ? 1 : 0;
    var networkScore = Math.round(clamp(uptime * 55 + delivery * 45, 0, 100));
    var decisionQuality = metrics.decisions ? metrics.correctDecisions / metrics.decisions : 0;
    var behaviourScore = Math.round(clamp(decisionQuality * 75 + completion * 0.25 - metrics.collisions * 5 - metrics.unmatchedStimuli * 1.5, 0, 100));
    var hardwareScore = Math.round(clamp(state.readiness.hardware.score - metrics.collisions * (has(state, 'protection') ? 2 : 5) - (state.robot.battery <= 0 ? 20 : 0), 0, 100));
    var scores = { hardware: hardwareScore, network: networkScore, behaviour: behaviourScore, completion: completion };
    var reasons = [
      'Hardware: ' + state.readiness.hardware.power.demand + '/24 power units used; ' + Math.round(state.robot.battery) + '% charge and ' + Math.round(state.robot.integrity) + '% integrity remained.',
      'Network: ' + metrics.packetsDelivered + '/' + metrics.packetsAttempted + ' packets delivered; the required route was available for ' + Math.round(uptime * 100) + '% of the run.',
      'Behaviour: ' + metrics.correctDecisions + '/' + metrics.decisions + ' selected responses supported the observed situation. Feedback strength and rule order determined selection.',
      'Completion: ' + done + '/' + state.objectives.length + ' mission objectives achieved.'
    ];
    if (metrics.collisions) reasons.push('Collisions show that the obstacle response needs a different movement action.');
    if (!objective(state, 'return') || objective(state, 'return').done) {} else reasons.push('The robot must reach the site and then use a return response to finish at base.');
    if (state.missionId === 'monitor' && !objective(state, 'safe').done) reasons.push('A full safe cycle needs a stop, a delivered temperature alert, and a restart only after the safe-temperature observation.');
    if (state.missionId === 'search' && !objective(state, 'report').done) reasons.push('Detecting a person is not enough: a message response must deliver their location to the control computer.');
    if (state._finishReason) reasons.push(state._finishReason);
    return { status: state.status, scores: scores, overall: Math.round((scores.hardware + scores.network + scores.behaviour + scores.completion) / 4), summary: state.status === 'success' ? 'Mission complete. Your hardware, network and rules worked together.' : state.status === 'partial' ? 'Some objectives succeeded. Use the event trace to improve the next run.' : state.status === 'running' ? 'The mission is still running.' : 'The mission failed. Review the selected rules and the physical route.', reasons: reasons, objectives: copy(state.objectives), metrics: copy(metrics), elapsed: state.time, feedback: 'Strength changes affect which authored association wins; they do not train a general-purpose AI model.' };
  }

  return { VERSION: VERSION, CONFIG_VERSION: VERSION, catalogs: catalogs, createConfig: createConfig, defaultConfig: createConfig, validateConfig: validateConfig, getRecommendedConfig: getRecommendedConfig, getCapabilities: getCapabilities, checkHardware: checkHardware, checkNetwork: checkNetwork, checkRules: checkRules, checkReadiness: checkReadiness, findMatchingRule: findMatchingRule, testRule: testRule, applyFeedback: applyFeedback, createSimulation: createSimulation, tick: tick, buildReport: buildReport };
});
