'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const E = require('../public/engine.js');

function run(config, steps = [1]) {
  const state = E.createSimulation(config);
  let i = 0;
  while (state.status === 'running') {
    E.tick(state, steps[i++ % steps.length]);
    assert.ok(i < 10000, 'simulation must terminate');
  }
  return state;
}

test('all three recommended machines complete real objectives in 30–60 seconds', () => {
  for (const machine of E.catalogs.machines) {
    const config = E.getRecommendedConfig(machine.id);
    assert.equal(E.checkReadiness(config).ready, true, machine.id);
    const state = run(config);
    assert.equal(state.status, 'success', machine.id);
    assert.ok(state.time >= 30 && state.time <= 60);
    assert.ok(state.objectives.every(o => o.done));
    assert.ok(state.metrics.packetsDelivered > 0);
    assert.equal(state.metrics.collisions, 0);
    assert.ok(state.metrics.decisions > 0);
    if (machine.id !== 'industrial') assert.ok(state.metrics.distance > 900, 'rover physically goes out and returns');
  }
});

test('simulation is deterministic across RAF rates and serializable midway', () => {
  const config = E.getRecommendedConfig('exploration');
  const wholeSeconds = run(config);
  const irregularFrames = run(config, [0.016, 0.087, 0.034, 0.21, 0.002]);
  assert.deepEqual(irregularFrames.report, wholeSeconds.report);
  assert.deepEqual(irregularFrames.robot, wholeSeconds.robot);
  let restored = E.createSimulation(config);
  E.tick(restored, 5);
  restored = JSON.parse(JSON.stringify(restored));
  while (restored.status === 'running') E.tick(restored, 0.1);
  assert.deepEqual(restored.report, wholeSeconds.report);
});

test('a blank build cannot start, and a mission cannot run on another machine', () => {
  const blank = E.createConfig('service');
  assert.equal(E.checkReadiness(blank).ready, false);
  assert.throws(() => E.createSimulation(blank), /Mission not ready/);
  assert.equal(E.checkReadiness(E.getRecommendedConfig('service'), 'monitor').ready, false);
});

test('power distribution, compatible drive and sensor processing are actual requirements', () => {
  const service = E.getRecommendedConfig('service');
  service.components = service.components.filter(id => id !== 'power');
  assert.equal(E.checkHardware(service).ready, false);
  service.components.push('power');
  service.components = service.components.filter(id => id !== 'sbc');
  service.components.push('microcontroller');
  assert.equal(E.checkHardware(service).ready, false);
  assert.ok(E.checkHardware(service).issues.some(issue => /Camera needs/.test(issue)));
  service.components.push('tracks');
  assert.ok(E.checkHardware(service).issues.some(issue => /does not fit/.test(issue)));
});

test('adding high-power modules can overload the build', () => {
  const config = E.getRecommendedConfig('exploration');
  config.components = ['microcontroller', 'sbc', 'memory', 'wheels', 'motors', 'servos', 'ultrasonic', 'infrared', 'camera', 'temp', 'light', 'gps', 'battery', 'solar', 'power', 'chassis', 'arm', 'casing'];
  config.network.modules = E.catalogs.modules.map(m => m.id);
  const result = E.checkHardware(config);
  assert.ok(result.power.demand > result.power.capacity);
  assert.equal(result.ready, false);
  assert.ok(result.issues.some(issue => /Power demand/.test(issue)));
});

test('the required recipient must be reached by links, not merely listed', () => {
  const config = E.getRecommendedConfig('exploration');
  config.network.nodes.push('otherRobot');
  config.network.links[0].to = 'otherRobot';
  assert.equal(E.checkNetwork(config).ready, false);
  config.network.links.push({ id: 'relay', from: 'otherRobot', to: 'base', module: 'radio' });
  const result = E.checkNetwork(config);
  assert.equal(result.ready, true);
  assert.deepEqual(result.route.path, ['robot', 'otherRobot', 'base']);
  assert.ok(result.route.reliability < result.links[0].reliability, 'per-hop reliability compounds');
});

