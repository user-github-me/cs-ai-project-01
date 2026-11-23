# Chapter 3 — Mission and optional resource

## ACT-03 — The kitchen with four stations

**Chapter 3 — Hardware**

Pip needs three sensor calculations. One worker finishes all four steps of a job before starting the next. Another team proposes four stations. Will each job suddenly take one step?

**Goal:** Distinguish pipeline throughput from the latency of one instruction and identify the effect of a dependency.

**Preparation:** Draw a grid with cycles 1–8 as columns and instructions I1–I3 as rows. Use stages F (fetch), D (decode), E (execute), W (write back). Assume one cycle per stage, independent instructions and no stalls initially.

**Task:**

1. Schedule I1 in F/D/E/W across cycles 1–4; start I2 at cycle 2 and I3 at cycle 3.
2. Predict the finish cycles and compare total elapsed cycles with three instructions run without overlap.
3. Now assume I2 needs a result from I1 that is unavailable until the end of I1’s W. State this dependency explicitly; postpone I2’s E to cycle 5 and propagate later stages without letting instructions overtake.
4. Optional command: python3 supporting/BlueImpulse_Demonstrations.py --topic hardware. Use its ideal trace for the first case. Treat your stalled case as a separate scheduling model.

**Observe and record:** Ideal finish cycles are 4, 5 and 6. Mark every occupied stage and every inserted wait. Do not equate elapsed cycles with the sum of all stage work.

**Reflect:** What improved: single-instruction latency or completed instructions per unit time? Why must a claim of speedup list its assumptions?

**Feedback — check after trying:** Ideal case takes six cycles rather than twelve sequential stage cycles, but each instruction still uses four stages. In the stated dependency model I2 executes at 5 and writes at 6; I3 must wait behind it and can execute at 6 and write at 7. Real forwarding, stage timings and hazards differ, so this trace does not predict every CPU.

**Optional resource:** R2 (full introduction and offline alternative follow).

## R2 — Nand to Tetris — Project 5: Computer Architecture

Noam Nisan and Shimon Schocken / Nand to Tetris.

https://www.nand2tetris.org/project05

**Relevant section:** Project overview, proposed computer architecture and hardware simulator guidance

**Why use it:** A concrete educational computer architecture connects logic, CPU state and memory.

**Learner task:** After ACT-01, compare the purpose of an instruction address and a data-memory address with the project’s computer model. Name one part the models share and one detail that differs.

**Limits:** The Hack computer is a different ISA; its instructions and registers must not be substituted directly into this guide’s toy program. Software installation is optional and not required for the paper task.

**Offline alternative:** ACT-01 includes its full program, trace and expected output. ACT-03 provides a complete paper pipeline grid specification.

**Access:** Optional public web resource; no account required to read the cited page. Signed-out HTTP access was checked on 7 November 2026. Availability on every campus network is not guaranteed. All essential task instructions and feedback are supplied locally.
