# Chapter 2 — Behaviorism & Behaviorist AI

**Learning outcome:** Distinguish classical and operant conditioning; identify stimulus–response rules and layered robotics; explain reinforcement-learning components, policies, values and exploration; interpret a Q update and the parts of an MDP.

**Prerequisites:** Read the relevant earlier chapters; this chapter connects those ideas to behaviorism & behaviorist ai.

## Learning from the environment

### Start with observable behaviour

Behaviourism studies the relationship between observable behaviour and environmental events. A stimulus is a detectable event; a response is an observable reaction. Pavlov, Watson and Skinner contributed to different strands of this tradition. The approach helped make learning measurable, although it is not a complete description of every kind of human learning.

### Two kinds of conditioning

| Classical conditioning | Operant conditioning |
| --- | --- |
| A cue becomes associated with another stimulus. | An action becomes associated with its consequences. |
| A bell paired with food can trigger salivation. | Sitting followed by a treat can become more frequent. |
| Focus: an elicited response. | Focus: behaviour shaped by reinforcement or punishment. |

### Connect the analogy carefully

Reinforcement learning borrows the idea of learning from consequences, but an algorithm is not a human or animal mind. A numerical reward is a training signal. It does not imply feelings, understanding or consciousness. Use the analogy to identify a feedback relationship, then describe the computational mechanism precisely.

### Apply and check

**Try before reading feedback:** A robot receives reward +1 after turning left. Does that numerical signal prove it feels pleasure?

**Feedback:** No. Reward is an algorithmic training signal. The animal-learning analogy does not establish subjective experience.

**Practice connection:** Exercise 2.1 in exercises.md; explained answer in solutions.md.

## React first: behaviour-based robots

### A sensor can trigger a useful action

A simple robotic vacuum may move forward until a bumper is pressed, then reverse and turn. Its environment is the room, its stimulus is the bumper signal, and its response is the movement. These rules can produce useful behaviour without a detailed map. If the rules never change from experience, this is reactive control rather than reinforcement learning.

### A direct feedback path

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Sensor |
| 2 | Behaviour rule |
| 3 | Actuator |
| 4 | Environment |

Situated systems act in an environment; embodied systems have a physical body that constrains and enables action.

### Layers and priorities

Brooks’ subsumption architecture coordinates relatively simple behaviour modules. A module can inhibit or suppress another module’s output under specified conditions. A designer might combine wandering, obstacle avoidance and task seeking while protecting a safety stop. This is one design approach, not a claim that all map-based planning is slow or unreliable; practical robots often combine reactive control and planning.

### Apply and check

**Try before reading feedback:** Pip always reverses when its bumper triggers. No parameter ever changes. Is that alone evidence of reinforcement learning?

**Feedback:** No. It demonstrates a fixed reactive rule. RL requires a learning mechanism that uses experience to update values or a policy.

**Practice connection:** Exercise 2.3 in exercises.md; explained answer in solutions.md.

## The reinforcement-learning loop

### Learn a policy through experience

Reinforcement learning is a way for an agent to learn decisions through interaction. The agent observes a state or observation, selects an action, and receives feedback from the environment. A learning algorithm uses that experience to improve a policy: the rule or strategy for choosing actions. The objective is usually expected cumulative reward, not just the next reward.

### One interaction at time t

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Agent / policy |
| 2 | Action |
| 3 | Environment |
| 4 | Next state + reward |

Repeat: observe, act, receive feedback, then update. The learning update may occur during training rather than every deployed action.

### Name the components

| Component | Grid-world example |
| --- | --- |
| Agent / environment | A simulated rover / a grid with obstacles. |
| State / action | Current square / move up, down, left or right. |
| Reward / policy | Points for outcomes / a strategy for selecting moves. |

### Apply and check

**Try before reading feedback:** In a maze, identify an action and a reward without confusing them.

**Feedback:** “Move left” is an action; “−1 for that transition” is a numerical reward. The environment also returns a next state or observation.

