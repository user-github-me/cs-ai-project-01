# Blue Impulse — Stage 2 classroom teaching content V1.0

Module: Hardware, Networking and Behaviorist AI. This checked medium-specific Markdown is the content source for the editable slides and native presenter notes. All figures are original diagrams and all activities have a debrief below or on a later slide.


## Slide 1: Pip saw it. Why did Pip not stop?

Chapter 1 — The Fundamentals; subtopic: **The stored-program computer**. Planned time: 2 minute(s).

Audience-facing content:

- OBSTACLE DETECTED
- MESSAGE ARRIVES LATE
- THE ROBOT KEEPS MOVING

Teaching notes:

Open with Pip, a fictional campus delivery rover. Its sensor detects a box, but a remote stop instruction arrives late. Ask for two possible causes before defining anything. A good policy is only one part of a working system: representation, execution, hardware, communication and timing all matter. This is an imagined teaching scenario, not an accident report.

Activity: 30 seconds: tell a neighbor one possible cause.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 2: By the end, diagnose the whole system

Chapter 1 — The Fundamentals; subtopic: **The stored-program computer**. Planned time: 1 minute(s).

Audience-facing content:

- A · Bits → programs → actions
- B · Hardware → packets → trust
- C · Control → constraints → decisions

Teaching notes:

Three teaching sessions of approximately 25–35 minutes are suggested. Session A uses slides 1–25, B uses 26–45, and C uses 46 to the end. Take breaks between sessions. Learners should be able to trace a program and Q update, interpret a network delay, and justify a safe division of local and remote work.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 3: Same bits. Different meanings.

Chapter 1 — The Fundamentals; subtopic: **Numbers, characters & codes**. Planned time: 1 minute(s).

Audience-facing content:

- 01000001
- 65 as an unsigned integer
- A in ASCII

Teaching notes:

Data needs an agreed interpretation. This 8-bit pattern represents unsigned integer 65; ASCII code 65 is A. Unicode is a repertoire of code points; UTF-8 is a byte encoding and does not use a fixed one-byte width for all characters. An address, a colour and an instruction also need a format. Source: Python documentation on Unicode and character encodings.

Reference: Unicode; Guide. Full attribution is in `supporting/Sources.md`.

## Slide 4: Predict the value before decoding

Chapter 1 — The Fundamentals; subtopic: **Represent negative values**. Planned time: 2 minute(s).

Audience-facing content:

- 8 bits: 11111101
- Unsigned: ?
- Two’s complement: ?

Teaching notes:

Give 45 seconds of individual thinking, then a show of hands. Keep the answer hidden until the next slide. Ask which bit changes its weight in the signed interpretation. Fixed width is essential.

Activity: 45 seconds · calculate both interpretations.

Expected answer / debrief: Unsigned 253. Eight-bit two’s complement −3.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 5: The width and encoding decide the value

Chapter 1 — The Fundamentals; subtopic: **Represent negative values**. Planned time: 1 minute(s).

Audience-facing content:

- Unsigned: 128 + 64 + 32 + 16 + 8 + 4 + 1 = 253
- Signed: −128 + 64 + 32 + 16 + 8 + 4 + 1 = −3

Teaching notes:

In eight-bit two’s complement the most significant bit has weight −128. The remaining set bits total 125, giving −3. The unsigned range is 0–255; the signed range is −128–127. Hexadecimal FD abbreviates the same eight bits but does not by itself decide signedness. BCD would instead encode each decimal digit separately.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 6: An image is a grid of encoded colours

Chapter 1 — The Fundamentals; subtopic: **Build a digital image**. Planned time: 1 minute(s).

Audience-facing content:

- 100 × 100 pixels
- 24 bits per pixel
- 100 × 100 × 24 ÷ 8 = 30,000 bytes

Teaching notes:

This is raw pixel data for a 100 by 100 image with 24 bits per pixel; it excludes headers, metadata and compression. Resolution concerns the pixel grid; colour depth concerns representable colours per pixel. Lossless compression can restore the original data exactly; lossy compression discards information. File sizes are not determined by dimensions alone.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 7: Sampling turns a signal into numbers

Chapter 1 — The Fundamentals; subtopic: **Sample, store & compress**. Planned time: 1 minute(s).

Audience-facing content:

- MEASURE · at regular times
- QUANTISE · to a finite level
- ENCODE · with bits

Teaching notes:

Use claps as an analogy: a sampling rate counts measurements per second, while bit depth controls how many amplitude levels can be encoded. For raw mono audio, bytes = seconds × samples per second × bits per sample ÷ 8. More channels multiply the size. Sampling and quantisation are different decisions; compression is a later representation choice.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 8: Instructions and data share memory

Chapter 1 — The Fundamentals; subtopic: **The stored-program computer**. Planned time: 1 minute(s).

Audience-facing content:

- INPUT
- MEMORY
- CPU
- OUTPUT

Teaching notes:

The stored-program model keeps instructions and data in addressable memory. The CPU contains a control unit, arithmetic and logic unit, and registers. Address signals identify a location; data signals transfer values; control signals coordinate read/write and other operations. The diagram is a conceptual model, not the physical layout of a modern chip. Cache and separate physical instruction/data paths can exist within a stored-program system.

Reference: Guide; Nand2Tetris. Full attribution is in `supporting/Sources.md`.

## Slide 9: One instruction, three useful questions

