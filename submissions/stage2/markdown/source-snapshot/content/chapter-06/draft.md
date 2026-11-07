# Chapter 6 — Strengths & Limitations

**Learning outcome:** Evaluate physical and network constraints; distinguish scalability, interoperability and resilience; compare predictive analytics with behavioural modelling; assess resource allocation, explainability, bias and responsible deployment.

**Prerequisites:** Read the relevant earlier chapters; this chapter connects those ideas to strengths & limitations.

## Judge the whole system

### Strengths and limitations interact

| Part | Strength | Limitation |
| --- | --- | --- |
| Hardware | Senses, computes and acts locally. | Power, heat, memory and physical reliability. |
| Networks | Share resources and coordinate devices. | Delay, loss, availability and security. |
| AI / control software | Selects actions and may learn from experience. | Model errors, limited evidence and unclear objectives. |

### There is no universally best architecture

Choose a design for its task, operating conditions and consequences of failure. A model with excellent offline accuracy may be unsuitable if it misses a deadline or requires too much memory. A highly connected system may be fragile if local operation depends on one remote service. A simple fixed-rule controller can be appropriate for a well-defined task.

### Make the comparison explicit

State the intended outcome, identify constraints, compare options and define measures for success. Evaluate the combination of hardware, networking, algorithms and human operation. A component’s specification is useful evidence, but it is not proof that the complete application meets its requirements.

### Apply and check

**Try before reading feedback:** A model gains accuracy but misses the motor-control deadline. Is it automatically the better system?

**Feedback:** No. Evaluate the whole objective, including timing, safety, energy and accuracy in the operating domain.

**Practice connection:** Exercise 6.5 in exercises.md; explained answer in solutions.md.

## Four physical budgets

### Every device has limits

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Power |
| 2 | Heat |
| 3 | Memory |
| 4 | Processing |

A design must fit all four budgets, not just the model’s arithmetic requirement.

### Understand the constraint

| Budget | What can go wrong |
| --- | --- |
| Power | A battery drains too quickly for the required mission. |
| Heat | Thermal throttling reduces sustained performance. |
| Memory | Weights, inputs or intermediate results do not fit. |
| Processing | An inference or control computation misses its deadline. |

### Optimise with evidence

A smaller model, quantised representation, reduced input resolution or lower update rate can reduce cost, but may change accuracy or responsiveness. Measure the resulting behaviour. Dedicated accelerators can improve efficiency on supported workloads, but data conversion, memory movement and idle power remain relevant. Local computing removes a remote round trip; it does not mean zero total latency.

### Apply and check

**Try before reading feedback:** Pip meets its deadline when cold but throttles after ten minutes. Which budget was overlooked?

**Feedback:** Thermal behaviour and sustained power. Test warm steady-state operation, not only short benchmark bursts.

**Practice connection:** Exercise 6.1 in exercises.md; explained answer in solutions.md.

## Reliable decisions need reliable inputs

### Sensors are imperfect

Noise creates random variation; drift changes a sensor’s behaviour over time. Obstruction, calibration error or environmental conditions can produce misleading observations. Sensor fusion combines information from multiple sources, often after time alignment and filtering. Different sensors can have complementary strengths, but they can also share common failure causes.

### A fusion pipeline

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Camera / range / motion |
| 2 | Align + check |
| 3 | Combine evidence |
| 4 | State estimate |

Do not combine incompatible units or measurements from different times as if they described the same instant.

### Define reliability under conditions

Reliability concerns performing an intended function for a stated period under stated conditions. MTBF is a statistical measure for repairable systems, not a promise that a particular unit cannot fail earlier. Monitor drift, error rates, temperature and data quality. Redundancy can help when failures are sufficiently independent and the system can recognise and manage disagreement.

### Apply and check

**Try before reading feedback:** Two sensors disagree after months of use. Why should the controller consider drift?

**Feedback:** Calibration can change gradually. Compare reference measurements, inspect conditions and use a justified fault or recalibration process.

**Practice connection:** Exercise 6.1 in exercises.md; explained answer in solutions.md.

## Grow without losing coordination

### Three network qualities

| Quality | Meaning |
| --- | --- |
| Scalability | Handle more devices or work at acceptable performance. |
| Interoperability | Exchange data and use it correctly across different systems. |
| Resilience | Maintain or recover an acceptable service during disruption. |

### Capacity is only one part of scaling

Adding hundreds of IoT devices can increase addressing, authentication, message traffic, storage and maintenance work. Agree on data formats, units, timestamps and interface versions as well as the physical link. Two products using Wi-Fi do not automatically interpret one another’s messages correctly.

### Plan for failures

Redundant links, retry policies, local buffering and controlled reconnection can improve resilience. A mesh can route around some failures when an alternative path exists and the protocols support it. It does not guarantee communication through every outage. Test overload and partial failure, not just the normal case with every device online.

### Apply and check

**Try before reading feedback:** A receiver reads 250 centimetres as 250 metres. Is adding network capacity the main fix?

**Feedback:** No. It is a semantic interoperability failure. Specify and check units and schema/version information.

**Practice connection:** Exercise 6.2 in exercises.md; explained answer in solutions.md.

## Put each computation where it fits

### Three deployment patterns

