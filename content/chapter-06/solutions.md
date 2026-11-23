# Chapter 6 — Answers and expected outcomes

> Attempt each activity in draft.md before reading its answer. Calculations show every step; open questions list the
> points a good answer contains. Numbering matches draft.md.

## Pause & Try

### Pause & Try 6.1 — Robot vacuum as a system

One good set of answers (other sensible choices are fine):

- **Sensor:** a bump sensor in the front bumper. Also acceptable: cliff sensors that detect stairs, a LiDAR or camera for mapping, a dirt sensor.
- **Actuator:** the wheel motors. Also acceptable: the brush motor or the suction fan.
- **Job for its network connection:** receive cleaning schedules and commands from the owner's phone app, and send back the map and a "bin full" alert. Also acceptable: downloading software updates, uploading data for a cloud model to learn from.
- **Behaviour it could learn from feedback:** a shorter route round the room that avoids bumping into furniture. In the chapter's worked example that route earns +35 instead of 0, so it is reinforced. Also acceptable: learning which rooms get dirty fastest and cleaning them more often.

**If the network fails:** a well-designed robot keeps cleaning safely, because its sensors, processor and motors work locally (embedded hardware works offline). Its bump and cliff sensors still stop it hitting furniture or falling down the stairs, and it can follow the last schedule and map stored in its own memory. It loses everything that needs the network: no commands or schedule changes from the app, no alerts or map on the phone, no updates, and no new data for cloud learning, so it stops improving until the connection returns. A robot that waited for the cloud before every move would simply stop, which is why safety-critical decisions belong on the device.

### Pause & Try 6.2 — Smart doorbell strengths and limits

| Technology | One strength | One limitation |
|---|---|---|
| Hardware (camera, motion sensor, button, chip, battery) | reacts at once to motion or a button press, and can save a clip to its own memory with no network | battery and memory budgets: it sleeps between events and may miss a quick visitor; old clips are overwritten; the camera is weak in darkness and glare |
| Network (home Wi-Fi and the internet) | sends a live alert and video to your phone wherever you are, and stores clips in the cloud | weak Wi-Fi at the front door means late or missed alerts and jerky video; it is a way in for attackers (e.g. a default password) |
| AI | learns to tell people from cars, animals or moving branches, so you get fewer false alerts | can be wrong in conditions it rarely saw in training (night, heavy rain) and cannot explain why; recognising faces raises privacy concerns for visitors and passers-by |

**One technology covering another (one example is enough):** the hardware covers the network. If the Wi-Fi drops, the doorbell still rings the indoor chime and saves the clip in its own memory, then uploads it when the connection returns.

Also acceptable: the network and cloud cover the hardware (the doorbell's small chip cannot run a large face-recognition model, so that model runs in the cloud); the hardware covers the AI (a fixed rule makes the chime ring whenever the button is pressed, whatever the AI decides).

### Pause & Try 6.3 — Drone reaction distance

**a)** Distance = speed × time. Change milliseconds to seconds first (÷ 1000).

- Cloud server: 120 ms = 0.120 s, so 15 m/s × 0.120 s = **1.8 m**
- Own processor: 5 ms = 0.005 s, so 15 m/s × 0.005 s = **0.075 m** (7.5 cm)

Waiting for the cloud, the drone flies about 1.7 m further (24 times as far) before it can even start to swerve.

**b)** Any two of these:

- **It works offline:** the radio link can drop (distance, buildings, interference), but the on-board hardware still decides.
- **Deterministic timing:** a dedicated controller takes the same time every time, so the deadline can be guaranteed; a network round trip varies and can suddenly take much longer.
- **No video streaming:** sending live camera images to the cloud uses bandwidth and battery power; deciding on board saves both.
- **Security:** a decision that never leaves the drone cannot be delayed or altered by an attack on the network.

### Pause & Try 6.4 — Which budget runs out

- **a) Hearing aid — power.** Its battery is tiny but must last a week, so its average power draw must be extremely small; every extra calculation shortens battery life.
- **b) Games console in a closed cabinet — thermal.** The heat cannot escape, so the chip gets too hot and throttles (the frame rate drops) or shuts down. Ventilation helps; running the chip faster would only make more heat.
- **c) Parking sensor that must react within 50 ms — speed.** The deadline is the limit: if the processor cannot read the echo, work out the distance and warn the driver within 50 ms, the warning comes too late (a processing limitation). It needs a dedicated controller with deterministic timing.
- **d) Dashcam keeping 24 hours of video — memory (storage).** A day of video is a lot of data. At, for example, 8 Mbit/s: 8 Mbit/s × 86 400 s = 691 200 Mbit; ÷ 8 = 86 400 MB ≈ 86 GB. When the card is full, the oldest clips must be overwritten.

Another budget earns credit only with a clear reason linked to the device's job.

### Pause & Try 6.5 — Fitness band battery and AI

**a)**

- Energy stored = 200 mAh × 3.7 V = 740 mWh
- Battery life = energy ÷ power = 740 mWh ÷ 25 mW = **29.6 hours** (about 1.2 days)

**b)**