Chapter 1 — The Fundamentals; subtopic: **Fetch / decode / execute**. Planned time: 1 minute(s).

Audience-facing content:

- FETCH · Which instruction?
- DECODE · What operation?
- EXECUTE · What changes?

Teaching notes:

In the teaching trace, PC holds the next instruction address, MAR an accessed address, MDR transferred data, CIR the current instruction, and ACC an arithmetic result. Real register sets differ. During fetch we copy the instruction to the current-instruction register and increment PC. Execution may change PC for a branch. We use one address per toy instruction for clarity.

Reference: Guide; Nand2Tetris. Full attribution is in `supporting/Sources.md`.

## Slide 10: Can you trace this tiny program?

Chapter 1 — The Fundamentals; subtopic: **Trace a tiny program**. Planned time: 2 minute(s).

Audience-facing content:

- 100 / LOAD #3
- 101 / ADD #4
- 102 / STORE 200
- 103 / HALT

Teaching notes:

Starting state is PC 100, ACC 0 and memory[200] unset. Explain that # means an immediate literal, while STORE 200 writes to memory address 200. Ask learners to trace ACC and the stored result. This is an invented teaching instruction set, not machine code for a particular CPU.

Activity: 60 seconds · predict ACC and memory[200].

Expected answer / debrief: ACC becomes 3, then 7; memory[200] receives 7. PC is 104 after HALT is fetched.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 11: The result is a state change

Chapter 1 — The Fundamentals; subtopic: **Trace a tiny program**. Planned time: 2 minute(s).

Audience-facing content:

- LOAD #3 / 0 → 3 / —
- ADD #4 / 3 → 7 / —
- STORE 200 / 7 → 7 / 7
- HALT / 7 → 7 / 7

Teaching notes:

Reveal the rows in order verbally. LOAD replaces ACC, ADD changes it, STORE copies it to a location, and HALT stops the trace. PC is 104 because fetch increments it even for HALT in this model. Run the supplied demonstration with --topic execution if desired; this static trace is the full offline fallback. Changing ADD #4 to ADD #9 produces 12.

Reference: Checked Python teaching model. Full attribution is in `supporting/Sources.md`.

## Slide 12: Source code is not a CPU instruction

Chapter 1 — The Fundamentals; subtopic: **From source code to execution**. Planned time: 1 minute(s).

Audience-facing content:

- SOURCE · human readable
- TRANSLATE / RUN · compiler or interpreter
- MACHINE · instructions

Teaching notes:

An assembler translates assembly mnemonics into machine instructions. A compiler usually translates source ahead of execution; interpreters execute a representation at runtime. Real systems may mix compilation, interpretation and just-in-time compilation. An IDE brings editing, execution and debugging tools together; it is not itself a translator category.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 13: The operating system shares the machine

Chapter 1 — The Fundamentals; subtopic: **The operating system’s jobs**. Planned time: 1 minute(s).

Audience-facing content:

- CPU time + memory
- Files + devices
- Protection + coordination

Teaching notes:

Use a shared classroom as an analogy: a timetable allocates time, rooms separate activities, and a sign-out desk manages shared equipment. OS scheduling, memory management, file systems and device drivers support programs. Utilities help with tasks such as backup and diagnostics. Protection is enforced through mechanisms and policy; it is not guaranteed merely by having an OS.

Reference: Guide; OSTEP. Full attribution is in `supporting/Sources.md`.

## Slide 14: An interrupt is a request for attention

Chapter 1 — The Fundamentals; subtopic: **Events, interrupts & peripherals**. Planned time: 1 minute(s).

Audience-facing content:

- SAVE · relevant context
- HANDLE · the event
- RESUME · interrupted work

Teaching notes:

An interrupt can signal an I/O event, timer expiry or other condition. A handler runs after appropriate state is saved, then execution resumes. Polling repeatedly asks whether work is ready; interrupts notify. Priorities and masking may delay handling, so an interrupt does not automatically imply immediate response. Ports and buses connect peripherals using agreed electrical and protocol interfaces.

Reference: Guide; OSTEP. Full attribution is in `supporting/Sources.md`.

## Slide 15: A response can be designed or learned

Chapter 2 — Behaviorism & Behaviorist AI; subtopic: **Learning from the environment**. Planned time: 1 minute(s).

Audience-facing content:

- Reactive rule / If obstacle is near, stop.
- Learned policy / Choose actions using experience.

Teaching notes:

Behaviorism studies observable behavior and environment interactions. Classical conditioning associates stimuli; operant conditioning concerns consequences of actions. Behaviorist-inspired AI is not identical to psychology and is not synonymous with reinforcement learning. A reactive controller can be hand-coded with no training. Learning can produce a policy that is later executed without online updates.

Reference: Guide; Sutton & Barto. Full attribution is in `supporting/Sources.md`.

## Slide 16: Urgent behaviour can take priority

Chapter 2 — Behaviorism & Behaviorist AI; subtopic: **React first: behaviour-based robots**. Planned time: 1 minute(s).

Audience-facing content:

- AVOID COLLISION
- SEEK A GOAL
- EXPLORE

Teaching notes:

In a simplified layered robot, collision avoidance can suppress a lower-priority movement command. Subsumption architectures coordinate layers through suppression or inhibition. This diagram illustrates priority, not the complete Brooks architecture or a universal design rule. Ask why an exploration action should not override the emergency stop layer.

