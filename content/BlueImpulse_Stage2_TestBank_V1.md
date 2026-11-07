# Blue Impulse — Stage 2 Test Bank V1.0

**Module:** Hardware, Networking and Behaviorist AI  
**Version/date:** V1.0 — 7 November 2026  
**Coverage:** Six chapters; 24 True/False, 24 single-answer Multiple Choice and 6 open-ended tasks.

## Instructions

Attempt the questions before reading the answer key. For True/False, correct any false statement. For multiple choice, select exactly one answer. Open responses require developed reasoning: normally at least 120 words (150 for OE06), or an equivalent labelled diagram, decision matrix, calculations or worked trace with explanations. Every question includes its own required numerical data; no online platform is needed. Suggested self-assessment: 1 mark for each T/F decision plus 1 for reasoning; 1 mark for each MC choice plus 1 for reasoning; 10 marks for each open response. Total 156 marks. This is a practice allocation, not a teacher-issued grading scheme.

## Questions — True/False

### TF01 — Chapter 1: The Fundamentals / Represent negative values

In eight-bit two’s complement, the representable range is −128 to +127.

### TF02 — Chapter 1: The Fundamentals / Numbers, characters & codes

Unicode requires every character to occupy exactly one byte.

### TF03 — Chapter 1: The Fundamentals / The stored-program computer

A 3 GHz clock guarantees exactly three billion completed instructions every second.

### TF04 — Chapter 1: The Fundamentals / Trace a tiny program

In the guide’s toy program, STORE 200 copies ACC into memory address 200 without making 200 the result.

### TF05 — Chapter 2: Behaviorism & Behaviorist AI / React first: behaviour-based robots

A fixed thermostat rule that never changes from experience is, by itself, an example of reinforcement learning.

### TF06 — Chapter 2: Behaviorism & Behaviorist AI / Rewards, policies & values

An RL policy can prefer an action with a small immediate cost when it offers greater expected future return.

### TF07 — Chapter 2: Behaviorism & Behaviorist AI / Update a Q value

For a terminal next state in the guide’s Q-learning update, the future-value term is zero.

### TF08 — Chapter 2: Behaviorism & Behaviorist AI / Training is different from using a policy

Every action chosen by a deployed learned policy necessarily changes its trained parameters.

### TF09 — Chapter 3: Hardware / Memory: capacity versus speed

SRAM and DRAM normally retain their data after all power is removed.

### TF10 — Chapter 3: Hardware / Overlap work with a pipeline

An ideal four-stage pipeline can finish three independent instructions in six cycles while each instruction still traverses four stages.

### TF11 — Chapter 3: Hardware / The hardware behind an AI model

A GPU is guaranteed to beat a CPU on every program because it has many parallel execution units.

### TF12 — Chapter 3: Hardware / Sense, decide, act, sense again

A fan controller can use different switch-on and switch-off thresholds to reduce rapid toggling near one temperature.

### TF13 — Chapter 4: Networking / Capacity is not responsiveness

High network bandwidth alone guarantees low command latency.

### TF14 — Chapter 4: Networking / Sharing a communication medium

Modern switched full-duplex Ethernet links normally avoid the shared-medium collisions that CSMA/CD handles.

### TF15 — Chapter 4: Networking / Trust, signatures & certificates

A digital signature by itself keeps a message confidential.

### TF16 — Chapter 4: Networking / Find a host with DNS

Successful DNS resolution does not guarantee that the web server will return a requested page.

### TF17 — Chapter 5: Applications / Real-time means meeting a deadline

A system meets every 100 ms deadline if its average response time is 40 ms, even when one response takes 120 ms.

### TF18 — Chapter 5: Applications / Networking for a behaviour-based agent

A correctly authenticated message can still be too old to execute safely.

### TF19 — Chapter 5: Applications / Feedback can change a policy

Delayed reward should always be assigned to the most recently received action, regardless of its origin.

### TF20 — Chapter 5: Applications / Turn a decision into an action

