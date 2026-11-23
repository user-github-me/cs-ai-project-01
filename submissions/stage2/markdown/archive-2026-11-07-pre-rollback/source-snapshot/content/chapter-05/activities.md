# Chapter 5 — Mission and optional resource

## ACT-05 — Yesterday’s command arrives today

**Chapter 5 — Applications**

Pip has stopped safely. A delayed “move” packet arrives and looks correctly formatted. Should it obey a message just because the bytes make sense?

**Goal:** Apply identity, unit, version, freshness and sequence checks while distinguishing secure transport from safe command handling.

**Preparation:** Receiver device ID robot-7; expected units m; policy_version 3; maximum age 200 ms; last accepted sequence 41. Assume the upstream authentication check is true for these examples. The toy Boolean is not a cryptographic implementation.

**Task:**

1. Inspect packets in order: A = sequence 42, age 50 ms; B = sequence 43, age 600 ms; C = sequence 42, age 60 ms. All other listed fields match.
2. For each packet, decide ACCEPT, REJECT STALE or REJECT DUPLICATE. Only update last accepted sequence when a packet is accepted.
3. Predict what would happen if a developer updated last sequence before checking age, and explain why reject paths should not corrupt accepted-state bookkeeping.
4. Optional command: python3 supporting/BlueImpulse_Demonstrations.py --topic networked-ai. Test the same order and compare receiver state.

**Observe and record:** Write the decision and last accepted sequence after each packet. Identify which check fails; do not invent a new packet timestamp.

**Reflect:** What must a real deployment add for clock assumptions, authentication, session resets and a safe local response when the network fails?

**Feedback — check after trying:** A is ACCEPT and advances last sequence to 42. B is STALE; last sequence stays 42. C is DUPLICATE; last sequence stays 42. Version, identity and unit checks add semantic protection. Real systems need authenticated messages, replay/session design, trustworthy timing and explicit fallback, not only this toy validation function.

**Optional resource:** R4 (full introduction and offline alternative follow).

## R4 — RFC 8446 — The Transport Layer Security (TLS) Protocol Version 1.3

IETF / Eric Rescorla, 2018.

https://www.rfc-editor.org/rfc/rfc8446

**Relevant section:** Section 1 (Introduction) and Section 8 (0-RTT and anti-replay)

**Why use it:** Distinguishes transport confidentiality/integrity from application-level decisions, including replay considerations.

**Learner task:** After ACT-05, explain why authenticated transport alone does not decide whether an old command is still appropriate to execute.

**Limits:** The Python receiver is a validation demonstration, not a TLS implementation. Do not implement cryptography from this worksheet.

**Offline alternative:** ACT-05 includes the packet fields, state transitions and rejection explanations; no network service or account is needed.

**Access:** Optional public web resource; no account required to read the cited page. Signed-out HTTP access was checked on 7 November 2026. Availability on every campus network is not guaranteed. All essential task instructions and feedback are supplied locally.