Activity: 20 seconds · which action should win near an obstacle?

Expected answer / debrief: Collision avoidance should take priority in this simplified design.

Reference: Brooks 1986; Guide. Full attribution is in `supporting/Sources.md`.

## Slide 17: Learning closes a feedback loop

Chapter 2 — Behaviorism & Behaviorist AI; subtopic: **The reinforcement-learning loop**. Planned time: 1 minute(s).

Audience-facing content:

- OBSERVATION / STATE
- ACTION
- REWARD + NEXT STATE

Teaching notes:

The agent chooses an action, the environment changes, and the agent receives numerical reward and a new observation. State and observation need not be identical: a noisy sensor may not reveal the full situation. Reward is feedback, not an action and not a policy. A positive reward is not proof that the objective is safe or well specified.

Reference: Sutton & Barto, Chapters 3–6. Full attribution is in `supporting/Sources.md`.

## Slide 18: Policy chooses. Value estimates.

Chapter 2 — Behaviorism & Behaviorist AI; subtopic: **Rewards, policies & values**. Planned time: 1 minute(s).

Audience-facing content:

- POLICY / Which action should I take?
- VALUE / How much return do I expect?

Teaching notes:

A policy maps a state or observation to action choices, possibly probabilistically. A value estimates expected cumulative return. An action value Q(s,a) estimates return for choosing action a in state s and following a policy thereafter. Immediate reward and long-term value are different. Discounting weights future rewards; it does not make uncertain estimates certain.

Reference: Sutton & Barto, Chapters 3–6. Full attribution is in `supporting/Sources.md`.

## Slide 19: Try something new—or use what works?

Chapter 2 — Behaviorism & Behaviorist AI; subtopic: **Explore or exploit?**. Planned time: 2 minute(s).

Audience-facing content:

- Route A: known reward estimate 3
- Route B: barely explored
- Which should the agent try?

Teaching notes:

Give pairs 45 seconds. There is no uniquely correct choice without the exploration strategy, risks and remaining learning budget. Debrief that exploitation uses current estimates; exploration gathers information. In epsilon-greedy behavior, a probability epsilon is assigned to an exploratory choice. Unsafe experimentation requires safeguards; do not imply every action can be tried freely.

Activity: 45 seconds · justify a choice, not just A or B.

Expected answer / debrief: It depends on risk, uncertainty and the exploration strategy; exploration can improve future decisions.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 20: A Q update moves partway to a target

Chapter 2 — Behaviorism & Behaviorist AI; subtopic: **Update a Q value**. Planned time: 2 minute(s).

Audience-facing content:

- Old Q = 2 · learning rate = 0.5
- Reward = 1 · discount = 0.9 · next best Q = 4
- Target = 1 + 0.9 × 4 = 4.6

Teaching notes:

Use the non-terminal Q-learning update Q ← Q + alpha[r + gamma max Q(next, action) − Q]. First compute the target 4.6. The next slide asks for the movement toward it. These numbers are illustrative estimates rather than measured robot performance. For terminal transitions, the future term is zero.

Reference: Sutton & Barto, Chapter 6; checked Python model. Full attribution is in `supporting/Sources.md`.

## Slide 21: Where does the estimate move?

Chapter 2 — Behaviorism & Behaviorist AI; subtopic: **Update a Q value**. Planned time: 1 minute(s).

Audience-facing content:

- Old estimate: 2
- Target: 4.6
- Move halfway: new Q = ?

Teaching notes:

Give 30 seconds and ask learners to show a value with their neighbor. Warn against adding the entire target or confusing the error 2.6 with the new value.

Activity: 30 seconds · calculate the updated value.

Expected answer / debrief: Error 4.6 − 2 = 2.6; change 0.5 × 2.6 = 1.3; new Q = 3.3.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 22: The new estimate is 3.3

Chapter 2 — Behaviorism & Behaviorist AI; subtopic: **Update a Q value**. Planned time: 1 minute(s).

Audience-facing content:

- Error = 4.6 − 2 = 2.6
- Change = 0.5 × 2.6 = 1.3
- New Q = 2 + 1.3 = 3.3

Teaching notes:

Check the arithmetic with --topic rl. For a terminal transition using the same old Q, reward and learning rate, target is 1, so new Q is 1.5. Do not bootstrap from a terminal next state. The update changes one estimate; one update does not guarantee an optimal policy.

Reference: Checked Python teaching model. Full attribution is in `supporting/Sources.md`.

## Slide 23: An MDP makes assumptions explicit

Chapter 2 — Behaviorism & Behaviorist AI; subtopic: **A decision problem as an MDP**. Planned time: 1 minute(s).

Audience-facing content:

- STATES + ACTIONS
- TRANSITIONS + REWARDS
- DISCOUNT + MARKOV ASSUMPTION

Teaching notes:

An MDP specifies states, available actions, transition probabilities, rewards and a discount factor in the formulation used here. The Markov property says the present state and action contain the information needed for the next-step distribution. It does not mean deterministic outcomes. A slippery floor can make an intended action produce several possible next states.

Reference: Sutton & Barto, Chapter 3. Full attribution is in `supporting/Sources.md`.

## Slide 24: Training and deployment have different jobs

Chapter 2 — Behaviorism & Behaviorist AI; subtopic: **Training is different from using a policy**. Planned time: 1 minute(s).

