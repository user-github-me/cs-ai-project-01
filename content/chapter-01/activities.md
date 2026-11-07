# Chapter 1 — Mission and optional resource

## ACT-01 — The parcel total is wrong

**Chapter 1 — The Fundamentals**

Pip’s delivery receipt says 200 parcels. The team expected 7. A programmer has confused an address with a value. Can you find the mistake?

**Goal:** Trace stored instructions and distinguish an immediate value, an address and the content stored there.

**Preparation:** Paper and pencil are sufficient. Optional: Python 3.9 or newer and supporting/BlueImpulse_Demonstrations.py. This is an invented teaching ISA, not a real processor.

**Task:**

1. Write columns for PC before fetch, instruction, ACC after execution and memory[200]. Start at PC 100, ACC 0 and memory[200] 0.
2. Run: 100 LOAD #3; 101 ADD #4; 102 STORE 200; 103 HALT. The # symbol means a literal value. PC advances by one when each instruction is fetched.
3. Predict the final result before checking the output. Then replace ADD #4 with ADD #9 and trace again.
4. Optional command: python3 supporting/BlueImpulse_Demonstrations.py --topic execution --add 9. Compare its state trace with your table.

**Observe and record:** Record ACC after every instruction, memory[200] after STORE, and final PC. Note the difference between a number used as data and a number used as an address.

**Reflect:** Why does STORE 200 copy 7 rather than replace the accumulator with 200? Which parts of the model would depend on a real ISA?

**Feedback — check after trying:** First run: after LOAD, ACC 3; after ADD, ACC 7; after STORE, memory[200] 7; after HALT, final PC 104. The modified run stores 12. STORE’s operand is a destination address. PC increments, instruction size and register names are model choices, not universal CPU rules.

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