- **Thermal limits:** the band has no fan and sits on the skin. A complex model keeps the chip busy, so the chip heats up and must throttle (results arrive later), or the band becomes uncomfortably warm.
- **Memory boundaries:** a complex model has millions of parameters, each needing at least 1 byte, and they must all fit into the band's small memory. Even a 1-million-parameter model (1 000 000 bytes) is almost four times too big for 256 KiB (262 144 bytes) of RAM.
- **Processing speed:** each prediction needs millions of calculations. The band's small processor cannot finish them in time, so it misses deadlines or can analyse only some of the readings.
- These limits are linked through **power**: if the model raised the average draw to 250 mW, as it did for the smartwatch, the band would last only 740 mWh ÷ 250 mW ≈ 3 hours.

**One technique (with its cost):** use a smaller or compressed model, which saves memory, power and time but loses some accuracy. Also acceptable: a dedicated low-power accelerator (NPU), which costs money; running the large model on the paired phone or in the cloud and sending only the results back, which needs a connection; sleeping between readings, which may miss a sudden event.

### Pause & Try 6.6 — Fusing camera and radar

**a)** Fused distance = (radar weight × radar reading) + (camera weight × camera reading). The weights add up to 0.6 + 0.4 = 1.0.

- 0.6 × 5.4 m + 0.4 × 5.0 m = 3.24 m + 2.00 m = **5.24 m**

The result lies between the two readings and nearer the radar's, because the radar is trusted more: it measures distance directly, while a camera can only estimate it.

**b)** Example: at night, in fog or in strong glare, the camera cannot see the box clearly, so its distance estimate is wrong or missing. Radar works in darkness and fog, so the fused system still knows how far away the box is (redundancy). The fusion engine can lower the camera's weight, or ignore it, until it is reliable again. When both work, each covers the other's weakness: the camera recognises *what* the object is, and the radar measures *how far away* it is.

### Pause & Try 6.7 — Farm robot sensor choice

**a)** One good answer: **radar + LiDAR**.

- Both send out their own signal (radio waves, laser light), so neither needs daylight: they work by day and by night.
- LiDAR gives a precise 3D shape, so the robot can tell a person from a post or a bale.
- Radar keeps measuring distance and movement through dust and rain, where LiDAR gets weaker; LiDAR supplies the detail that radar lacks.
- They are different kinds of sensor, so one condition is unlikely to blind both. Missing a person could injure them, which justifies the extra cost.

Also acceptable: radar + a thermal (infrared) camera, which sees body heat even in total darkness; radar + a camera with infrared lights. An ordinary camera on its own is a weak choice because it cannot see at night.

**b)** Example: both sensors are mounted on the front of the robot and get **coated with mud or dust**, so neither can see the worker. Also acceptable: a worker crouching or lying behind tall crops, hidden from both sensors; one power supply or cable whose failure switches off both; a dust storm too thick for either sensor. A good answer adds a fix: mount the sensors in different places, keep them clean, and make the robot stop if a sensor stops giving sensible readings.

### Pause & Try 6.8 — Infusion pump MTBF

**a)**

- Total operating time = 50 pumps × 2 000 h = 100 000 pump-hours
- MTBF = total operating time ÷ number of failures = 100 000 h ÷ 8 = **12 500 hours**

**b)** The MTBF is an **average** for the whole group of pumps, not a promise about any single pump.

- Failures happen at random times. Some pumps fail early (all 8 of these failures happened within the first 2 000 hours), while others run far longer.
- No pump has actually run for 12 500 hours (each ran 2 000); the figure comes from the combined hours of all 50 pumps.
- It is based on only 8 failures under this hospital's conditions; older pumps, heavier use or harsher conditions can make failures more frequent.

So the hospital still needs regular checks and spare pumps. For planning: if all 50 run at the same time, 2 000 h ÷ 8 = 250 h, so expect one failure somewhere in the hospital about every 250 hours.

### Pause & Try 6.9 — Scalability and interoperability defined

- **Scalability:** the ability to handle more work or more devices without performance collapsing.
- **Interoperability:** the ability of different devices and systems, often from different manufacturers, to exchange data and use it correctly.

Why both are critical when hundreds of new IoT devices from different makers join a local network:

- **Scalability:** hundreds of devices add traffic, connections and management work. Without more access points, bandwidth and server capacity, readings arrive late or are lost. Each new device also needs an address, security credentials and updates.
- **Interoperability:** different makers may use different protocols (Zigbee, Bluetooth, Wi-Fi), data formats, units (°C or °F), timestamps and software versions. Without a shared standard such as Matter, or a gateway that translates, the devices cannot be controlled from one system and their data cannot be combined, or it is misread (a °F reading treated as °C).
- **Together:** a network that scales but does not interoperate holds hundreds of devices that cannot work together; one that interoperates but does not scale works with 20 devices and slows down with 500.

### Pause & Try 6.10 — School sensors and upload time

**a)** Any two problems, each with a fix:

| Problem | Practical fix |
|---|---|
| **Different protocols:** some sensors use Zigbee, some Bluetooth, some Wi-Fi, so they cannot talk to each other directly | a hub or gateway that translates, or buying devices that follow a shared standard such as Matter |
| **Different data formats:** one maker reports °F and another °C, or the device clocks disagree, so readings are combined wrongly | agree one format and convert at the gateway; synchronise all device clocks |