Audience-facing content:

- TRAIN / Collect experience; update the policy.
- DEPLOY / Use a policy; monitor its behavior.

Teaching notes:

Training often uses repeated trials and more computation. Deployment executes a selected policy under actual timing and resource constraints. Some systems learn online, but that is a deliberate architecture choice. A robot using a learned policy is not necessarily training during every action. Separate logging, updates and safety decisions.

Reference: Sutton & Barto; Guide. Full attribution is in `supporting/Sources.md`.

## Slide 25: Session A checkpoint: explain an action

Chapter 2 — Behaviorism & Behaviorist AI; subtopic: **Training is different from using a policy**. Planned time: 2 minute(s).

Audience-facing content:

- Bits need an interpretation.
- Programs change machine state.
- A policy chooses; feedback can update it.

Teaching notes:

Ask two volunteers for a 20-second explanation: one traces data through execution, one distinguishes a reactive rule from a learned policy. Use the prepared activities in Chapters 1 and 2 after class. Video 05 revisits program execution; Video 01 revisits Q-learning. Next session asks whether the hardware and network can deliver that action in time.

Activity: 60 seconds · explain the chain to a neighbor.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 26: A good decision still needs a body

Chapter 3 — Hardware; subtopic: **Hardware gives software a body**. Planned time: 1 minute(s).

Audience-facing content:

- SENSE · input device
- COMPUTE · processor + memory
- ACT · output device

Teaching notes:

Reconnect to the robot. A sensor measures a physical condition, a processor evaluates a policy, and an actuator changes the environment. Storage retains programs and records. Hardware is the physical part of the system; software defines operations. Devices may combine roles.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 27: Memory trades capacity against access time

Chapter 3 — Hardware; subtopic: **Memory: capacity versus speed**. Planned time: 1 minute(s).

Audience-facing content:

- REGISTERS
- CACHE
- RAM
- SSD / HDD

Teaching notes:

A conceptual hierarchy puts small, low-latency storage close to the CPU. Cache stores copies to exploit locality; a cache miss fetches data from a lower level. DRAM uses charge and refresh, while SRAM uses bistable cells. Both are generally volatile. The shape widths show an idea, not measured timings or prices. Increasing capacity alone does not guarantee faster software.

Reference: Guide; OSTEP. Full attribution is in `supporting/Sources.md`.

## Slide 28: Keep data after the power disappears

Chapter 3 — Hardware; subtopic: **Keep data when power is off**. Planned time: 1 minute(s).

Audience-facing content:

- RAM / Working state; generally volatile.
- FLASH / SSD / Non-volatile electronic storage.
- HDD / OPTICAL / Magnetic / laser-readable storage.

Teaching notes:

Choose storage using capacity, latency, endurance, energy, durability and cost. ROM-family devices store persistent firmware; PROM is programmed once, EPROM can be erased with ultraviolet light, and EEPROM electrically. Flash commonly erases in blocks. Non-volatile is not the same as indestructible: backups and integrity checks still matter.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 29: Pipelining overlaps different instructions

Chapter 3 — Hardware; subtopic: **Overlap work with a pipeline**. Planned time: 2 minute(s).

Audience-facing content:


Teaching notes:

Four one-cycle stages: Fetch, Decode, Execute, Write. Three independent instructions complete in cycles 4, 5 and 6. One instruction still takes four stages; steady-state throughput improves. Real dependencies, branches and resource conflicts can cause stalls. This is an idealized teaching pipeline, not a claim about a specific processor. The Python hardware example prints the same schedule.

Activity: 30 seconds · when does instruction 3 finish?

Expected answer / debrief: Cycle 6, assuming no hazards or stalls.

Reference: Checked Python teaching model. Full attribution is in `supporting/Sources.md`.

## Slide 30: Parallel hardware is useful only when work fits

Chapter 3 — Hardware; subtopic: **The hardware behind an AI model**. Planned time: 1 minute(s).

Audience-facing content:

- CPU / Flexible control and varied work.
- GPU / NPU / Many suitable operations in parallel.

Teaching notes:

AI workloads often use tensor operations that parallel hardware can accelerate. Data movement, memory capacity, arithmetic precision and software support can become bottlenecks. RISC and CISC describe instruction-set design families; neither label alone guarantees speed or energy efficiency. Flynn categories describe instruction/data streams: SISD, SIMD, MISD and MIMD. The categories do not by themselves predict performance.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 31: A logic gate makes a precise choice

Chapter 3 — Hardware; subtopic: **Reason with logic gates**. Planned time: 1 minute(s).

Audience-facing content:

- 0 / 0 / 0
- 0 / 1 / 0
- 1 / 0 / 0
- 1 / 1 / 1

Teaching notes:

A toy actuator permission requires Enabled AND Safe. Both input conditions must be true. This truth table is complete for two binary inputs. Real safety circuits need more than one gate and require appropriate assurance. NOT reverses a bit; OR needs at least one true input. Boolean simplification should preserve every row of the truth table.

Activity: 20 seconds · what happens when either input is zero?

Expected answer / debrief: The AND output is zero.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 32: The physical world needs an interface

Chapter 3 — Hardware; subtopic: **Sense, decide, act, sense again**. Planned time: 1 minute(s).

Audience-facing content:

- SENSOR · analogue signal
- ADC + CONTROLLER · digital decision
- DRIVER + ACTUATOR · physical output

