# Blue Impulse — Offline activity setup

All six missions work with paper and the data in the chapter. For five optional demonstrations, use Python 3.9 or newer; no third-party package, account, internet connection or API key is required.

From this folder run:

```sh
python3 BlueImpulse_Demonstrations.py --topic all
python3 BlueImpulse_Demonstrations.py --topic execution --add 9
python3 BlueImpulse_Demonstrations.py --topic network --speed 2
```

The available topic values are `rl`, `hardware`, `network`, `networked-ai`, and `execution`. Output is JSON so a learner can compare exact intermediate states. `expected-results.json` records the default output; `modified-results.json` records the two changes above. The toy models are deliberately limited: no physical braking simulation, cryptographic authentication or real ISA is implemented. ACT-06 uses a supplied fictional design table and needs no code.
