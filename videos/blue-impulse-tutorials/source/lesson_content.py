"""Narration and teaching direction. Page references target the frozen 96-page guide.

Each non-empty narration line is a complete caption cue, synthesized separately.
Cue timestamps therefore come from measured audio, never evenly spread words.
"""

def scene(key, kind, title, page, narration, **visual):
    return dict(key=key, kind=kind, title=title, page=page,
                cues=[s.strip() for s in narration.strip().splitlines() if s.strip()], **visual)


LESSONS = [
 dict(number=1, slug="Basic_Reinforcement_Learning", title="Basic reinforcement learning",
      pages=[24,25,26,27,28,31], objectives=["Name the learning loop", "Balance exploration and exploitation", "Calculate one Q-value update"],
      scenes=[
 scene("hook", "hook", "How does a rover learn a route?", 25, """
Have you ever wondered how a rover could learn a useful route without someone writing every turn?
Imagine a simulated rover choosing between two paths, trying moves, and receiving points for the outcomes.
The important question is how that experience changes its next decision.
Keep your Blue Impulse study guide open at page twenty-five. We will work directly through the book.
By the end, you will calculate a learning update yourself and explain what the result actually means.
""", hero="A route learned from experience", diagram="rover"),
 scene("welcome", "objectives", "Today’s route", 25, """
Today you will identify an agent, an environment, a state, an action, a reward, and a policy.
You will compare exploration with exploitation, then work through the numerical example on page twenty-eight.
Welcome to the tutorial on basic reinforcement learning by Blue Impulse.
Have paper ready for one calculation. The tutorial PDF includes the same worked steps and practice question.
Treat our rover as an illustration. We are explaining a learning method, not claiming every real rover learns this way.
"""),
 scene("loop", "book", "Follow the learning loop", 25, """
Look at the diagram on page twenty-five, titled One interaction at time t.
The agent selects an action. The environment changes and returns the next state and a reward.
The learning algorithm uses that experience to improve the policy, which is the strategy for choosing actions.
For our grid, the state could be the current square, and an action could be moving right.
The reward is a number associated with the result. It is feedback, not a complete instruction manual.
Notice the return arrow. Learning depends on connecting an action to what happened after it.
""", block=1, quote="The objective is usually expected cumulative reward, not just the next reward."),
 scene("distinctions", "compare", "Reward, policy, value", 26, """
Page twenty-six separates three ideas that are easy to confuse: reward, policy, and value.
Think of a journey. The reward scores an outcome now, while the policy chooses the next move.
A value estimate predicts how much return a choice may lead to, including later outcomes.
A route with a small cost now can still be worthwhile if it reaches a better destination.
That is why choosing the biggest immediate reward is not always the best long-term decision.
The book also warns that poorly chosen rewards can encourage shortcuts that miss the designer's real goal.
""", labels=["Reward: score now", "Policy: choose an action", "Value: estimate return"]),
 scene("explore", "book", "The restaurant analogy", 27, """
Turn to page twenty-seven and use the book's restaurant analogy.
Ordering the dish you currently believe is best is exploitation. Trying a different dish is exploration.
Exploration gathers information because your current estimates might be wrong.
In the book's epsilon-greedy example, epsilon is zero point one, giving a ten percent exploration probability.
Otherwise, the agent chooses an action with the highest current Q value.
These percentages describe probabilities over choices, not a promise that exactly one out of every ten choices explores.
In a real physical system, exploration also needs safety constraints. A simulation is a useful place to experiment.
""", block=1, quote="Early estimates can be wrong, so always exploiting can lock an agent into an inferior policy."),
 scene("think", "question", "Is the familiar route certainly best?", 27, """
Pause and think. One route has worked twice. Another route has never been tried.
Does that prove the first route is better? Take a few seconds before we reveal the answer.
No. The evidence is incomplete, so the familiar route is not certainly the better one.
Exploration may improve the estimate, but it has a cost. The design must balance information and performance.
Write one sentence explaining why exploitation uses estimated future return, rather than only the next reward.
""", prompt="Two successes versus an untried route: proof?", answer="No. The evidence is incomplete.", pause_after=1, pause=5),
 scene("qintro", "book", "What is a Q value?", 28, """
Now open page twenty-eight, Update a Q value. Q associates a state and an action with an estimated return.
The book calls Q-learning model-free because it does not require a supplied model of environment transitions.
Model-free does not mean memory-free. The estimates still live in a table or another representation.
The update combines an old estimate with a target derived from new experience.
Alpha controls how far the estimate moves toward that target. Gamma discounts the future-value contribution.
We will use exactly the numbers in the guide, so you can check each line against the page.
""", block=0, quote="Alpha controls the size of an update. Gamma discounts future rewards."),
 scene("qdemo", "q-demo", "Work through the book’s update", 28, """
Start with an old Q value of two and a learning rate, alpha, of zero point five.
The reward is one, gamma is zero point nine, and the best next Q value is four.
First calculate the target: one plus zero point nine times four. The target is four point six.
Next subtract the old estimate. Four point six minus two gives an error of two point six.
Multiply that error by alpha. Half of two point six is one point three.
Finally add the change to the old value. Two plus one point three gives three point three.
Watch the estimate move halfway toward the target. That halfway movement is what alpha equals one half means here.
The supporting Python file repeats this calculation and prints every intermediate value for you to inspect.
""", values={"old":2,"alpha":0.5,"reward":1,"gamma":0.9,"next":4,"target":4.6,"error":2.6,"change":1.3,"new":3.3}),
 scene("interpret", "book", "A better estimate, not a proof", 28, """
Return to the final paragraph on page twenty-eight. This experience raised the estimate from two to three point three.
It did not prove that the action is always best. One observation is not a reliable policy.
Repeated experience, an appropriate learning schedule, and enough exploration are still important.
There is also a special case: when the next state is terminal, the future-value term is zero.
That prevents the calculation from inventing future reward after the episode has ended.
Compare these two ideas: updating an estimate from evidence, and guaranteeing the outcome of the next action.
They are different claims, and only the first follows from our calculation.
""", block=3, quote="It did not prove the action is always best."),
 scene("practice", "question", "Try a terminal state", 28, """
Your turn. Keep the old value at two, alpha at one half, and the reward at one.
Make the next state terminal. What is the new Q value? Pause the video if you need more time.
The future contribution is zero, so the target is one. The error is one minus two, or negative one.
Half that error is negative one half. Add it to two, giving a new value of one point five.
The estimate falls because the observed target is lower. A learning update can decrease a value as well as increase it.
""", prompt="Terminal state: old Q = 2, α = 0.5, reward = 1", answer="New Q = 2 + 0.5 × (1 − 2) = 1.5", pause_after=1, pause=6),
 scene("recap", "recap", "Experience changes estimates", 31, """
Let's recap using pages twenty-five through twenty-eight. The agent acts, receives feedback, and learns a policy from experience.
Reward scores an outcome. Value estimates return. Exploration improves information, while exploitation uses the best current estimates.
Our worked Q update produced three point three, and our terminal-state practice produced one point five.
Page thirty-one adds an important distinction: running an already learned policy is not the same as training it online.
A fixed sensor-response rule can control a machine without learning at all.
Before moving on, explain the loop to someone else and run the included calculation with one changed reward.
""", labels=["Observe → act → feedback", "Explore and exploit", "Q update: 2 → 3.3", "Deployment is not necessarily learning"]),
 scene("credits", "credits", "Blue Impulse study guide", 1, """
This tutorial was taught from the Blue Impulse study guide, especially pages twenty-four to twenty-eight and thirty-one.
The cover on screen is the original cover of your book.
Use the companion tutorial PDF, narration script, subtitles, and Python demonstration to practise at your own pace.
Blue Impulse study guide. Learn the reasoning, then test it with an example.
""")]),
 dict(number=2, slug="How_Hardware_Enables_AI", title="How hardware enables AI",
      pages=[35,36,39,44,46,86], objectives=["Trace sensing to action", "Explain memory and processing roles", "Diagnose a hardware bottleneck"],
      scenes=[
 scene("hook", "hook", "What gives an AI decision a body?", 35, """
Have you ever wondered how a prediction inside a computer becomes a robot moving across a room?
A model cannot see, remember, calculate, or turn a wheel without physical components doing those jobs.
Today we will follow one observation through the hardware, all the way to an action and new feedback.
Open the Blue Impulse study guide at page thirty-five, Hardware gives software a body.
Keep page forty-four nearby too. It explains why a control signal and motor power are different things.
""", hero="From an observation to an action", diagram="hardware"),
 scene("welcome", "objectives", "Today’s route", 35, """
You will trace the sensing, memory, processing, and actuation path of a small robot.
You will explain why memory movement can limit a fast processor and what a pipeline actually improves.
You will also choose hardware by its job, rather than assuming every AI system needs the same chip.
Welcome to the tutorial on how hardware enables AI by Blue Impulse.
We are using the guide as our lesson: read the pictured excerpts, then follow the demonstrations beside them.
"""),
 scene("roles", "book", "Follow the physical path", 35, """
Page thirty-five groups hardware by the job it performs: input, processing, output, and storage.
For our robot, the sensor supplies observations. Memory holds inputs, model parameters, and working results.
The processor evaluates the program or model, and an output communicates the resulting decision.
If the robot needs to move, an actuator must turn that decision into physical motion.
Notice that one device can have multiple roles. A touchscreen both displays output and senses input.
The diagram is a chain of responsibilities, not a claim that every box must be a separate physical chip.
""", block=1, quote="More powerful hardware can increase capacity or speed, but does not itself create a learning algorithm."),
 scene("kitchen", "compare", "Use the kitchen analogy", 36, """
Use a kitchen to remember the memory hierarchy on page thirty-six.
Registers are like the tiny workspace immediately in your hands. Cache keeps useful ingredients close to the cook.
Main memory is the larger active workbench, while persistent storage is more like the pantry.
The analogy is about access and capacity, not a literal map of computer components.
A huge pantry does not help if ingredients arrive too slowly. Similarly, a processor can wait for data.
Capacity asks how much fits. Memory bandwidth asks how quickly data can move. These are different questions.
""", labels=["Registers: immediately available", "Cache: frequently used copies", "RAM: active work", "Storage: persistent data"]),
 scene("memory", "book", "The processor may be waiting", 36, """
Look at the final paragraph on page thirty-six. Model weights, inputs, and intermediate results must fit somewhere.
When memory bandwidth is insufficient, a fast processor may spend time waiting instead of doing useful arithmetic.
Adding storage capacity alone does not automatically remove a memory-transfer bottleneck.
The table also distinguishes cache, main RAM, and secondary storage. They are not interchangeable names for one resource.
Both static RAM and dynamic RAM are volatile, although their circuits and refresh requirements differ.
For this tutorial, focus on the system question: is the limiting factor how much fits, or how quickly it arrives?
""", block=2, quote="Capacity answers “how much fits?” Bandwidth answers “how quickly can it move?”"),
 scene("chips", "compare", "Match the processor to the work", 46, """
Now compare the processing roles in the table on page forty-six.
A CPU handles general control, branches, and diverse tasks. A GPU can accelerate suitable parallel arithmetic workloads.
Specialised accelerators can efficiently perform supported tensor operations, but their benefits depend on the actual workload.
Simple tabular reinforcement learning can run on an ordinary CPU. AI does not always require a GPU.
Training changes model parameters. Inference uses an existing model to produce an output.
A model can be trained on a large server and deployed on a smaller device if the deployment requirements fit.
""", labels=["CPU: control and varied work", "GPU: suitable parallel arithmetic", "Accelerator: supported operations"]),
 scene("pipeline", "pipeline-demo", "Overlap work, increase throughput", 39, """
Page thirty-nine uses laundry to explain pipelining. One load can dry while a later load is washing.
In our simplified processor, the stages are fetch, decode, execute, and write.
Instruction one enters fetch in cycle one. In cycle two, it decodes while instruction two enters fetch.
Keep stepping forward. The instructions occupy different stages, so several instructions make progress during the same cycle.
After the pipeline fills, this ideal example completes one instruction per cycle, assuming no stalls.
It does not make an individual four-stage instruction take just one cycle from start to finish.
Real pipelines can pause for dependencies, uncertain branches, or shared resources. The guide names these as hazards.
Use the included Python table to compare completion cycles rather than relying only on the moving picture.
""", stages=["Fetch","Decode","Execute","Write"], instructions=3),
 scene("sensor", "book", "A signal is not motor power", 44, """
Turn to page forty-four and trace the environmental control loop.
An analogue sensor may need an analogue-to-digital converter. Many sensors already provide digital measurements.
The processor evaluates a decision, then a driver or power stage supplies what the actuator needs.
Some actuators use a digital interface or pulse-width modulation. They do not all require a digital-to-analogue converter.
Pulse-width modulation is timed switching, not the same thing as converting a value into an analogue voltage.
A control signal can tell a motor what to do without being able to supply the current that moves it.
""", block=1, quote="A motor driver or power stage supplies the current needed to move a motor or operate a valve."),
 scene("feedback", "diagram", "Close the loop", 44, """
Imagine the robot detects an obstacle, selects a turn, and sends a command to its motor driver.
The driver powers the motor, the wheels move, and the sensor measures the changed situation.
That final measurement closes the feedback loop. The command alone does not prove the movement succeeded.
A wheel might slip, a sensor might be noisy, or the actuator might reach a mechanical limit.
The book also separates monitoring from control. Displaying a measurement monitors; changing the environment adds control.
This loop can use a fixed rule or a learned policy. The hardware path alone does not tell you which.
""", labels=["Sense", "Decide", "Drive motor", "Measure again"]),
 scene("practice", "question", "Will a faster GPU fix this?", 86, """
Pause and diagnose a system. Its processor repeatedly waits for data, and its motor driver cannot supply enough current.
Would replacing the processor with a faster GPU solve both problems? Think before the answer appears.
No. Memory movement and actuator power are separate limits that a new GPU does not automatically remove.
Measure the path, identify the limiting stage, and match the intervention to that evidence.
Page eighty-six broadens the discussion to power, heat, memory, and physical constraints.
An advertised arithmetic rate describes one capability. It is not a complete measurement of the robot's useful performance.
""", prompt="Waiting for data + insufficient motor current", answer="Fix the memory path and power stage.", pause_after=1, pause=6),
 scene("recap", "recap", "Hardware enables every step", 46, """
Recap the path from page thirty-five: observations enter, memory holds information, processing evaluates it, and outputs communicate or act.
Page thirty-six explains why memory capacity and bandwidth both matter. Page thirty-nine separates pipeline throughput from instruction latency.
Page forty-four explains conversion, control signals, and actuator power. Page forty-six compares processing strengths.
Choose hardware by the workload, deadlines, power budget, and physical task.
To check your understanding, draw a robot's path from camera to wheel, and label one possible bottleneck at each stage.
Then explain why a more powerful chip does not, by itself, create a learning algorithm.
""", labels=["Sense → store → compute → act", "Capacity differs from bandwidth", "Throughput differs from latency", "Signals differ from power"]),
 scene("credits", "credits", "Blue Impulse study guide", 1, """
This tutorial used the Blue Impulse study guide, pages thirty-five, thirty-six, thirty-nine, forty-four, forty-six, and eighty-six.
The original book cover is shown on screen as our credit.
The companion tutorial PDF and pipeline demonstration help you repeat the lesson without replaying every explanation.
Blue Impulse study guide. Trace the whole system before choosing the hardware.
""")]),
 dict(number=3, slug="Network_Challenges", title="Network challenges",
      pages=[56,59,61,62,63,74,88], objectives=["Distinguish five network measures", "Calculate the effect of delay", "Choose a response to the actual problem"],
      scenes=[
 scene("hook", "hook", "Why can fast Wi-Fi still feel slow?", 62, """
Have you ever wondered why a connection advertised as fast can still make a video call freeze or a controller respond late?
The advertised rate describes only part of the journey. Delay, variation, loss, and shared demand also matter.
Open your Blue Impulse study guide at page sixty-two, Capacity is not responsiveness.
We will use that page to diagnose problems instead of treating every network problem as a need for more bandwidth.
Then we will calculate the effect of delay using the book's example on page seventy-four.
""", hero="Capacity is not responsiveness", diagram="network"),
 scene("welcome", "objectives", "Today’s route", 62, """
Today you will distinguish bandwidth, throughput, latency, jitter, and packet loss.
You will use a numerical example to connect delay with a physical consequence.
You will choose responses such as compression, fewer round trips, buffering, or local control for specific problems.
Welcome to the tutorial on network challenges by Blue Impulse.
Keep a calculator or paper ready. Every book example has a page citation, and the tutorial PDF includes the practice answers.
"""),
 scene("metrics", "book", "Name the problem before fixing it", 62, """
Read the table at the top of page sixty-two. Bandwidth describes how much data a link can carry per second.
Throughput is the successful transfer rate actually achieved. It can be lower than the link's capacity.
Latency is how long a transfer or response takes. Jitter is variation in that delay.
Packet loss means some packets do not arrive as expected.
These measures answer different questions. A connection can carry a lot of data and still take a long time to respond.
When describing an experiment, specify what you measured: one-way delay, round-trip delay, or complete task response time.
""", block=0, quote="High bandwidth does not remove propagation delay, queueing or server processing."),
 scene("road", "compare", "Use the road analogy", 62, """
Use the guide's road analogy. A wider road can carry more cars at once, like greater bandwidth.
How many cars actually arrive each second is closer to throughput.
How long one journey takes is closer to latency. Uneven arrival times illustrate jitter, while missing deliveries illustrate loss.
Widening a road does not shorten the distance to the destination or remove every queue.
Likewise, increasing link capacity does not erase propagation time, server processing, or unnecessary back-and-forth exchanges.
The analogy helps separate the ideas, but measure the actual network before deciding which factor dominates.
""", labels=["Road capacity: bandwidth", "Delivered traffic: throughput", "Journey time: latency", "Uneven arrivals: jitter"]),
 scene("contention", "book", "Shared demand changes the result", 56, """
Now connect page sixty-two with the media and contention discussion on page fifty-six.
Wireless devices may share a medium, compete for transmission time, and experience interference.
Heavy demand can create queues. Retransmissions after loss can use more capacity and add delay.
Modern switched full-duplex Ethernet should not be described as suffering the old shared-hub collision model.
The useful diagnosis depends on the network technology, the traffic, and the end-to-end path.
Try testing near the access point, with fewer competing transfers, and at different times before blaming one advertised number.
""", block=1, quote="Measure the entire task, not just the advertised link rate.", quote_page=62),
 scene("transport", "book", "Reliability has a timing cost", 59, """
Page fifty-nine explains TCP and IP. IP routes packets, while TCP can provide an ordered, reliable byte stream.
Reliability can require acknowledgements and retransmission, so recovery may add delay.
A transport choice does not by itself guarantee an application deadline or protect every message from an attacker.
Some applications prefer timely delivery and handle missing data themselves. Others need complete, correctly ordered transfer.
Read the application's requirements before selecting a protocol or interpreting a performance measurement.
Pages sixty-three through sixty-five discuss security separately. Confidentiality, integrity, and availability are distinct from simply having a fast link.
""", block=0, quote="Retransmitting lost data can add delay; interference and contention can reduce throughput.", quote_page=62),
 scene("delay", "latency-demo", "What happens during the delay?", 74, """
Turn to page seventy-four. The guide uses a constant speed of thirty metres per second for an illustrative calculation.
Distance travelled during delay equals speed multiplied by delay. First convert milliseconds into seconds.
Five hundred milliseconds is zero point five seconds. Thirty times zero point five gives fifteen metres.
Fifty milliseconds is zero point zero five seconds. That gives one point five metres.
Five milliseconds is zero point zero zero five seconds. That gives zero point one five metres.
Watch the three distances grow from the same starting point. We changed delay while keeping speed fixed.
These are distances before a response begins, not complete stopping distances and not safety guarantees.
Sensing, processing, actuation, and physical braking can contribute additional delay or distance in a real system.
""", speeds=30, delays=[500,50,5], distances=[15,1.5,0.15]),
 scene("real-time", "book", "Real-time means a deadline", 74, """
Read the first paragraph on page seventy-four. A real-time system must respond within a specified deadline.
Real-time does not simply mean very fast. Correctness includes whether the result arrives in time for its task.
Missing a hard deadline can violate the system's requirements. Missing a soft deadline reduces quality of service.
Moving a computation locally may remove some communication delay, but does not automatically guarantee a safe outcome.
Use this distinction when evaluating a remote controller: what is its deadline, and what happens if the response is late?
A good average is insufficient when the important problem is an occasional deadline miss.
""", block=0, quote="“Real-time” does not simply mean very fast."),
 scene("responses", "compare", "Match the remedy to the symptom", 62, """
Return to the final paragraph on page sixty-two and match each response to a problem.
When capacity is limited, compress or summarise suitable data. When round trips dominate, reduce unnecessary exchanges.
Timestamps help detect stale measurements. A playback buffer can smooth jitter, but the buffer adds delay.
Reconnect logic and redundancy can improve resilience, while designed local control reduces dependence on an unavailable remote link.
Page eighty-eight reminds us that growing a system adds load and coordination challenges, not just more devices.
Every remedy has a trade-off. Diagnose, change one factor, and measure again using the metric that matters.
""", labels=["Capacity: compress or summarise", "Latency: fewer round trips", "Jitter: buffer, with added delay", "Outage: designed fallback"]),
 scene("practice", "question", "Calculate a new delay", 74, """
Your turn. At thirty metres per second, how far does an object travel during a two hundred millisecond delay?
Convert the units before multiplying. Take a few seconds, or pause the video to work it out.
Two hundred milliseconds is zero point two seconds. Thirty times zero point two is six metres.
This is only distance during the delay. It does not include the rest of a real stopping process.
Now consider a separate question: would adding a playback buffer always help a time-critical controller? No, because buffering adds delay.
The right network design depends on the task, not a single universally best setting.
""", prompt="30 m/s × 200 ms = ?", answer="30 × 0.200 = 6 metres during delay", pause_after=1, pause=6),
 scene("recap", "recap", "Measure the whole task", 62, """
Let's recap page sixty-two. Capacity is the limit, throughput is achieved transfer, latency is delay, jitter is variation, and loss is missing data.
Our page seventy-four demonstration gave fifteen, one point five, and zero point one five metres during three different delays.
Those numbers illustrate timing; they are not total stopping distances.
Use the road analogy to keep the measures distinct, then replace the analogy with an actual measurement.
For practice, describe a slow application, name the metric you would test, and justify one targeted improvement.
Run the supporting delay calculator to check a second speed and explain the units in your answer.
""", labels=["Separate the five measures", "Convert milliseconds to seconds", "Match remedies to symptoms", "Check deadlines and trade-offs"]),
 scene("credits", "credits", "Blue Impulse study guide", 1, """
This tutorial was taught from the Blue Impulse study guide, especially pages fifty-six, fifty-nine, sixty-two, seventy-four, and eighty-eight.
The original cover on screen credits the book we used throughout the lesson.
Keep the companion tutorial PDF, subtitles, narration, and delay calculator for revision.
Blue Impulse study guide. Measure the whole task, then choose the fix.
""")]),
]