Also acceptable: each brand needing its own app or software version (fix: a common platform or standard); a maker ending support (fix: prefer open standards and devices that also work locally).

**b)** Use the throughput, because that is the rate actually achieved.

- Size in megabits: 70 MB × 8 = 560 Mbit
- Time = 560 Mbit ÷ 35 Mbit/s = **16 s**

(At the full bandwidth it would take 560 Mbit ÷ 50 Mbit/s = 11.2 s, but a real link never reaches its bandwidth.)

### Pause & Try 6.11 — Resource optimisation explained

**Model answer.** Resource optimisation means deciding where each task runs (on the device, on a nearby fog server or in the cloud) so that the system meets its goal at the lowest total cost in time, energy, bandwidth and money. Processing on the device costs **hardware**: a more capable chip is more expensive, uses more energy, produces more heat and can still run only small models. Sending data away costs **transmission**: bandwidth, data fees, latency, dependence on a connection and privacy risk. The right balance depends on the task's deadline, data volume, privacy needs, connectivity, energy and cost.

**The camera example, step by step:**

- All video to the cloud: 25 cameras × 4 Mbit/s = 100 Mbit/s, all day and night. Per day: 100 Mbit/s × 86 400 s = 8 640 000 Mbit; ÷ 8 = 1 080 000 MB ≈ **1.08 TB** (about 1 TB). The cameras are cheap, but the upload is huge and expensive.
- Person detection on each camera: 25 cameras × 200 events × 50 KB = 250 000 KB = **250 MB per day**, roughly 4 000 times less (1 080 000 MB ÷ 250 MB ≈ 4 320). The price: every camera needs a more capable chip that costs more and uses more energy.
- Judgement: here edge processing is worth it, because the saving in bandwidth (plus the privacy gain) is far larger than the extra chip cost. Heavy jobs with no deadline, such as retraining the detector, still belong in the cloud.

**Key points:** the definition; the cost of local processing; the cost of transmission; a justified decision about which part of the workload goes where (often a split).

### Pause & Try 6.12 — Hospital monitors: edge, fog, cloud

- **a) Sounding an alarm when a heartbeat stops — edge** (on the bedside monitor itself). It must sound at once, every time, even if the network or a server is down. The decision is simple and safety-critical, and the data does not need to leave the room.
- **b) Comparing all the patients on the ward — fog** (on the ward's own server, e.g. at the nurses' station). It needs data from every monitor on the ward at once, which no single bedside device has. A local server is fast enough (seconds) and keeps patient data inside the hospital.
- **c) Retraining every month with data from many hospitals — cloud.** Retraining needs heavy computation on large amounts of data from many sites, which no ward server holds, and a monthly job has no tight deadline, so latency does not matter. The data should be anonymised before it leaves each hospital.

### Pause & Try 6.13 — Delivery robot total reward

**a)**

- Deliveries: 4 × (+10) = +40
- Time: 25 minutes × (−1) = −25
- Collisions: 1 × (−30) = −30
- Total reward = 40 − 25 − 30 = **−15**

The single collision cost as much as three deliveries, so the shift scored below zero.

**b)** At first the robot tries actions it is unsure about: different routes, speeds and ways of passing obstacles. After each result it updates its estimate of how good each action is. Actions that led to collisions (−30) or wasted minutes (−1 each) earn less total reward, so they are chosen less often; quick, collision-free routes earn more and are reinforced. Over many shifts its policy moves towards more deliveries per minute and no collisions; for example, 5 deliveries in 25 minutes with no collision scores 5 × 10 − 25 = **+25**. It learns only what the reward measures, though: anything without a penalty, such as near misses with people, can still happen.

### Pause & Try 6.14 — Adaptive intelligence explained

**Definition:** adaptive intelligence is the ability to adjust behaviour or strategy appropriately in response to new information, unexpected obstacles or changing conditions.

**How it helps an autonomous agent:** an autonomous agent works for long periods with no human to change its rules, so it will meet situations nobody foresaw, where a fixed rule fails. An adaptive agent senses the change and uses feedback to adjust what it does. For example, a drone hit by a sudden gust notices that it is drifting and changes its motor power at once, without a programmer having written a rule for every wind angle. Learned grasping policies picked up objects they had never seen 96% of the time.

**Why it is not the same as behaviourist AI:** adaptive intelligence is a **capability**, *what* a system can do. Behaviourist AI is one **method** of achieving it, *how*: by learning from rewards and penalties.

- A system can adapt without behaviourist AI: a weather app adapts by re-running its forecast with new data, with no reward at all.
- A behaviourist system may stop adapting: many robots are trained in simulation, then deployed with a frozen policy that no longer changes.

### Pause & Try 6.15 — Predictive analytics vs behavioural modelling

Both learn from historical records, but they use them to answer different questions.