A logged motor command does not prove that the requested physical movement occurred.

### TF21 — Chapter 6: Strengths & Limitations / Four physical budgets

A model that fits in storage automatically fits the device’s working-memory, timing, power and thermal budgets.

### TF22 — Chapter 6: Strengths & Limitations / Grow without losing coordination

Agreeing on units and schema versions supports interoperability between different devices.

### TF23 — Chapter 6: Strengths & Limitations / Put each computation where it fits

Moving every computation to the cloud always improves resilience during network loss.

### TF24 — Chapter 6: Strengths & Limitations / Understand why a policy acted

A useful post-hoc explanation is not necessarily a faithful account of the exact causal process that produced a model’s decision.

## Questions — Multiple Choice

### MC01 — Chapter 1: The Fundamentals / From bits to bytes

How many bytes are in 2 KiB?

A. 16,384

B. 2,000

C. 16,000

D. 2,048

### MC02 — Chapter 1: The Fundamentals / Build a digital image

A 500 × 200 bitmap uses 16 colours and no padding. What is its raw pixel-data size, excluding headers and compression?

A. 100,000 bytes

B. 12,500 bytes

C. 25,000 bytes

D. 50,000 bytes

### MC03 — Chapter 1: The Fundamentals / Fetch / decode / execute

Which register identifies the memory location being accessed in the teaching model?

A. CIR

B. ACC

C. MAR

D. MDR

### MC04 — Chapter 1: The Fundamentals / Trace a tiny program

Starting with ACC = 0, run LOAD #3; ADD #9; STORE 200; HALT. What is memory[200]?

A. 12

B. 9

C. 200

D. 3

### MC05 — Chapter 2: Behaviorism & Behaviorist AI / The reinforcement-learning loop

Which description best defines a policy?

A. The numerical score after a transition

B. A strategy for choosing actions from a state or observation

C. A guarantee that every action succeeds

D. The physical environment around the agent

### MC06 — Chapter 2: Behaviorism & Behaviorist AI / Update a Q value

Old Q = 2, alpha = 0.5, reward = 1, gamma = 0.9, best next Q = 4. What is the updated non-terminal Q value?

A. 2.6

B. 1.3

C. 3.3

D. 4.6

### MC07 — Chapter 2: Behaviorism & Behaviorist AI / Explore or exploit?

Pip always chooses the route that looked best in its first two trials. What is the most direct learning concern?

A. It may never gather evidence about a better untried route

B. It must receive a negative reward every time

C. It is guaranteed to explore every route equally

D. It must have a perfect transition model

### MC08 — Chapter 2: Behaviorism & Behaviorist AI / Actions can have uncertain outcomes

An action gives reward +10 with probability 0.8 and −5 with probability 0.2. What is expected immediate reward?

A. 8

B. 5

C. 7

D. 10

### MC09 — Chapter 3: Hardware / Memory: capacity versus speed

Which description correctly distinguishes DRAM from SRAM?

A. DRAM charge needs refresh; powered SRAM bistable cells do not need periodic refresh

B. SRAM is a magnetic disk technology

C. SRAM can only store instructions and not data

D. DRAM is always non-volatile

### MC10 — Chapter 3: Hardware / Overlap work with a pipeline

An ideal four-stage pipeline processes five independent instructions with no stalls. How many cycles elapse from the first fetch through the last write-back?

A. 8

B. 4

C. 20

D. 5

### MC11 — Chapter 3: Hardware / Reason with logic gates

Movement is allowed when battery_ok AND NOT obstacle. What is the output for battery_ok = 1, obstacle = 1?

A. It must alternate

B. 1

C. 0

D. The expression is undefined

### MC12 — Chapter 3: Hardware / The hardware behind an AI model

Which task most naturally exposes SIMD-style parallelism?

A. Following a fully dependent branch chain

B. Executing a single unpredictable pointer dependency

C. Waiting for one keyboard key

D. Applying the same arithmetic operation to many image pixels

### MC13 — Chapter 4: Networking / Capacity is not responsiveness