Teaching notes:

An ADC maps an analogue input to digital samples. A DAC can produce an analogue output; PWM instead varies pulse duty cycle and needs suitable downstream hardware. Microcontrollers integrate processor, memory and peripherals. An embedded system performs a role inside a larger device. User interfaces should show meaningful system state and permit appropriate human control.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 33: A message crosses several different jobs

Chapter 4 — Networking; subtopic: **The devices along a network path**. Planned time: 1 minute(s).

Audience-facing content:

- DEVICE
- ACCESS POINT / SWITCH
- ROUTER
- SERVER

Teaching notes:

A NIC attaches a device to a link. An access point provides wireless access, a switch forwards local frames, and a router forwards IP packets between networks. The diagram is a simplified path: multiple routers or combined devices may exist. A LAN covers a limited local area, WAN spans wider areas, PAN is personal scope and MAN metropolitan scope.

Reference: IETF RFC 1122; Guide. Full attribution is in `supporting/Sources.md`.

## Slide 34: Who requests—and who provides?

Chapter 4 — Networking; subtopic: **Clients, servers & peers**. Planned time: 1 minute(s).

Audience-facing content:

- CLIENT / SERVER / Requester and service provider.
- PEER TO PEER / Participants can do both jobs.

Teaching notes:

These are roles, not necessarily different hardware types. Thin clients rely more on remote services; thick clients perform more local work. Cloud infrastructure offers shared remote resources; edge processing happens near the source. Cloud is not simply another name for the Internet. A distributed system must coordinate partial failures and concurrent work.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 35: Name resolution is not page delivery

Chapter 4 — Networking; subtopic: **Find a host with DNS**. Planned time: 1 minute(s).

Audience-facing content:

- DOMAIN NAME · example.org
- DNS LOOKUP · find address data
- CONNECTION · request the resource

Teaching notes:

DNS resolves domain names to records such as IP addresses; caches and recursive resolvers are involved. The web is an application using the Internet, not the entire Internet. In a URL, the scheme identifies access semantics, the host names the destination, and path/query identify application resources. A fragment is interpreted by the client and is not sent as part of an HTTP request target.

Reference: IETF RFC 1034; RFC 3986. Full attribution is in `supporting/Sources.md`.

## Slide 36: Layering separates responsibilities

Chapter 4 — Networking; subtopic: **Give each protocol layer a job**. Planned time: 1 minute(s).

Audience-facing content:

- APPLICATION · message meaning
- TRANSPORT · process to process
- INTERNET · packet routing
- LINK · the local hop

Teaching notes:

This four-layer Internet model is a teaching organization, not the only layering convention. Encapsulation adds layer-specific metadata as data moves down the stack. Receivers interpret corresponding layers. A protocol establishes syntax and behavior between peers. The application still needs to check whether received values make sense for the task.

Reference: IETF RFC 1122. Full attribution is in `supporting/Sources.md`.

## Slide 37: Reliable delivery is not a deadline guarantee

Chapter 4 — Networking; subtopic: **Give each protocol layer a job**. Planned time: 1 minute(s).

Audience-facing content:

- TCP / Ordered reliable byte stream.
- UDP / Datagrams without that guarantee.

Teaching notes:

TCP handles retransmission, ordering and flow/congestion control, but cannot promise application usefulness before a hard deadline. UDP preserves message datagrams without TCP-like reliable ordered delivery; the application can add checks and recovery. UDP is not automatically safe or always faster. HTTP is used for web resources; SMTP sends mail while IMAP accesses mailboxes. File transfers have protocols such as SFTP and FTP, whose security properties differ.

Reference: IETF RFC 9293; RFC 768; Guide. Full attribution is in `supporting/Sources.md`.

## Slide 38: Shared capacity creates waiting

Chapter 4 — Networking; subtopic: **Sharing a communication medium**. Planned time: 1 minute(s).

Audience-facing content:

- PACKET A
- PACKET B
- PACKET C

Teaching notes:

When arrivals exceed the service opportunity, packets queue. Wireless devices also coordinate access and may face interference. Packet switching shares links; circuit switching reserves resources along a path. Fiber, copper and radio offer different capacity, distance, mobility and interference characteristics. Ethernet collision detection concerns traditional shared half-duplex links; modern switched full-duplex Ethernet does not use CSMA/CD in that way.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 39: Capacity is not responsiveness

Chapter 4 — Networking; subtopic: **Capacity is not responsiveness**. Planned time: 1 minute(s).

Audience-facing content:

- BANDWIDTH · available capacity
- THROUGHPUT · achieved transfer rate
- LATENCY / JITTER · delay / variation

Teaching notes:

Add packet loss as another key measure. A high-capacity link can still have large propagation or queueing delay. Jitter makes arrival times vary, which can disrupt control or media even when mean delay is acceptable. State units: capacity and throughput usually bits per second; delay usually seconds or milliseconds. Do not compare a throughput number with latency as if they were the same quantity.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 40: How far does the robot move while waiting?

Chapter 4 — Networking; subtopic: **Capacity is not responsiveness**. Planned time: 2 minute(s).

Audience-facing content:

- Speed = 30 metres / second
- Delay = 200 milliseconds
- Distance during delay = ?

Teaching notes:

Give 45 seconds. Ask students to convert milliseconds before multiplying. This is a deliberately high-speed hypothetical vehicle/robot calculation; it is not a recommended operating speed. We calculate distance during delay only, not braking distance, sensing delay or total stopping distance.

Activity: 45 seconds · convert, then multiply.

Expected answer / debrief: 200 ms = 0.2 s; 30 × 0.2 = 6 metres.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 41: A short delay can have a physical consequence

Chapter 4 — Networking; subtopic: **Capacity is not responsiveness**. Planned time: 1 minute(s).

Audience-facing content:

- 500 ms / 15
- 200 ms / 6
- 50 ms / 1.5
- 5 ms / 0.15

Teaching notes:

All bars use one linear scale. At 30 m/s, distances are 15, 6, 1.5 and 0.15 metres. Tiny values must not be inflated visually. A shorter network delay reduces this component of travel but does not solve sensor, control, actuator or braking delays. Run --topic network for the numerical fallback.

Reference: Checked Python teaching model. Full attribution is in `supporting/Sources.md`.

## Slide 42: Correct delivery is not correct meaning

Chapter 4 — Networking; subtopic: **Protect data and its meaning**. Planned time: 1 minute(s).

Audience-facing content:

- VALIDATION / Does this value obey the rules?
- VERIFICATION / Does it match a source or expected copy?

Teaching notes:

Validation might check a temperature is within a specified range or that a field uses metres. Verification might compare against a trusted source or use double entry. Neither guarantees truth: a plausible but inaccurate sensor value can pass a range check. Security protects systems and data; privacy concerns appropriate collection, use and disclosure of personal information. Integrity concerns unauthorized or accidental alteration.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 43: Protect secrecy, identity and integrity

Chapter 4 — Networking; subtopic: **Trust, signatures & certificates**. Planned time: 1 minute(s).

Audience-facing content:

- ENCRYPTION · keep data confidential
- SIGNATURE / MAC · detect changes, authenticate
- CERTIFICATE · bind an identity to a key

Teaching notes:

Symmetric encryption uses shared secret key material. Public-key systems use a public/private key pair. Digital signatures provide authenticity and integrity checks, not confidentiality. A certificate is an issuer-signed binding and must be validated, including identity and trust chain. MACs use a shared secret and do not provide the same public verifiability as signatures. Modern protocols normally combine mechanisms.

Reference: IETF RFC 8446; NIST. Full attribution is in `supporting/Sources.md`.

## Slide 44: Secure transport still needs safe application logic

Chapter 4 — Networking; subtopic: **Encryption modes & quantum ideas**. Planned time: 1 minute(s).

Audience-facing content:

- TLS · protect the channel
- VALIDATE · interpret the data
- DECIDE · respect the deadline

Teaching notes:

TLS uses authenticated key establishment and symmetric authenticated encryption in modern configurations. SSL is obsolete. Block/stream encryption descriptions are not enough to assess a mode; nonce reuse and missing authentication can destroy security. QKD concerns key establishment under physical and protocol assumptions; it does not replace endpoint security, authentication or application checks. Do not implement cryptography from these teaching slides.

Reference: IETF RFC 8446; NIST. Full attribution is in `supporting/Sources.md`.

## Slide 45: Session B checkpoint: useful, not merely delivered

Chapter 4 — Networking; subtopic: **Capacity is not responsiveness**. Planned time: 2 minute(s).

Audience-facing content:

- Hardware limits execution.
- Networks add delay and uncertainty.
- A secure packet can still be stale.

Teaching notes:

Ask each pair for one hardware bottleneck and one reason a correctly delivered message might be unusable. Connect to Video 02 (hardware), Video 03 (network challenges), and Video 04 (networked behaviorist AI). Chapter 3 and 4 practice develops the same ideas. Next session integrates a safe local behavior with remote coordination.

Activity: 60 seconds · name one bottleneck and one message risk.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 46: A smart system is a chain of responsibilities

Chapter 5 — Applications; subtopic: **A system that senses and acts**. Planned time: 1 minute(s).

Audience-facing content:

- SENSE + VALIDATE
- DECIDE + ACT
- OBSERVE + REVIEW

Teaching notes:

Start session C by revisiting the delayed stop message. A useful system needs valid measurements, a decision rule, executable actions, feedback and a way to detect failures. Networking and AI are options inside this chain, not definitions of intelligence or guarantees of quality. The same chain appears in irrigation, warehouse robotics and monitoring systems.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 47: Irrigation: what should happen when data is missing?

Chapter 5 — Applications; subtopic: **Example: an irrigation system**. Planned time: 2 minute(s).

Audience-facing content:

- Moisture report is old.
- The valve can flood the bed.
- Keep watering—or pause and alert?

Teaching notes:

Give pairs 45 seconds and require one reason. In this illustrative design, pause watering and alert a person rather than treat missing data as a dry-soil reading. Explain that the correct fallback is hazard- and context-specific: other systems could require a different safe state. The goal is to make the assumption explicit, not to prescribe a universal response.

Activity: 45 seconds · choose and justify a fallback.

Expected answer / debrief: For this flooding-risk example: pause, alert, and request a fresh reading.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 48: A deadline is part of the result

Chapter 5 — Applications; subtopic: **Real-time means meeting a deadline**. Planned time: 1 minute(s).

Audience-facing content:

- CORRECT VALUE, TOO LATE / May be unusable for control.
- CORRECT VALUE, ON TIME / Can inform the intended decision.