| | Predictive analytics | Behavioural modelling |
|---|---|---|
| Question it answers | What is likely to happen next? | How will an agent react if conditions change? |
| Historical data it uses | number histories: sensor logs, failure records | sequences of states and actions: what agents did in each situation |
| What it produces | probabilities, scores, time-to-failure estimates | a model of decision rules that can simulate new situations: decision policies, state transitions, paths |
| How it informs action | plan ahead: 20 of 80 motors above 7 mm/s failed, so a 25% risk, so book a repair | test a change before making it: pedestrians cross when the gap is over about 4 s, so simulate a longer green light first |
| Main weakness | assumes the future resembles the past (many forecasts failed in early 2020) | every model simplifies; people may behave differently, or change because of the system |

**Key point:** predictive analytics turns past patterns into a number about the future; behavioural modelling uses past behaviour to simulate situations that have not happened yet. Strong systems use both, like the vehicle that books a service at a 30% brake-pad risk while planning its path around pedestrians.

### Pause & Try 6.16 — Choosing the right forecast

- **a) Ambulances needed on New Year's Eve — predictive analytics.** The answer is a number forecast from historical data: call-outs on past New Year's Eves, the day of the week, the weather.
- **b) How drivers react when a bridge lane closes — behavioural modelling.** It asks how agents (drivers) will react to a change that may never have happened. A model of how drivers choose lanes and routes can simulate the closure before it is made.
- **c) When a lift motor needs replacing — predictive analytics.** It needs a time-to-failure estimate from the motor's sensor logs (vibration, temperature, hours run) and the failure records of similar motors.
- **d) How a delivery robot behaves when a child runs towards it — behavioural modelling.** It needs a model of how a child may move (suddenly, unpredictably) and a decision policy for the robot (slow down, stop, keep its distance), which can be practised safely in simulation. The robot's actual reaction must still run on its own hardware, with a hard rule to stop.

### Pause & Try 6.17 — Explainability and the black box

**Definition:** explainability (XAI) is the degree to which a human can understand how an AI system reached a decision.

**Why deep reinforcement learning (DRL) agents struggle with it:**

- The policy is a neural network with millions of numerical parameters, and each decision is the result of millions of multiplications spread across many layers.
- No single number or rule means "brake" or "turn left", so there is no step a person can read and check.
- The behaviour was learned by trial and error, not written by a person, so it is whatever earned reward in training, loopholes included.
- Compare a small Q-table, which is readable: Q(s, left) = 5 and Q(s, right) = 8, so the agent turns right because it expects more reward.

**The "black box" problem:** you can see the inputs (camera, LiDAR, speed) and the output action, but not why that action was chosen. When the agent makes a catastrophic error, such as swerving into an obstacle, engineers often cannot find the cause, so they cannot easily fix it (debugging and safety). Doctors, drivers and courts get no reasons (trust and accountability), and regulators lack evidence that it is safe in every situation (certification).

### Pause & Try 6.18 — Cleaning robot reward loophole

**a)** The reward counts minutes when the *camera* sees no dirt, not minutes when the *floor* is clean. The robot can collect +1 a minute by pointing its camera at a clean wall or the ceiling, covering or switching off the camera, or parking in one spotless corner, all without cleaning anything. Trial and error will find a loophole like this whenever it is easier than cleaning, just as the boat learned to circle in the lagoon.

**b)** Reward the real result, measured in a way the robot cannot fool, and make cheating cost reward. For example:

- +10 for each area of floor that an independent check (a fixed ceiling camera, or a staff inspection at the end of the shift) confirms is clean;
- −1 for each minute, so it cleans efficiently;
- −50 whenever its camera is covered or points away from the floor.

Now the easiest way to earn reward is to clean. Other answers are fine if the reward depends on checked cleaning. Beware: rewarding "dirt collected" alone could teach a robot to tip dirt out and pick it up again, so the trained robot must be tested for new loopholes.

**c)** Example: wards and corridors would stay dirty while the robot's records suggest they are clean, so staff trust a false picture, infections can spread to vulnerable patients, and people can be harmed. Responsibility lies with the designers who chose the reward, not with the robot. Also acceptable: lost trust in hospital automation; cleaning staff cut on the assumption that the robot works; money wasted.

### Pause & Try 6.19 — Biased attendance camera

**a)** The camera has learned what faces look like in bright daylight. On dark winter mornings, under artificial light or far from a window, it recognises students less reliably (distribution shift). It can then mark present students as **absent**, leading to wrong messages to parents, attendance warnings or penalties, or it can mark the wrong student present. The errors are **systematic**, not random: they come back again and again in the same situations and, because dim light makes some faces harder to recognise than others, for the same students. Inside a black box this can go unnoticed for a long time.

**b)** Any two of:

- **Detect:** test accuracy separately in different lighting conditions and for different groups of students, and compare the camera's register with a teacher's manual register.
- **Reduce:** retrain with representative photos: dim, artificial-light and winter conditions, and all kinds of faces.
- **Reduce:** improve the input with better classroom lighting or an infrared camera.
- **Safeguard:** a teacher confirms every absence before any action, students can appeal to a human, and the system is audited regularly after deployment.

### Pause & Try 6.20 — Fusion against sticker attacks

