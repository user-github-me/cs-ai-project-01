# Video 04 — Networking for behaviorist AI: narration script and teaching outline

**Video file:** BlueImpulse_Video04_Networking_for_Behaviorist_AI.mp4  
**Viewing position:** 4 of 5  
**Duration:** 10:00 (600 seconds)  
**Format:** MP4, 1920 × 1080, 60 fps  
**File size:** 50,061,875 bytes (50.06 MB)

**Prerequisites:** Understand fixed reactive rules versus learned policies (Video 01 / Chapter 2), and latency versus bandwidth (Video 03 / Chapter 4).

**Learning goals:**

- Separate local control from shared services
- Interpret network messages safely
- Associate feedback with its original action

**Chapter and subtopic connections:**

- Chapter 5 — Applications / Networking for a behaviour-based agent
- Chapter 2 — Behaviorism & Behaviorist AI / React first: behaviour-based robots
- Chapter 6 — Strengths & Limitations / Put each computation where it fits

**Apply in the learning system:** Complete ACT-05 in the Study Guide / Markdown activity file. Use Test Bank questions TF17–TF20, MC17–MC20 and OE05 for review. The six-chapter PPT deck introduces the same chapter concepts through classroom discussion.

**Optional interactive companion:** ROVERLAB lets you apply these ideas by building a robot, connecting its network and comparing stimulus-response rules. Play at https://roverlab-blue-impulse.vercel.app and use the ROVERLAB activity in the Study Guide. It is a simplified rule-and-feedback model, not a neural network or the numerical Q-learning algorithm taught in Video 01.

**Materials:** Paper and a calculator are sufficient. The optional supporting Python demonstration uses Python 3.9 or newer with no third-party packages or account.

```sh
python3 supporting/BlueImpulse_Demonstrations.py --topic networked-ai
```

## Chapter timestamps and teaching route

| Time | Teaching step | Chapter / subtopic |
| --- | --- | --- |
| 00:00–00:29 | Three commands. One decision. | Chapter 5 — Applications / Networking for a behaviour-based agent |
| 00:29–01:06 | Today’s route | Chapter 5 — Applications / Networking for a behaviour-based agent |
| 01:06–01:59 | Reactive behaviour is not always learning | Chapter 2 — Behaviorism & Behaviorist AI / React first: behaviour-based robots |
| 01:59–02:45 | Keep the time-critical loop close | Chapter 5 — Applications / Networking for a behaviour-based agent |
| 02:45–03:36 | Let the network do useful shared work | Chapter 5 — Applications / Networking for a behaviour-based agent |
| 03:36–04:41 | A number needs context | Chapter 5 — Applications / Networking for a behaviour-based agent |
| 04:41–05:54 | Inspect three incoming messages | Chapter 5 — Applications / Networking for a behaviour-based agent |
| 05:54–06:43 | Match feedback to the original action | Chapter 5 — Applications / Networking for a behaviour-based agent |
| 06:43–07:31 | Define what an outage means | Chapter 6 — Strengths & Limitations / Put each computation where it fits |
| 07:31–08:26 | The feedback packet never arrived | Chapter 5 — Applications / Networking for a behaviour-based agent |
| 08:26–09:31 | Connect the responsibilities | Chapter 5 — Applications / Networking for a behaviour-based agent |
| 09:31–10:00 | Pip completes the shift | Chapter 5 — Applications / Networking for a behaviour-based agent |

## Using this script

The following narration is the exact measured cue text for the revised recording. Cue timestamps refer to the video timeline; small gaps include intentional thinking time and transition space. The voice is synthetic (Kokoro ONNX, am_michael), not a recording of a student. The full teaching outline states the purpose, visual focus and learner action alongside the words spoken.

### 00:00–00:29 — Three commands. One decision.

**Content reference:** Chapter 5 — Applications / Networking for a behaviour-based agent

**Teaching / visual direction:** Keep Pip’s problem visible while the opening question establishes why the concept matters. Key visual labels: FRESH / LATE / REPEATED.

**00:00.150–00:03.307:** Three commands. Only one belongs now.

