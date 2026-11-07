# Video 02 — How hardware enables AI: narration script and teaching outline

**Video file:** BlueImpulse_Video02_How_Hardware_Enables_AI.mp4  
**Viewing position:** 2 of 5  
**Duration:** 10:00 (600 seconds)  
**Format:** MP4, 1920 × 1080, 60 fps  
**File size:** 48,161,007 bytes (48.16 MB)

**Prerequisites:** Know that software executes instructions and stores data. Chapter 1 — The Fundamentals supplies this foundation; Video 05 is an optional preparatory lesson.

**Learning goals:**

- Trace sensing to action
- Explain memory and processing roles
- Diagnose a hardware bottleneck

**Chapter and subtopic connections:**

- Chapter 3 — Hardware / Hardware gives software a body
- Chapter 3 — Hardware / Memory: capacity versus speed
- Chapter 3 — Hardware / The hardware behind an AI model
- Chapter 3 — Hardware / Overlap work with a pipeline
- Chapter 3 — Hardware / Sense, decide, act, sense again
- Chapter 6 — Strengths & Limitations / Four physical budgets

**Apply in the learning system:** Complete ACT-03 in the Study Guide / Markdown activity file. Use Test Bank questions TF09–TF12, MC09–MC12 and OE03 for review. The six-chapter PPT deck introduces the same chapter concepts through classroom discussion.

**Optional interactive companion:** ROVERLAB lets you apply these ideas by building a robot, connecting its network and comparing stimulus-response rules. Play at https://roverlab-blue-impulse.vercel.app and use the ROVERLAB activity in the Study Guide. It is a simplified rule-and-feedback model, not a neural network or the numerical Q-learning algorithm taught in Video 01.

**Materials:** Paper and a calculator are sufficient. The optional supporting Python demonstration uses Python 3.9 or newer with no third-party packages or account.

```sh
python3 supporting/BlueImpulse_Demonstrations.py --topic hardware
```

## Chapter timestamps and teaching route

| Time | Teaching step | Chapter / subtopic |
| --- | --- | --- |
| 00:00–00:28 | Pip’s plan is waiting | Chapter 3 — Hardware / Hardware gives software a body |
| 00:28–01:04 | Today’s route | Chapter 3 — Hardware / Hardware gives software a body |
| 01:04–01:52 | Follow the physical path | Chapter 3 — Hardware / Hardware gives software a body |
| 01:52–02:35 | Use the kitchen analogy | Chapter 3 — Hardware / Memory: capacity versus speed |
| 02:35–03:47 | The processor may be waiting | Chapter 3 — Hardware / Memory: capacity versus speed |
| 03:47–04:39 | Match the processor to the work | Chapter 3 — Hardware / The hardware behind an AI model |
| 04:39–05:45 | Overlap work, increase throughput | Chapter 3 — Hardware / Overlap work with a pipeline |
| 05:45–06:49 | A signal is not motor power | Chapter 3 — Hardware / Sense, decide, act, sense again |
| 06:49–07:35 | Close the loop | Chapter 3 — Hardware / Sense, decide, act, sense again |
| 07:35–08:32 | Will a faster GPU fix this? | Chapter 6 — Strengths & Limitations / Four physical budgets |
| 08:32–09:32 | Hardware enables every step | Chapter 3 — Hardware / The hardware behind an AI model |
| 09:32–10:00 | Pip completes the shift | Chapter 3 — Hardware / Hardware gives software a body |

## Using this script

The following narration is the exact measured cue text for the revised recording. Cue timestamps refer to the video timeline; small gaps include intentional thinking time and transition space. The voice is synthetic (Kokoro ONNX, am_michael), not a recording of a student. The full teaching outline states the purpose, visual focus and learner action alongside the words spoken.

### 00:00–00:28 — Pip’s plan is waiting

**Content reference:** Chapter 3 — Hardware / Hardware gives software a body

**Teaching / visual direction:** Keep Pip’s problem visible while the opening question establishes why the concept matters. Key visual labels: PLAN READY / DATA WAITING / WHEELS WAIT.

**00:00.150–00:02.965:** Pip has a plan. The wheels still wait.