**How fusion helps:** the stickers fool only the **camera's** vision model. A car with sensor fusion cross-checks sources that the stickers do not affect: the LiDAR still sees an eight-sided sign standing at a junction, radar and LiDAR show the crossing road and its traffic, and the car's map (if it uses one) says there is a stop sign here. When the camera's "speed limit" disagrees with everything else, the reading is flagged as a fault or an attack, and the car takes the safe option and stops. To succeed, an attacker would have to fool several different kinds of sensor at once.

**A threat fusion does not prevent: remote takeover through the network.** An attacker who reaches the brakes or steering over the network, as in the 2015 Jeep hack through the entertainment system, bypasses the sensors completely. Also acceptable: a malicious, unsigned software update; a DDoS or botnet attack on the car's online services; privacy leaks of recorded data; an attack that covers or blinds all the sensors at once.

### Pause & Try 6.21 — Security and ethical risks

**Two security concerns** (any two, each explained):

1. **Remote takeover:** an attacker who gets into the network sends commands to actuators (opens a valve, brakes a car), as in the 2015 Jeep hack. With no human watching, nobody stops it in time.
2. **Adversarial or spoofed data:** crafted inputs, such as stickers on a stop sign, make the AI choose a harmful action.

Also acceptable: botnets and DDoS (weak devices hijacked, like Mirai in 2016); privacy leaks from sensors that collect too much; a larger attack surface with every connected device.

**Two ethical implications** (any two, each explained):

1. **Moral accountability:** when the system causes harm, responsibility is split between the developers, the manufacturer, the network provider and any supervisor, so it can be unclear who is to blame. In Tempe in 2018 the safety driver was prosecuted but the company was not charged.
2. **Algorithmic discrimination (bias):** a biased algorithm can favour or penalise some people or places at scale, like the US healthcare algorithm that chose too few Black patients for extra care. With no human checking, the harm can continue for years.

Also acceptable: loss of human judgement on decisions that are hard to undo; privacy and consent of the people being monitored.

### Pause & Try 6.22 — Campus delivery robot judgement

A model answer using the four steps:

1. **Purpose:** carry parcels from the campus mail room to buildings and students along shared footpaths, safely, on time and more cheaply than human couriers.
2. **Strengths (with evidence):**
   - Hardware: on-board processing reacts in milliseconds and works offline. At about walking pace, 6 km/h = 6000 m ÷ 3600 s ≈ 1.67 m/s, so during a 10 ms on-board decision the robot moves under 2 cm (1.67 m/s × 0.010 s ≈ 0.017 m), against 0.25 m during a 150 ms cloud round trip. Fusing cameras with radar or ultrasonic sensors covers day and night.
   - Network: campus Wi-Fi or mobile data lets a fog or cloud server assign parcels, track every robot and unlock the parcel box from the recipient's phone.
   - Behaviourist AI: it learns efficient routes and how to get through crowds, rewarded for on-time deliveries and penalised for near misses.
3. **Limits and risks:**
   - crowded paths with pedestrians, cyclists, wheelchair users and dogs; rain, glare or snow can blind sensors;
   - Wi-Fi dead spots between buildings; batteries drain faster in the cold; breakdowns (plan with MTBF and spare robots);
   - a reward for speed alone could teach a dangerous shortcut (like the canteen example), and a robot trained on a quiet campus meets a much busier one at the start of term (distribution shift);
   - theft of parcels or of the robot, hacking or remote takeover, and cameras filming students.
4. **Judgement:** suitable for routine, low-value parcels on mapped routes at walking pace, **provided** that hard safety rules run outside the AI (a speed cap, always stop for a person close ahead, never block ramps), the reward penalises near misses, the robot stops safely when sensors disagree or the connection drops, parcels are locked and released only to an authenticated recipient, software updates are signed, and camera footage is kept to a minimum.
   - **Oversight needed:** a human supervises and can override. Remote operators watch the fleet and can stop or steer any robot, staff review incidents and the learned routes regularly, and valuable or sensitive items are delivered by hand. Start with a supervised trial at quiet times before full use.

## Practice

### Question 1 — Hardware constraints on embedded AI

**Model answer.** A small embedded device must stay inside four linked budgets (thermal, power, memory and speed). A complex AI model can exceed all of them, and the device's performance is set by whichever budget runs out first.

Key points (1 mark each, 4 marks; each constraint must be linked to its effect on running the model):

- **Thermal:** a complex model needs millions of calculations per decision, and almost all the electrical energy becomes heat. A small, fanless device cannot get rid of it, so the chip throttles (slower, less predictable responses) or shuts down.
- **Power:** the extra calculations raise the power draw and drain the battery. A smartwatch with a 1140 mWh battery lasts 1140 mWh ÷ 40 mW = 28.5 h normally, but only 1140 mWh ÷ 250 mW ≈ 4.6 h while running a heavy model.
- **Memory:** the model's parameters must fit into the device's RAM and flash. A 1-million-parameter model needs at least 1 000 000 bytes, almost four times the 262 144 bytes of a 256 KiB microcontroller.
- **Processing speed:** a small processor cannot finish the calculations before the deadline, so it misses video frames or reacts too late (a processing limitation).

Credit also: the budgets are linked (more speed draws more power, which makes more heat); every fix, such as a compressed model or an NPU, costs something (accuracy, money).

### Question 2 — Scalability and interoperability