**00:03.307–00:11.885:** Pip, our simulated campus delivery rover, receives a fresh command, an old command, and a command it has already handled.

**00:11.885–00:16.343:** They look similar on screen. Treating them alike would be a mistake.

**00:16.343–00:21.505:** Have you ever wondered how a connected agent preserves the meaning of a message?

**00:21.505–00:28.033:** Chapter five, Applications, connects local control, shared services, and message context.

### 00:29–01:06 — Today’s route

**Content reference:** Chapter 5 — Applications / Networking for a behaviour-based agent

**Teaching / visual direction:** Reveal the learning goals in the order spoken, then retain a small progress cue. Key visual labels: LOCAL CONTROL / SHARED SERVICES / MESSAGE CONTEXT.

**00:29.889–00:37.334:** You will separate a fast local control loop from shared analysis, coordination, and training services.

**00:37.334–00:45.760:** You will explain why messages need context such as identity, time, sequence, units, and policy version.

**00:45.760–00:50.644:** You will also connect delayed learning feedback to the action that produced it.

**00:50.644–00:56.553:** Welcome to the tutorial on networking for behaviorist AI by Blue Impulse.

**00:56.553–01:04.534:** Connect the subtopics Real-time response, Networking for a behaviour-based agent, and Where should the intelligence run?

### 01:06–01:59 — Reactive behaviour is not always learning

**Content reference:** Chapter 2 — Behaviorism & Behaviorist AI / React first: behaviour-based robots

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: REACTIVE RULE / LEARNED POLICY / TRAINING.

**01:06.933–01:16.301:** Start with Chapter two, Behaviorism and Behaviorist AI. A reactive agent may map a sensed condition directly to an action.

**01:16.301–01:24.684:** A fixed rule such as avoiding a detected obstacle can produce useful behaviour without learning from reward.

**01:24.684–01:31.531:** Reinforcement learning adds a different claim: experience is used to improve a policy.

**01:31.531–01:39.897:** A network connection does not turn a fixed rule into a learning algorithm, and not every connected agent learns online.

**01:39.897–01:48.945:** For our campus delivery system example, think of a locally evaluated policy with separate, reviewed updates from a server.

**01:48.945–01:56.453:** We will label architectural choices clearly instead of treating them as properties of every AI system.

### 01:59–02:45 — Keep the time-critical loop close

**Content reference:** Chapter 5 — Applications / Networking for a behaviour-based agent

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: SENSE / EVALUATE / ACT.

**01:59.628–02:06.305:** Time-critical sensing, policy evaluation, and actuator control can stay near the device.

**02:06.305–02:14.649:** Our robot observes an obstacle, evaluates its current policy, and sends a control signal to the actuator hardware.

**02:14.649–02:18.766:** This local path need not wait for every cloud exchange.

**02:18.766–02:24.909:** A real-time task must meet a specified deadline, not just be fast on average.

**02:24.909–02:34.853:** Local processing removes some network dependency, but it still needs adequate compute, trustworthy sensing, and suitable physical controls.

**02:34.853–02:42.792:** Local does not automatically mean safe. The requirements and failure behaviour still have to be designed and checked.

### 02:45–03:36 — Let the network do useful shared work

**Content reference:** Chapter 5 — Applications / Networking for a behaviour-based agent

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: ROBOT / NETWORK / SERVER.

**02:46.063–02:53.401:** In our illustrative campus delivery system, each robot handles immediate motion control locally.

**02:53.401–03:02.040:** A shared service can allocate tasks, coordinate inventory, and analyse selected telemetry from several devices.

**03:02.040–03:08.952:** Imagine a local driver following a route while a dispatcher coordinates deliveries across the fleet.

**03:08.952–03:17.274:** The driver needs immediate awareness; the dispatcher benefits from a broader view. The analogy separates responsibilities.

**03:17.274–03:25.533:** The network may distribute reviewed policy updates, but a received update should not automatically bypass validation.

**03:25.533–03:33.426:** Edge and cloud are not opposing teams. Put each part of the workload where its deadlines and resource needs fit.

### 03:36–04:41 — A number needs context