test('a gateway bridges link types without requiring its external radio on the robot', () => {
  const config = E.getRecommendedConfig('industrial');
  config.network.nodes.push('gateway');
  config.network.links = [
    { id: 'local', from: 'robot', to: 'gateway', module: 'ethernet' },
    { id: 'uplink', from: 'gateway', to: 'server', module: 'cellular' }
  ];
  assert.equal(E.checkNetwork(config).ready, true);
  assert.deepEqual(E.checkNetwork(config).route.modules, ['ethernet', 'cellular']);
});

test('range is evaluated at the robot’s real position and disabled links cannot deliver', () => {
  const config = E.getRecommendedConfig('service');
  config.network.modules = ['wifi'];
  config.network.links[0].module = 'wifi';
  assert.equal(E.checkNetwork(config).ready, true);
  assert.equal(E.checkNetwork(config, { x: 650, y: 210 }).ready, false);
  assert.equal(E.checkNetwork(config, { x: 650, y: 210 }).links[0].status, 'out-of-range');
  config.network.links[0].enabled = false;
  assert.equal(E.checkNetwork(config).ready, false);
});

test('dynamic Wi-Fi range prevents a remote service report and changes the outcome', () => {
  const config = E.getRecommendedConfig('service');
  config.network.modules = ['wifi'];
  config.network.links[0].module = 'wifi';
  assert.equal(E.checkReadiness(config).ready, true, 'link works at the starting position');
  const state = run(config);
  assert.equal(state.status, 'partial');
  assert.equal(state.objectives.find(o => o.id === 'report').done, false);
  assert.equal(state.metrics.packetsDelivered, 0);
  assert.ok(state.metrics.packetsLost > 0);
  assert.ok(state.report.scores.network < 60);
});

test('three rules and per-mission stimulus coverage are both required', () => {
  const config = E.getRecommendedConfig('exploration');
  config.rules.pop();
  assert.equal(E.checkRules(config).ready, false);
  config.rules.push({ id: 'duplicate', stimulus: 'obstacle', response: 'wait', strength: 0 });
  assert.equal(E.checkRules(config).ready, false, 'three rows cannot substitute for low-battery coverage');
  config.rules[2].stimulus = 'batteryLow';
  assert.equal(E.checkRules(config).ready, true, 'wrong but physically supported responses can be tested');
  config.rules[2].enabled = false;
  assert.equal(E.checkRules(config).ready, false);
});

test('rules require installed sensor and actuator capabilities', () => {
  const config = E.getRecommendedConfig('exploration');
  config.rules.push({ id: 'person', stimulus: 'person', response: 'arm' });
  const check = E.checkRules(config);
  assert.equal(check.ready, false);
  assert.ok(check.issues.some(issue => /camera with a single-board computer/.test(issue)));
  assert.ok(check.issues.some(issue => /robotic arm/.test(issue)));
  assert.equal(E.testRule(config, 'person'), null);
});

test('feedback strength changes rule selection, with stable priority ties and bounds', () => {
  const config = E.getRecommendedConfig('exploration');
  config.rules.unshift({ id: 'rival', stimulus: 'obstacle', response: 'move', strength: 0 });
  assert.equal(E.testRule(config, 'obstacle').id, 'rival');
  E.applyFeedback(config, 'rule-1', 1);
  assert.equal(E.testRule(config, 'obstacle').id, 'rule-1');
  E.applyFeedback(config, 'rule-1', -1);
  assert.equal(E.testRule(config, 'obstacle').id, 'rival');
  E.applyFeedback(config, 'rival', 100);
  assert.equal(config.rules[0].strength, 5);
  E.applyFeedback(config, 'rival', -100);
  assert.equal(config.rules[0].strength, -5);
  assert.equal(E.testRule(config, 'obstacle').id, 'rule-1');
  config.rules.reverse();
  config.rules.forEach(r => { r.strength = 0; });
  assert.equal(E.testRule(config, 'obstacle').id, 'rule-1');
});

test('a wrong obstacle association passes readiness but physically collides and fails', () => {
  const config = E.getRecommendedConfig('exploration');
  config.rules[0].response = 'move';
  assert.equal(E.checkReadiness(config).ready, true);
  const state = run(config);
  assert.equal(state.status, 'failed');
  assert.ok(state.metrics.collisions > 0);
  assert.equal(state.objectives.find(o => o.id === 'survey').done, false);
  assert.ok(state.report.scores.behaviour < 40);
});