| Location | Benefit | Cost or limit |
| --- | --- | --- |
| On-device edge | Low communication delay; local data. | Limited local resources and maintenance. |
| Nearby gateway / fog | Aggregates local devices. | Another service to size and manage. |
| Remote cloud | Shared compute and flexible capacity. | Network dependency, latency and transfer cost. |

### An illustrative warehouse design

Each robot handles immediate motion control locally. A shared service allocates tasks and coordinates inventory. Robots send selected telemetry and receive authorised updates. If the coordination service is unavailable, the design defines whether a robot pauses, completes a limited task or enters another safe state; continued operation must not be assumed.

### Optimise across the whole path

Compare local compute energy with transmission energy, available bandwidth, deadlines, privacy and model capacity. Summarising data locally can reduce transfer volume. Centralised analysis can reveal patterns across devices. The useful decision is which part of the workload belongs where, not whether edge or cloud is always superior.

### Apply and check

**Try before reading feedback:** Choose a location for emergency stopping and a location for weekly fleet analytics, and justify each.

**Feedback:** Local control avoids remote round-trip dependence for stopping; cloud or central processing can aggregate fleet history for slower analytics. Both need security and resource planning.

**Practice connection:** Exercise 6.5 in exercises.md; explained answer in solutions.md.

## Predict an outcome or model behaviour?

### Two useful questions

| Predictive analytics | Behavioural modelling |
| --- | --- |
| What is likely to happen? | How does an agent or system behave? |
| Forecasts, scores or probability estimates. | Rules, transitions, trajectories or action patterns. |
| Example: estimate a component’s failure risk. | Example: model a robot’s response to an obstacle. |

### The approaches can overlap

A behavioural model can be used to make predictions, and predictive features can inform an action policy. They are not mutually exclusive categories defined by one kind of data. Choose the model and evaluation method based on the question being asked and the evidence available.

### Adaptation is not guaranteed generalisation

Adaptive intelligence describes changing behaviour appropriately using new information or experience. Autonomy describes operating with limited direct human control. An autonomous device may use a fixed policy; an adaptive model may still need supervision. Performance in familiar conditions does not prove reliability in a new environment.

### Apply and check

**Try before reading feedback:** A model predicts a busy corridor at noon. Has it proved why students choose that corridor?

**Feedback:** No. A predictive association can be useful without a causal explanation. Behavioural modelling may represent decisions, but also needs justified assumptions.

**Practice connection:** Exercise 6.4 in exercises.md; explained answer in solutions.md.

## Understand why a policy acted

### Explainability is a practical capability

Explainability concerns making relevant aspects of a model’s behaviour understandable to people. A small rule set or Q table may be inspectable. A deep RL policy can be harder to interpret because many parameters contribute to each output. Complexity does not mean analysis is impossible, but a simple story about one decision may be incomplete or misleading.

### Look beyond one successful outcome

Inspect representative cases, counterexamples, changed conditions and failure logs. Separate a faithful explanation of the computation from a plausible narrative generated after the fact. An explanation does not establish that the action was correct; validation requires evidence about outcomes and requirements.

### Reward errors and bias

An agent rewarded only for speed may neglect an important constraint. Training environments can under-represent some conditions or groups. Distribution shift can reduce performance when deployment differs from training. Track both overall performance and relevant subsets. Correcting a reward or dataset requires re-evaluation of the resulting policy.

### Apply and check

**Try before reading feedback:** A heat map highlights an obstacle. Does it prove the model used exactly the reasoning a human expects?

**Feedback:** No. It is an explanatory aid with limits, not conclusive access to the model’s causal decision process.

**Practice connection:** Exercise 6.6 in exercises.md; explained answer in solutions.md.

## Balance benefit, risk & oversight

### Questions for a deployment review

| Area | Evidence to seek |
| --- | --- |
| Security | Authenticated updates, restricted access and recovery plans. |
| Privacy | Necessary data collection, appropriate retention and access. |
| Fairness | Evaluation across relevant people and conditions. |
| Accountability | Named responsibilities, review and correction routes. |
| Reliability | Measured deadlines, failure handling and monitoring. |

### Physical effects raise the stakes

A connected controller can change the physical world, so a corrupted measurement or unauthorised command may have consequences beyond a damaged file. Protect sensor inputs, model updates and actuator commands according to the task. Test how the system responds to missing, stale and contradictory data.

### Finish with a justified judgement

State the benefit you expect, the evidence supporting it, the conditions under which it applies and the remaining limitations. Decide what a human must monitor or approve and how the system should respond when its assumptions fail. The strongest design is the one suited to its purpose, with limitations that are understood and managed.

### Apply and check

**Try before reading feedback:** Pip succeeds on one sunny test run. Name two further checks before claiming robust deployment.

**Feedback:** Test changed lighting/weather or sensor faults, and evaluate adverse traffic/network conditions with monitored fallback. A single success does not establish reliability across the operating domain.

**Practice connection:** Exercise 6.7 in exercises.md; explained answer in solutions.md.

## Chapter review

Complete ACT-06 using the supplied mission instructions. Then choose two related terms and explain a mechanism using both; identify one limitation of the teaching model and one condition that could change the result.

## Reference support

- R5: Artificial Intelligence Risk Management Framework (AI RMF 1.0) — Framework functions Govern, Map, Measure and Manage; trustworthy AI characteristics. https://www.nist.gov/itl/ai-risk-management-framework

Full resource introductions, optional tasks and access alternatives are in ../references.md.
