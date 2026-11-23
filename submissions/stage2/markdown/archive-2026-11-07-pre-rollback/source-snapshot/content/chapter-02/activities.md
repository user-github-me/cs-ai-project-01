# Chapter 2 — Mission and optional resource

## ACT-02 — One lucky route is not a policy

**Chapter 2 — Behaviorism & Behaviorist AI**

Pip takes a new route and arrives early once. “Best route forever!” it announces. Its teammate asks whether one reward is enough evidence.

**Goal:** Calculate a Q-learning update and distinguish an estimate from a guaranteed outcome.

**Preparation:** Calculator or paper. Optional standard-library Python script. Know reward, policy, value, alpha and gamma from this chapter.

**Task:**

1. Use old Q = 2, alpha = 0.5, reward = 1, gamma = 0.9 and best next Q = 4. Predict whether the estimate will rise or fall.
2. Calculate target = reward + gamma × best next Q; error = target − old Q; change = alpha × error; new Q = old Q + change.
3. Repeat with the same old Q, alpha and reward but a terminal next state. Set future value to zero.
4. Optional command: python3 supporting/BlueImpulse_Demonstrations.py --topic rl. Compare values. Explain whether either update proves a route is safest.

**Observe and record:** Record the target, temporal-difference error, change and new value for both cases.

**Reflect:** Why is the future term zero at termination? Why can exploration remain useful after a positive outcome? What safety rule would constrain a real robot’s exploration?

**Feedback — check after trying:** Non-terminal: target 4.6, error 2.6, change 1.3, new Q 3.3. Terminal: target 1, error −1, change −0.5, new Q 1.5. These are updated estimates, not proofs. Use many relevant transitions and evaluate behaviour against the task, including safety constraints.

**Optional resource:** R1 (full introduction and offline alternative follow).

## R1 — Reinforcement Learning: An Introduction, second edition

Richard S. Sutton and Andrew G. Barto, MIT Press, 2018.

http://incompleteideas.net/book/the-book-2nd.html

**Relevant section:** Chapter 3 (finite Markov decision processes) and Section 6.5 (Q-learning)

**Why use it:** Primary textbook support for the agent/environment distinction, expected return and the Q-learning update.

**Learner task:** After ACT-02, explain in your own words what the bootstrapped target includes, then compare it with the terminal-state case.

**Limits:** The book is mathematically deeper than this beginner guide. Start with the supplied worked calculation; do not treat the browser page as required activity content.

**Offline alternative:** The formula, both complete calculations and interpretation are included in ACT-02 and the chapter, so the task works offline.

**Access:** Optional public web resource; no account required to read the cited page. Signed-out HTTP access was checked on 7 November 2026. Availability on every campus network is not guaranteed. All essential task instructions and feedback are supplied locally.
