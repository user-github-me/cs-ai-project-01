# Chapter 2 — Answers and expected outcomes

> Attempt each activity in draft.md before reading its answer. Calculations show every step; open questions list the
> points a good answer contains. Numbering matches draft.md.

## Pause & Try

### Pause & Try 2.1 — Learned, modified and maintained behaviour

Your examples will be personal. Any real behaviour is fine as long as you name what in the environment, or which consequence, shaped it. A model answer:

| | Example | What shaped it |
|---|---|---|
| Learned | riding a bicycle | practice and its consequences: staying balanced felt good, falling off hurt |
| Modified | leaving home 10 minutes earlier for school | a change in the environment: a new bus timetable made you late |
| Maintained | revising with flashcards before tests | a consequence that keeps paying off: good marks. If it stopped working, you would use it less |

Key points:
- A **learned** behaviour is new and appeared through experience.
- A **modified** behaviour is one you already had that changed because the environment changed.
- A **maintained** behaviour continues because it keeps paying off, and would fade if it stopped.
- Each example names something observable (a part of the environment or a consequence), not a thought or feeling.

### Pause & Try 2.2 — Self-checkout beep as S–R

- **Stimulus:** the beep after you scan the item.
- **Response:** you place the item in the bagging area.
- **Learned, not inborn.** Nobody is born knowing what a self-checkout beep means. You learned the link through experience: from the instructions on the screen, from watching other shoppers, and from the consequences (the machine waits, or warns you, until the item is in the bagging area). An inborn link, such as blinking when something flies at your face, happens without any learning. This one is like the end-of-lesson bell in the chapter's table.

### Pause & Try 2.3 — Classical conditioning at the dentist

| Part | At the dentist |
|---|---|
| UCS (unconditioned stimulus) | the painful moment (the pain itself) |
| UCR (unconditioned response) | tensing up at the pain |
| NS (neutral stimulus) | the whine of the drill before it has been paired with pain: at first it causes no tensing |
| CS (conditioned stimulus) | the sound of the drill after it has been paired with pain |
| CR (conditioned response) | tensing up at the sound of the drill alone |

The UCR and the CR are the same behaviour (tensing); only the trigger changes. The NS and the CS are the same sound, before and after learning. Tensing is an involuntary reflex that is elicited, which is why this is classical conditioning. If the drill sound kept coming without pain, the response would gradually fade (extinction).

### Pause & Try 2.4 — Praise for homework on time

- **Type of consequence:** positive reinforcement. Something pleasant (praise) is **added**, and the behaviour **increases**.
- **Voluntary or reflex:** voluntary. The student chooses to hand the homework in; it is not an automatic reaction.
- **Why operant, not classical:** the learning comes from a **consequence** (praise) that follows a voluntary action and changes how often it happens. The key event comes **after** the behaviour. In classical conditioning, an involuntary reflex becomes linked to a new stimulus that comes **before** the response, and the response earns nothing.

### Pause & Try 2.5 — Why RL is operant conditioning

Model answer: in reinforcement learning, an agent chooses an **action**, and the environment sends back a **consequence**: a numerical reward or penalty. Actions followed by good consequences become more likely, and actions followed by bad ones become less likely. This is exactly operant conditioning. Skinner's rat chose to press the lever (the action), a food pellet followed (the consequence), and it pressed more often. Classical conditioning has no chosen action and no consequence: an involuntary reflex becomes attached to a stimulus that comes before it.

Key points:
- RL means choosing actions and learning from their consequences.
- Operant conditioning means voluntary actions whose consequences change how often they happen.
- Each part has a machine version: rat → agent, lever press → action, food pellet → reward, new habit → policy.
- Classical conditioning is an association between two stimuli, with no action and no consequence.

### Pause & Try 2.6 — Symbolic robot and the moved chair

**What goes wrong:** the robot keeps following its planned route and may drive into the chair. Even if it notices the chair, it has to stop and spend about another 20 seconds mapping the room and planning again before it can move.

**Why:** a symbolic (GOFAI) robot works in the order sense → model → plan → act. It acts on its **internal map**, not on the world as it is now. The map was made before the chair moved, so 2 seconds into the journey it is already out of date and still shows the path as clear. Each stage waits for the one before, so the robot cannot react quickly to change, and the real world changes all the time. A behaviour-based robot would detect the chair with its sensors and turn away within milliseconds.