**Content reference:** Chapter 5 — Applications / Networking for a behaviour-based agent

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: IDENTITY / TIME / SEQUENCE / UNITS / POLICY.

**03:36.672–03:44.586:** A message needs enough context to be interpreted correctly. A number by itself is not a complete instruction.

**03:44.586–03:52.649:** Device identity tells us which source or destination it concerns. A timestamp helps determine freshness.

**03:52.649–04:00.926:** A sequence number can expose repeated or out-of-order messages. Units prevent confusing metres with centimetres.

**04:00.926–04:06.493:** A policy version connects an action or update to the model that produced it.

**04:06.493–04:16.245:** These fields are useful evidence, but fields alone do not authenticate a sender. Security checks must support the claimed identity.

**04:16.245–04:24.095:** Before acting, the receiver needs a policy for rejecting stale, unexpected, or unauthorised commands.

**04:24.095–04:37.093:** Pip is a story name; robot-seven is the device identity used in this demonstration. A receiver must check the identity expected by the protocol, not guess from a friendly label.

### 04:41–05:54 — Inspect three incoming messages

**Content reference:** Chapter 5 — Applications / Networking for a behaviour-based agent

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: ACCEPT / STALE / DUPLICATE.

**04:41.367–04:50.074:** Run the supporting packet-checking example. This is an illustrative receiver design, not a universal network protocol.

**04:50.074–04:56.644:** Our toy receiver expects robot seven, metres as the unit, and policy version three.

**04:56.644–05:04.473:** For this demonstration, it rejects commands older than two hundred milliseconds and sequences already processed.

**05:04.473–05:13.094:** The first message has the expected context, a new sequence, and an age of fifty milliseconds. It passes these checks.

**05:13.094–05:21.651:** The second is six hundred milliseconds old. The receiver rejects it as stale, even if the network eventually delivered it.

**05:21.651–05:30.721:** The third repeats an already processed sequence. The receiver rejects it as a duplicate instead of executing the command twice.

**05:30.721–05:41.667:** Our example assumes authentication was checked elsewhere. It does not implement cryptographic authentication or certify a safety-critical controller.

**05:41.667–05:50.246:** The useful lesson is why delivery alone is insufficient: the receiver must decide whether the message is still meaningful.

### 05:54–06:43 — Match feedback to the original action

**Content reference:** Chapter 5 — Applications / Networking for a behaviour-based agent

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: ACTION 42 / ACTION 43 / FEEDBACK 43.

**05:54.933–05:59.625:** Delayed feedback must be associated with the action that produced it.

**05:59.625–06:08.545:** Suppose action forty-two turns left, and action forty-three moves forward. Their feedback packets arrive in the opposite order.

**06:08.545–06:14.817:** Updating whichever action happened most recently would connect evidence to the wrong decision.

**06:14.817–06:23.737:** Use identifiers and recorded context to match each result with its original state and action before a learning update.

**06:23.737–06:31.395:** If a feedback packet is lost, the evidence is missing. That does not silently mean the reward was zero.

**06:31.395–06:40.315:** This is how networking details can affect the data used by a learning algorithm, even when policy evaluation stays local.

### 06:43–07:31 — Define what an outage means

**Content reference:** Chapter 6 — Strengths & Limitations / Put each computation where it fits

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: LOCAL TASK / SHARED TASK / SAFE STATE.

**06:43.454–06:48.702:** Now inspect the outage condition for our illustrative delivery system.

**06:48.702–06:56.402:** The design must say whether the robot pauses, completes a limited task, or enters another defined state.

**06:56.402–07:03.740:** Continuing safely during a link outage cannot simply be assumed because some computation is local.

**07:03.740–07:12.468:** Consider expiring permissions, missing coordination, conflicting routes, and how the system reconnects after the interruption.

**07:12.468–07:19.422:** Record what happened locally so the shared service can reconcile state when communication returns.

**07:19.422–07:28.961:** The right fallback depends on the task and its hazards. Our tutorial demonstrates the reasoning rather than certifying a physical robot.

### 07:31–08:26 — The feedback packet never arrived

**Content reference:** Chapter 5 — Applications / Networking for a behaviour-based agent

