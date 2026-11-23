# Chapter 5 — Applications

## Explained answers

These are expected answers, not the only acceptable wording. Credit a correct alternative with clear assumptions and reasoning. Try the exercises before reading this section.

### Answer 5.1

A smart system connects sensing, computation, communication and action to a goal. For irrigation, a moisture sensor supplies readings, software compares them with the policy, a network reports status and a valve changes water flow. It need not use machine learning simply because it is connected.

### Answer 5.2a

Real-time processing means meeting a defined timing deadline, not merely being fast on average. Communication, queueing, computation and actuator delays all contribute. At 30 m/s, an extra 0.2 s delay means 6 m travelled before a response; this is delay distance, not total braking distance.

### Answer 5.2b

Automation reduces direct manual operation of a task. It can improve consistency and throughput, but can also repeat a wrong rule at scale, fail on unusual inputs or change workers’ monitoring responsibilities. Assess the actual process rather than assuming all errors disappear.

### Answer 5.3a

An RL algorithm uses transitions and rewards to update policy parameters or value estimates, aiming at expected cumulative reward. A deployed agent may use a fixed learned policy without updating it on every action. Correctly associate feedback with the state and action that produced it.

### Answer 5.3b

An actuator turns an electrical control signal into physical action: a motor moves a wheel, a valve changes flow, or a heater produces heat. The controller must respect limits and use feedback where needed; a software command is not proof the requested movement occurred.

### Answer 5.4a

Human-AI interaction concerns how people work with AI-driven systems. Uncertainty, opaque decisions, changing performance and delegated actions add challenges to general interface design. Interfaces should communicate limits, support correction and provide meaningful human control.

### Answer 5.4b

A user may over-trust an unexplained “safe” decision and ignore a hazard, or be unable to recover when an autonomous action is wrong. Display relevant status and uncertainty, explain the available action and offer an effective override or recovery process.

### Answer 5.5a

Ethical AI considers consequences for people as well as performance: fairness across groups, explanations appropriate to users, privacy and accountable responsibility. Trade-offs must be evaluated in context, with monitoring and redress. A fairness score alone is not a complete ethical judgement.

### Answer 5.5b

Opportunity: remote monitoring can find faults and reduce wasted energy. Risk: compromised devices can expose personal data or accept dangerous commands. Minimise collected data, authenticate access and maintain update and incident-response processes.
