# Video 01: Basic reinforcement learning

Duration: 08:35. Video: `BlueImpulse_Video01_Basic_Reinforcement_Learning.mp4`.

## Learning objectives

- Name the learning loop
- Balance exploration and exploitation
- Calculate one Q-value update

## 00:00–00:34 · How does a rover learn a route?

Study guide page 25. Visual: hook.

Have you ever wondered how a rover could learn a useful route without someone writing every turn?

Imagine a simulated rover choosing between two paths, trying moves, and receiving points for the outcomes.

The important question is how that experience changes its next decision.

Keep your Blue Impulse study guide open at page twenty-five. We will work directly through the book.

By the end, you will calculate a learning update yourself and explain what the result actually means.


## 00:34–01:11 · Today’s route

Study guide page 25. Visual: objectives.

Today you will identify an agent, an environment, a state, an action, a reward, and a policy.

You will compare exploration with exploitation, then work through the numerical example on page twenty-eight.

Welcome to the tutorial on basic reinforcement learning by Blue Impulse.

Have paper ready for one calculation. The tutorial PDF includes the same worked steps and practice question.

Treat our rover as an illustration. We are explaining a learning method, not claiming every real rover learns this way.


## 01:11–01:52 · Follow the learning loop

Study guide page 25. Visual: book.

Look at the diagram on page twenty-five, titled One interaction at time t.

The agent selects an action. The environment changes and returns the next state and a reward.

The learning algorithm uses that experience to improve the policy, which is the strategy for choosing actions.

For our grid, the state could be the current square, and an action could be moving right.

The reward is a number associated with the result. It is feedback, not a complete instruction manual.

Notice the return arrow. Learning depends on connecting an action to what happened after it.


## 01:52–02:34 · Reward, policy, value

Study guide page 26. Visual: compare.

Page twenty-six separates three ideas that are easy to confuse: reward, policy, and value.

Think of a journey. The reward scores an outcome now, while the policy chooses the next move.

A value estimate predicts how much return a choice may lead to, including later outcomes.

A route with a small cost now can still be worthwhile if it reaches a better destination.

That is why choosing the biggest immediate reward is not always the best long-term decision.

The book also warns that poorly chosen rewards can encourage shortcuts that miss the designer's real goal.


## 02:34–03:24 · The restaurant analogy

Study guide page 27. Visual: book.

Turn to page twenty-seven and use the book's restaurant analogy.

Ordering the dish you currently believe is best is exploitation. Trying a different dish is exploration.

Exploration gathers information because your current estimates might be wrong.

In the book's epsilon-greedy example, epsilon is zero point one, giving a ten percent exploration probability.

Otherwise, the agent chooses an action with the highest current Q value.

These percentages describe probabilities over choices, not a promise that exactly one out of every ten choices explores.

In a real physical system, exploration also needs safety constraints. A simulation is a useful place to experiment.


## 03:24–04:05 · Is the familiar route certainly best?

Study guide page 27. Visual: question.

Pause and think. One route has worked twice. Another route has never been tried.

Does that prove the first route is better? Take a few seconds before we reveal the answer.

**[Pause for 5 seconds. Keep the answer hidden.]**

No. The evidence is incomplete, so the familiar route is not certainly the better one.

Exploration may improve the estimate, but it has a cost. The design must balance information and performance.

Write one sentence explaining why exploitation uses estimated future return, rather than only the next reward.

On-screen question: Two successes versus an untried route: proof?

Answer after the pause: No. The evidence is incomplete.


## 04:05–04:49 · What is a Q value?

Study guide page 28. Visual: book.

Now open page twenty-eight, Update a Q value. Q associates a state and an action with an estimated return.

The book calls Q-learning model-free because it does not require a supplied model of environment transitions.

Model-free does not mean memory-free. The estimates still live in a table or another representation.

The update combines an old estimate with a target derived from new experience.

Alpha controls how far the estimate moves toward that target. Gamma discounts the future-value contribution.

We will use exactly the numbers in the guide, so you can check each line against the page.


## 04:49–05:45 · Work through the book’s update

Study guide page 28. Visual: q-demo.

Start with an old Q value of two and a learning rate, alpha, of zero point five.

The reward is one, gamma is zero point nine, and the best next Q value is four.

First calculate the target: one plus zero point nine times four. The target is four point six.

Next subtract the old estimate. Four point six minus two gives an error of two point six.

Multiply that error by alpha. Half of two point six is one point three.

Finally add the change to the old value. Two plus one point three gives three point three.

Watch the estimate move halfway toward the target. That halfway movement is what alpha equals one half means here.

The supporting Python file repeats this calculation and prints every intermediate value for you to inspect.


## 05:45–06:34 · A better estimate, not a proof

Study guide page 28. Visual: book.

Return to the final paragraph on page twenty-eight. This experience raised the estimate from two to three point three.

It did not prove that the action is always best. One observation is not a reliable policy.

Repeated experience, an appropriate learning schedule, and enough exploration are still important.

There is also a special case: when the next state is terminal, the future-value term is zero.

That prevents the calculation from inventing future reward after the episode has ended.

Compare these two ideas: updating an estimate from evidence, and guaranteeing the outcome of the next action.

They are different claims, and only the first follows from our calculation.


## 06:34–07:17 · Try a terminal state

Study guide page 28. Visual: question.

Your turn. Keep the old value at two, alpha at one half, and the reward at one.

Make the next state terminal. What is the new Q value? Pause the video if you need more time.

**[Pause for 6 seconds. Keep the answer hidden.]**

The future contribution is zero, so the target is one. The error is one minus two, or negative one.

Half that error is negative one half. Add it to two, giving a new value of one point five.

The estimate falls because the observed target is lower. A learning update can decrease a value as well as increase it.

On-screen question: Terminal state: old Q = 2, α = 0.5, reward = 1

Answer after the pause: New Q = 2 + 0.5 × (1 − 2) = 1.5


## 07:17–08:07 · Experience changes estimates

Study guide page 31. Visual: recap.

Let's recap using pages twenty-five through twenty-eight. The agent acts, receives feedback, and learns a policy from experience.

Reward scores an outcome. Value estimates return. Exploration improves information, while exploitation uses the best current estimates.

Our worked Q update produced three point three, and our terminal-state practice produced one point five.

Page thirty-one adds an important distinction: running an already learned policy is not the same as training it online.

A fixed sensor-response rule can control a machine without learning at all.

Before moving on, explain the loop to someone else and run the included calculation with one changed reward.


## 08:07–08:35 · Blue Impulse study guide

Study guide page 1. Visual: credits.

This tutorial was taught from the Blue Impulse study guide, especially pages twenty-four to twenty-eight and thirty-one.

The cover on screen is the original cover of your book.

Use the companion tutorial PDF, narration script, subtitles, and Python demonstration to practise at your own pace.

Blue Impulse study guide. Learn the reasoning, then test it with an example.
