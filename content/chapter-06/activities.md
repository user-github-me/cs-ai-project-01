# Chapter 6 — Mission and optional resource

## ACT-06 — Choose a system, not a leaderboard

**Chapter 6 — Strengths & Limitations**

A larger model wins an accuracy contest but overheats Pip’s computer. A cloud model is accurate too, until the network drops. The team must choose a deployment, not a single impressive number.

**Goal:** Evaluate edge/cloud placement against explicit latency, memory, power, privacy and resilience constraints.

**Preparation:** Use this fictional design table: local small model = 30 ms compute, 180 MB working memory, 4 W, 92% measured task accuracy; local large model = 90 ms, 700 MB, 9 W, 96%; remote model = 20 ms server compute plus 100–300 ms round trip, 98%, uploads images. Device budgets: 512 MB, 6 W and 80 ms deadline. Treat accuracies as supplied hypothetical measurements, not research results.

**Task:**

1. Eliminate designs that violate hard local memory, power or timing budgets. For the remote model add the network and server times.
2. Choose where emergency control and overnight fleet analytics should run. State how the system behaves during lost connectivity.
3. A software update improves the small model to 94% but needs 70 ms and 5 W. Decide what to test before accepting it; do not assume that one benchmark settles safety.
4. Draw a two-column decision record: constraint/evidence, then choice/trade-off. Propose one privacy safeguard and one monitoring measure.

**Observe and record:** Separate hard failures from preferences and record the worst stated time rather than only the mean. Identify unknowns such as warm-device timing and test-data coverage.

**Reflect:** Why is 98% accuracy not sufficient to choose the remote model for the 80 ms task? Which human decision remains after the calculations?

**Feedback — check after trying:** The small local model fits the stated budgets. The large local model violates memory, power and latency. The remote option takes 120–320 ms and misses the deadline; it may suit slower analytics with privacy controls. The updated small model fits the listed limits but leaves only 10 ms timing margin, requiring end-to-end/warm-device testing, relevant accuracy evaluation and a fallback. Valid alternatives earn credit if their assumptions and trade-offs are explicit.

**Optional resource:** R5 (full introduction and offline alternative follow).

## R5 — Artificial Intelligence Risk Management Framework (AI RMF 1.0)

NIST, NIST AI 100-1, January 2023.

https://www.nist.gov/itl/ai-risk-management-framework

**Relevant section:** Framework functions Govern, Map, Measure and Manage; trustworthy AI characteristics

**Why use it:** Connects measured performance with context, impacts, monitoring and responsibility.

**Learner task:** For ACT-06, assign one concrete action to each framework function: identify an owner, describe the operating domain, measure a relevant failure and plan a response.

**Limits:** A voluntary risk-management framework is not certification that a product is safe, fair or legally compliant. Context and evidence still matter.

**Offline alternative:** ACT-06 supplies the design table and expected trade-off reasoning. A suitable four-action response is: Govern — name an accountable operator; Map — define the campus operating domain; Measure — test missed deadlines and uneven accuracy; Manage — maintain fallback and an incident response process.

**Access:** Optional public web resource; no account required to read the cited page. Signed-out HTTP access was checked on 7 November 2026. Availability on every campus network is not guaranteed. All essential task instructions and feedback are supplied locally.