**00:02.965–00:08.703:** A sensor stream reaches our campus rover faster than its computer can process it.

**00:08.703–00:15.743:** A clever decision still needs memory, processing, connections, and enough power to become an action.

**00:15.743–00:20.542:** Have you ever wondered what gives an AI decision a physical body?

**00:20.542–00:26.707:** Chapter three, Hardware, will help us follow the whole path and find the actual bottleneck.

### 00:28–01:04 — Today’s route

**Content reference:** Chapter 3 — Hardware / Hardware gives software a body

**Teaching / visual direction:** Reveal the learning goals in the order spoken, then retain a small progress cue. Key visual labels: HARDWARE PATH / MEMORY / PIPELINE.

**00:28.846–00:35.245:** You will trace the sensing, memory, processing, and actuation path of a small robot.

**00:35.245–00:42.455:** You will explain why memory movement can limit a fast processor and what a pipeline actually improves.

**00:42.455–00:49.622:** You will also choose hardware by its job, rather than assuming every AI system needs the same chip.

**00:49.622–00:54.998:** Welcome to the tutorial on how hardware enables AI by Blue Impulse.

**00:54.998–01:01.482:** Follow each part of the diagram, then predict what happens when that part becomes the bottleneck.

### 01:04–01:52 — Follow the physical path

**Content reference:** Chapter 3 — Hardware / Hardware gives software a body

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: INPUT / PROCESS / OUTPUT / STORE.

**01:04.324–01:11.897:** The subtopic Hardware gives software a body groups hardware by input, processing, output, and storage.

**01:11.897–01:20.195:** For our robot, the sensor supplies observations. Memory holds inputs, model parameters, and working results.

**01:20.195–01:27.127:** The processor evaluates the program or model, and an output communicates the resulting decision.

**01:27.127–01:33.271:** If the robot needs to move, an actuator must turn that decision into physical motion.

**01:33.271–01:40.929:** Notice that one device can have multiple roles. A touchscreen both displays output and senses input.

**01:40.929–01:48.544:** The diagram is a chain of responsibilities, not a claim that every box must be a separate physical chip.

### 01:52–02:35 — Use the kitchen analogy

**Content reference:** Chapter 3 — Hardware / Memory: capacity versus speed

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: CACHE / RAM / STORAGE.

**01:52.324–01:56.121:** Use a kitchen to remember the memory hierarchy.

**01:56.121–02:03.419:** Registers are like the tiny workspace immediately in your hands. Cache keeps useful ingredients close to the cook.

**02:03.419–02:10.352:** Main memory is the larger active workbench, while persistent storage is more like the pantry.

**02:10.352–02:16.495:** The analogy is about access and capacity, not a literal map of computer components.

**02:16.495–02:24.601:** A huge pantry does not help if ingredients arrive too slowly. Similarly, a processor can wait for data.

**02:24.601–02:32.579:** Capacity asks how much fits. Memory bandwidth asks how quickly data can move. These are different questions.

### 02:35–03:47 — The processor may be waiting

**Content reference:** Chapter 3 — Hardware / Memory: capacity versus speed

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: WEIGHTS / INPUTS / INTERMEDIATE RESULTS.

**02:35.628–02:43.567:** Model weights, inputs, and intermediate results must fit somewhere. A processor cannot use data that has not arrived.

**02:43.567–02:51.655:** When memory bandwidth is insufficient, a fast processor may spend time waiting instead of doing useful arithmetic.

**02:51.655–02:58.545:** Adding storage capacity alone does not automatically remove a memory-transfer bottleneck.

**02:58.545–03:07.977:** The table also distinguishes cache, main RAM, and secondary storage. They are not interchangeable names for one resource.

**03:07.977–03:15.998:** Both static RAM and dynamic RAM are volatile, although their circuits and refresh requirements differ.

**03:15.998–03:23.915:** For this tutorial, focus on the system question: is the limiting factor how much fits, or how quickly it arrives?

**03:23.915–03:34.051:** Imagine the processor as a cook waiting for ingredients. Hiring a faster cook does not shorten the time a missing ingredient spends in transit.

**03:34.051–03:42.438:** Likewise, a faster arithmetic unit can still spend time waiting for memory. Measure that waiting before choosing the upgrade.

