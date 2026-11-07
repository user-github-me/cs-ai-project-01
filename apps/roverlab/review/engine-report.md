# ROVERLAB engine verification

Verified on 2026-11-07 with Node.js, using only its standard library.

From the repository root:

```sh
node --test apps/roverlab/tests/engine.test.cjs
```

Result: **21 tests passed; 0 failed; 0 skipped**.

## Mission evidence

| Configuration | Observed result |
| --- | --- |
| Recommended exploration rover | Success in 42.8 simulated seconds; collected and transmitted research, physically returned to base; zero collisions. |
| Recommended service robot | Success in 43.3 simulated seconds; detected and reported the person, reached the assistance point and returned; zero collisions. |
| Recommended industrial machine | Success in 30 simulated seconds; sensed heating, stopped the motor, delivered a server alert, cooled and restarted safely. |
| Exploration obstacle → move | Readiness allows the physically supported rule; repeated collisions cause actual mission failure. |
| Exploration destination → wait | Research succeeds, but the robot does not return; partial mission. |
| Service robot using direct Wi-Fi | The link passes at the start, goes out of range in the field and cannot deliver the person report; partial mission. |
| Industrial high temperature → message | Alert packets arrive, but the motor continues heating; overheating causes failure. |
| Industrial high temperature → stop | Temperature stays controlled, but no alert reaches the server; partial mission. |

## Main checks

- Hardware prerequisites enforce processor, memory, power distribution, battery, compatible movement and mission sensors; camera recognition requires the single-board computer.
- Combined component and communication demand can exceed the 24-unit supply and prevent launch.
- Required network recipients need a real route. Merely adding a node or reaching another robot is insufficient. Multi-hop routing, gateway link types, per-hop reliability, disabled links and dynamic range are checked.
- Training requires at least three supported enabled rules plus mission stimulus coverage. Wrong but physically possible responses remain testable.
- Feedback weights change the actual selected rule and mission outcome. Strongest weight wins; current array order resolves ties; weights are bounded from −5 to +5.
- Actual movement differs for wheels and tracks. Low battery causes an authored return response without granting unvisited research objectives.
- Fixed 0.1-second internal steps produce identical reports for irregular browser frame timing and whole-second calls. JSON serialization and restoration midway produce the same result.
- Malformed saved configurations fail validation safely; simulations do not need a DOM, network service or browser storage.
- Reports contain hardware, network, behaviour and completion scores with event evidence. Sensor → processor → rule → actuator traces and conditional packet events remain inspectable.

## Educational model audit

These are explicit player-authored associations with bounded selection weights, not a neural network or a full reinforcement-learning algorithm. The engine does not invent new rules from feedback. Power and map distances are fictional teaching units; ranges, battery drain, thermal behaviour and packet probabilities are simplified.

A navigation controller supplies ordinary movement between rule triggers. The authored rule determines stopping, turning, return, indicators, manipulation and explicit reports. Only `stop, then turn` constructs an obstacle-avoidance waypoint. A bad response can leave the robot stuck, collide or miss its goal.

Exploration research is collected automatically by an installed research sensor at the site, then queued for telemetry over the actual route. Its return must still be commanded by a rule. Service person reports and industrial alerts require a message-capable rule. Missing routes do not deliver packets. The stationary industrial motor heats while running and cools while stopped; an alert alone cannot cool it.

Three playable mission types are covered. Optional stimuli and actuators support experiments but are not all exercised by each recommended mission. The result establishes behaviour in this deterministic teaching simulation; it is not evidence of physical robot safety or a student usability study. Browser journeys and accessibility/responsive checks are recorded separately in `qa-report.md`.
