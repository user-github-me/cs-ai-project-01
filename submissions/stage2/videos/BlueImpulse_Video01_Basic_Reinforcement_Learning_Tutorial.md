# Video 01 — Basic reinforcement learning: tutorial companion

**Video file:** BlueImpulse_Video01_Basic_Reinforcement_Learning.mp4  
**Viewing position:** 1 of 5  
**Duration:** 10:00 (600 seconds)  
**Format:** MP4, 1920 × 1080, 60 fps  
**File size:** 47,425,849 bytes (47.43 MB)

**Prerequisites:** Basic arithmetic and the meanings of state and action. No programming experience is needed.

**Learning goals:**

- Name the learning loop
- Balance exploration and exploitation
- Calculate one Q-value update

**Chapter and subtopic connections:**

- Chapter 2 — Behaviorism & Behaviorist AI / The reinforcement-learning loop
- Chapter 2 — Behaviorism & Behaviorist AI / Rewards, policies & values
- Chapter 2 — Behaviorism & Behaviorist AI / Explore or exploit?
- Chapter 2 — Behaviorism & Behaviorist AI / Update a Q value
- Chapter 2 — Behaviorism & Behaviorist AI / Training is different from using a policy

**Apply in the learning system:** Complete ACT-02 in the Study Guide / Markdown activity file. Use Test Bank questions TF05–TF08, MC05–MC08 and OE02 for review. The six-chapter PPT deck introduces the same chapter concepts through classroom discussion.

**Optional interactive companion:** ROVERLAB lets you apply these ideas by building a robot, connecting its network and comparing stimulus-response rules. Play at https://roverlab-blue-impulse.vercel.app and use the ROVERLAB activity in the Study Guide. It is a simplified rule-and-feedback model, not a neural network or the numerical Q-learning algorithm taught in Video 01.

**Materials:** Paper and a calculator are sufficient. The optional supporting Python demonstration uses Python 3.9 or newer with no third-party packages or account.

```sh
python3 supporting/BlueImpulse_Demonstrations.py --topic rl
```

## How to learn with this tutorial

Watch the opening problem, write a prediction, and follow the labelled mechanism. Pause during each learning check before reading the feedback. After the worked example, change one input and explain why the result changes. The tutorial is self-contained: all inputs, instructions and expected outputs are below.

## Chapter timestamps and teaching route

| Time | Teaching step | Chapter / subtopic |
| --- | --- | --- |
| 00:00–00:32 | Pip’s route is blocked | Chapter 2 — Behaviorism & Behaviorist AI / The reinforcement-learning loop |
| 00:32–01:11 | Today’s route | Chapter 2 — Behaviorism & Behaviorist AI / The reinforcement-learning loop |
| 01:11–02:15 | Follow the learning loop | Chapter 2 — Behaviorism & Behaviorist AI / The reinforcement-learning loop |
| 02:15–03:19 | Reward, policy, value | Chapter 2 — Behaviorism & Behaviorist AI / Rewards, policies & values |
| 03:19–04:11 | The restaurant analogy | Chapter 2 — Behaviorism & Behaviorist AI / Explore or exploit? |
| 04:11–04:53 | Is the familiar route certainly best? | Chapter 2 — Behaviorism & Behaviorist AI / Explore or exploit? |
| 04:53–05:38 | What is a Q value? | Chapter 2 — Behaviorism & Behaviorist AI / Update a Q value |
| 05:38–06:36 | Work through the worked update | Chapter 2 — Behaviorism & Behaviorist AI / Update a Q value |
| 06:36–07:45 | A better estimate, not a proof | Chapter 2 — Behaviorism & Behaviorist AI / Update a Q value |
| 07:45–08:29 | Try a terminal state | Chapter 2 — Behaviorism & Behaviorist AI / Update a Q value |
| 08:29–09:30 | Experience changes estimates | Chapter 2 — Behaviorism & Behaviorist AI / Training is different from using a policy |
| 09:30–10:00 | Pip completes the shift | Chapter 2 — Behaviorism & Behaviorist AI / The reinforcement-learning loop |