### Pause & Try 2.7 — Defining Behaviourist AI

**Definition (in your own words):** Behaviourist AI is a way of building intelligent machines that react directly to what their sensors detect, using simple links from sensors to actions. The intelligent behaviour comes from interacting with the environment, not from building a detailed internal model of the world and reasoning about it.

- **Similar:** both explain behaviour through observable interaction with the environment (stimulus → response), without relying on hidden inner states. For psychologists those are mental states; for engineers they are detailed world models.
- **Different (any one):** behaviourism is a theory in psychology that explains how animals and people learn, while Behaviourist AI is an approach in AI and robotics for building machines that behave usefully. Also acceptable: learning is the main thing behaviourism studies, but it is optional in Behaviourist AI, and many such robots never learn.

### Pause & Try 2.8 — Automatic sliding door

| Part | Automatic door |
|---|---|
| Sensor | a motion or presence sensor above the door (usually microwave or infrared) |
| Behaviour rule | IF someone is detected approaching THEN open the door; close it again once no one has been detected for a few seconds |
| Actuator | the electric motor (with its belt) that slides the door panels |
| Environment | the shop entrance: the people walking towards and through it, and the space in front of the door |

- **Stimulus:** a person moving towards the door.
- **Response:** the door slides open.

The door has no map and never learns. It is a simple reactive, behaviour-based system.

### Pause & Try 2.9 — A cat crosses the path

- **Takes control:** the **avoid obstacles** layer, which has the highest priority. Its trigger fires because an object is closer than 30 cm.
- **Suppresses:** the **seek target** layer, which was steering towards the dock. While avoid obstacles is active, its "turn away" command replaces seek target's command at the suppression point. Basic movement, which seek target was already suppressing, stays suppressed.
- **Once the cat has passed:** avoid obstacles goes quiet, so it stops suppressing. Seek target carries on steering towards the dock, as in the 9 s row of the table. If the dock signal had been lost, basic movement would drive straight ahead.

### Pause & Try 2.10 — Reactive control or learned behaviour

| System | Type | Why |
|---|---|---|
| a) thermostat: heating on below 19 °C | reactive control | a fixed rule written by a designer (IF temperature < 19 °C THEN heating on). It gives the same response every time, and experience changes nothing |
| b) chess program that wins more often after every game | learned behaviour | its performance improves with experience. It uses results (wins and losses) as feedback to change its choices |
| c) headlights that switch on when it gets dark | reactive control | a fixed rule (IF the light level is low THEN lights on) that never changes |
| d) delivery robot that starts avoiding a crowded corridor | learned behaviour | its response to the same situation changed after weeks of experience. Delays in the corridor worked like penalties |

A quick test: a system that behaves the same on day 1 and day 100 is reactive; one that gets better with experience is learning.

### Pause & Try 2.11 — Car-racing game as RL

- **Agent:** the learning program that controls the car.
- **Environment:** the game itself: the track, the other cars, the game's physics and the timer (everything outside the program).
- **State (one example):** the car's position on the track and its speed. The current screen image is also acceptable.
- **Two actions:** any two of accelerate, brake, steer left and steer right.
- **Sensible reward:** for example +1 for each checkpoint passed, a large bonus (such as +100) for finishing, −1 for every second used and −10 for crashing or leaving the track. This rewards finishing quickly and safely. A reward for speed alone would not be sensible, because it could teach the car to drive fast and crash.

### Pause & Try 2.12 — One interaction from C1

1. **Observe:** the agent sees its state. It is on C1.
2. **Choose:** its policy picks an action: move up.
3. **Respond:** the environment moves the rover to C2, an ordinary square (not the wall, the trap or the goal).
4. **Reward:** the environment sends back **−1** and the new state, **C2**.
5. **Learn:** the experience (C1, up, −1, C2) improves the agent's estimates and its policy.

### Pause & Try 2.13 — Reward, return and value from C1