### 03:47–04:39 — Match the processor to the work

**Content reference:** Chapter 3 — Hardware / The hardware behind an AI model

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: CPU / GPU / ACCELERATOR.

**03:47.628–03:52.556:** Now compare the processor roles in the subtopic Hardware for AI.

**03:52.556–04:02.692:** A CPU handles general control, branches, and diverse tasks. A GPU can accelerate suitable parallel arithmetic workloads.

**04:02.692–04:11.484:** Specialised accelerators can efficiently perform supported tensor operations, but their benefits depend on the actual workload.

**04:11.484–04:20.934:** Simple tabular reinforcement learning can run on an ordinary CPU. AI does not always require a GPU.

**04:20.934–04:27.632:** Training changes model parameters. Inference uses an existing model to produce an output.

**04:27.632–04:35.610:** A model can be trained on a large server and deployed on a smaller device if the deployment requirements fit.

### 04:39–05:45 — Overlap work, increase throughput

**Content reference:** Chapter 3 — Hardware / Overlap work with a pipeline

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: FETCH / DECODE / EXECUTE / WRITE.

**04:39.280–04:45.680:** Use laundry to understand pipelining. One load can dry while a later load is washing.

**04:45.680–04:51.503:** In our simplified processor, the stages are fetch, decode, execute, and write.

**04:51.503–04:59.460:** Instruction one enters fetch in cycle one. In cycle two, it decodes while instruction two enters fetch.

**04:59.460–05:08.081:** Keep stepping forward. The instructions occupy different stages, so several instructions make progress during the same cycle.

**05:08.081–05:15.995:** After the pipeline fills, this ideal example completes one instruction per cycle, assuming no stalls.

**05:15.995–05:23.120:** It does not make an individual four-stage instruction take just one cycle from start to finish.

**05:23.120–05:32.850:** Real pipelines can pause for dependencies, uncertain branches, or shared resources. These hazards limit the ideal improvement.

**05:32.850–05:40.530:** Use the included Python table to compare completion cycles rather than relying only on the moving picture.

### 05:45–06:49 — A signal is not motor power

**Content reference:** Chapter 3 — Hardware / Sense, decide, act, sense again

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: SENSOR / CONVERSION / CONTROL / ACTUATOR.

**05:45.541–05:55.251:** Trace the environmental control loop: measurement becomes a signal, processing chooses an output, and an actuator changes the environment.

**05:55.251–06:03.677:** An analogue sensor may need an analogue-to-digital converter. Many sensors already provide digital measurements.

**06:03.677–06:10.908:** The processor evaluates a decision, then a driver or power stage supplies what the actuator needs.

**06:10.908–06:20.319:** Some actuators use a digital interface or pulse-width modulation. They do not all require a digital-to-analogue converter.

**06:20.319–06:28.681:** Pulse-width modulation is timed switching, not the same thing as converting a value into an analogue voltage.

**06:28.681–06:35.549:** A control signal can tell a motor what to do without being able to supply the current that moves it.

**06:35.549–06:45.088:** Pip's control signal communicates what the motor driver should do. The energy that turns a loaded wheel still comes through the power system.

### 06:49–07:35 — Close the loop

**Content reference:** Chapter 3 — Hardware / Sense, decide, act, sense again

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: MEASURE / COMPARE / CHANGE / REPEAT.

**06:49.715–06:57.032:** Imagine the robot detects an obstacle, selects a turn, and sends a command to its motor driver.

**06:57.032–07:03.645:** The driver powers the motor, the wheels move, and the sensor measures the changed situation.

**07:03.645–07:10.705:** That final measurement closes the feedback loop. The command alone does not prove the movement succeeded.

**07:10.705–07:17.361:** A wheel might slip, a sensor might be noisy, or the actuator might reach a mechanical limit.

**07:17.361–07:24.955:** Monitoring and control differ. Displaying a measurement monitors; changing the environment adds control.

**07:24.955–07:32.058:** This loop can use a fixed rule or a learned policy. The hardware path alone does not tell you which.

### 07:35–08:32 — Will a faster GPU fix this?

**Content reference:** Chapter 6 — Strengths & Limitations / Four physical budgets

