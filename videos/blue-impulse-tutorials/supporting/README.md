# Repeat the demonstrations

Requires Python 3.9 or newer. No packages, network connection, credentials, or hardware are needed.

```sh
python3 BlueImpulse_Demonstrations.py --topic all
python3 BlueImpulse_Demonstrations.py --topic rl --reward 2
python3 BlueImpulse_Demonstrations.py --topic hardware
python3 BlueImpulse_Demonstrations.py --topic network --speed 30
python3 BlueImpulse_Demonstrations.py --topic networked-ai
python3 BlueImpulse_Demonstrations.py --topic execution --add 9
```

Predict the result before running each example, then compare it with the guide:

| Tutorial | Guide page | Result to explain |
| --- | --- | --- |
| Reinforcement learning | 28 | Target 4.6; new Q 3.3. Terminal-state practice: 1.5. |
| Hardware | 39 | Ideal pipeline completes three instructions in cycles 4, 5, 6. Each still passes through four stages. |
| Network challenges | 74 | 500/50/5 ms at 30 m/s gives 15/1.5/0.15 m during delay. 200 ms gives 6 m. |
| Networking for behaviorist AI | 75 | Accept the fresh packet, reject the stale packet, reject the duplicate. |
| Program execution | 13–15 | ACC becomes 3 then 7; memory[200] receives 7. Changing ADD to 9 gives 12. |

The packet validator is an illustrative policy with a 200 ms freshness limit. The `authenticated` field represents the outcome of a check performed elsewhere; it is not authentication. The example never controls a device. Missing feedback must not be silently treated as reward zero.

The execution trace is an invented teaching instruction set, with one instruction per address. It is not the implementation of a particular physical processor. The pipeline model assumes one cycle per stage, independent instructions, and no stalls. Delay distance is not complete stopping distance.

`expected-results.json` records the defaults used in the videos.
