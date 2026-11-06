# Video 02: How hardware enables AI

Duration: 09:04. Video: `BlueImpulse_Video02_How_Hardware_Enables_AI.mp4`.

## Learning objectives

- Trace sensing to action
- Explain memory and processing roles
- Diagnose a hardware bottleneck

## 00:00–00:36 · What gives an AI decision a body?

Study guide page 35. Visual: hook.

Have you ever wondered how a prediction inside a computer becomes a robot moving across a room?

A model cannot see, remember, calculate, or turn a wheel without physical components doing those jobs.

Today we will follow one observation through the hardware, all the way to an action and new feedback.

Open the Blue Impulse study guide at page thirty-five, Hardware gives software a body.

Keep page forty-four nearby too. It explains why a control signal and motor power are different things.


## 00:36–01:11 · Today’s route

Study guide page 35. Visual: objectives.

You will trace the sensing, memory, processing, and actuation path of a small robot.

You will explain why memory movement can limit a fast processor and what a pipeline actually improves.

You will also choose hardware by its job, rather than assuming every AI system needs the same chip.

Welcome to the tutorial on how hardware enables AI by Blue Impulse.

We are using the guide as our lesson: read the pictured excerpts, then follow the demonstrations beside them.


## 01:11–01:56 · Follow the physical path

Study guide page 35. Visual: book.

Page thirty-five groups hardware by the job it performs: input, processing, output, and storage.

For our robot, the sensor supplies observations. Memory holds inputs, model parameters, and working results.

The processor evaluates the program or model, and an output communicates the resulting decision.

If the robot needs to move, an actuator must turn that decision into physical motion.

Notice that one device can have multiple roles. A touchscreen both displays output and senses input.

The diagram is a chain of responsibilities, not a claim that every box must be a separate physical chip.


## 01:56–02:38 · Use the kitchen analogy

Study guide page 36. Visual: compare.

Use a kitchen to remember the memory hierarchy on page thirty-six.

Registers are like the tiny workspace immediately in your hands. Cache keeps useful ingredients close to the cook.

Main memory is the larger active workbench, while persistent storage is more like the pantry.

The analogy is about access and capacity, not a literal map of computer components.

A huge pantry does not help if ingredients arrive too slowly. Similarly, a processor can wait for data.

Capacity asks how much fits. Memory bandwidth asks how quickly data can move. These are different questions.


## 02:38–03:28 · The processor may be waiting

Study guide page 36. Visual: book.

Look at the final paragraph on page thirty-six. Model weights, inputs, and intermediate results must fit somewhere.

When memory bandwidth is insufficient, a fast processor may spend time waiting instead of doing useful arithmetic.

Adding storage capacity alone does not automatically remove a memory-transfer bottleneck.

The table also distinguishes cache, main RAM, and secondary storage. They are not interchangeable names for one resource.

Both static RAM and dynamic RAM are volatile, although their circuits and refresh requirements differ.

For this tutorial, focus on the system question: is the limiting factor how much fits, or how quickly it arrives?


## 03:28–04:16 · Match the processor to the work

Study guide page 46. Visual: compare.

Now compare the processing roles in the table on page forty-six.

A CPU handles general control, branches, and diverse tasks. A GPU can accelerate suitable parallel arithmetic workloads.

Specialised accelerators can efficiently perform supported tensor operations, but their benefits depend on the actual workload.

Simple tabular reinforcement learning can run on an ordinary CPU. AI does not always require a GPU.

Training changes model parameters. Inference uses an existing model to produce an output.

A model can be trained on a large server and deployed on a smaller device if the deployment requirements fit.


## 04:16–05:19 · Overlap work, increase throughput

Study guide page 39. Visual: pipeline-demo.

Page thirty-nine uses laundry to explain pipelining. One load can dry while a later load is washing.

In our simplified processor, the stages are fetch, decode, execute, and write.

Instruction one enters fetch in cycle one. In cycle two, it decodes while instruction two enters fetch.

Keep stepping forward. The instructions occupy different stages, so several instructions make progress during the same cycle.

After the pipeline fills, this ideal example completes one instruction per cycle, assuming no stalls.

It does not make an individual four-stage instruction take just one cycle from start to finish.

Real pipelines can pause for dependencies, uncertain branches, or shared resources. The guide names these as hazards.

Use the included Python table to compare completion cycles rather than relying only on the moving picture.


## 05:19–06:06 · A signal is not motor power

Study guide page 44. Visual: book.

Turn to page forty-four and trace the environmental control loop.

An analogue sensor may need an analogue-to-digital converter. Many sensors already provide digital measurements.

The processor evaluates a decision, then a driver or power stage supplies what the actuator needs.

Some actuators use a digital interface or pulse-width modulation. They do not all require a digital-to-analogue converter.

Pulse-width modulation is timed switching, not the same thing as converting a value into an analogue voltage.

A control signal can tell a motor what to do without being able to supply the current that moves it.


## 06:06–06:50 · Close the loop

Study guide page 44. Visual: diagram.

Imagine the robot detects an obstacle, selects a turn, and sends a command to its motor driver.

The driver powers the motor, the wheels move, and the sensor measures the changed situation.

That final measurement closes the feedback loop. The command alone does not prove the movement succeeded.

A wheel might slip, a sensor might be noisy, or the actuator might reach a mechanical limit.

The book also separates monitoring from control. Displaying a measurement monitors; changing the environment adds control.

This loop can use a fixed rule or a learned policy. The hardware path alone does not tell you which.


## 06:50–07:43 · Will a faster GPU fix this?

Study guide page 86. Visual: question.

Pause and diagnose a system. Its processor repeatedly waits for data, and its motor driver cannot supply enough current.

Would replacing the processor with a faster GPU solve both problems? Think before the answer appears.

**[Pause for 6 seconds. Keep the answer hidden.]**

No. Memory movement and actuator power are separate limits that a new GPU does not automatically remove.

Measure the path, identify the limiting stage, and match the intervention to that evidence.

Page eighty-six broadens the discussion to power, heat, memory, and physical constraints.

An advertised arithmetic rate describes one capability. It is not a complete measurement of the robot's useful performance.

On-screen question: Waiting for data + insufficient motor current

Answer after the pause: Fix the memory path and power stage.


## 07:43–08:34 · Hardware enables every step

Study guide page 46. Visual: recap.

Recap the path from page thirty-five: observations enter, memory holds information, processing evaluates it, and outputs communicate or act.

Page thirty-six explains why memory capacity and bandwidth both matter. Page thirty-nine separates pipeline throughput from instruction latency.

Page forty-four explains conversion, control signals, and actuator power. Page forty-six compares processing strengths.

Choose hardware by the workload, deadlines, power budget, and physical task.

To check your understanding, draw a robot's path from camera to wheel, and label one possible bottleneck at each stage.

Then explain why a more powerful chip does not, by itself, create a learning algorithm.


## 08:35–09:04 · Blue Impulse study guide

Study guide page 1. Visual: credits.

This tutorial used the Blue Impulse study guide, pages thirty-five, thirty-six, thirty-nine, forty-four, forty-six, and eighty-six.

The original book cover is shown on screen as our credit.

The companion tutorial PDF and pipeline demonstration help you repeat the lesson without replaying every explanation.

Blue Impulse study guide. Trace the whole system before choosing the hardware.