At 30 m/s, how far is travelled during 50 ms of communication delay alone?

A. 0.15 m

B. 1.5 m

C. 150 m

D. 15 m

### MC14 — Chapter 4: Networking / Give each protocol layer a job

In the four-layer TCP/IP teaching model, where does IP routing belong?

A. Link/network-access

B. Transport

C. Application

D. Internet

### MC15 — Chapter 4: Networking / Protect data and its meaning

Which check primarily establishes that data obeys an allowed format or range?

A. A device driver

B. Validation

C. Lossy compression

D. Encryption

### MC16 — Chapter 4: Networking / Trust, signatures & certificates

Which combination best describes how a digital signature is created and checked?

A. Encrypt every message with a password shown inside it

B. Sign with a private signing key; verify with the matching public key

C. Sign by hashing alone; no key is involved

D. Sign with a public key; hide with the same public key

### MC17 — Chapter 5: Applications / Real-time means meeting a deadline

A local task has a maximum permitted response of 80 ms. Which listed response meets that deadline?

A. 100 ms

B. 60 ms

C. An average of 40 ms with this response at 90 ms

D. 120 ms

### MC18 — Chapter 5: Applications / Networking for a behaviour-based agent

Receiver last accepted sequence is 42; allowed age is 200 ms. A matching, authenticated packet has sequence 43 and age 600 ms. What should the toy receiver do?

A. Accept because the sequence is new

B. Reject stale and keep the accepted sequence at 42

C. Accept because authentication overrides age

D. Reset the accepted sequence to 0

### MC19 — Chapter 5: Applications / Turn a decision into an action

Which component directly changes water flow in an automated irrigation system?

A. Valve actuator

B. Moisture sensor

C. DNS resolver

D. Reward value

### MC20 — Chapter 5: Applications / Feedback can change a policy

What is needed before using a delayed reward in a learning update?

A. Associate it with the relevant transition or episode

B. Discard all earlier records forever

C. Assume it belongs to whichever action arrived last

D. Replace every negative reward with zero

### MC21 — Chapter 6: Strengths & Limitations / Four physical budgets

Pip has 512 MB working memory and a 6 W budget. Which design meets both stated limits?

A. 700 MB and 4 W

B. 700 MB and 9 W

C. 180 MB and 4 W

D. 400 MB and 9 W

### MC22 — Chapter 6: Strengths & Limitations / Grow without losing coordination

A sensor sends 250 centimetres, but a receiver treats the value as 250 metres. Which problem is this?

A. A binary addition carry

B. Insufficient colour depth

C. Semantic interoperability failure

D. A guaranteed encryption failure

### MC23 — Chapter 6: Strengths & Limitations / Put each computation where it fits

Which is the strongest reason to keep an emergency stop loop local?

A. Cloud servers can never learn models

B. Local models are always perfectly accurate

C. Local computation has unlimited energy

D. Avoid dependence on a variable remote round trip for a strict deadline

### MC24 — Chapter 6: Strengths & Limitations / Understand why a policy acted

Which statement best evaluates a model explanation?

A. A colourful heat map proves the model reasons like a human

B. Explanations replace testing on new cases

C. Any explanation proves fairness

D. Its faithfulness, audience and limitations must be assessed

## Questions — Open-ended

### OE01 — Chapter 1: The Fundamentals / Trace a tiny program

Pip’s parcel counter uses the toy instructions 100 LOAD #3; 101 ADD #4; 102 STORE 200; 103 HALT. Start with PC 100, ACC 0 and memory[200] 0. Trace PC, ACC and memory[200] after each instruction; explain immediate values versus addresses; change the ADD operand to #9 and predict the result. Then explain how a source program reaches execution and state two limits of this teaching model. Provide at least 120 words or an equivalently detailed labelled trace plus explanations.

### OE02 — Chapter 2: Behaviorism & Behaviorist AI / Update a Q value