**Model answer.** Scalability is the ability to handle more work or more devices without performance collapsing. Interoperability is the ability of different devices and systems, often from different manufacturers, to exchange data and use it correctly. Both are needed because the expansion adds *many* devices *and* many *different kinds* of device (see also Pause & Try 6.9).

Key points (1 mark each, 4 marks):

- A correct definition of scalability.
- A correct definition of interoperability.
- Why scalability matters: hundreds of devices add traffic, addresses, security credentials and updates. Without more access points, bandwidth and server capacity, readings are delayed or lost.
- Why interoperability matters: different makers use different protocols (Zigbee, Bluetooth, Wi-Fi), formats, units (°C or °F) and timestamps. Without a shared standard such as Matter, or a translating gateway, devices cannot work together or their data is misread.

### Question 3 — Adaptive intelligence

**Model answer.** Adaptive intelligence is the ability to adjust behaviour or strategy appropriately in response to new information, unexpected obstacles or changing conditions. It lets an autonomous agent cope with situations nobody programmed for: the agent senses the change and uses feedback to adjust, instead of failing when a fixed rule no longer fits.

Key points (1 mark each, 3 marks):

- Definition: adjusting behaviour or strategy when new information or conditions appear.
- How: the agent senses changes and learns from feedback (rewards, penalties, errors), so it handles situations no programmer foresaw, where hand-written rules fail.
- Example: a drone in a sudden gust adjusts its motor power at once, without a rule for every wind angle (or the grasping robots that picked up unseen objects 96% of the time).

### Question 4 — Predictive analytics vs behavioural modelling

**Model answer.** Both techniques learn from historical data. Predictive analytics uses statistics on past records to forecast *what is likely to happen*. Behavioural modelling uses records of past behaviour to build a model of *how agents decide*, so that it can simulate how they would react to new conditions. The table in Pause & Try 6.15 sets out the full comparison.

Key points (1 mark each, 4 marks):

- Predictive analytics uses number histories (sensor logs, failure records) and statistics to link measurements to outcomes.
- It turns these into probabilities, scores or time-to-failure estimates that guide planning: 20 of 80 motors above 7 mm/s failed, so 20 ÷ 80 = 25% risk, and a repair is booked.
- Behavioural modelling uses sequences of states and actions to represent how an agent (person, robot, vehicle or crowd) behaves: its states, actions and decision rules.
- It simulates "what if?" situations that have not happened yet and produces decision policies or paths. For example, pedestrians step out when the gap is over about 4 s, so a longer green light can be tested before the real lights change.

Credit also: predictive analytics assumes the future resembles the past; behavioural models simplify reality; strong systems use both together.

### Question 5 — Resource optimisation

**Model answer.** Resource optimisation is the strategic balancing of local processing power against network transmission costs, to maximise speed while saving energy, bandwidth and money. In practice it means deciding which part of the workload runs on the edge, in the fog or in the cloud (see also Pause & Try 6.11).

Key points (1 mark each, 3 marks):

- Definition: deciding where each task runs so that the system meets its goal efficiently.
- The trade-off: processing locally avoids latency, transmission costs and privacy risks, but needs costlier, more power-hungry hardware with strict limits. Sending data away uses the cloud's power but costs bandwidth, fees and delay, and depends on the connection.
- An example or a decision rule: 25 cameras streaming to the cloud need 100 Mbit/s (about 1 TB a day), while on-camera detection sends only about 250 MB a day, at the price of better chips. Choose by deadline, data volume, privacy, connectivity, energy and cost.

### Question 6 — Explainability and the black box

**Model answer.** Explainability (XAI) is the degree to which a human can understand how an AI system reached a decision. Deep reinforcement learning agents struggle with it because their policy is a large neural network learned by trial and error: the inputs and outputs are visible, but the reasoning in between is not (see also Pause & Try 6.17).

Key points (1 mark each, 4 marks):

- A correct definition of explainability.
- The policy is a neural network with millions of parameters. Each decision comes from millions of multiplications across many layers, so no single number or rule means "brake".
- The behaviour was learned from rewards rather than written by people, so there is no human-readable rule to inspect. In a Q-table, by contrast, Q(s, right) = 8 > Q(s, left) = 5 explains the choice.
- The result is a "black box": after a catastrophic error, engineers cannot trace the cause, so debugging, trust, accountability and certification all become hard.

### Question 7 — Security and ethical concerns

**Model answer.** Two security concerns are remote takeover and adversarial data; two ethical implications are unclear moral accountability and algorithmic discrimination. Without human oversight, nobody is in the loop to notice an attack or an unfair decision and stop it in time (see also Pause & Try 6.21).

Key points (1 mark each, 4 marks; each briefly explained):

- **Security concern 1:** remote takeover, where unauthorised commands reach actuators through the network (the 2015 Jeep hack).
- **Security concern 2:** adversarial or spoofed sensor data that fools the AI (stop-sign stickers). Also acceptable: botnets and DDoS through weak IoT devices (Mirai, 2016); privacy leaks.
- **Ethical implication 1:** moral accountability. Responsibility is split between the developers, the manufacturer, the network provider and any supervisor, so victims may not know who is responsible (Tempe, 2018).
- **Ethical implication 2:** algorithmic discrimination. A biased algorithm treats some people or places unfairly at scale, and the harm runs unnoticed (the US healthcare algorithm). Also acceptable: loss of human judgement on decisions that are hard to undo; privacy and consent.