## Reproduce the Q-learning demonstration

Use old Q = 2, alpha = 0.5, reward = 1, gamma = 0.9 and best next Q = 4. Alpha is the learning rate and gamma discounts future return. The step-by-step arithmetic is:

| Step | Calculation | Result |
| --- | --- | --- |
| Target | 1 + 0.9 × 4 | 4.6 |
| Error | 4.6 − 2 | 2.6 |
| Change | 0.5 × 2.6 | 1.3 |
| Updated value | 2 + 1.3 | 3.3 |

**Practice:** Keep old Q, alpha and reward unchanged but make the next state terminal. Predict the new value before reading on.

**Checked answer:** The future contribution is zero. Target = 1; error = −1; change = −0.5; new Q = 1.5. An estimate may fall after evidence as well as rise. Neither update proves that the next action will succeed.


## Guided explanation

### 00:00 — Pip’s route is blocked

**Reference:** Chapter 2 — Behaviorism & Behaviorist AI / The reinforcement-learning loop

Pip, the coffee is getting cold! Our simulated campus rover has a delivery to make, but its familiar route is blocked. Repeating yesterday's move will not solve today's problem. Pip needs useful feedback, and a way to change its estimates.

Have you ever wondered how an agent learns which action to try? In Chapter two, Behaviorism and Behaviorist AI, we will connect the reinforcement-learning loop to one numerical update.

### 01:11 — Follow the learning loop

**Reference:** Chapter 2 — Behaviorism & Behaviorist AI / The reinforcement-learning loop

Start with the subtopic The reinforcement-learning loop. One interaction connects an observation, an action, and feedback. The agent selects an action. The environment changes and returns the next state and a reward. The learning algorithm uses that experience to improve the policy, which is the strategy for choosing actions.

For our grid, the state could be the current square, and an action could be moving right. The reward is a number associated with the result. It is feedback, not a complete instruction manual. Notice the return arrow. Learning depends on connecting an action to what happened after it.

For Pip, define the state before choosing an action. A location alone may be insufficient if a barrier can change the route. The environment includes what happens after the action. The reward is feedback about that outcome, not a replacement for observing the next state.

### 02:15 — Reward, policy, value

**Reference:** Chapter 2 — Behaviorism & Behaviorist AI / Rewards, policies & values

The subtopic Rewards, policies and values separates three ideas that are easy to confuse. Think of a journey. The reward scores an outcome now, while the policy chooses the next move. A value estimate predicts how much return a choice may lead to, including later outcomes.

A route with a small cost now can still be worthwhile if it reaches a better destination. That is why choosing the biggest immediate reward is not always the best long-term decision. A poorly chosen reward can encourage a shortcut that misses the designer's real goal.

Suppose the reward gives a point for moving, regardless of direction. Pip could keep moving in circles and collect points without completing a delivery. An objective and a reward design are connected, but they are not automatically identical. Test whether the rewarded behaviour is the behaviour you actually wanted.

### 03:19 — The restaurant analogy

**Reference:** Chapter 2 — Behaviorism & Behaviorist AI / Explore or exploit?

Use a restaurant to understand the subtopic Explore or exploit? Ordering the dish you currently believe is best is exploitation. Trying a different dish is exploration. Exploration gathers information because your current estimates might be wrong.

In our epsilon-greedy example, epsilon is zero point one, giving a ten percent exploration probability. Otherwise, the agent chooses an action with the highest current Q value. These percentages describe probabilities over choices, not a promise that exactly one out of every ten choices explores.

In a real physical system, exploration also needs safety constraints. A simulation is a useful place to experiment.

### 04:11 — Is the familiar route certainly best?

**Reference:** Chapter 2 — Behaviorism & Behaviorist AI / Explore or exploit?

