# Chapter 5 — Applications

**Learning outcome:** Trace an integrated smart-system workflow; explain real-time deadlines and edge/cloud choices; connect policies to actuators; evaluate automation, human-AI interaction, ethical concerns and connected applications.

**Prerequisites:** Read the relevant earlier chapters; this chapter connects those ideas to applications.

## A system that senses and acts

### Combine the parts

An integrated smart system connects physical hardware, communication and software to carry out a useful task. Sensors collect information; processing interprets it and selects an output; actuators change the world. A network lets components exchange data or use remote services. Some systems use fixed rules, some use learned models, and some combine both.

### Follow one complete workflow

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Sense |
| 2 | Communicate |
| 3 | Decide |
| 4 | Act |

The changed environment supplies the next observation. The communication step may be local, remote or partly unnecessary for a self-contained controller.

### Use the body analogy carefully

Sensors resemble senses, actuators resemble muscles and communication links resemble nerves. Software coordinates the response. This is an analogy for the roles, not a claim that the machine has a human mind. Explain the actual mechanism: what is measured, what message is sent, what computation runs and what physical output follows.

### Apply and check

**Try before reading feedback:** The rover’s sensor is correct but its motor cable is disconnected. Has a successful software decision completed the workflow?

**Feedback:** No. Physical actuation and feedback are required; logging a command is not proof that the environment changed.

**Practice connection:** Exercise 5.1 in exercises.md; explained answer in solutions.md.

## Example: an irrigation system

### Trace the flow of information

| Stage | Illustrative design |
| --- | --- |
| Measure | Soil-moisture sensors report readings and timestamps. |
| Communicate | A low-power network sends readings to a local gateway. |
| Decide | A controller selects a watering action using targets and constraints. |
| Act | A driver energises a valve; later readings show the effect. |

### Add learning only when it has a role

A fixed threshold can open a valve when soil is dry. A learned policy might instead use moisture, recent rain and other state variables to trade off water use and crop needs. Reinforcement learning would require a defined reward and a process for updating the policy from experience. Merely connecting a sensor to Wi-Fi does not make the system learn.

### Check assumptions before action

Sensors can drift; messages can arrive late; a valve can fail. Timestamp readings, detect implausible values and monitor the effect of each action. A real deployment needs domain-specific limits and testing. This example explains an architecture rather than prescribing watering durations for a particular crop.

### Apply and check

**Try before reading feedback:** A moisture sensor sticks at “dry.” What failure could a simple watering rule create?

**Feedback:** It could keep the valve open. Time/volume limits, plausibility checks and fault handling can contain the failure.

**Practice connection:** Exercise 5.3b in exercises.md; explained answer in solutions.md.

## Real-time means meeting a deadline

### Correctness includes timing

A real-time system must produce the required response within a specified deadline. “Real-time” does not simply mean very fast. Missing a hard deadline can make a system fail its requirements; missing a soft deadline reduces service quality. Batch work, such as a monthly report, usually has different timing needs.

### Illustrative delay distance at 30 m/s

| Delay before response | Distance travelled |
| --- | --- |
| 500 ms = 0.500 s | 30 × 0.500 = 15 metres |
| 50 ms = 0.050 s | 30 × 0.050 = 1.5 metres |
| 5 ms = 0.005 s | 30 × 0.005 = 0.15 metres |

### Interpret the calculation correctly

Distance during delay = speed × delay. This is only the distance travelled before a response begins, not total stopping distance. Sensing, processing, communication, actuation and physical braking all contribute to a real system. Moving a critical computation locally removes some communication delay, but it does not guarantee a particular safe outcome.

### Apply and check

**Try before reading feedback:** A deadline is 100 ms. One response takes 120 ms, while the average is 40 ms. Was that response on time?

**Feedback:** No. Average speed does not excuse a missed specified deadline. The consequence depends on the task’s real-time requirements.

**Practice connection:** Exercise 5.2a in exercises.md; explained answer in solutions.md.

## Networking for a behaviour-based agent

### Separate the fast loop from shared services

A useful architecture keeps time-critical sensing, policy evaluation and actuator control near the device. A network can carry telemetry, coordinate multiple devices or distribute reviewed model updates. Training may occur centrally while a fixed policy runs locally. A system can continue its local task during a link outage only if it was designed to do so.

### Two connected responsibilities

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Device: observe / act |
| 2 | Network: data + updates |
| 3 | Server: analyse / train |

Local action does not have to wait for every cloud exchange. This is an architectural choice, not a property of all AI systems.