**Teaching / visual direction:** Keep the supplied question legible during the thinking interval; reveal the answer only after the pause. Key visual labels: FASTER GPU? / MEMORY WAIT / MEASURE FIRST.

**Learner question:** Waiting for data + insufficient motor current

**Thinking interval:** 07:52.057–07:58.057. The viewer may pause for longer.

**07:35.628–07:44.442:** Pause and diagnose a system. Its processor repeatedly waits for data, and its motor driver cannot supply enough current.

**07:44.442–07:52.057:** Would replacing the processor with a faster GPU solve both problems? Think before the answer appears.

**07:58.057–08:06.227:** No. Memory movement and actuator power are separate limits that a new GPU does not automatically remove.

**08:06.227–08:12.541:** Measure the path, identify the limiting stage, and match the intervention to that evidence.

**08:12.541–08:18.898:** Chapter six, Strengths and Limitations, adds power, heat, memory, and physical constraints.

**08:18.898–08:28.116:** An advertised arithmetic rate describes one capability. It is not a complete measurement of the robot's useful performance.

**Expected learning-check result:** Fix the memory path and power stage.

### 08:32–09:32 — Hardware enables every step

**Content reference:** Chapter 3 — Hardware / The hardware behind an AI model

**Teaching / visual direction:** Follow the spoken explanation with concise labels and the corresponding diagram state; transform the existing objects into the next scene. Key visual labels: DATA / COMPUTE / POWER / ACTION.

**08:32.498–08:42.122:** Trace Pip's whole path: observations enter, memory holds information, processing evaluates it, and outputs communicate or act.

**08:42.122–08:49.950:** Memory capacity and bandwidth both matter. Pipeline throughput is different from the latency of one instruction.

**08:49.950–08:57.352:** Conversion, control signals, actuator power, and processor strengths all affect what the system can do.

**08:57.352–09:02.706:** Choose hardware by the workload, deadlines, power budget, and physical task.

**09:02.706–09:10.858:** To check your understanding, draw a robot's path from camera to wheel, and label one possible bottleneck at each stage.

**09:10.858–09:17.002:** Then explain why a more powerful chip does not, by itself, create a learning algorithm.

**09:17.002–09:27.970:** An upgrade should target the constrained part of the task. Check the input rate, memory traffic, compute load, and actuator response as a connected system.

### 09:32–10:00 — Pip completes the shift

**Content reference:** Chapter 3 — Hardware / Hardware gives software a body

**Teaching / visual direction:** Resolve the opening problem and use a concise Blue Impulse end title, returning to the opening composition. Key visual labels: BLUE IMPULSE / FOLLOW THE SIGNAL.

**09:32.498–09:36.422:** Pip's small problem now has an explanation you can test.

**09:36.422–09:42.011:** Use Chapter 3, Hardware, and the named subtopics to revisit the reasoning.

**09:42.011–09:51.464:** The tutorial guide includes the full teaching steps and the checked practice answers. Run the supporting demonstration and change one input.

**09:51.464–09:56.968:** Blue Impulse. Follow the signal, predict the result, and check your explanation.

## Supporting demonstration and limits


Assume four equal one-cycle stages: F = fetch, D = decode, E = execute, W = write-back. Instructions are independent and no stage stalls. Record the occupied stage in each cycle:

| Instruction | Cycle 1 | Cycle 2 | Cycle 3 | Cycle 4 | Cycle 5 | Cycle 6 |
| --- | --- | --- | --- | --- | --- | --- |
| I1 | F | D | E | W | — | — |
| I2 | — | F | D | E | W | — |
| I3 | — | — | F | D | E | W |

Completion cycles are 4, 5 and 6. Three instructions finish in six cycles, rather than twelve sequential stage cycles. Each instruction still traverses four stages: pipeline throughput and individual latency are different.

**Practice:** The processor repeatedly waits for data, and a motor driver cannot supply enough current. Does a faster GPU fix both problems?

**Checked answer:** No. Memory movement and actuator power are distinct bottlenecks. Measure the limiting path, improve the memory transfer or working set as appropriate, and size the driver/power system for the actuator. A processor upgrade alone does not establish either fix.
