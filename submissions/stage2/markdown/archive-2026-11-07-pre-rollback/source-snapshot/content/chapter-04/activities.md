# Chapter 4 — Mission and optional resource

## ACT-04 — The fast network sends a late warning

**Chapter 4 — Networking**

Pip’s dashboard celebrates a high link rate. A stop warning arrives half a second late. “But the Wi-Fi is fast!” says the operator. The parcels keep moving.

**Goal:** Separate link capacity from response latency and calculate distance travelled during communication delay.

**Preparation:** Paper or calculator. Use a constant illustrative speed of 30 m/s and delays 500, 50, 5 and 200 milliseconds. This is not a campus-rover speed claim or a braking simulation.

**Task:**

1. Predict which delay causes the greatest extra travel before a response.
2. Convert each delay to seconds by dividing by 1,000. Calculate delay distance = speed × delay.
3. Create a two-column table of delay and distance. Explain why increasing Mb/s alone need not remove propagation, queueing or processing delay.
4. Optional command: python3 supporting/BlueImpulse_Demonstrations.py --topic network. Compare results and change the speed in your own calculation to 2 m/s.

**Observe and record:** Record units at each step and compare ratios: a ten-times smaller delay creates ten-times smaller delay distance at constant speed.

**Reflect:** What does the calculation omit? How could jitter or occasional long queueing delays matter even when average latency is low?

**Feedback — check after trying:** 500/50/5/200 ms correspond to 0.5/0.05/0.005/0.2 s and 15/1.5/0.15/6 m at 30 m/s. At 2 m/s they give 1/0.1/0.01/0.4 m. This excludes reaction after receipt, actuator lag and braking distance; do not call it total stopping distance.

**Optional resource:** R3 (full introduction and offline alternative follow).

## R3 — RFC 1122 — Requirements for Internet Hosts: Communication Layers

IETF / R. Braden, editor, 1989.

https://www.rfc-editor.org/rfc/rfc1122

**Relevant section:** Section 1.1.3 (Internet protocol suite) and the link, IP and transport sections

**Why use it:** An authoritative foundation for the layered Internet model used in Chapter 4.

**Learner task:** Draw the four teaching layers and place HTTP, TCP, IP and Ethernet/Wi-Fi by role. Explain why a large link capacity does not set an end-to-end response time.

**Limits:** This is a technical historical standards document; current protocols have later updates. Use it for layer roles, not as a complete modern security checklist.

**Offline alternative:** The chapter and ACT-04 contain the layer explanations and all delay inputs/results offline.

**Access:** Optional public web resource; no account required to read the cited page. Signed-out HTTP access was checked on 7 November 2026. Availability on every campus network is not guaranteed. All essential task instructions and feedback are supplied locally.
