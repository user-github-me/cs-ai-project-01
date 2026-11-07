# Video 01 — Basic reinforcement learning: narration script and teaching outline

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

**Materials:** Paper and a calculator are sufficient. The optional supporting Python demonstration uses Python 3.9 or newer with no third-party packages or account.

```sh
python3 supporting/BlueImpulse_Demonstrations.py --topic rl
```

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

## Using this script

The following narration is the exact measured cue text for the revised recording. Cue timestamps refer to the video timeline; small gaps include intentional thinking time and transition space. The voice is synthetic (Kokoro ONNX, am_michael), not a recording of a student. The full teaching outline states the purpose, visual focus and learner action alongside the words spoken.

### 00:00–00:32 — Pip’s route is blocked

**Content reference:** Chapter 2 — Behaviorism & Behaviorist AI / The reinforcement-learning loop

**Teaching / visual direction:** Keep Pip’s problem visible while the opening question establishes why the concept matters. Key visual labels: PIP / ROUTE BLOCKED / TRY AGAIN.

**00:00.150–00:02.347:** Pip, the coffee is getting cold!

**00:02.347–00:08.533:** Our simulated campus rover has a delivery to make, but its familiar route is blocked.

**00:08.533–00:17.133:** Repeating yesterday's move will not solve today's problem. Pip needs useful feedback, and a way to change its estimates.

**00:17.133–00:21.591:** Have you ever wondered how an agent learns which action to try?

**00:21.591–00:30.660:** In Chapter two, Behaviorism and Behaviorist AI, we will connect the reinforcement-learning loop to one numerical update.

### 00:32–01:11 — Today’s route

**Content reference:** Chapter 2 — Behaviorism & Behaviorist AI / The reinforcement-learning loop

**Teaching / visual direction:** Reveal the learning goals in the order spoken, then retain a small progress cue. Key visual labels: LOOP / CHOICES / Q UPDATE.

**00:32.498–00:39.921:** Today you will identify an agent, an environment, a state, an action, a reward, and a policy.

**00:39.921–00:47.984:** You will compare exploration with exploitation, then calculate the example in the subtopic Update a Q value.

**00:47.984–00:53.338:** Welcome to the tutorial on basic reinforcement learning by Blue Impulse.

**00:53.338–01:01.338:** Have paper ready for one calculation. The tutorial PDF includes the same worked steps and practice question.

**01:01.338–01:09.468:** Treat our rover as an illustration. We are explaining a learning method, not claiming every real rover learns this way.

### 01:11–02:15 — Follow the learning loop

**Content reference:** Chapter 2 — Behaviorism & Behaviorist AI / The reinforcement-learning loop

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: STATE / ACTION / REWARD / NEXT STATE.

**01:11.628–01:20.271:** Start with the subtopic The reinforcement-learning loop. One interaction connects an observation, an action, and feedback.

**01:20.271–01:27.097:** The agent selects an action. The environment changes and returns the next state and a reward.

**01:27.097–01:34.968:** The learning algorithm uses that experience to improve the policy, which is the strategy for choosing actions.

**01:34.968–01:40.536:** For our grid, the state could be the current square, and an action could be moving right.

**01:40.536–01:47.938:** The reward is a number associated with the result. It is feedback, not a complete instruction manual.

**01:47.938–01:54.102:** Notice the return arrow. Learning depends on connecting an action to what happened after it.

**01:54.102–02:02.617:** For Pip, define the state before choosing an action. A location alone may be insufficient if a barrier can change the route.

**02:02.617–02:12.220:** The environment includes what happens after the action. The reward is feedback about that outcome, not a replacement for observing the next state.

### 02:15–03:19 — Reward, policy, value

**Content reference:** Chapter 2 — Behaviorism & Behaviorist AI / Rewards, policies & values

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: REWARD / POLICY / VALUE.

**02:15.280–02:21.914:** The subtopic Rewards, policies and values separates three ideas that are easy to confuse.

**02:21.914–02:28.442:** Think of a journey. The reward scores an outcome now, while the policy chooses the next move.

**02:28.442–02:34.798:** A value estimate predicts how much return a choice may lead to, including later outcomes.

**02:34.798–02:41.326:** A route with a small cost now can still be worthwhile if it reaches a better destination.

**02:41.326–02:47.981:** That is why choosing the biggest immediate reward is not always the best long-term decision.

**02:47.981–02:54.316:** A poorly chosen reward can encourage a shortcut that misses the designer's real goal.

**02:54.316–03:04.708:** Suppose the reward gives a point for moving, regardless of direction. Pip could keep moving in circles and collect points without completing a delivery.

