# Chapter 2 — Behaviorism & Behaviorist AI

## Explained answers

These are expected answers, not the only acceptable wording. Credit a correct alternative with clear assumptions and reasoning. Try the exercises before reading this section.

### Answer 2.1

Classical conditioning associates a cue with another stimulus so the cue can elicit a response. Operant conditioning changes the likelihood of an action through its consequences. A bell paired with food and a voluntary action followed by a reward illustrate the difference. They are analogies, not proof that numerical RL reproduces animal experience.

### Answer 2.2

A thermostat is a fixed reflex example: environment = room; stimulus = measured temperature below the set point; response = switch heating on. With unchanged thresholds it reacts but does not learn a policy from rewards.

### Answer 2.3

Subsumption coordinates behaviour modules with defined priority, inhibition or suppression relationships. Obstacle avoidance may suppress a wandering command. Useful behaviour can emerge without a single detailed central map, although practical robots can combine reactive modules with mapping and planning.

### Answer 2.4a

The agent chooses an action using its policy; the environment produces the next state and reward according to the task’s dynamics. An MDP specifies states, actions, transition probabilities, rewards and discounting. A policy maps states to actions or action probabilities; it is not the reward function.

### Answer 2.4b

Exploration obtains information about insufficiently tested actions. Exploitation chooses an action using the best current value estimate, which may include future rewards. Always exploiting can lock in an inferior early estimate; always exploring can waste known good actions. Physical exploration needs safety constraints.