- **Reward for the first move:** the arrow on C1 points up, so the first move is C1 → C2. Its reward is **−1**.
- **Return:** following the arrows, C1 → C2 (−1), C2 → C3 (−1), then C3 → D3, the goal (+10). Return = −1 − 1 + 10 = **+8**.
- **Value of C1:** V(C1) = **8**. In this grid world every move goes where intended, so the return the rover can expect from C1 is exactly the return above, which matches the 8 on the value grid.
- **Why the rover on C2 should never move right:** moving right from C2 enters D2, the trap. That earns −10 and ends the episode, so the rover can never reach the goal. Its return would be −10, against +9 for moving up (C2 → C3 → goal: −1 + 10 = 9). Moving right is 19 points worse, and because moves always go where intended it would fall in every time.

### Pause & Try 2.14 — Music app explores or exploits

- **What the app is doing:** **exploiting**. It keeps choosing the option with the best current estimate (the artist you liked first).
- **What it might be missing:** other artists or genres you would like even more. Its estimate is based on very little experience (one artist), so it could be wrong, and without exploring it can never find out. You may also get bored, so that artist's value to you can fall over time.
- **How to balance the two:** use an ε-greedy approach. For example, it could play known favourites about 90% of the time (exploit) and a new or similar artist about 10% of the time (explore). Skips and likes act as penalties and rewards that update its estimates. It can explore more at first and less once it knows your taste well.

### Pause & Try 2.15 — Epsilon-greedy with ε = 0.2

**When it exploits:** it chooses **B**, the action with the highest Q-value (6).

**Out of 100 decisions:**
- it exploits 0.8 × 100 = 80 times, always choosing B;
- it explores 0.2 × 100 = 20 times, picking A, B or C at random: 20 ÷ 3 ≈ 6.7 times each.

| Action | From exploiting | From exploring | Expected total |
|---|---|---|---|
| A (Q = 2) | 0 | ≈ 6.7 | about 7 |
| B (Q = 6) | 80 | ≈ 6.7 | 80 + 6.7 ≈ 87 |
| C (Q = 4) | 0 | ≈ 6.7 | about 7 |

The exact expected numbers are 86⅔ for B and 6⅔ each for A and C, which add up to 100. A real run of 100 decisions will vary a little. C (Q = 4) is not chosen more often than A (Q = 2), because when it explores the agent ignores the Q-values and picks completely at random.

### Pause & Try 2.16 — Reading the Q-table

- **A1:** up or right. Both have the highest Q-value, 6, so they are equally good and either answer is correct. The agent breaks the tie, for example at random.
- **C2:** up (9).
- **C3:** right (10).
- **Why right on C2 is so low (−10):** moving right from C2 enters the trap, D2. The reward is −10 and the episode ends, so no future rewards are added: Q(C2, right) = −10 + 0 = −10.
- **Why up on C3 is worth 9:** C3 is in the top row, so moving up would take the rover off the grid. It stays on C3 and the move costs −1. Acting well from C3 afterwards (right, into the goal) earns +10. So Q(C3, up) = −1 + 10 = **9**: one wasted move, then the goal.

### Pause & Try 2.17 — Short-sighted or far-sighted γ

**Answer:** the agent with **γ = 0.95** is more likely to accept a small penalty now in order to reach a large reward later.

**Why:** in the target r + γ max Q(s′, a′), γ multiplies the value of what can happen next. With γ = 0.95 the future counts almost in full; with γ = 0.1 it counts only one tenth. For example, suppose action X costs r = −1 now but leads to a state whose best Q-value is 10, and action Y earns r = +1 now but leads to a state worth 0.

| | Target for X (penalty now, +10 later) | Target for Y (+1 now, nothing later) | Preferred |
|---|---|---|---|
| γ = 0.1 | −1 + 0.1 × 10 = 0 | 1 + 0.1 × 0 = 1 | Y |
| γ = 0.95 | −1 + 0.95 × 10 = 8.5 | 1 + 0.95 × 0 = 1 | X |

The short-sighted agent (γ = 0.1) sees mostly the immediate r, so the small penalty puts it off. The far-sighted agent (γ = 0.95) sees that the later reward outweighs the cost. The gap grows with distance: a reward two steps further away is scaled by 0.1 × 0.1 = 0.01 for one agent, but by 0.95 × 0.95 ≈ 0.90 for the other.

### Pause & Try 2.18 — Q-update, ordinary and terminal

**When s′ is not terminal:**
1. Target = r + γ × max Q(s′, a′) = −1 + 0.9 × 10 = −1 + 9 = 8
2. Error = target − Q(s, a) = 8 − 4 = 4
3. New Q(s, a) = 4 + 0.2 × 4 = 4 + 0.8 = **4.8**