LESSONS += [
 dict(number=4, slug="Networking_for_Behaviorist_AI", title="Networking for behaviorist AI",
      pages=[24,25,72,74,75,77,78,89], objectives=["Separate local control from shared services", "Interpret network messages safely", "Associate feedback with its original action"],
      scenes=[
 scene("hook", "hook", "Should a robot wait for the cloud?", 75, """
Have you ever wondered what a connected robot should do when its network drops during a task?
Sending every decision to a distant server may create a delay exactly when the robot needs a timely response.
Open the Blue Impulse study guide at page seventy-five, Networking for a behaviour-based agent.
We will design the responsibilities of a small warehouse robot, then examine the messages it sends and receives.
The lesson is about making the connection useful without assuming a network is always available or a message is always current.
""", hero="A local loop, connected responsibilities", diagram="networked"),
 scene("welcome", "objectives", "Today’s route", 75, """
You will separate a fast local control loop from shared analysis, coordination, and training services.
You will explain why messages need context such as identity, time, sequence, units, and policy version.
You will also connect delayed learning feedback to the action that produced it.
Welcome to the tutorial on networking for behaviorist AI by Blue Impulse.
We will use pages seventy-four, seventy-five, and eighty-nine, with an illustrative packet-checking demonstration you can run yourself.
"""),
 scene("terms", "book", "Reactive behaviour is not always learning", 24, """
Begin with the distinction on page twenty-four. A reactive agent may map a sensed condition directly to an action.
A fixed rule such as avoiding a detected obstacle can produce useful behaviour without learning from reward.
Page twenty-five adds reinforcement learning: experience is used to improve a policy.
A network connection does not turn a fixed rule into a learning algorithm, and not every connected agent learns online.
For our warehouse example, think of a locally evaluated policy with separate, reviewed updates from a server.
We will label architectural choices clearly instead of treating them as properties of every AI system.
""", block=0, quote="Training may occur centrally while a fixed policy runs locally.", quote_page=75),
 scene("local", "book", "Keep the time-critical loop close", 75, """
Read the first paragraph on page seventy-five. Time-critical sensing, policy evaluation, and actuator control can stay near the device.
Our robot observes an obstacle, evaluates its current policy, and sends a control signal to the actuator hardware.
This local path need not wait for every cloud exchange.
Page seventy-four explains the reason: a real-time task must meet a specified deadline, not just be fast on average.
Local processing removes some network dependency, but it still needs adequate compute, trustworthy sensing, and suitable physical controls.
Local does not automatically mean safe. The requirements and failure behaviour still have to be designed and checked.
""", block=0, quote="A useful architecture keeps time-critical sensing, policy evaluation and actuator control near the device."),
 scene("shared", "diagram", "Let the network do useful shared work", 89, """
Now read the warehouse example on page eighty-nine. Each robot handles immediate motion control locally.
A shared service can allocate tasks, coordinate inventory, and analyse selected telemetry from several devices.
Imagine a local driver following a route while a dispatcher coordinates deliveries across the fleet.
The driver needs immediate awareness; the dispatcher benefits from a broader view. The analogy separates responsibilities.
The network may distribute reviewed policy updates, but a received update should not automatically bypass validation.
Edge and cloud are not opposing teams. Put each part of the workload where its deadlines and resource needs fit.
""", labels=["Robot: immediate control", "Network: telemetry and updates", "Server: coordination and analysis"]),
 scene("fields", "book", "A number needs context", 75, """
Look at the final paragraph on page seventy-five. A message should carry enough context to be interpreted correctly.
Device identity tells us which source or destination it concerns. A timestamp helps determine freshness.
A sequence number can expose repeated or out-of-order messages. Units prevent confusing metres with centimetres.
A policy version connects an action or update to the model that produced it.
These fields are useful evidence, but fields alone do not authenticate a sender. Security checks must support the claimed identity.
Before acting, the receiver needs a policy for rejecting stale, unexpected, or unauthorised commands.
""", block=2, quote="Reject stale or unauthorised commands."),
 scene("messages", "message-demo", "Inspect three incoming messages", 75, """
Let's run the supporting packet-checking example. This is an illustrative design, not a universal protocol from the book.
Our toy receiver expects robot seven, metres as the unit, and policy version three.
For this demonstration, it rejects commands older than two hundred milliseconds and sequences already processed.
The first message has the expected context, a new sequence, and an age of fifty milliseconds. It passes these checks.
The second is six hundred milliseconds old. The receiver rejects it as stale, even if the network eventually delivered it.
The third repeats an already processed sequence. The receiver rejects it as a duplicate instead of executing the command twice.
Our example assumes authentication was checked elsewhere. It does not implement cryptographic authentication or certify a safety-critical controller.
The useful lesson is why delivery alone is insufficient: the receiver must decide whether the message is still meaningful.
""", examples=[{"sequence":42,"age_ms":50,"result":"ACCEPT"},{"sequence":43,"age_ms":600,"result":"STALE"},{"sequence":42,"age_ms":60,"result":"DUPLICATE"}]),
 scene("feedback", "diagram", "Match feedback to the original action", 75, """
The guide makes a second point on page seventy-five: delayed feedback must be associated with the action that produced it.
Suppose action forty-two turns left, and action forty-three moves forward. Their feedback packets arrive in the opposite order.
Updating whichever action happened most recently would connect evidence to the wrong decision.
Use identifiers and recorded context to match each result with its original state and action before a learning update.
If a feedback packet is lost, the evidence is missing. That does not silently mean the reward was zero.
This is how networking details can affect the data used by a learning algorithm, even when policy evaluation stays local.
""", labels=["Action 42: turn left", "Action 43: move forward", "Feedback 43 arrives first", "Match by recorded identity"]),
 scene("outage", "book", "Define what an outage means", 89, """
Return to the warehouse paragraph on page eighty-nine and read the outage condition carefully.
The design must say whether the robot pauses, completes a limited task, or enters another defined state.
Continuing safely during a link outage cannot simply be assumed because some computation is local.
Consider expiring permissions, missing coordination, conflicting routes, and how the system reconnects after the interruption.
Record what happened locally so the shared service can reconcile state when communication returns.
The right fallback depends on the task and its hazards. Our tutorial demonstrates the reasoning rather than certifying a physical robot.
""", block=1, quote="Continued operation must not be assumed."),
 scene("practice", "question", "The feedback packet never arrived", 75, """
Pause and think. The robot performed action forty-two, but its reward packet never arrived.
Should the learner record a reward of zero? And should a repeated command be executed again automatically?
No to both. Missing evidence is not an observed zero, and a duplicate needs the receiver's defined handling policy.
Associate any later feedback with the original action. Decide how long to wait and how to record missing data.
Then explain why a timestamp alone does not prove a message came from an authorised sender.
Use the packet demonstration to change an age or sequence and predict which validation rule should reject it.
""", prompt="Missing feedback = reward zero?", answer="No. Missing evidence is not an observed zero.", pause_after=1, pause=6),
 scene("recap", "recap", "Connect the responsibilities", 75, """
Recap page seventy-five. Keep suitable time-critical work local, and use the network for telemetry, coordination, and reviewed updates.
Messages need interpretable context and appropriate authentication. Stale or repeated commands must not be treated as automatically valid.
Delayed learning feedback belongs to its original action. Lost evidence must not silently become zero reward.
Page eighty-nine adds the deployment question: which part belongs on the robot, at a nearby gateway, or in the cloud?
Finally, distinguish a fixed reactive rule, a deployed learned policy, and an algorithm currently updating that policy.
Draw the local and shared responsibilities, then explain your outage behaviour before calling the architecture complete.
""", labels=["Local control + shared services", "Context and authentication", "Feedback belongs to its action", "Explicit outage behaviour"]),
 scene("credits", "credits", "Blue Impulse study guide", 1, """
This tutorial used the Blue Impulse study guide, especially pages twenty-four, twenty-five, seventy-four, seventy-five, and eighty-nine.
The original book cover on screen credits the source of the lesson.
The companion PDF, narration, subtitles, and illustrative packet-checking code are included for your revision.
Blue Impulse study guide. Connect the system, and preserve the meaning of its data.
""")]),
 dict(number=5, slug="Program_Execution", title="Program execution",
      pages=[12,13,14,15,39], objectives=["Trace fetch, decode, and execute", "Give each register its job", "Follow a four-instruction program"],
      scenes=[
 scene("hook", "hook", "How does a line of code become a result?", 13, """
Have you ever wondered what changes inside a computer after you press Run?
A program does not execute because the processor understands the whole page like a person reading an essay.
It follows encoded instructions, changing registers, memory, and the next instruction address as it works.
Open the Blue Impulse study guide at page thirteen, Fetch, decode, execute.
We will use that page and the tiny program on page fifteen to track every important state change by hand.
""", hero="From an instruction to changed state", diagram="cpu"),
 scene("welcome", "objectives", "Today’s route", 13, """
You will explain fetch, decode, and execute, and give each teaching-model register a clear job.
You will trace four instructions and distinguish an immediate value from a memory address.
You will also connect source code, translators, and machine instructions without oversimplifying how modern language implementations work.
Welcome to the tutorial on program execution by Blue Impulse.
Have a small table ready with columns for the program counter, current instruction, accumulator, and memory location two hundred.
"""),
 scene("source", "book", "Before the processor executes", 14, """
Start with page fourteen, From source code to execution. Machine code contains the instructions the processor executes.
An assembler translates assembly mnemonics and labels. A compiler produces another representation, often native code or bytecode.
An interpreter runs operations through a runtime, sometimes working with bytecode.
The same language can have compiled and interpreted implementations, and modern systems may combine several techniques.
Avoid the blanket claim that every interpreter translates exactly one source line at a time.
For our demonstration, the book supplies an invented assembly notation so that the state changes remain easy to see.
""", block=0, quote="A language may have both compiled and interpreted implementations."),
 scene("recipe", "compare", "Use the recipe analogy", 13, """
Page thirteen uses a recipe to explain the register jobs. The program counter marks the next recipe line.
The memory address register selects the location. The memory data register carries the item read from memory.
The current instruction register holds the instruction being followed. The accumulator is a temporary mixing bowl for arithmetic.
We abbreviate those names as P C, M A R, M D R, C I R, and A C C.
The analogy helps you remember the jobs, but these are electronic storage locations inside a processor model.
Keep the jobs distinct: an address points to a location, while an instruction or value is the content being handled.
""", labels=["PC: next instruction address", "MAR: selected memory address", "MDR: item moving to/from memory", "CIR: current instruction", "ACC: intermediate arithmetic"]),
 scene("fetch", "book", "Fetch one instruction", 13, """
Follow the numbered table on page thirteen. First copy the address in the program counter to the memory address register.
Read the instruction at that memory location into the memory data register.
Advance the program counter so it identifies the next instruction address, then copy the fetched instruction into the current instruction register.
The control unit can now decode the operation and its operand, and the processor executes the required work.
In this simplified model, every instruction occupies one word, so the program counter advances by one.
Real instruction sizes and exact timing depend on the architecture. Our table is a teaching model, not every processor's wiring diagram.
""", block=0, quote="A branch instruction may replace the normal next value of PC."),
 scene("program", "book", "Read the four instructions", 15, """
Turn to page fifteen. The program starts at address one hundred with LOAD, hash three.
The hash sign denotes an immediate value in this invented notation, so that instruction puts the number three into the accumulator.
Address one hundred and one contains ADD, hash four. Address one hundred and two contains STORE, two hundred.
Address one hundred and three contains HALT, which ends this teaching program.
The number two hundred in STORE identifies a memory location. It is not the value to put into the accumulator.
Before running anything, predict what that memory location will contain when the program finishes.
""", block=0, quote="STORE copies 7 to address 200; it does not mean “store the number 200”."),
 scene("trace", "cpu-demo", "Single-step the book’s program", 15, """
Let's single-step. Initially, the program counter is one hundred. Fetch the LOAD instruction and advance to one hundred and one.
Decode and execute LOAD, hash three. The accumulator now contains three.
Next fetch ADD, hash four from address one hundred and one. The program counter advances to one hundred and two.
Execution adds four to the accumulator's three, giving seven. Memory location two hundred has not been written yet.
Fetch STORE, two hundred. The program counter advances to one hundred and three, and execution copies seven into memory location two hundred.
The accumulator still contains seven. STORE copies the value; it does not turn the accumulator into an address.
Finally fetch HALT. In this simplified trace, the fetch advances the counter to one hundred and four before execution stops.
Our runnable Python model prints these same states and the register transfers, so you can check the trace against page fifteen.
""", program=[[100,"LOAD #3"],[101,"ADD #4"],[102,"STORE 200"],[103,"HALT"]]),
 scene("address", "question", "Value or address?", 15, """
Pause and check your prediction. After the STORE instruction, what are the accumulator and memory location two hundred?
Also ask yourself whether STORE, two hundred means storing the number two hundred.
The accumulator remains seven, and memory location two hundred receives seven. Two hundred is the destination address.
The hash sign in our LOAD and ADD operands marks literal values. The STORE operand has a different role.
This distinction prevents a common tracing mistake: confusing where data lives with the value stored there.
Use the book's instruction meanings before applying assumptions from a different programming language or processor.
""", prompt="After STORE 200: ACC = ? and memory[200] = ?", answer="ACC = 7; memory[200] = 7", pause_after=1, pause=5),
 scene("branch", "diagram", "The next address can change", 13, """
Return to page thirteen. It notes that a branch instruction may replace the normal next value of the program counter.
That is how the instruction sequence can follow a decision or repeat a loop instead of always moving forward.
Our four-instruction program contains no branch, so the normal next addresses stay easy to follow.
Page thirty-nine adds pipelining: real processors may overlap work on several instructions while preserving the required program behaviour.
Overlapping the implementation does not make the logical effects of a program arbitrary.
For a basic trace, first understand the defined instruction effects, then study how a specific processor implements them.
""", labels=["Normal next address", "Branch selects another address", "Instruction effects still matter"]),
 scene("practice", "question", "Change one instruction", 15, """
Your turn. Change ADD, hash four to ADD, hash nine, while keeping LOAD, hash three and STORE, two hundred.
What value should reach memory location two hundred? Work through the accumulator before we reveal it.
LOAD gives three. Adding nine gives twelve. STORE copies twelve into memory location two hundred.
That is a small example of testing a prediction by changing one input to the program.
The included simulator accepts a different add value, prints the trace, and checks that the final memory result matches the arithmetic.
Try another value and explain each register's role aloud as the instruction moves through the cycle.
""", prompt="LOAD #3; ADD #9; STORE 200", answer="memory[200] = 3 + 9 = 12", pause_after=1, pause=6),
 scene("recap", "recap", "Instructions change machine state", 13, """
Recap the lesson. Source code reaches execution through a translator or runtime appropriate to its implementation.
The program counter identifies the next instruction. Fetch brings it from memory, decode interprets it, and execute performs its operation.
The memory address register selects a location, the memory data register carries data, and the current instruction register holds the operation.
Our teaching accumulator went from three to seven, and STORE copied seven to memory location two hundred.
Addresses and values have different roles. Branches can change the normal next instruction address.
Revisit pages thirteen through fifteen and complete the trace without watching the moving highlight. Understanding means predicting the state changes yourself.
""", labels=["Fetch → decode → execute", "Each register has a job", "Addresses differ from values", "Trace: 3 + 4 → memory[200] = 7"]),
 scene("credits", "credits", "Blue Impulse study guide", 1, """
This tutorial used the Blue Impulse study guide, especially pages twelve through fifteen, with the pipeline connection on page thirty-nine.
The original cover on screen credits the book we followed.
Use the companion tutorial PDF, complete narration, subtitles, and runnable instruction simulator for revision.
Blue Impulse study guide. Follow the instruction, predict the state, and check the result.
""")]),
]