Pip tries a route. Old Q = 2, alpha = 0.5, reward = 1, gamma = 0.9 and best next Q = 4. Calculate target, error, change and updated Q. Repeat if the next state is terminal. Explain reward versus policy versus value, why one successful trip is insufficient, and how exploration can be useful without ignoring safety. Provide at least 120 words or equivalently developed calculations and reasoning.

### OE03 — Chapter 3: Hardware / Overlap work with a pipeline

A fictional CPU has four one-cycle stages F, D, E, W. Schedule three independent instructions in an ideal pipeline and compare the elapsed cycles with no overlap. Explain throughput versus single-instruction latency. Then discuss what changes if I2 needs I1’s result, available only after the end of I1’s W, with no forwarding. Finally explain why GPU, RISC or clock-rate labels alone do not establish the best processor for Pip. Provide a labelled schedule and developed explanation.

### OE04 — Chapter 4: Networking / Capacity is not responsiveness

A warning travels over a 100 Mb/s connection but can arrive after 500, 50, 5 or 200 ms. Use a constant illustrative speed of 30 m/s to calculate distance travelled during each delay. Explain why this is not total stopping distance, how latency differs from bandwidth and jitter, and why switching from UDP to TCP cannot automatically guarantee the safety deadline. Propose two measurements and one design response. Give at least 120 words or equivalent calculations and analysis.

### OE05 — Chapter 5: Applications / Networking for a behaviour-based agent

A receiver expects robot-7, units m, policy_version 3, authenticated input, maximum age 200 ms and sequence greater than last accepted sequence 41. Process A: sequence 42, age 50 ms; B: sequence 43, age 600 ms; C: sequence 42, age 60 ms. All other fields match. Give each decision and receiver state. Explain identity, freshness, replay and unit checks, why stale rejected input must not advance accepted state, and how delayed rewards should be associated with actions. Include at least 120 words or equivalent explicit decision reasoning.

### OE06 — Chapter 6: Strengths & Limitations / Put each computation where it fits

Choose a design for an 80 ms local control task with 512 MB RAM and a 6 W budget. Small local model: 30 ms, 180 MB, 4 W, 92% task accuracy. Large local: 90 ms, 700 MB, 9 W, 96%. Remote: 20 ms compute plus 100–300 ms network round trip, 98%, with image uploads. These are fictional supplied measurements. Evaluate each option, propose a split between local control and fleet analytics, and discuss thermal testing, privacy, fairness and responsibility. Give at least 150 words or an equivalent decision matrix with developed reasoning.

# Answer key — read after attempting all questions

## True/False answers and corrections

### TF01: True

The most significant bit has weight −128; the remaining seven bits can contribute 0 through 127.

### TF02: False

Unicode assigns code points; encodings such as UTF-8 use variable numbers of bytes. A displayed grapheme can also contain more than one code point.

### TF03: False

It specifies clock cycles per second. Instruction mix, stalls, issue width and microarchitecture affect completed work.

### TF04: True

The operand is a destination address; the stored value is the accumulator’s current content.

### TF05: False

It is reactive control. RL requires an experience-based update to value estimates or a policy.

### TF06: True

The objective normally concerns cumulative reward, not only the next reward.

### TF07: True

The episode ends, so no later return is bootstrapped from that terminal state.

### TF08: False

Inference can use fixed parameters. Online learning is a separate design choice.

### TF09: False

Both are normally volatile. SRAM avoids periodic refresh while powered; this does not make it non-volatile.

### TF10: True

The finish cycles are 4, 5 and 6 under the stated equal-stage, no-stall assumptions.

### TF11: False

Parallelism only helps workloads that expose suitable independent work; transfer overhead and dependencies also matter.

### TF12: True

This hysteresis prevents small fluctuations around a single threshold from repeatedly toggling the actuator.

### TF13: False

Propagation, queues, endpoint processing and other factors can create delay even on a high-capacity link.

### TF14: True

Legacy shared half-duplex Ethernet used collision detection. Congestion can still occur on modern switched networks.

### TF15: False