**03:04.708–03:16.341:** An objective and a reward design are connected, but they are not automatically identical. Test whether the rewarded behaviour is the behaviour you actually wanted.

### 03:19–04:11 — The restaurant analogy

**Content reference:** Chapter 2 — Behaviorism & Behaviorist AI / Explore or exploit?

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: EXPLORE / EXPLOIT / COMPARE.

**03:19.454–03:24.040:** Use a restaurant to understand the subtopic Explore or exploit?

**03:24.040–03:31.805:** Ordering the dish you currently believe is best is exploitation. Trying a different dish is exploration.

**03:31.805–03:37.479:** Exploration gathers information because your current estimates might be wrong.

**03:37.479–03:45.756:** In our epsilon-greedy example, epsilon is zero point one, giving a ten percent exploration probability.

**03:45.756–03:50.768:** Otherwise, the agent chooses an action with the highest current Q value.

**03:50.768–03:59.902:** These percentages describe probabilities over choices, not a promise that exactly one out of every ten choices explores.

**03:59.902–04:09.056:** In a real physical system, exploration also needs safety constraints. A simulation is a useful place to experiment.

### 04:11–04:53 — Is the familiar route certainly best?

**Content reference:** Chapter 2 — Behaviorism & Behaviorist AI / Explore or exploit?

**Teaching / visual direction:** Keep the supplied question legible during the thinking interval; reveal the answer only after the pause. Key visual labels: FAMILIAR / UNTRIED / EVIDENCE?.

**Learner question:** Two successes versus an untried route: proof?

**Thinking interval:** 04:23.232–04:28.232. The viewer may pause for longer.

**04:11.628–04:17.452:** Pause and think. One route has worked twice. Another route has never been tried.

**04:17.452–04:23.232:** Does that prove the first route is better? Take a few seconds before we reveal the answer.

**04:28.232–04:34.354:** No. The evidence is incomplete, so the familiar route is not certainly the better one.

**04:34.354–04:42.396:** Exploration may improve the estimate, but it has a cost. The design must balance information and performance.

**04:42.396–04:50.950:** Write one sentence explaining why exploitation uses estimated future return, rather than only the next reward.

**Expected learning-check result:** No. The evidence is incomplete.

### 04:53–05:38 — What is a Q value?

**Content reference:** Chapter 2 — Behaviorism & Behaviorist AI / Update a Q value

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: OLD ESTIMATE / TARGET / UPDATE.

**04:53.367–05:01.708:** Now use the subtopic Update a Q value. Q associates a state and an action with an estimated return.

**05:01.708–05:09.302:** Q-learning is called model-free because it does not require a supplied model of environment transitions.

**05:09.302–05:16.725:** Model-free does not mean memory-free. The estimates still live in a table or another representation.

**05:16.725–05:22.357:** The update combines an old estimate with a target derived from new experience.

**05:22.357–05:30.335:** Alpha controls how far the estimate moves toward that target. Gamma discounts the future-value contribution.

**05:30.335–05:36.179:** We will keep every input visible, so you can reproduce the arithmetic yourself.

### 05:38–06:36 — Work through the worked update

**Content reference:** Chapter 2 — Behaviorism & Behaviorist AI / Update a Q value

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: OLD Q = 2 / TARGET = 4.6 / NEW Q = 3.3.

**05:38.759–05:45.051:** Start with an old Q value of two and a learning rate, alpha, of zero point five.

**05:45.051–05:51.131:** The reward is one, gamma is zero point nine, and the best next Q value is four.

**05:51.131–05:58.511:** First calculate the target: one plus zero point nine times four. The target is four point six.

**05:58.511–06:05.615:** Next subtract the old estimate. Four point six minus two gives an error of two point six.

**06:05.615–06:11.310:** Multiply that error by alpha. Half of two point six is one point three.

**06:11.310–06:17.795:** Finally add the change to the old value. Two plus one point three gives three point three.

**06:17.795–06:25.819:** Watch the estimate move halfway toward the target. That halfway movement is what alpha equals one half means here.

**06:25.819–06:33.669:** The supporting Python file repeats this calculation and prints every intermediate value for you to inspect.

### 06:36–07:45 — A better estimate, not a proof

**Content reference:** Chapter 2 — Behaviorism & Behaviorist AI / Update a Q value

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: ONE EXPERIENCE / BETTER ESTIMATE / NO GUARANTEE.

**06:36.672–06:44.436:** This experience raised the estimate from two to three point three. Now decide what that result actually means.

**06:44.436–06:51.668:** It did not prove that the action is always best. One observation is not a reliable policy.