Pause and think. One route has worked twice. Another route has never been tried. Does that prove the first route is better? Take a few seconds before we reveal the answer. No. The evidence is incomplete, so the familiar route is not certainly the better one.

Exploration may improve the estimate, but it has a cost. The design must balance information and performance. Write one sentence explaining why exploitation uses estimated future return, rather than only the next reward.

**Check your answer:** No. The evidence is incomplete.

### 04:53 — What is a Q value?

**Reference:** Chapter 2 — Behaviorism & Behaviorist AI / Update a Q value

Now use the subtopic Update a Q value. Q associates a state and an action with an estimated return. Q-learning is called model-free because it does not require a supplied model of environment transitions. Model-free does not mean memory-free. The estimates still live in a table or another representation.

The update combines an old estimate with a target derived from new experience. Alpha controls how far the estimate moves toward that target. Gamma discounts the future-value contribution. We will keep every input visible, so you can reproduce the arithmetic yourself.

### 05:38 — Work through the worked update

**Reference:** Chapter 2 — Behaviorism & Behaviorist AI / Update a Q value

Start with an old Q value of two and a learning rate, alpha, of zero point five. The reward is one, gamma is zero point nine, and the best next Q value is four. First calculate the target: one plus zero point nine times four. The target is four point six.

Next subtract the old estimate. Four point six minus two gives an error of two point six. Multiply that error by alpha. Half of two point six is one point three. Finally add the change to the old value. Two plus one point three gives three point three.

Watch the estimate move halfway toward the target. That halfway movement is what alpha equals one half means here. The supporting Python file repeats this calculation and prints every intermediate value for you to inspect.

### 06:36 — A better estimate, not a proof

**Reference:** Chapter 2 — Behaviorism & Behaviorist AI / Update a Q value

This experience raised the estimate from two to three point three. Now decide what that result actually means. It did not prove that the action is always best. One observation is not a reliable policy. Repeated experience, an appropriate learning schedule, and enough exploration are still important.

There is also a special case: when the next state is terminal, the future-value term is zero. That prevents the calculation from inventing future reward after the episode has ended. Compare these two ideas: updating an estimate from evidence, and guaranteeing the outcome of the next action.

They are different claims, and only the first follows from our calculation. Imagine that the next trial gives different feedback. One sample is noisy evidence, so another update can move the estimate again. The learning rate controls how strongly this experience changes the estimate. It does not turn a single successful delivery into a guarantee.

### 07:45 — Try a terminal state

**Reference:** Chapter 2 — Behaviorism & Behaviorist AI / Update a Q value

Your turn. Keep the old value at two, alpha at one half, and the reward at one. Make the next state terminal. What is the new Q value? Pause the video if you need more time. The future contribution is zero, so the target is one. The error is one minus two, or negative one.

Half that error is negative one half. Add it to two, giving a new value of one point five. The estimate falls because the observed target is lower. A learning update can decrease a value as well as increase it.

**Check your answer:** New Q = 2 + 0.5 × (1 − 2) = 1.5

### 08:29 — Experience changes estimates

**Reference:** Chapter 2 — Behaviorism & Behaviorist AI / Training is different from using a policy

Return to Pip's blocked route. The agent acts, receives feedback, and learns a policy from experience. Reward scores an outcome. Value estimates return. Exploration improves information, while exploitation uses the best current estimates. Our worked Q update produced three point three, and our terminal-state practice produced one point five.

The training-and-deployment distinction matters: running an already learned policy is not the same as training it online. A fixed sensor-response rule can control a machine without learning at all. Before moving on, explain the loop to someone else and run the included calculation with one changed reward.

Pip's improvement is a change in an estimate and, possibly, a later choice. It is not proof that every new street or unexpected obstacle has been solved.

## Finish by explaining, not copying

Complete ACT-02 and the named Test Bank questions, then explain the mechanism without following the highlight. State one assumption of the worked model and one condition that could make the outcome differ in a real system. A correct calculation supports only the conclusion it actually measures.