A signature supports origin and integrity relative to a trusted verification key. Encryption is a separate confidentiality mechanism.

### TF16: True

Name resolution is one stage; network reachability, server availability or application errors can still prevent a response.

### TF17: False

That 120 ms response misses the stated deadline. An average hides individual delays.

### TF18: True

Authentication and freshness answer different questions. Replay, sequence and timing checks may still be needed.

### TF19: False

The reward must be associated with its actual transition or episode; arrival order alone can associate it incorrectly.

### TF20: True

The actuator can stall, saturate or fail; outcome feedback is needed to check the physical result.

### TF21: False

Storage is only one constraint. Weights, activations, runtime buffers, sustained power and deadline performance also matter.

### TF22: True

Correct use of exchanged information requires shared meaning, not merely delivery of bytes.

### TF23: False

Cloud-dependent tasks can fail when connectivity is unavailable. Local fallbacks and placement must match task requirements.

### TF24: True

Explanation methods have assumptions and limits. Evaluate what the explanation establishes for its audience.

## Multiple-choice answers and reasoning

### MC01: D

Ki means 1,024: 2 × 1,024 = 2,048 bytes. Multiplying by 8 would convert bytes to bits.

### MC02: D

16 colours need 4 bits per pixel. 500 × 200 × 4 / 8 = 50,000 bytes.

### MC03: C

MAR contains the address. MDR carries the transferred value or instruction; CIR holds the current instruction.

### MC04: A

LOAD sets ACC to 3 and ADD makes 12. STORE copies 12 to address 200.

### MC05: B

A policy governs action choices. Reward scores outcomes; the environment supplies transitions and feedback.

### MC06: C

Target = 1 + 0.9 × 4 = 4.6; error = 2.6; change = 1.3; new Q = 2 + 1.3 = 3.3.

### MC07: A

Always exploiting early estimates can prevent learning about alternatives. Exploration addresses uncertainty, subject to costs and safety constraints.

### MC08: C

0.8 × 10 + 0.2 × (−5) = 8 − 1 = 7. This is an expectation, not the outcome of every trial.

### MC09: A

DRAM stores leaking charge; SRAM uses bistable circuits. Both normally lose data without power.

### MC10: A

For k equal stages and n instructions the ideal time is k + n − 1 = 4 + 5 − 1 = 8 cycles.

### MC11: C

NOT 1 = 0, then 1 AND 0 = 0. The obstacle prevents movement even with a healthy battery.

### MC12: D

Independent pixel operations can use the same instruction over multiple data elements. This does not imply every image workload has no dependencies.

### MC13: B

50 ms = 0.05 s; 30 × 0.05 = 1.5 m. This excludes braking and other delays.

### MC14: D

The Internet layer handles IP addressing and routing. TCP is transport; HTTP is application.

### MC15: B

Validation tests conformance to rules. A plausible but factually wrong value can still pass.

### MC16: B

Signature algorithms use a private signing key and a matching public verification key. Trust in the public key’s identity is also necessary.

### MC17: B

60 ms is below 80 ms. A good average does not make a particular 90 ms response timely.

### MC18: B

Age exceeds the threshold. A rejected packet must not advance the accepted-sequence state.

### MC19: A

The valve actuator creates physical change. The sensor measures a condition; software selects a command.

### MC20: A

Learning needs the correct state/action/outcome association. Network arrival order may differ from event order.

### MC21: C

180 MB ≤ 512 MB and 4 W ≤ 6 W. Timing and accuracy still need separate evaluation.

### MC22: C

The systems disagree about meaning/units despite exchanging a value. A schema and unit agreement are needed.

### MC23: D

Local control can remove a network dependency from a timing-critical path, while still requiring reliable hardware and safety design.

### MC24: D

An explanation should be judged by what it validly reveals to a user, not by its visual polish. It complements, rather than replaces, evaluation.

## Open-ended expected points and sample responses

Valid alternatives receive credit when justified with correct assumptions and evidence. These sample responses demonstrate one acceptable line of reasoning.