**When s′ is terminal**, nothing can follow it, so the γ max Q(s′, a′) term is 0:
1. Target = r = −1
2. Error = −1 − 4 = −5
3. New Q(s, a) = 4 + 0.2 × (−5) = 4 − 1 = **3**

**Why the answers differ:** in the first case the target includes the discounted value of the next state (0.9 × 10 = 9). That outweighs the −1 penalty, so the target (8) is above the old estimate (4) and Q rises. In the terminal case the episode ends, so only the −1 counts. The target is below the old estimate, so Q falls. In both cases Q moves only a fraction α = 0.2 of the way towards the target.

### Pause & Try 2.19 — A board game as an MDP

Model answer (Ludo):
- **States:** the positions of all the counters on the board (yours and your opponents'), plus the number you have just rolled.
- **Two actions:** for example, "bring a new counter out of the base" (after rolling a six) or "move my leading counter forward by the number rolled".
- **Uncertainty:** the dice roll (you cannot choose which number comes up) and your opponents' moves.
- **Reward or penalty:** for example, +10 when one of your counters reaches home and +50 for winning, or −5 when an opponent captures one of your counters and sends it back to base.

Other games are also acceptable. In Monopoly, for example, the states are your square, money and properties; the actions are buying or not buying, or building a house; the uncertainty is the dice and the Chance cards; rent received is a reward and rent paid or going to jail is a penalty. In a maze game, the states are your position and the enemies' positions; the actions are moving or jumping; the uncertainty is enemies that move unpredictably or slippery floors; coins are rewards and losing a life is a penalty. Whatever the game, the answer must include a **choice** (action) as well as the element of chance.

### Pause & Try 2.20 — Lane-only state is not Markov

**Why it is not Markov:** knowing only the lane, you cannot predict what happens next. Two cars in the same lane can have very different futures. One is travelling at 100 km/h with a stopped lorry 30 m ahead; the other is standing still at a red light. To tell them apart you would need the history (where was the car a moment ago?), so the state does not hold all the information that matters.

**Information to add (any two):**
- its speed (and direction of travel);
- its position along the road;
- the distance to the vehicle in front;
- the positions and speeds of nearby vehicles and pedestrians;
- the state of the traffic lights ahead.

### Pause & Try 2.21 — Windy-day drone as an MDP

| Ingredient | Example for the drone |
|---|---|
| S: states | the drone's position (which rooftop it is at), its battery level and whether it is carrying a parcel |
| A: actions | fly to a neighbouring rooftop (north, south, east or west), land, hover and wait, or return to base |
| P: transition probabilities | flying east reaches the intended rooftop with probability 0.7, and a gust blows it to the rooftop on either side with probability 0.15 each (0.7 + 0.15 + 0.15 = 1) |
| R: reward function | +10 for delivering a parcel to the right rooftop, −1 per flight (time and battery), −50 for crashing or running out of battery |
| γ: discount factor | γ = 0.9: future rewards count slightly less, so the drone prefers to deliver sooner |

Other sensible values are acceptable. The probabilities for one action must add up to 1, and on a windy day the chance of going where intended should be lower than on a calm day.

### Pause & Try 2.22 — Expected reward, 70% and 30%

Expected immediate reward = 0.7 × 10 + 0.3 × (−4) = 7 + (−1.2) = **5.8**

**Why the actual reward may differ:** no single attempt ever earns 5.8. Each attempt earns either +10 or −4, and chance decides which. The 5.8 is the long-run average: over 100 attempts, about 70 earn +10 and about 30 earn −4, a total of 700 − 120 = 580, or 5.8 per attempt. Over only a few attempts, luck can push the average much higher or lower (three −4s in a row, for example).

### Pause & Try 2.23 — Moving to a wet slope

**Ingredients that have changed:**
- **P (transition probabilities):** on a wet slope the wheels slip and the robot can slide, so its actions no longer lead where intended as reliably.
- **S (states):** it is a different factory with a different layout, so its positions are new. The state may also need extra information (the slope, its speed, wheel slip) to stay Markov.
- **R (reward function):** the old rewards may no longer fit. A reward for speed alone would push the robot to race across a wet floor, so designers should add a penalty for skidding or dropping parcels.
- The actions (A) and γ normally stay the same. γ is the designer's choice and does not depend on the floor.

**Two ways to adapt (any two):**
- retrain it, first in a simulation of the sloping, wet factory, building on what it already knows rather than starting from scratch;
- use online learning: keep updating its Q-values on the job with a small ε and strict safety rules;
- change the reward function (a penalty for skidding) and add slope or slip information to its state;
- keep reactive safety rules (for example, "stop if anything is within 50 cm") that override the learner.

**One risk of learning while it works:** exploring means trying untested actions on a real, slippery floor. The robot could skid into people or machines, damage parcels or slow production, and its behaviour is hard to predict while it learns. This is why a small ε, safety rules and a human supervisor are used.

### Pause & Try 2.24 — Matching parts to three ideas

| Part | Idea | Why |
|---|---|---|
| the neural network that recognises parcels | neural network | a computational model of a complex link from inputs to outputs: camera pixels go in, and which parcel it is (and where) comes out |
| Q-learning to choose routes | reinforcement learning | a learning framework: by trial and error, the robot learns from rewards and penalties which route (action) is best |
| the bumper rule that stops it on contact | behaviour-based robotics | a fixed stimulus–response rule that links a sensor (the bumper) directly to the actuators (the wheel motors), with no map and no learning. It overrides the learner like a high-priority layer in a subsumption architecture |

This robot combines all three ideas, like the walking robot in the chapter's last table.

## Practice

### Question 1 — Central principle of behaviourism

**(a)** [1 mark] Behaviour is learned, modified and maintained through interaction with the environment and through the consequences of that behaviour.

**(b)** [3 marks] One mark for each, with an example that shows the environment or a consequence at work:
- **Learned:** a new behaviour appears through experience. Example: a puppy learns to sit when told, because sitting is followed by a treat.
- **Modified:** a behaviour changes when the environment changes. Example: you take a new route to school when roadworks slow down the old one.
- **Maintained:** a behaviour continues while it keeps paying off, and fades when it stops. Example: the puppy keeps sitting while treats keep coming; if the treats stopped for good, sitting on command would gradually fade.

Other examples are acceptable if they show the same three ideas.

### Question 2 — Classical vs operant conditioning

Model answer: in classical conditioning (Pavlov), learning happens by **association between two stimuli**. A neutral stimulus (a sound) that is repeatedly paired with food comes to trigger salivation on its own, and the behaviour is an involuntary, elicited reflex. In operant conditioning (Skinner), learning happens through the **consequences of a voluntary action**. Reinforcement makes the action more likely and punishment makes it less likely, as when the rat presses the lever more because it brings food. In AI, classical conditioning parallels **pattern recognition**: learning which signals predict others. Operant conditioning is the ancestor of **reinforcement learning**: an agent learns from numerical rewards and penalties which actions to take.

Key points (4 marks):
- Classical: learning by associating two stimuli; the reflex is involuntary and the key event comes before the response.
- Operant: learning from the consequences of voluntary behaviour (reinforcement or punishment); the key event comes after the response.
- AI parallel of classical conditioning: pattern recognition (for example, a system that learns that one sensor signal usually comes just before an event).
- AI parallel of operant conditioning: reinforcement learning (rat → agent, lever press → action, food → reward, habit → policy).

### Question 3 — Defining Behaviourist AI

Model answer: Behaviourist AI is an approach to designing intelligent systems in which intelligent behaviour emerges from the interaction between sensors, control mechanisms and the environment, rather than from reasoning about a detailed internal model of the world. It follows behaviourism because it explains behaviour through observable interaction with the environment: a sensor reading (stimulus) leads directly to an action (response), with no hidden inner states. It differs because behaviourism is part of psychology and aims to explain how animals and people learn, whereas Behaviourist AI is part of AI and robotics and aims to build machines that behave usefully.

Key points (3 marks):
- Definition: behaviour emerges from sensors, control and the environment, not from an internal world model ("the world is its own best model").
- Link: both rely on observable stimulus–response interaction with the environment and avoid hidden inner states.
- One difference: different field and aim (explaining learning in living things vs building useful machines). Also acceptable: learning is central to behaviourism but optional in Behaviourist AI, and many such robots never learn.

### Question 4 — Stimulus, response and environment

Either device is acceptable:

| | Smart thermostat | Robotic lawnmower |
|---|---|---|
| **(a)** primary stimulus | the room temperature falling below the set point (for example, below 19 °C), detected by its temperature sensor | bumping into an obstacle (bump sensor), or detecting the boundary wire at the edge of the lawn |
| **(b)** associated response | it switches the heating on, and off again once the set temperature is reached | it stops, reverses and turns to a new direction, then drives straight on |
| **(c)** operating environment | the home: the air in the rooms, the heating system, open windows and the weather outside | the garden: the grass, the boundary wire, obstacles such as trees, flower beds and toys, slopes and the weather |

Neither device stores a map. Each one reacts directly to its current sensor reading.

### Question 5 — Subsumption architecture

Model answer: Brooks' subsumption architecture builds a robot from **layers** of simple behaviours, for example basic movement (always drive forward), seek target (dock signal detected → steer to the dock) and avoid obstacles (object closer than 30 cm → turn away). Each layer links its sensors directly to the motors on its own, and there is no central map or planner. The layers have priorities. When a higher layer's trigger fires, it **suppresses** the layers below, and its command replaces theirs; when it goes quiet, they carry on.

This is more responsive than map-building AI because each layer reacts to its current sensor readings in milliseconds, with no map to rebuild and no plan to recalculate. A change in the world, such as a moved chair or a passing cat, is dealt with at once. A map-building robot has to wait for sense → model → plan → act, like Shakey standing still while it planned. Also, if one layer fails, the others keep working.

Key points (4 marks):
- Behaviours are organised as layers of simple modules, each linking sensors directly to actuators (with an example of the layers).
- A higher-priority layer suppresses (takes over from) the layers below when its trigger fires; they resume when it goes quiet.
- There is no central map or planner: the robot senses the world itself.
- It is more responsive because it reacts in milliseconds to current sensor data, with no map or plan to update; it is also robust if one layer fails.

### Question 6 — Reactive control vs learned behaviour

Model answer: in **reactive control**, a designer writes fixed stimulus–response rules before the robot starts work. The same stimulus always produces the same response, and experience changes nothing. It is fast and predictable, but it cannot improve and fails in situations nobody foresaw. With **learned behaviour**, the robot discovers from feedback (rewards and penalties) which actions work best. Its response to a stimulus can change with experience, so its performance improves over time, although learning takes time and data.

Key points (4 marks):
- Reactive: fixed rules written by a designer, the same response every time, no change with experience (like an inborn reflex).
- Reactive example: a robot vacuum that always turns 45° to the right when bumped. A thermostat, automatic headlights or an automatic door are also acceptable.
- Learned: the response changes with experience through feedback, and performance improves (like operant conditioning; in AI, reinforcement learning).
- Learned example: a robot vacuum that earns +1 for each new patch cleaned and −1 for each bump, and learns to turn left to escape a corner. A delivery robot that learns to avoid a crowded corridor is also acceptable.

### Question 7 — Reward, return and value

**(a)** [1 mark] **−1.** The first move is an ordinary move, not the final move into the charger.

**(b)** [1 mark] The four moves earn −1, −1, −1 and +10, so:
Return = 3 × (−1) + 10 = −3 + 10 = **+7**

**(c)** [2 marks] The value of a square is the return the rover expects from that square to the end of the episode, not the reward for one move. From the start, that total is +7 (see b), because the +10 for reaching the charger outweighs the three −1 costs (−3 in total). So the value of the start square is positive even though the first reward is negative.

Key points:
- Value is the expected return (the total of all future rewards), not the next reward. (1 mark)
- The +10 at the end outweighs the −3 of small penalties, giving +7. (1 mark)

### Question 8 — MDP roles; exploration and exploitation

**(a)** [3 marks]
- **Agent:** the learner and decision-maker. It observes the current state, chooses an action and learns from the rewards it receives.
- **Environment:** everything outside the agent, described by the MDP. After each action it decides what happens next: the new state (through the transition probabilities P) and the reward (through R).
- **Policy (π):** the agent's rule for which action to take in each state. The aim is the optimal policy, π*, which collects the most reward in the long run.

**(b)** [4 marks] Model answer: **exploration** means trying unfamiliar or apparently worse actions to gather information and improve the agent's estimates. **Exploitation** means choosing the action with the best current estimate (the highest Q-value), to collect as much reward as possible now. A balance is needed because early estimates are based on little experience and may be wrong. An agent that only exploits sticks with the first action that worked and may never find a better one. In the grid world, it would keep repeating a nine-move route worth +2 and never find the five-move route worth +6. An agent that only explores never uses what it has learned, so its rewards stay low. A method such as ε-greedy, with ε reduced over time, balances the two.

Key points:
- Exploration defined: trying new actions to gather information. (1 mark)
- Exploitation defined: choosing the best-known action to collect reward now. (1 mark)
- Only exploiting can lock in a worse action, because early estimates may be wrong. (1 mark)
- Only exploring wastes what has been learned, so rewards stay low; a balance such as ε-greedy is needed. (1 mark)

### Question 9 — Epsilon-greedy choice

**(a)** [2 marks]
- **When it exploits** (probability 1 − ε = 0.9), it chooses **right**, the action with the highest Q-value (7).
- **When it explores** (probability ε = 0.1), it ignores the Q-values and picks left, right or stay completely at random, each equally likely. Over 100 decisions you would expect right about 90 + 10 ÷ 3 ≈ 93 times, and left and stay about 3 times each.

**(b)** [2 marks] The Q-values are only estimates based on the experience so far, and they are updated after every step. Exploring gives new rewards for left and stay. Suppose left's estimate of 4 came from a few unlucky tries and it really earns more. Its Q-value can then rise above 7, and left becomes the preferred action. In the same way, right's value could fall if it starts receiving penalties, or if the environment changes.

Key points:
- Q-values are estimates that change with every update. (1 mark)
- Exploration or further experience can show that another action is better, so its Q-value overtakes right's. (1 mark)

### Question 10 — Discounting, penalties and a Q-update

**(a)** [2 marks] γ sets how much future rewards count compared with immediate ones. In the target r + γ max Q(s′, a′), it scales the value of the next state. This lets the agent value actions whose pay-off comes later, while rewards that come sooner count for more, so it prefers to reach a goal sooner. If **γ = 0**, the target is just r. The agent becomes completely short-sighted: it judges each action only by its immediate reward and ignores all future consequences, so it would never accept a −1 step towards a +10 goal.

Key points:
- γ weights future rewards against immediate ones. (1 mark)
- With γ = 0 the target is r, so only the immediate reward counts (short-sighted). (1 mark)

**(b)** [2 marks] Each time an action leads to a penalty, the target is lower than the current Q-value. The error is negative, so the update lowers that Q-value. Over many iterations the value moves step by step towards the penalty. In the chapter's example, Q(C2, right) goes from 0 to −5, −7.5 and then −8.75, approaching −10 with α = 0.5. Because the agent picks the highest Q-values, an action whose value has fallen is chosen less and less. Through the max Q(s′, a′) term, a penalty also lowers the values of earlier states and actions that lead towards it.

Key points:
- A penalty gives a negative error, so the Q-value falls a fraction α each time, towards the penalty value. (1 mark)
- The action is then chosen less often, until the agent avoids it. (1 mark)

**(c)** [3 marks, one for each step]
1. Target = r + γ × max Q(s′, a′) = 2 + 0.9 × 8 = 2 + 7.2 = 9.2
2. Error = target − Q(s, a) = 9.2 − 5 = 4.2
3. New Q(s, a) = Q(s, a) + α × error = 5 + 0.5 × 4.2 = 5 + 2.1 = **7.1**

### Question 11 — A cleaning robot as an MDP

**(a)** [5 marks, one for each ingredient with its meaning and an example]

| Ingredient | Meaning | Example for the cleaning robot |
|---|---|---|
| S: states | every situation the robot can be in | which room it is in (kitchen, hall, bedroom, bathroom), with its battery level and which rooms are already clean |
| A: actions | every choice it can make | move to a neighbouring room, clean the current room, or return to its charging dock |
| P: transition probabilities | the chance that action a in state s leads to state s′ | "move from the kitchen to the hall" succeeds with probability 0.9. With probability 0.1 the robot stays in the kitchen because a door is shut or a pet is in the way |
| R: reward function | the number earned for taking action a in state s | +10 for cleaning a dirty room, −1 per move (time and energy), −20 for running out of battery away from the dock |
| γ: discount factor | how much future rewards count, from 0 to 1 | γ = 0.9, so the robot prefers to finish the cleaning sooner rather than later |

**(b)** [2 marks] Knowing only the room is not enough to predict what happens next. Two robots can both be in the kitchen. One has a full battery and the kitchen is still dirty, so it will clean the kitchen and carry on. The other has 5% battery and has already cleaned the kitchen, so it must head back to its dock. With a room-only state the two situations look identical, yet their futures are different. To predict the next step you would need the history (how long it has been working, which rooms it has already cleaned), so the Markov property does not hold. Adding the battery level and which rooms are clean to the state fixes this.

Key points:
- The Markov property means the future depends only on the current state and action, not on the history. (1 mark)
- An example of two identical room-only states with different futures, such as different battery levels or rooms already cleaned. (1 mark)

### Question 12 — Expected immediate reward

**(a)** [2 marks]
- X: 0.5 × 6 + 0.5 × 2 = 3 + 1 = **4**
- Y: 0.4 × 12 + 0.6 × (−3) = 4.8 − 1.8 = **3**

X has the higher expected immediate reward (4 against 3).

**(b)** [2 marks] Y has the lower expected immediate reward, but it could still be the better choice, because a good agent maximises the expected total reward (the return), not just the next reward. Y's outcomes might lead to states with a higher future value. For example, suppose both of X's outcomes lead to a state where the best that can follow is −5 (a ditch that needs a rescue), while both of Y's outcomes lead to a state from which +6 follows. With no discounting, X's expected total is 4 + (−5) = −1 and Y's is 3 + 6 = **9**, so Y is better. The chapter's example works the same way: the icy ramp has an expected immediate reward of 7 but a total of 3, while the dry corridor has −1 and 9.

Key points:
- The best action depends on future rewards (value or return), not only on the immediate reward. (1 mark)
- Y's outcomes may lead to more valuable states (or X's to worse ones), so Y's expected total can be higher. (1 mark)