### Make messages interpretable

Include a device identity, timestamp, sequence number, units and model or policy version where needed. Reject stale or unauthorised commands. Delayed feedback must be associated with the action that produced it before a learning update is made. Network loss can reduce the evidence available for training; it should not silently become a reward of zero.

### Apply and check

**Try before reading feedback:** Pip receives sequence 43 after 600 ms; the allowed age is 200 ms. Should it execute the command just because the ID is correct?

**Feedback:** No. Reject the stale command and use the defined safe local behaviour. Correct identity alone does not satisfy freshness.

**Practice connection:** Exercise 6.5 in exercises.md; explained answer in solutions.md.

## Automation changes work and errors

### A spectrum of responsibility

| Mode | Who does what? |
| --- | --- |
| Manual | A human performs the task directly. |
| Assistance | The system supports selected actions or provides alerts. |
| Partial automation | The system handles parts of the task; the human supervises. |
| Higher autonomy | The system acts within a defined operating domain. |

### Benefits depend on the setting

Automation can improve repeatability, throughput and availability for suitable work. It can also shift errors from isolated human mistakes to systematic software, sensor or model failures affecting many operations. Do not assume that automation gives zero errors, unlimited uptime or a fixed percentage improvement.

### Keep the operating domain explicit

A warehouse robot may work well on a mapped, maintained floor but fail on an unfamiliar surface. A human must understand what the system can handle, what it cannot handle and how a handover works. Formal driving-automation levels describe a specific domain; they should not be treated as a universal ladder for every smart appliance.

### Apply and check

**Try before reading feedback:** What is the danger of automating an incorrect calibration rule across 500 devices?

**Feedback:** The same systematic error can be reproduced quickly at scale. Automation changes error patterns rather than eliminating them.

**Practice connection:** Exercise 5.2b in exercises.md; explained answer in solutions.md.

## Feedback can change a policy

### Describe the learning mechanism

An RL agent collects transitions: a state, an action, a reward and a next state. A learning algorithm uses those transitions to update values or policy parameters. A positive reward does not mechanically guarantee that an action becomes more likely in every algorithm; updates depend on the method and its estimates of future return.

### Design an illustrative delivery task

| Element | Possible definition |
| --- | --- |
| State | Location, remaining energy and relevant obstacle information. |
| Action | Choose a permitted move. |
| Reward | Score progress and successful completion; penalise undesirable outcomes. |
| Constraint | Disallow unsafe actions even if a reward would favour them. |

### A deployment may stop learning

A trained policy can be evaluated repeatedly on new observations without changing its parameters. Online learning requires a controlled update process and evidence that changes improve performance. Separate “the action changed because the observation changed” from “the policy changed because the agent learned”.

### Apply and check

**Try before reading feedback:** A reward arrives late. What association must be retained before using it to update learning?

**Feedback:** Associate it with the relevant episode, state/action or transition. Applying it to the latest unrelated action can corrupt learning.

**Practice connection:** Exercise 5.3a in exercises.md; explained answer in solutions.md.

## Turn a decision into an action

### A command needs an execution path

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Policy output |
| 2 | Controller |
| 3 | Power driver |
| 4 | Actuator |

Feedback from position, current or other sensors can confirm whether the requested action happened.

### Different physical outputs

| Actuator | Example role |
| --- | --- |
| Electric motor / servo | Rotate a wheel or position a joint. |
| Solenoid valve | Open or close a fluid path. |
| Hydraulic actuator | Produce force using pressurised liquid. |
| Pneumatic actuator | Produce movement using compressed air. |

### Distinguish information from energy

A software value such as “target angle = 15 degrees” is information. Interface electronics convert it into a suitable control signal; a powered mechanism supplies the force. Some systems use analogue voltages, others PWM or digital commands. A DAC alone normally cannot supply motor power. Mechanical limits, response time and feedback all affect whether an intended action is achieved.

### Apply and check

**Try before reading feedback:** Why should software read motor or position feedback after a move command?

**Feedback:** The motor may stall, saturate or fail. Feedback helps determine whether the intended physical outcome occurred.

**Practice connection:** Exercise 5.3b in exercises.md; explained answer in solutions.md.

## Help people understand the system

### Human-AI interaction is part of HCI

Human-computer interaction studies how people use computing systems. Human-AI interaction focuses on challenges raised by AI, including uncertainty, adaptation, delegation and trust. It is not a strict division between deterministic old interfaces and always-probabilistic new ones. The important question is what the person needs to understand and control.