**Practice connection:** Exercise 2.4a in exercises.md; explained answer in solutions.md.

## Rewards, policies & values

### Feedback evaluates an outcome

A reward is a numerical signal associated with an interaction. It may be positive, zero or negative. A reward of −1 is not a moral judgement: its role is defined by the task. Designers might reward reaching a goal, penalise a collision and charge a small cost per step. Poorly chosen rewards can encourage shortcuts that defeat the intended goal.

### Distinguish the three ideas

The reward says how an outcome scores now. A policy says what action to choose in a situation. A value estimate says how much future reward is expected from a state or a state–action choice. A good policy may accept a small immediate cost to achieve a larger long-term return. Q-learning estimates action values and derives choices from them.

### The learning question

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Experience |
| 2 | Value estimate |
| 3 | Policy improvement |

A fixed rule such as “if hot, turn on fan” may control a system effectively without learning any values or changing a policy.

### Apply and check

**Try before reading feedback:** A route costs −1 now but leads to a large later reward. Why might a good policy choose it?

**Feedback:** It can maximise expected cumulative return. Immediate reward and long-term value are different quantities.

**Practice connection:** Exercise 5.3a in exercises.md; explained answer in solutions.md.

## Explore or exploit?

### Use the restaurant analogy

Exploitation is ordering a dish you already believe is best. Exploration is trying another dish to learn more about it. In an RL task, exploitation chooses the action with the best current value estimate, including future return. Exploration gathers information about other actions. Early estimates can be wrong, so always exploiting can lock an agent into an inferior policy.

### An epsilon-greedy example

| Choice rule | With epsilon = 0.10 |
| --- | --- |
| Explore | With 10% probability, choose a random permitted action. |
| Exploit | Otherwise choose an action with the highest current Q value. |
| During training | Measure outcomes and update estimates; epsilon may change over time. |

### Think before choosing

Suppose one route has worked twice and another has never been tried. Is the first route certainly better? No: evidence is incomplete. Exploration can improve knowledge, but it also has a cost. In physical systems, experiments must respect safety constraints; training in a simulation does not automatically make every real-world action safe.

### Apply and check

**Try before reading feedback:** A policy always selects the route with the best estimate from just one trial. What is the risk?

**Feedback:** An inaccurate early estimate may never be corrected because other routes are not explored. Exploration provides evidence but may have costs.

**Practice connection:** Exercise 2.4b in exercises.md; explained answer in solutions.md.

## Update a Q value

### A table of learned action values

Q(s, a) estimates the return from taking action a in state s and then following a good policy. Q-learning is model-free: it learns from transitions without needing a supplied transition model. “Model-free” does not mean memory-free or that the agent lacks a table or neural network.

### The update rule

Q(new) = Q(old) + alpha × [reward + gamma × max Q(next state, next action) − Q(old)]. Alpha controls the size of an update. Gamma discounts future rewards. The quantity in square brackets is the temporal-difference error. For a terminal next state, use zero for the future-value term.

### Work through one illustrative update

| Quantity | Value |
| --- | --- |
| Old Q / alpha | 2 / 0.5 |
| Reward / gamma / best next Q | 1 / 0.9 / 4 |
| Target | 1 + 0.9 × 4 = 4.6 |
| New Q | 2 + 0.5 × (4.6 − 2) = 3.3 |

### Interpret the result

This experience raised the estimate from 2 to 3.3. It did not prove the action is always best. Repeated experience, an appropriate learning schedule and sufficient exploration are important; one reward does not establish a reliable policy.

### Apply and check

**Try before reading feedback:** For old Q = 2, alpha = 0.5 and a terminal reward of 1, what is new Q?

**Feedback:** At a terminal state future value is zero: 2 + 0.5 × (1 − 2) = 1.5.

**Practice connection:** Exercise 2.4b in exercises.md; explained answer in solutions.md.

## A decision problem as an MDP

### Five parts of a Markov decision process