### Question 8 — Sensor fusion in a delivery van

**(a)** [3 marks: 1 per sensor for a correct strength and weakness]

| Sensor | Strength | Weakness |
|---|---|---|
| Camera | colours, signs and lane markings; recognises objects | darkness, glare and fog; no direct distance |
| Radar | distance and speed, even in rain, fog or darkness | little detail; cannot read signs |
| LiDAR | precise 3D shape and distance | heavy rain, snow and fog; expensive |

**(b)** [2 marks]

- Fused distance = 0.7 × 11.6 m + 0.3 × 12.0 m (the weights add up to 0.7 + 0.3 = 1.0) (1 mark)
- = 8.12 m + 3.60 m = **11.72 m** (≈ 11.7 m) (1 mark)

The result is closer to the LiDAR reading because LiDAR is trusted more.

**(c)** [2 marks: 1 for an advantage, 1 for a disadvantage, each with its effect]

- **Advantage:** redundancy and accuracy. If one sensor fails or is blinded (the camera in fog), the others keep working; independent errors partly cancel out; and a reading that disagrees with the others can be flagged as a fault or an attack.
- **Disadvantage:** every extra sensor adds cost, weight and power, and the readings must be aligned and calibrated, which adds processing and delay. Fusion also cannot help when one cause, such as mud, covers all the front sensors at once.
- **Evaluation:** for a self-driving van, where a wrong reading can cost a life, the advantage outweighs the extra cost.

### Question 9 — MTBF of warehouse robots

**(a)** [2 marks]

- Total operating time = 40 robots × 1 500 h = 60 000 robot-hours (1 mark)
- MTBF = 60 000 h ÷ 12 failures = **5 000 hours** (1 mark)

**(b)** [2 marks: 1 for what it tells them, 1 for what it does not]

- **What it tells them:** on average, a robot runs about 5 000 hours between failures. For the whole fleet, 12 failures in 1 500 hours means about one failure every 1 500 h ÷ 12 = 125 hours if all 40 run at once. This helps the company plan spare parts, repair staff and maintenance.
- **What it does not tell them:** when any particular robot will fail, because it is only an average and some robots fail much sooner. It is based on only 12 failures (no robot has actually run 5 000 hours), and it says nothing about the causes of failure, how long repairs take, or how reliability changes as the robots age.

### Question 10 — Latency and edge, fog or cloud

**(a)** [1 mark]

- 200 ms = 0.200 s; distance = 25 m/s × 0.200 s = **5.0 m**, travelled before the reply even arrives.

**(b)** [6 marks: 1 for each correct choice, 1 for each justification]

- **Emergency braking — edge** (on the car). It must react in milliseconds (a 200 ms cloud round trip already means 5 m travelled) and must work with no signal; a safety-critical decision cannot depend on a network.
- **Sharing live traffic conditions across a city — fog.** It combines data from many nearby vehicles and roadside sensors, and it must be live (within seconds) but not within milliseconds. A city-level server, such as a traffic-control centre or roadside units, is closer and faster than a distant data centre and keeps the data local. Cloud is also accepted if justified: the service is city-wide, and a delay of a second or two is fine for traffic information.
- **Training a new driving policy — cloud.** Training needs huge computing power and storage, using data from the whole fleet over months, and there is no real-time deadline, so latency does not matter. The new policy is tested and then sent to the cars.

### Question 11 — Five manufacturers, one smart home

**(a)** [2 marks: 1 per problem explained]

- **Different protocols:** some devices may use Zigbee, others Bluetooth or Wi-Fi, so they cannot talk to each other directly without a hub or a shared standard such as Matter.
- **Different data formats or apps:** one device reports °F and another °C, or their clocks disagree, so data is combined wrongly. Or each brand needs its own app, so one rule ("lock the door when the lights go off") cannot work across brands.

Also acceptable: a maker ending support (as when Nest switched off the Revolv hub in 2016), so its devices stop working with the rest; uneven security, where one cheap device becomes the weak point.

**(b)** [2 marks]

- Size in megabits: 50 MB × 8 = 400 Mbit (1 mark)
- Time = 400 Mbit ÷ 25 Mbit/s (the throughput, the rate actually achieved) = **16 s** (1 mark)

(At the full bandwidth it would be 400 Mbit ÷ 40 Mbit/s = 10 s, but real transfers run at the throughput.)

### Question 12 — Reward design and biased data

**(a)** [2 marks]

- The reward gives +5 for every parcel packed and nothing for damage, so a damaged parcel costs the robot nothing (1 mark).
- Packing faster earns more reward per hour, so trial and error reinforced fast, rough packing. The robot did exactly what the reward said, not what its designers meant (1 mark).

**(b)** [2 marks: 1 for the change, 1 for its effect]

