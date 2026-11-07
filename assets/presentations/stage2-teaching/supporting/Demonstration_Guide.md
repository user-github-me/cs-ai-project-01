# Offline demonstrations — Blue Impulse Stage 2 PPT V1.0

All classroom activities work with the submitted slides alone. This optional Python file lets the presenter reproduce or vary the worked examples. It requires Python 3.9 or newer and only the standard library. It does not use the internet, credentials, devices or hardware.

Run from this folder:

```sh
python3 BlueImpulse_Demonstrations.py --topic all
```

The file `expected-results.json` contains the complete default output. The relevant slide is an offline visual fallback if Python is unavailable. Ask for a prediction before running the command, then discuss why the result follows.

| Slides | Question and command | Expected result and debrief |
| --- | --- | --- |
| 10–11 | What is stored at address 200? `python3 BlueImpulse_Demonstrations.py --topic execution` | ACC becomes 3, then 7; memory[200] becomes 7; final PC is 104 in this teaching model. |
| 10–11 | Change the ADD operand: `python3 BlueImpulse_Demonstrations.py --topic execution --add 9` | The stored result is 12. LOAD replaces ACC; ADD changes it; STORE copies it. |
| 20–22 | Move halfway toward the target: `python3 BlueImpulse_Demonstrations.py --topic rl` | Target 4.6, error 2.6, change 1.3, new Q 3.3. A terminal next state gives no future term and new Q 1.5. |
| 29 | When does instruction 3 complete? `python3 BlueImpulse_Demonstrations.py --topic hardware` | Cycles 4, 5 and 6 complete I1, I2 and I3. Each instruction still takes four stages. |
| 40–41 | How far is travelled during delay? `python3 BlueImpulse_Demonstrations.py --topic network` | At 30 m/s, 500/50/5/200 ms gives 15/1.5/0.15/6 metres. Convert milliseconds to seconds first. |
| 49–51 | Accept, stale or duplicate? `python3 BlueImpulse_Demonstrations.py --topic networked-ai` | A accepted; B stale; C duplicate. Only acceptance advances last sequence from 41 to 42. |

Suggested demonstration sequence: establish the starting state on the question slide; give 30–60 seconds for predictions; run only the relevant command; compare the output with the answer slide; change one input if time permits. Do not spend class time installing software.

The model assumptions in `Sources.md` are part of the teaching. In particular, the message validator does not implement authentication, sequence wraparound or general distributed clock synchronization. Missing learning feedback must not be silently converted to reward zero.
