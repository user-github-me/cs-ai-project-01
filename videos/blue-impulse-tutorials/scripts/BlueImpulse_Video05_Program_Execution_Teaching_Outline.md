# Teaching outline: Program execution

Open the guide at the pages below. Let learners answer before continuing through a thinking pause. Use the matching Python demonstration to change an input and explain the resulting change.

| Time | Teaching step | Guide page | What to show or ask |
|---|---|---|---|
| 00:00 | How does a line of code become a result? | 13 | How does a line of code become a result? |
| 00:35 | Today’s route | 13 | Today’s route |
| 01:13 | Before the processor executes | 14 | A language may have both compiled and interpreted implementations. |
| 02:01 | Use the recipe analogy | 13 | PC: next instruction address; MAR: selected memory address; MDR: item moving to/from memory; CIR: current instruction; ACC: intermediate arithmetic |
| 02:51 | Fetch one instruction | 13 | A branch instruction may replace the normal next value of PC. |
| 03:43 | Read the four instructions | 15 | STORE copies 7 to address 200; it does not mean “store the number 200”. |
| 04:27 | Single-step the book’s program | 15 | Single-step the book’s program |
| 05:34 | Value or address? | 15 | After STORE 200: ACC = ? and memory[200] = ? |
| 06:25 | The next address can change | 13 | Normal next address; Branch selects another address; Instruction effects still matter |
| 07:14 | Change one instruction | 15 | LOAD #3; ADD #9; STORE 200 |
| 08:06 | Instructions change machine state | 13 | Fetch → decode → execute; Each register has a job; Addresses differ from values; Trace: 3 + 4 → memory[200] = 7 |
| 09:01 | Blue Impulse study guide | 1 | Blue Impulse study guide |

The written tutorial PDF contains the full explanation and exact book excerpts. Numerical examples are teaching models, with assumptions stated in the guide, narration, and supporting file.