Teaching notes:

Real-time means meeting specified timing constraints, not merely running quickly on average. Hard and soft deadline requirements have different consequences. End-to-end budgets include sensing, communication, queueing, computation and actuation. The system must state the deadline and what happens when it cannot meet it.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 49: A control message needs context

Chapter 5 — Applications; subtopic: **Networking for a behaviour-based agent**. Planned time: 1 minute(s).

Audience-facing content:

- Device / robot-7
- Units / policy / metres / version 3
- Sequence / age / 42 / 50 ms

Teaching notes:

A message should be tied to the intended device, schema, units, policy version and action or sequence. Freshness checks need a clock or protocol model; timestamps are not magically comparable across unsynchronized devices. Our toy validator uses a known now value and a 200 ms limit. Authentication is an input from a separate validated mechanism, not something a Boolean field provides.

Reference: Checked Python teaching model. Full attribution is in `supporting/Sources.md`.

## Slide 50: Which messages should the robot accept?

Chapter 5 — Applications; subtopic: **Networking for a behaviour-based agent**. Planned time: 2 minute(s).

Audience-facing content:

- A / 42 / 50 ms
- B / 43 / 600 ms
- C / 42 / 60 ms

Teaching notes:

Process A, then B, then C. Start with last accepted sequence 41. All messages have the correct device, units, policy version and an externally verified authentication result. Freshness limit is 200 ms. Give 60 seconds; ask pairs to update last accepted sequence only when a message is accepted.

Activity: 60 seconds · accept or reject each in order.

Expected answer / debrief: A accepted; B stale; C duplicate. Last accepted sequence stays 42.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 51: Accept once. Reject stale and duplicate commands.

Chapter 5 — Applications; subtopic: **Networking for a behaviour-based agent**. Planned time: 2 minute(s).

Audience-facing content:

- A · 42 · 50 ms / ACCEPT / 41 → 42
- B · 43 · 600 ms / STALE / 42 → 42
- C · 42 · 60 ms / DUPLICATE / 42 → 42

Teaching notes:

B has a higher sequence but is too old; rejecting it must not advance the accepted sequence. C is fresh but duplicates A. The teaching validator does not handle all real distributed-systems concerns such as sequence wraparound, restarts, clock drift or malicious timestamps. Run --topic networked-ai for the exact offline trace.

Reference: Checked Python teaching model. Full attribution is in `supporting/Sources.md`.

## Slide 52: Delayed feedback must belong to the right action

Chapter 5 — Applications; subtopic: **Feedback can change a policy**. Planned time: 1 minute(s).

Audience-facing content:

- ACTION ID · what was chosen?
- OUTCOME · what happened?
- MATCH + UPDATE · which experience?

Teaching notes:

A delayed reward should be associated with the experience that produced it. Missing feedback must not silently become numerical reward zero. Reordered or duplicated feedback can corrupt training data if not tracked. Logging should preserve enough context for diagnosis while respecting data minimization and privacy. Deployment and training are separate processes even when connected.

Reference: Guide; Sutton & Barto. Full attribution is in `supporting/Sources.md`.

## Slide 53: People need an understandable system state

Chapter 5 — Applications; subtopic: **Help people understand the system**. Planned time: 1 minute(s).

Audience-facing content:

- SHOW · what the system knows
- EXPLAIN · uncertainty and limits
- ALLOW · oversight and recovery

Teaching notes:

Automation can remove repetitive work and also move errors into design, configuration and monitoring. Appropriate trust depends on visible limits and feedback. Human-AI interaction includes uncertainty, delegation and changing behavior; conventional HCI still supplies useful usability principles. An override should have a clear effect and should not be an unexplained magic fix.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 54: A faster system can still be a worse system

Chapter 5 — Applications; subtopic: **Evaluate more than performance**. Planned time: 1 minute(s).

Audience-facing content:

- MEASURE PERFORMANCE / Timing, accuracy, energy, reliability.
- MEASURE IMPACT / Privacy, fairness, access, accountability.

Teaching notes:

Ask whose data is collected, who benefits, who bears errors and who can contest a decision. An accessible interface and clear accountability are part of deployment quality. Opportunities in automation do not remove social and organizational responsibility. No claims about measured user outcomes are made here; these are evaluation dimensions for a proposed system.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 55: Four physical budgets constrain every design

Chapter 6 — Strengths & Limitations; subtopic: **Four physical budgets**. Planned time: 1 minute(s).

Audience-facing content:

- TIME
- ENERGY + HEAT
- MEMORY + COMPUTE

Teaching notes:

Time, energy, memory and compute are four budgets; heat is a consequence and constraint linked to energy and packaging. Trading one budget can stress another. A larger model may improve a metric but miss the deadline or exceed memory. State operating conditions and worst-case concerns instead of quoting a single ideal benchmark.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 56: Bad inputs can look perfectly plausible

Chapter 6 — Strengths & Limitations; subtopic: **Reliable decisions need reliable inputs**. Planned time: 1 minute(s).

Audience-facing content:

- SENSOR DRIFT / Measurements gradually change.
- DISTRIBUTION SHIFT / Deployment differs from training.

Teaching notes:

A sensor can report a plausible value while being miscalibrated. Drift detection, calibration and redundant measurements may help depending on the task. Distribution shift concerns a change in the data-generating situation between training and deployment. Neither a successful range check nor high past accuracy guarantees correct current decisions. Include fault detection and a defined fallback.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 57: More devices create coordination work