### Question 13 — Moving to a new warehouse

Model answer: the learned policy will probably not work well. At best it works only as far as the new warehouse resembles the old one. Its Q-values were learned for the old warehouse's states, and a Q-table for the old layout says nothing about the new one, so routes that used to be good may now lead into shelves or dead ends. In MDP terms, the states (S) have changed, and possibly P and R as well. Simple reactive skills, such as stopping when the bumper is pressed, still work.

To adapt, the robot needs more training. Ideally this builds on what it already knows rather than starting from scratch, and it often happens first in a simulation of the new layout, where mistakes are cheap. After it has been evaluated and deployed, online learning lets it keep updating its Q-values on the job, with a small ε, strict safety rules and monitoring. If the reward assumptions no longer fit (because of new hazards, for example), designers should change the reward function.

Key points (4 marks):
- The policy will not fully transfer, because it was learned for the old states and layout (S changed; maybe P and R too).
- It works only where the new place resembles the old one; reactive safety rules still work.
- Retrain the robot, ideally starting from its existing knowledge and in a simulation of the new layout first.
- Use online learning on the job (small ε, safety rules, monitoring), and update the reward function if needed.

### Question 14 — Three related ideas

Model answer:
- **Behaviour-based robotics** is an approach to robot **control and architecture**. It answers the question "how should a robot's behaviours be organised and linked to sensors and motors?", for example as layered reactive rules in a subsumption architecture.
- **Reinforcement learning** is a **learning framework**. It answers "how can an agent learn from rewards which actions to take?", using trial and error to improve a policy.
- A **neural network** is a **computational model** of a function. It answers "how can a computer represent a complex link from inputs to outputs?", such as from camera pixels to Q-values.

**A system that combines them:** a walking robot that uses deep reinforcement learning plus a safety stop uses all three. A neural network takes the robot's sensor readings and outputs its policy or Q-values. The network is trained by reinforcement learning, with rewards for walking forward without falling. A reactive safety-stop rule (behaviour-based robotics) overrides the learner if the robot is about to fall or hit something.

Also acceptable: DeepMind's DQN agent learning Atari games (reinforcement learning plus a neural network), the warehouse robot in Pause & Try 2.24, or a learning robot vacuum that keeps a reactive "stop if the bumper is pressed" rule (behaviour-based robotics plus reinforcement learning).

Key points (4 marks): one for each of the three explanations, and one for a system that combines at least two of them, with each part named.