**Teaching / visual direction:** Keep the supplied question legible during the thinking interval; reveal the answer only after the pause. Key visual labels: NO PACKET / MISSING EVIDENCE / NOT ZERO REWARD.

**Learner question:** Missing feedback = reward zero?

**Thinking interval:** 07:46.076–07:52.076. The viewer may pause for longer.

**07:31.976–07:38.781:** Pause and think. The robot performed action forty-two, but its reward packet never arrived.

**07:38.781–07:46.076:** Should the learner record a reward of zero? And should a repeated command be executed again automatically?

**07:52.076–08:00.761:** No to both. Missing evidence is not an observed zero, and a duplicate needs the receiver's defined handling policy.

**08:00.761–08:09.059:** Associate any later feedback with the original action. Decide how long to wait and how to record missing data.

**08:09.059–08:15.373:** Then explain why a timestamp alone does not prove a message came from an authorised sender.

**08:15.373–08:23.202:** Use the packet demonstration to change an age or sequence and predict which validation rule should reject it.

**Expected learning-check result:** No. Missing evidence is not an observed zero.

### 08:26–09:31 — Connect the responsibilities

**Content reference:** Chapter 5 — Applications / Networking for a behaviour-based agent

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: LOCAL LOOP / VALID MESSAGES / MATCHED FEEDBACK.

**08:26.759–08:34.395:** Keep suitable time-critical work local, and use the network for telemetry, coordination, and reviewed updates.

**08:34.395–08:44.851:** Messages need interpretable context and appropriate authentication. Stale or repeated commands must not be treated as automatically valid.

**08:44.851–08:53.427:** Delayed learning feedback belongs to its original action. Lost evidence must not silently become zero reward.

**08:53.427–09:00.082:** Decide which responsibility belongs on the robot, at a nearby gateway, or in the cloud.

**09:00.082–09:08.661:** Finally, distinguish a fixed reactive rule, a deployed learned policy, and an algorithm currently updating that policy.

**09:08.661–09:16.770:** Draw the local and shared responsibilities, then explain your outage behaviour before calling the architecture complete.

**09:16.770–09:27.631:** A message can be perfectly formatted and still be too late, duplicated, or unauthorised. Meaning depends on the receiver's state and the surrounding checks.

### 09:31–10:00 — Pip completes the shift

**Content reference:** Chapter 5 — Applications / Networking for a behaviour-based agent

**Teaching / visual direction:** Resolve the opening problem and use a concise Blue Impulse end title, returning to the opening composition. Key visual labels: BLUE IMPULSE / FOLLOW THE SIGNAL.

**09:31.976–09:35.901:** Pip's small problem now has an explanation you can test.

**09:35.901–09:41.959:** Use Chapter 5, Applications, and the named subtopics to revisit the reasoning.

**09:41.959–09:51.412:** The tutorial guide includes the full teaching steps and the checked practice answers. Run the supporting demonstration and change one input.

**09:51.412–09:56.915:** Blue Impulse. Follow the signal, predict the result, and check your explanation.

## Supporting demonstration and limits


The toy receiver expects device ID robot-7, units m, policy_version 3, age at most 200 ms, and a sequence greater than the last accepted sequence. Start at last accepted sequence 41. Assume authentication was checked upstream; a Boolean in this demonstration is not cryptography.

| Packet | Sequence | Age | Decision | Last accepted sequence after decision |
| --- | --- | --- | --- | --- |
| A | 42 | 50 ms | ACCEPT | 42 |
| B | 43 | 600 ms | REJECT STALE | 42 |
| C | 42 | 60 ms | REJECT DUPLICATE | 42 |

Only accepted messages advance accepted-sequence state. Delivery, correct format and authenticity do not by themselves establish that a command is fresh and suitable.

**Practice:** Action 42 occurred but its reward packet never arrived. Is the observed reward zero? Should a repeated command automatically execute again?

**Checked answer:** No to both. Missing evidence is not an observed zero. Record missing data explicitly, associate any later feedback with its original transition, and follow the defined receiver policy for duplicates. Real designs also need authenticated identity, appropriate clock/session assumptions and a defined fallback.