Chapter 6 — Strengths & Limitations; subtopic: **Grow without losing coordination**. Planned time: 1 minute(s).

Audience-facing content:

- SCALABILITY · handle growth
- INTEROPERABILITY · share meaning
- RESILIENCE · handle disruption

Teaching notes:

Scaling from one robot to a fleet adds contention, identity management, version compatibility and aggregate load. Interoperability needs common semantics, not just parsable bytes. Resilience means maintaining or recovering acceptable service under disruption; it is not the absence of all failures. Test overload, restart, loss of connectivity and mixed-version behavior.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 58: Predicting an outcome is not explaining behavior

Chapter 6 — Strengths & Limitations; subtopic: **Predict an outcome or model behaviour?**. Planned time: 1 minute(s).

Audience-facing content:

- PREDICTIVE ANALYTICS / Forecast a future outcome.
- BEHAVIOURAL MODELLING / Represent actions and interactions.

Teaching notes:

A model can predict equipment failure without modeling an agent policy. Behavioral modeling may describe interactions or decision patterns rather than only forecast a scalar outcome. Explainability should serve a user need: diagnosis, oversight or contestability. A plausible verbal explanation is not proof of causal faithfulness. Evaluate explanation usefulness and accuracy separately.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 59: Final design challenge: rescue Pip

Chapter 6 — Strengths & Limitations; subtopic: **Put each computation where it fits**. Planned time: 3 minute(s).

Audience-facing content:

- Local control: 5 ms loop
- Remote service: variable 500 ms delay
- Place stop, training and fleet planning.

Teaching notes:

Give groups of two or three 90 seconds. They must place emergency obstacle response, policy training, telemetry logging and fleet route coordination. Require one failure rule for network loss and one reason the proposal could still fail. Assume the local hardware can run the selected controller; do not assume 5 ms alone proves safety. This is a design exercise, not a validated safety case.

Activity: 90 seconds · choose local or remote; name a failure rule.

Expected answer / debrief: Local sensing/stop/controller; remote training and fleet planning where delays allow; buffer or reduce telemetry during loss. Explicit fallback and validation still required.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 60: Keep the urgent loop local; coordinate when useful

Chapter 6 — Strengths & Limitations; subtopic: **Put each computation where it fits**. Planned time: 2 minute(s).

Audience-facing content:

- LOCAL · Sense → validate → decide → act
- REMOTE · Train → coordinate → review
- GATE · Freshness + identity + version

Teaching notes:

This is one defensible proposal, not the only correct architecture. Local collision response avoids dependence on remote latency. Remote infrastructure can train models and coordinate wider plans if their deadlines permit it. Versioned, validated updates pass through an explicit gate. Losing the network should invoke the defined degraded mode. Reliable local sensors, adequate hardware, tested control and human oversight remain necessary.

Reference: Guide; checked teaching models. Full attribution is in `supporting/Sources.md`.

## Slide 61: The opening mystery has five possible failure points

Chapter 6 — Strengths & Limitations; subtopic: **Judge the whole system**. Planned time: 1 minute(s).

Audience-facing content:

- Representation + execution
- Policy + hardware
- Network timing + application checks

Teaching notes:

Return to slide 1. The robot may fail because the observation is misinterpreted, the program or policy is wrong, the processor cannot meet the budget, or a message arrives late or is used incorrectly. The central takeaway is that useful intelligence is a property of the integrated system under stated conditions. Ask each learner to write one question they would test before deployment.

Activity: 30 seconds · write your first verification question.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 62: Continue with the matching learning resources

Chapter 6 — Strengths & Limitations; subtopic: **Judge the whole system**. Planned time: 1 minute(s).

Audience-facing content:

- CH 1–2 · trace a program; update a Q value
- CH 3–4 · trace a pipeline; explain delay
- CH 5–6 · validate a packet; justify an architecture

Teaching notes:

The local Learning_Resource_Map.md lists exact chapter/subtopic titles, all five video filenames and matching demonstration commands. Videos 01 through 05 focus respectively on reinforcement learning, hardware, network challenges, networking for behaviorist AI and program execution. Use chapter exercises and solutions after attempting each task. No internet access is required for the submitted slide activities or Python demonstrations.

Reference: Guide. Full attribution is in `supporting/Sources.md`.

## Slide 63: Sources, scope and production credit

Chapter 6 — Strengths & Limitations; subtopic: **Sources & acknowledgements**. Planned time: 0.5 minute(s).

Audience-facing content:

- BLUE IMPULSE · Stage 2 · PPT V1.0
- Original editable diagrams + checked teaching models
- Full references and AI evidence included in this package

Teaching notes:

This classroom deck was generated with NeoGPT/Codex assistance on 7 November 2026 from the project’s six-chapter Markdown and study-guide content. AI wrote substantial teaching content, diagrams, notes and builder code; this is disclosed, not attributed to an unverified student contribution. Sources include Sutton and Barto, Brooks, OSTEP, Nand2Tetris, Unicode and relevant IETF RFCs; exact titles and locations are in Sources.md. Automated arithmetic, package and rendering checks are documented. A human teammate rehearsal and classroom projector check remain pending; do not mark them complete without evidence.

Reference: Guide. Full attribution is in `supporting/Sources.md`.