- **Change:** add a penalty for every damaged parcel, large enough to outweigh what speed gains, e.g. −25 per damaged parcel.
- **Effect:** rough packing now loses reward, so the robot learns to pack carefully, even if a little more slowly. For example, suppose fast packing manages 12 parcels a minute (1 in 10 damaged, so 1.2 damaged) and careful packing manages 10 a minute with none damaged:
  - Old reward: fast 12 × 5 = 60 a minute; careful 10 × 5 = 50 a minute, so fast wins.
  - With −25 per damaged parcel: fast 60 − 1.2 × 25 = 30 a minute; careful 50 a minute, so careful wins.
- Simply not paying for damaged parcels would not be enough here (fast: 10.8 undamaged × 5 = 54, which still beats 50), so the penalty matters. The robot must then be retrained and re-tested.

**(c)** [2 marks: 1 for the biased data, 1 for the real consequence]

Example: Amazon's experimental CV-screening tool learned from ten years of applications that came mostly from men, so it downgraded CVs containing the word "women's", and qualified women could have been unfairly rejected. The tool was scrapped (reported in 2018). Also acceptable: the US healthcare algorithm that used past spending as a stand-in for need and so chose too few Black patients for extra care (17.7% instead of 46.5%); a robot trained only in sunny weather that performs poorly in snow.

### Question 13 — Home security system

**(a)** [6 marks: 1 for each strength, 1 for each limitation]

| Technology | One strength | One limitation |
|---|---|---|
| Hardware (door sensors, cameras, local hub) | reacts at once and works without the internet; the hub can sound the alarm on its own | cameras struggle in darkness and glare; battery sensors need replacing; the hub's small processor cannot run the learning AI |
| Network (home Wi-Fi and the internet) | sends alerts and live video to the owner's phone anywhere, and reaches the cloud AI | Wi-Fi can drop or be jammed; limited upload bandwidth delays video; every connected device is a way in for attackers (default passwords) |
| AI (learning, in the cloud) | learns from feedback to tell residents from strangers, cutting false alarms without a rule for every face | makes mistakes in new conditions (night, a new hairstyle, guests), giving false alarms or missing a stranger; hard to explain; may be biased; stops working without the internet |

**(b)** [2 marks]

- The hub runs simple fixed rules on its own processor. If a door opens while the system is armed, it sounds the siren and switches on the lights without asking the cloud, and residents disarm it with a code or key fob (1 mark).
- It saves camera clips to local storage and, with a backup battery and a mobile (4G) link, can still send alerts. It uploads everything when the internet returns, just as the greenhouse controller keeps its last schedule (1 mark).

**(c)** [2 marks: 1 for the concern, 1 for why it matters]

Camera images of residents, children, visitors and passers-by, inside and outside the home, are very personal data, and once they are sent to the cloud they are stored on a company's servers. They could be leaked in a hack, kept longer than needed, viewed by staff or shared without consent, and people filmed outside the home never agreed to it. Good answers suggest a remedy: recognise faces on the hub (edge) where possible, encrypt uploads, and store as little as possible for as short a time as possible.

### Question 14 — Evaluating hospital delivery robots

**Marking guide (8 marks):** about 6 marks for developed points across hardware, network, behaviourist AI, reliability, security and oversight (strengths *and* limitations), and 2 marks for a justified conclusion about suitability and oversight.

Points a good answer contains:

- **Hardware.** Strength: on-board sensors and processing avoid people and obstacles in milliseconds and keep working without the network; fusing cameras with LiDAR or ultrasonic sensors copes with dim corridors at night. Limitation: battery life over a whole night; doors, lifts and narrow corridors; poor light for cameras; wear and breakdowns (plan with MTBF).
- **Network.** Strength: Wi-Fi lets the scheduler track every robot and send urgent jobs at once, and a fog server inside the hospital is fast and keeps the data in the building. Limitation: dead spots in lifts, stairwells and shielded rooms; when the link drops, the robot must finish its current move or stop somewhere safe.
- **Behaviourist AI.** Strength: the scheduler learns from feedback which routes and job orders work best, and adapts to busy nights without a rule for every case. Limitation: it needs many trials, is hard to explain and follows its reward even when the reward is wrong. Rewarded only for speed, it might favour easy routine jobs over urgent ones or take risky routes, and an unusual night (an emergency, a broken lift) is a distribution shift.
- **Reliability.** Spare robots and a manual back-up (a porter or nurse on call), so a breakdown never delays an urgent medicine; fail safe when sensors disagree; regular maintenance.
- **Security.** Medicines, especially controlled drugs, must travel in locked compartments opened only by authenticated staff (badge or PIN). Encrypt and separate the robots' network and accept only signed updates, because a hacked robot or scheduler could misdirect or expose medicines. Protect the patient details on delivery lists.
- **Human oversight.** A human supervises and can override: a night pharmacist or nurse approves urgent and controlled-drug deliveries, someone monitors the fleet and can stop or redirect any robot, and the receiving ward confirms each delivery.
- **Justified judgement.** Suitable for routine medicine deliveries at night *if* hard safety rules run outside the AI, the reward includes urgency and safety and not just speed, fail-safes and a manual back-up exist, security is strong and humans supervise. Not suitable as a fully unsupervised system for urgent or controlled medicines, because the stakes are high and mistakes are hard to undo.