| Symbol | Meaning |
| --- | --- |
| S | Possible states. |
| A | Available actions. |
| P | Transition probabilities: where an action can lead. |
| R | Reward function: how outcomes are scored. |
| gamma | Discount factor: how future rewards are weighted. |

### The Markov property

A state is Markov when it contains the information needed to predict the next-state and reward distribution, given the current action. Earlier history adds no further predictive information once that state is known. A position alone may be insufficient: a robot may also need speed, battery level or whether it is carrying a package.

### Observation is not always state

Sensors can provide incomplete or noisy observations. A camera view may hide an obstacle or omit velocity. An agent may need memory or a state estimate to work with partial information. A simple grid world is useful because we can explicitly specify the state, actions, transitions and rewards instead of assuming the agent knows everything.

### Apply and check

**Try before reading feedback:** Two robots occupy the same square but have different speeds. Can position alone always be a Markov state?

**Feedback:** No. If speed changes the distribution of next outcomes, a sufficient state must include it or an equivalent representation.

**Practice connection:** Exercise 2.4a in exercises.md; explained answer in solutions.md.

## Actions can have uncertain outcomes

### A slippery grid square

Imagine an agent choosing “forward”. In this illustrative environment, it reaches the intended square with probability 0.8 and slips sideways with probability 0.2. The action is chosen by the agent; the transition outcome is sampled by the environment. The probabilities for all possible next outcomes must sum to 1.

### One action, two outcomes

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Choose forward |
| 2 | Target: probability 0.8 |
| 3 | Slip: probability 0.2 |

For immediate rewards of +10 and −5, the expected immediate reward is 0.8 × 10 + 0.2 × (−5) = 7. Future rewards may change which action is best.

### Expected is not guaranteed

An expected value of 7 does not mean every attempt earns 7. It summarises the average implied by the model. A system that learns under one set of transition probabilities may perform poorly when its environment changes. Test across plausible conditions rather than judging a policy from a single successful run.

### Apply and check

**Try before reading feedback:** Pip earns +10 with probability 0.8 and −5 with probability 0.2. Must one trial earn the expected value 7?

**Feedback:** No. The expectation is 0.8 × 10 − 0.2 × 5 = 7, but an individual trial has one of the defined outcomes.

**Practice connection:** Exercise 2.4a in exercises.md; explained answer in solutions.md.

## Training is different from using a policy

### Separate two phases

During training, the system collects experience and updates estimates or policy parameters. During deployment, it may use a fixed learned policy without further learning. Some applications allow controlled online updates, but adaptation is not automatic. A robot can react to a new sensor reading while keeping exactly the same policy.

### Test what was actually learned

Check whether success persists with different starting states, sensor noise and changed conditions. Compare against a simple fixed-rule baseline. Examine failure cases as well as average reward. If the goal is “arrive safely”, a reward that only measures speed may produce an undesirable strategy even when the algorithm is working as specified.

### A responsible learning workflow

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Define the task |
| 2 | Train / explore |
| 3 | Evaluate |
| 4 | Deploy / monitor |

Behaviour-based robotics, reinforcement learning and neural networks are related ideas, not interchangeable labels. A system can use one without using all three.

### Apply and check

**Try before reading feedback:** Pip reacts to a newly seen obstacle using a frozen trained policy. Did that reaction necessarily train the model?

**Feedback:** No. Inference can choose a different action from a new observation without changing any learned parameter.

**Practice connection:** Exercise 2.2 in exercises.md; explained answer in solutions.md.

## Chapter review

Complete ACT-02 using the supplied mission instructions. Then choose two related terms and explain a mechanism using both; identify one limitation of the teaching model and one condition that could change the result.

## Reference support

- R1: Reinforcement Learning: An Introduction, second edition — Chapter 3 (finite Markov decision processes) and Section 6.5 (Q-learning). http://incompleteideas.net/book/the-book-2nd.html

Full resource introductions, optional tasks and access alternatives are in ../references.md.