**06:51.668–06:58.408:** Repeated experience, an appropriate learning schedule, and enough exploration are still important.

**06:58.408–07:05.021:** There is also a special case: when the next state is terminal, the future-value term is zero.

**07:05.021–07:11.186:** That prevents the calculation from inventing future reward after the episode has ended.

**07:11.186–07:19.078:** Compare these two ideas: updating an estimate from evidence, and guaranteeing the outcome of the next action.

**07:19.078–07:24.048:** They are different claims, and only the first follows from our calculation.

**07:24.048–07:33.139:** Imagine that the next trial gives different feedback. One sample is noisy evidence, so another update can move the estimate again.

**07:33.139–07:42.592:** The learning rate controls how strongly this experience changes the estimate. It does not turn a single successful delivery into a guarantee.

### 07:45–08:29 — Try a terminal state

**Content reference:** Chapter 2 — Behaviorism & Behaviorist AI / Update a Q value

**Teaching / visual direction:** Keep the supplied question legible during the thinking interval; reveal the answer only after the pause. Key visual labels: TERMINAL STATE / NO FUTURE RETURN / NEW Q = 1.5.

**Learner question:** Terminal state: old Q = 2, alpha = 0.5, reward = 1

**Thinking interval:** 07:58.414–08:04.414. The viewer may pause for longer.

**07:46.063–07:51.908:** Your turn. Keep the old value at two, alpha at one half, and the reward at one.

**07:51.908–07:58.414:** Make the next state terminal. What is the new Q value? Pause the video if you need more time.

**08:04.414–08:12.114:** The future contribution is zero, so the target is one. The error is one minus two, or negative one.

**08:12.114–08:19.218:** Half that error is negative one half. Add it to two, giving a new value of one point five.

**08:19.218–08:27.711:** The estimate falls because the observed target is lower. A learning update can decrease a value as well as increase it.

**Expected learning-check result:** New Q = 2 + 0.5 × (1 − 2) = 1.5

### 08:29–09:30 — Experience changes estimates

**Content reference:** Chapter 2 — Behaviorism & Behaviorist AI / Training is different from using a policy

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: OBSERVE / ACT / LEARN / TRY.

**08:29.889–08:37.312:** Return to Pip's blocked route. The agent acts, receives feedback, and learns a policy from experience.

**08:37.312–08:47.790:** Reward scores an outcome. Value estimates return. Exploration improves information, while exploitation uses the best current estimates.

**08:47.790–08:55.021:** Our worked Q update produced three point three, and our terminal-state practice produced one point five.

**08:55.021–09:03.216:** The training-and-deployment distinction matters: running an already learned policy is not the same as training it online.

**09:03.216–09:08.335:** A fixed sensor-response rule can control a machine without learning at all.

**09:08.335–09:16.462:** Before moving on, explain the loop to someone else and run the included calculation with one changed reward.

**09:16.462–09:27.686:** Pip's improvement is a change in an estimate and, possibly, a later choice. It is not proof that every new street or unexpected obstacle has been solved.

### 09:30–10:00 — Pip completes the shift

**Content reference:** Chapter 2 — Behaviorism & Behaviorist AI / The reinforcement-learning loop

**Teaching / visual direction:** Resolve the opening problem and use a concise Blue Impulse end title, returning to the opening composition. Key visual labels: BLUE IMPULSE / FOLLOW THE SIGNAL.

**09:30.933–09:34.857:** Pip's small problem now has an explanation you can test.

**09:34.857–09:42.750:** Use Chapter 2, Behaviorism & Behaviorist AI, and the named subtopics to revisit the reasoning.

**09:42.750–09:52.203:** The tutorial guide includes the full teaching steps and the checked practice answers. Run the supporting demonstration and change one input.

**09:52.203–09:57.707:** Blue Impulse. Follow the signal, predict the result, and check your explanation.

## Supporting demonstration and limits


Use old Q = 2, alpha = 0.5, reward = 1, gamma = 0.9 and best next Q = 4. Alpha is the learning rate and gamma discounts future return. The step-by-step arithmetic is:

| Step | Calculation | Result |
| --- | --- | --- |
| Target | 1 + 0.9 × 4 | 4.6 |
| Error | 4.6 − 2 | 2.6 |
| Change | 0.5 × 2.6 | 1.3 |
| Updated value | 2 + 1.3 | 3.3 |

**Practice:** Keep old Q, alpha and reward unchanged but make the next state terminal. Predict the new value before reading on.

**Checked answer:** The future contribution is zero. Target = 1; error = −1; change = −0.5; new Q = 1.5. An estimate may fall after evidence as well as rise. Neither update proves that the next action will succeed.