### OE01 — expected points (10 marks)

- Correct original trace: ACC 3, 7, 7, 7; memory[200] becomes 7 at STORE; final PC 104 under the stated fetch rule (3 marks).
- Modified result 12, with reasoning from 3 + 9 (1 mark).
- Distinguishes # immediate values from a memory address (2 marks).
- Explains assembler/compiler/interpreter or hybrid implementation without a language-wide false dichotomy (2 marks).
- States limits such as fixed instruction width, invented ISA/registers and simplified timing (2 marks).

**Sample response:** The program begins with PC 100. Fetching LOAD advances PC to 101 and execution places literal 3 in ACC. Fetching ADD advances PC to 102, then ACC becomes 7. STORE advances PC to 103 and copies the value 7 to address 200. HALT is fetched, advancing PC to 104 in this teaching model, and stops execution. The # mark denotes a literal value; 200 in STORE is a location rather than the result. Replacing ADD #4 with ADD #9 makes ACC and the stored result 12. In a real workflow, a compiler may produce machine code or an intermediate form, an assembler resolves assembly operations/labels, and a runtime may interpret or compile bytecode. These stages depend on the implementation. The example is an invented one-word ISA with simplified timing; real processors have architecture-specific instructions, state and control-flow rules.

### OE02 — expected points (10 marks)

- Non-terminal calculation: target 4.6, error 2.6, change 1.3, updated Q 3.3 (3 marks).
- Terminal calculation sets future term to zero, giving target 1 and new Q 1.5 (2 marks).
- Accurately distinguishes reward, policy and value (2 marks).
- Explains uncertainty and evidence/exploration rather than guaranteed success (2 marks).
- Includes a reasonable safety constraint or simulated-training limitation (1 mark).

**Sample response:** The non-terminal target is 1 + 0.9 × 4 = 4.6. Subtracting old Q = 2 gives temporal-difference error 2.6. The learning rate multiplies that by 0.5, so the change is 1.3 and the updated value is 3.3. If the next state is terminal, no future value is bootstrapped: target = 1, error = −1, change = −0.5 and updated Q = 1.5. Reward is the numerical feedback for an interaction; policy determines action choices; Q estimates expected return from a state–action choice. One trip is a noisy sample, not proof of a safe or optimal route. Exploration can reveal an untested route with better return, but its cost and risk matter. A robot can use restricted safe actions and simulation before physical trials, while still testing whether a policy trained in simulation transfers to the real operating domain.

### OE03 — expected points (10 marks)

- Ideal schedule completes I1/I2/I3 on cycles 4/5/6; sequential total 12 (3 marks).
- Distinguishes four-stage instruction latency from overall throughput (2 marks).
- Places I2 E no earlier than cycle 5 under the explicit no-forwarding assumption, with consistent downstream waiting (2 marks).
- Identifies workload, dependencies, memory and power/timing measures (2 marks).
- Avoids universal performance claims from RISC/CISC/GPU/GHz labels (1 mark).

**Sample response:** In the ideal schedule I1 occupies F1, D2, E3, W4; I2 occupies F2, D3, E4, W5; I3 occupies F3, D4, E5, W6. The batch finishes in six cycles rather than twelve sequential stage cycles. Each instruction still passes through four stages, so pipelining improves completion rate after filling rather than reducing an instruction to one stage. Under the separate no-forwarding assumption, I2 cannot execute before cycle 5 because I1’s result becomes available only after cycle 4. It writes in cycle 6. With instructions kept in order, I3 waits behind I2, executes in cycle 6 and writes in cycle 7. Actual CPU forwarding and hazard rules may differ. Pip’s processor choice should be evaluated on its real workload, sustained latency, memory traffic, parallelism and energy. A GPU helps suitable parallel arithmetic; an instruction-set label or clock frequency cannot by itself predict application performance.

### OE04 — expected points (10 marks)