test('waiting at the destination gives partial completion rather than auto-return', () => {
  const config = E.getRecommendedConfig('exploration');
  config.rules.find(r => r.stimulus === 'destination').response = 'wait';
  const state = run(config);
  assert.equal(state.status, 'partial');
  assert.equal(state.objectives.find(o => o.id === 'survey').done, true);
  assert.equal(state.objectives.find(o => o.id === 'return').done, false);
  assert.ok(state.robot.x > 600);
});

test('feedback changes the actual mission outcome, not only a displayed weight', () => {
  const config = E.getRecommendedConfig('exploration');
  config.rules.unshift({ id: 'unsafe', stimulus: 'obstacle', response: 'move', strength: 1 });
  assert.equal(run(config).status, 'failed');
  E.applyFeedback(config, 'unsafe', -2);
  assert.equal(run(config).status, 'success');
});

test('low battery causes an actual early return without granting research completion', () => {
  const state = E.createSimulation(E.getRecommendedConfig('exploration'));
  state.robot.battery = 24;
  E.tick(state, 0.5);
  assert.equal(state.phase, 'returning');
  assert.equal(state.lastRule.stimulus, 'batteryLow');
  while (state.status === 'running') E.tick(state, 1);
  assert.notEqual(state.status, 'success');
  assert.equal(state.objectives.find(o => o.id === 'survey').done, false);
});

test('industrial heat needs a stop command; a message alone cannot cool the motor', () => {
  const config = E.getRecommendedConfig('industrial');
  config.rules[0].response = 'message';
  assert.equal(E.checkReadiness(config).ready, true);
  const state = run(config);
  assert.equal(state.status, 'failed');
  assert.ok(state.metrics.maxTemperature >= 65);
  assert.equal(state.objectives.find(o => o.id === 'alert').done, true);
  assert.equal(state.objectives.find(o => o.id === 'halt').done, false);
});

test('stopping an industrial process without reporting leaves a partial mission', () => {
  const config = E.getRecommendedConfig('industrial');
  config.rules[0].response = 'stop';
  const state = run(config);
  assert.equal(state.status, 'partial');
  assert.equal(state.objectives.find(o => o.id === 'halt').done, true);
  assert.equal(state.objectives.find(o => o.id === 'alert').done, false);
  assert.equal(state.objectives.find(o => o.id === 'safe').done, false);
});

test('tracks alter physical travel time while remaining a viable exploration choice', () => {
  const wheels = E.getRecommendedConfig('exploration');
  const tracks = E.validateConfig(wheels);
  tracks.components = tracks.components.map(id => id === 'wheels' ? 'tracks' : id);
  const a = run(wheels), b = run(tracks);
  assert.equal(b.status, 'success');
  assert.ok(b.time > a.time + 5);
});

test('normalization is serializable and malformed saved selections fail safely', () => {
  const config = E.validateConfig({ machineId: '__proto__', components: ['battery', 'battery', 'bad-part'], network: { modules: ['wifi'], nodes: ['base'], links: [{ from: '__proto__', to: 'base', module: '__proto__' }] }, rules: [{ stimulus: '__proto__', response: 'toString' }] });
  assert.equal(config.machineId, 'exploration');
  assert.deepEqual(config.components, ['battery']);
  assert.deepEqual(JSON.parse(JSON.stringify(config)), config);
  assert.equal(E.checkNetwork(config).ready, false);
  assert.equal(E.checkRules(config).ready, false);
  assert.equal(E.testRule(config, '__proto__'), null);
});

test('sensor, processor, rule, actuator and conditional network events remain inspectable', () => {
  const state = run(E.getRecommendedConfig('industrial'));
  assert.ok(state.events.some(event => event.type === 'rule'));
  assert.ok(state.events.some(event => event.type === 'network'));
  assert.ok(state.trace.some(item => item.stage === 'sensor'));
  assert.ok(state.trace.some(item => item.stage === 'processor'));
  assert.ok(state.trace.some(item => item.stage === 'rule'));
  assert.ok(state.trace.some(item => item.stage === 'actuator'));
  assert.deepEqual(Object.keys(state.report.scores).sort(), ['behaviour', 'completion', 'hardware', 'network']);
  assert.match(state.report.feedback, /do not train a general-purpose AI/);
});