### Useful interface information

| Show | Why it helps |
| --- | --- |
| Current mode and operating limits | The user knows what the system is doing. |
| Relevant evidence and uncertainty | The user can judge an output appropriately. |
| Planned action and reason | The next behaviour is less surprising. |
| Override, handover and recovery | The user can respond when the system cannot continue. |

### Avoid over-trust and under-trust

Unclear automation can cause misuse through excessive reliance, or disuse when useful assistance is rejected. A handover should communicate the state of the task and why control is changing. A confident-looking score is not enough: the interface should support an informed decision and an appropriate human response.

### Apply and check

**Try before reading feedback:** A display says “AI approved” without uncertainty or override. Name a design improvement.

**Feedback:** State the relevant decision and its limits, show useful status, and provide an effective human override/recovery path appropriate to the risk.

**Practice connection:** Exercise 5.4b in exercises.md; explained answer in solutions.md.

## Evaluate more than performance

### Three important ethical concerns

| Concern | Design question |
| --- | --- |
| Fairness | Who benefits, who is disadvantaged, and how was this measured? |
| Transparency | Can affected people understand the system’s role and limitations? |
| Accountability | Who is responsible for deployment, oversight and correction? |

### Reward design can encode priorities

A reward that values only throughput can encourage neglect of other goals. Historical data can contain unequal representation or biased decisions. Evaluate outcomes across relevant groups and situations rather than assuming an algorithm is neutral because it uses numbers. The appropriate criteria depend on the task and the people affected.

### Make responsibility practical

Document the intended use, data sources, limitations and monitoring process. Provide channels to question or correct consequential outcomes. Ethical and legal requirements vary by context and jurisdiction; no single checklist proves a system is responsible. For high-stakes uses, performance testing and meaningful human oversight are essential parts of the deployment decision.

### Apply and check

**Try before reading feedback:** A routing model works worse for buildings with poor sensor coverage. What should the team investigate?

**Feedback:** Measure performance and impacts by relevant operating conditions, examine data coverage and accessibility, and adjust with accountable review.

**Practice connection:** Exercise 5.5a in exercises.md; explained answer in solutions.md.

## Opportunities bring responsibilities

### Illustrative connected applications

| Application | Opportunity | Risk to consider |
| --- | --- | --- |
| Traffic signals | Respond to changing demand. | Unsafe control or unequal service. |
| Water monitoring | Detect leaks and reduce waste. | Faulty sensors or unauthorised commands. |
| Street lighting | Adjust lighting to local need. | Privacy, coverage and maintenance. |
| Connected health monitoring | Support timely review of measurements. | Sensitive data and incorrect alerts. |

### Measure outcomes, not just activity

More sensor readings or more automated actions do not necessarily mean better service. Compare meaningful outcomes such as resource use, reliability, accessibility and user experience. Any claimed improvement needs evidence from the particular deployment; percentages from an unspecified example are not general guarantees.

### Every connected device adds responsibilities

Connected cameras, locks, sensors and controllers need updates, access management and appropriate data protection. Minimise unnecessary personal data, limit retention and protect communication. Consider what happens if a device is compromised or the network is unavailable. Convenience should be assessed alongside maintainability, privacy and safe operation.

### Apply and check

**Try before reading feedback:** Should a campus rover upload every camera frame merely because bandwidth is available?

**Feedback:** No. Determine a legitimate purpose, minimise data, consider privacy and retention, and use local processing where appropriate.

**Practice connection:** Exercise 5.5b in exercises.md; explained answer in solutions.md.

## Chapter review

Complete ACT-05 using the supplied mission instructions. Then choose two related terms and explain a mechanism using both; identify one limitation of the teaching model and one condition that could change the result.

## Reference support

- R1: Reinforcement Learning: An Introduction, second edition — Chapter 3 (finite Markov decision processes) and Section 6.5 (Q-learning). http://incompleteideas.net/book/the-book-2nd.html
- R4: RFC 8446 — The Transport Layer Security (TLS) Protocol Version 1.3 — Section 1 (Introduction) and Section 8 (0-RTT and anti-replay). https://www.rfc-editor.org/rfc/rfc8446
- R5: Artificial Intelligence Risk Management Framework (AI RMF 1.0) — Framework functions Govern, Map, Measure and Manage; trustworthy AI characteristics. https://www.nist.gov/itl/ai-risk-management-framework

Full resource introductions, optional tasks and access alternatives are in ../references.md.