- Converts ms to s and obtains 15, 1.5, 0.15 and 6 m respectively (3 marks).
- Separates delay distance from actuator/braking and other response terms (2 marks).
- Accurately defines bandwidth, latency and jitter (2 marks).
- Explains that reliable ordered transport does not promise a fixed deadline (1 mark).
- Proposes relevant worst-tail/end-to-end measurements and a local/fallback response (2 marks).

**Sample response:** The delays are 0.5, 0.05, 0.005 and 0.2 seconds. Multiplying by 30 m/s gives delay distances of 15, 1.5, 0.15 and 6 metres. These figures measure only travel during the stated communication delay. They omit processing after receipt, actuator response and braking, so they are not total stopping distances. Bandwidth is a link’s capacity; latency is delay; jitter is variation in delay. A high-capacity link can still suffer queues or long paths. TCP can provide ordered reliable delivery while retransmission and head-of-line waiting add time; it does not automatically guarantee the application’s deadline. Measure end-to-end command age under load, including high-percentile or worst observed delay, and measure complete sensor-to-actuator response under relevant failures. Keep timing-critical stopping local when appropriate and define safe behaviour on late, missing or invalid remote commands.

### OE05 — expected points (10 marks)

- A accepts and updates to 42; B rejects stale and remains 42; C rejects duplicate and remains 42 (3 marks).
- Distinguishes authentication, identity/units/version, freshness and replay checks (3 marks).
- Explains accepted-state consistency and safe local response on rejection (2 marks).
- Associates reward to its original transition/episode and notes toy authentication limitation (2 marks).

**Sample response:** Packet A satisfies the identity, units, version, age and sequence requirements, so the receiver accepts it and stores last accepted sequence 42. Packet B has a newer sequence but is 600 ms old, beyond the 200 ms limit; it is rejected as stale and the accepted sequence remains 42. Packet C is recent enough but repeats sequence 42, so it is rejected as a duplicate without changing state. Authentication concerns who may send a protected message; expected device identity and policy version route it to the correct interpretation. Units ensure the numerical value has the intended meaning. Freshness and sequence/session rules address delayed or replayed messages. A rejected packet must not corrupt the bookkeeping that describes accepted commands. The local controller should use its defined safe behaviour. Delayed rewards belong to identified transitions or episodes, not merely the latest action. The worksheet’s authentication Boolean assumes an upstream check and is not a cryptographic protocol.

### OE06 — expected points (10 marks)

- Correctly checks all three hard budgets and rejects local large (3 marks).
- Computes remote 120–320 ms and rejects it for the 80 ms task (2 marks).
- Justifies local control and slower remote analytics with a connectivity fallback (2 marks).
- Addresses sustained thermal/timing validation and relevant accuracy/impact testing (1 mark).
- Includes concrete privacy and accountability measures, recognising supplied accuracies are not proven deployment safety (2 marks).

**Sample response:** The small local model fits all stated limits: 30 ms is below 80 ms, 180 MB is below 512 MB and 4 W is below 6 W. The large local model misses the deadline and exceeds both memory and power budgets despite its better supplied accuracy. The remote option needs 20 + 100 to 20 + 300 ms, or 120–320 ms, and therefore fails the local deadline throughout the stated range. Its 98% figure cannot compensate for this hard constraint. I would keep the immediate control loop and a defined safe stop locally, and use remote processing for slower fleet analysis or training when connectivity is available. I would test warm-device sustained timing, memory peaks, adverse sensor conditions and differences across the intended environments. Image uploads need a legitimate purpose, minimised content, limited retention and access controls. A named team or operator must own monitoring, updates, incident response and appeals or correction where people are affected. These fictional average accuracy figures are useful comparison inputs, not evidence of a safe deployment.

## Review and provenance

This question set was AI-assisted and checked for coverage, arithmetic, answer alignment and document completeness on 7 November 2026. It has not been recorded as independently attempted by another team member. That mandatory human review remains pending and must be documented honestly. Questions are original teaching material based on the module; chapter references and resource attribution are included in the complete Study Guide and Markdown snapshot.
