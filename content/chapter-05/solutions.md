# Chapter 5 — Answers and expected outcomes

> Attempt each activity in draft.md before reading its answer. Calculations show every step; open questions list the
> points a good answer contains. Numbering matches draft.md.

## Pause & Try

### Pause & Try 5.1 — Parts of a home device

Model answer for a **robot vacuum cleaner** (any device is fine if all three parts are named correctly):

**(a) Sensors:** a bump sensor in the bumper (it has hit something), infrared cliff sensors underneath (no floor ahead, e.g. stairs), wheel sensors that measure how far it has moved, and a battery-level sensor. Many models also map the room with a camera or lidar.

**(b) Network:** Wi-Fi to the home router, then over the internet to the maker's cloud server and your phone app. It sends progress reports and its map, and receives commands such as "start cleaning" or a schedule.

**(c) Actuators and outputs:** wheel motors that drive and turn it, brush and suction motors that clean, and a speaker or lights that show its status.

Also acceptable: a smart thermostat (temperature and PIR motion sensors; Wi-Fi, Zigbee or Thread; a relay that switches the boiler) or a smartphone (touchscreen, camera, microphone, accelerometer, GPS; Wi-Fi, 4G/5G, Bluetooth; screen, speaker, vibration motor).

### Pause & Try 5.2 — Learned policy versus fixed rule

**Advantage of the learned policy:** it combines the moisture readings with the weather forecast and with feedback from earlier results, so it can skip watering when rain is coming and give each zone only what it needs. Over many weeks it learns to grow the same harvest with less water, and it keeps improving; the fixed rule never improves.

**Why a farmer might still prefer the fixed rule:** it is simple, predictable and easy to check, so the farmer always knows what it will do and why. It also works from day one, while the learned policy needs weeks of data and testing before it can be trusted, and a learning mistake (e.g. under-watering to avoid the water penalty) could damage a crop.

Also acceptable: the fixed rule is cheaper, needs no forecast or internet connection, and is easy to fix when it goes wrong.

### Pause & Try 5.3 — Classifying real-time systems

| Application | Type | Reason |
|---|---|---|
| (a) fly-by-wire control | hard real-time | a late control command could make the aircraft go out of control |
| (b) streaming a film | soft real-time | a late frame causes buffering or a blurry picture, but nothing is damaged |
| (c) heart pacemaker | hard real-time | a late pulse could harm or kill the patient |
| (d) weekly payroll | not real-time (batch) | all the pay is worked out together later; a delay of an hour harms nobody |

**Example justification, (c):** a pacemaker must deliver each electrical pulse at the right moment, every time. A pulse that arrives late cannot be made up afterwards, so missing the deadline means the system has failed and the patient may be harmed. That is exactly what hard real-time means.

(For (b), the player keeps a few seconds of film in a buffer, so its deadlines are looser than a video call's, but a late frame still lowers the quality.)

### Pause & Try 5.4 — Edge or cloud for robots

**(a)** Stop for a pedestrian: **edge** (on the robot).

**(b)** Plan tomorrow's routes for the fleet: **cloud**.

**(c)** Retrain its policy on a week of logs: **cloud**.

**Justification of (a):** stopping is a split-second, safety-critical decision. A cloud round trip adds about 50–200 ms of latency, and if the link fails the robot could not stop at all. Its own computer decides in about 1–10 ms and keeps working with no signal.

Also acceptable as the justified answer: (b) and (c) are heavy jobs that can wait hours and need data from the whole fleet and more computing power than one robot carries; the retrained policy is tested and then downloaded to the robots.

### Pause & Try 5.5 — Parts of a video doorbell

| Part | Type | What it does when a visitor arrives |
|---|---|---|
| PIR motion sensor | sensor | detects the body heat of the moving visitor and wakes the doorbell |
| Camera | sensor | records video of the visitor |
| Wi-Fi chip | network component | sends an alert and the live video, through the router and the cloud, to the owner's phone, and brings the owner's reply back |
| Speaker | actuator (output) | plays a chime, a recorded message or the owner's voice |

Together they make one trip around the loop: the PIR sensor and camera sense, Wi-Fi connects, the owner (or a routine) decides, and the speaker acts.

### Pause & Try 5.6 — Learning thermostat and security

**How it uses feedback:** every time someone changes the setting, the thermostat records the day, the time and the temperature chosen; these changes are its feedback. When it spots a pattern, e.g. the heating turned up from 17 °C to 21 °C at about 06:30 from Monday to Thursday, it changes its own schedule and starts heating at 06:00, so the house is already warm. If someone corrects it again, that correction works like a penalty for its last choice and the schedule shifts; a day with no corrections suggests it got things right. Its behaviour therefore changes with experience, unlike a fixed routine.

**Security risk:** an attacker could take control of it, for example through an unchanged factory password, as the Mirai malware did to hundreds of thousands of devices in 2016. A hijacked thermostat can be used in a DDoS attack, have its settings changed, or reveal when the house is empty.

**Reducing the risk:** change the default password to a strong, unique one. Also acceptable: install updates, use encryption and secure Wi-Fi, turn on two-factor authentication for the app, choose a device that collects only the data it needs.

**Key points:** records each manual change; finds a pattern; adjusts its own schedule; corrections act as penalties; one named risk; one matching protection.

### Pause & Try 5.7 — From smartwatch to nurse

1. **Optical heart-rate sensor** (in the watch): green LEDs shine into the skin and a light sensor measures the light that comes back; each heartbeat changes the reading.
2. **Watch processor** (edge computing): turns the raw light readings into a heart rate and a short summary.
3. **Bluetooth:** carries the summary from the watch to the phone.
4. **Mobile network** (4G/5G, or home Wi-Fi and the internet): the phone uploads the summary, encrypted, to the clinic's server.
5. **Clinic dashboard:** shows the reading on the nurse's screen and flags anything unusual.

**Benefit of processing on the watch:** it sends only summaries instead of a constant stream of raw readings, which saves battery power and network bandwidth. Also acceptable: it can react at once without a signal (e.g. detect a hard fall), and less raw personal data leaves the watch.

### Pause & Try 5.8 — AI X-ray screening

**(a)** Two efficiency advantages:
- **Speed:** it checks each X-ray in seconds and keeps up with hundreds a day, day and night, without getting tired.
- **Prioritising:** it marks areas that look abnormal and moves urgent cases to the top of the doctor's list, so the sickest patients are seen first.

Also acceptable: it is a tireless extra check that can catch something a busy doctor misses; doctors spend less time on clearly normal scans.

**(b)** The AI only recognises patterns like those in its training data. Faced with a deformity it has never seen, it may misread the image: label it normal, so the patient is not moved up the list and treatment is delayed, or confidently report the wrong illness. If the doctor over-relies on the AI, the mistake may not be caught. This is why the doctor still makes the diagnosis, and why the system should show how confident it is.

### Pause & Try 5.9 — Adaptive traffic signals

**How it reduces waiting:** sensors (wire loops buried in the road, cameras and radar) detect waiting cars and measure each queue. A network (fibre or mobile) carries the readings to the controller. Software then shares out the green time to match the queues instead of giving each road a fixed 30 s: with 18 cars on the main road and 6 on the side road it gives 45 s and 15 s. Long queues clear faster, and nobody waits at a red light beside an empty road at 3 a.m.

**Extra penalty (one good answer):** a penalty for every vehicle or pedestrian that has waited longer than a set time, e.g. 2 minutes. **Why:** a reward based only on total waiting time could be earned by keeping the busy main road green almost all the time, leaving a few drivers on the side road, or pedestrians, waiting for a very long time. The extra penalty makes the controller serve everyone fairly.

Also acceptable, with a reason: a penalty for delaying an emergency vehicle or a bus; for switching the lights too often (each change wastes amber time); for queues that back up into the previous junction; for the number of stops (stop-start driving adds pollution).

### Pause & Try 5.10 — Bus speed and latency

**(a)** 54 km/h = 54 × 1000 m ÷ 3600 s = 54 000 m ÷ 3600 s = **15 m/s**

**(b)** distance = speed × delay
- Cloud link: 300 ms = 300 ÷ 1000 = 0.300 s, so 15 m/s × 0.300 s = **4.5 m**
- Onboard computer: 4 ms = 4 ÷ 1000 = 0.004 s, so 15 m/s × 0.004 s = **0.06 m** (6 cm)
- Deciding on board means 4.5 − 0.06 = **4.44 m** less travel before braking begins. The bus then still needs its braking distance to stop.

**(c)** The urgent braking decision is made on board, but the network is still needed for jobs that can wait: receiving route, map and timetable updates and traffic information (e.g. how many seconds remain before a light turns red, over V2I); uploading logs to the cloud so engineers can retrain its AI, and downloading improved, tested policies; and letting the operator track the bus or call for help after a crash.

### Pause & Try 5.11 — HCI versus HAI driving

**(a)** In the **traditional manual car**. The human is the operator: they steer, accelerate, brake and change gear all the time, and the car does exactly what it is told (same input, same output).

**(b)** In the supervisory role the human no longer gives every command. New responsibilities:
- **setting the goal** (the destination) and checking the route the AI chooses;
- **monitoring** what the AI is doing and whether it seems safe, while avoiding over-trust (no longer paying attention) and under-trust (switching off a useful feature);
- **intervening** when needed: stopping the ride, calling the operator or reporting a problem if the AI makes a wrong best guess or meets a situation it cannot handle.

### Pause & Try 5.12 — Correcting a robot joint

**(a)** The controller compares the target with the measured angle: error = 45° − 41° = **4°**. The joint has stopped 4° short, so the controller sends a new command through the driver circuit to turn the motor a little further in the same direction. The encoder measures the new angle and the controller compares again. This loop repeats hundreds of times a second until the error is zero (or within a tiny tolerance), and then the motor holds the joint there. If the joint overshoots, the error becomes negative and the motor turns back.

**(b)** The actuator (the motor) makes the movement, but it cannot tell where the joint actually ended up: friction, the weight of the part or wear can make it stop short or overshoot. The sensor (the encoder) measures the real angle, so the controller can see the error and correct it. With only an actuator, errors would go unnoticed and parts would be misplaced; with only a sensor, the arm could detect an error but not fix it. Together they form a feedback loop.

**Key points:** error = target − measured = 4°; drive further and measure again; repeat until the error is zero; the actuator moves, the sensor checks; both are needed for a closed loop.

### Pause & Try 5.13 — Rewards for a delivery drone

**(a) State:** GPS position and altitude; distance and direction to the clinic; speed and tilt from the accelerometer and gyroscope; battery level; wind; distances to obstacles from cameras or lidar; whether the medicine is still on board.

**(b) Positive reward:** the medicine is delivered, undamaged, to the correct clinic (e.g. +100). Smaller rewards for getting closer to the clinic or landing gently are also acceptable.

**(c) Heavy penalty:** crashing into a tree, a building, a power line or a person (e.g. −500). Also acceptable: dropping or damaging the medicine, running out of battery in flight, entering a no-fly zone.

The drone should practise first in a simulation, and safety limits, such as landing at once when the battery is low, must never depend on the reward.

### Pause & Try 5.14 — Designing a smart campus

**Two areas (one good answer):** classroom heating and lighting; cafeteria food waste.

**Classroom heating in detail:**
- **Sensors:** a PIR occupancy sensor and a temperature sensor in each room (a CO₂ sensor can also show when fresh air is needed).
- **Network:** the campus Wi-Fi, or a low-power mesh such as Zigbee, carries the readings to the building's control software.
- **Action:** the software combines the readings with the timetable and switches the heating on (through a relay or a motorised radiator valve) just before a booked lesson, and off, with the lights, when a room is empty. This saves the energy and money wasted on heating and lighting empty rooms.

For food waste: smart bins with weight sensors record what is thrown away, Wi-Fi sends the data to the cloud, and AI predicts how much of each dish will be eaten so the kitchen cooks less of the unpopular ones. Other acceptable areas: library seating, water leaks, outdoor lighting.

### Pause & Try 5.15 — Levelling rule and learning

**(a)** The student finishes on **level 3**.

| Answer | Result | Run so far | Level afterwards |
|---|---|---|---|
| 1 | right | 1 right | 3 |
| 2 | wrong | 1 wrong (the right run is broken) | 3 |
| 3 | right | 1 right | 3 |
| 4 | right | 2 right | 3 |
| 5 | right | 3 right: up one level | 4 |
| 6 | wrong | 1 wrong | 4 |
| 7 | wrong | 2 wrong: down one level, with a hint | 3 |

**(b)** The fixed rule never changes, so it is reactive control: every student meets the same thresholds whatever happens. A reinforcement-learning version treats each choice of question as an action and earns a reward when the learner later gets a similar question right (e.g. a week later). Using thousands of students' results, it learns by trial and error which question, or which step up in difficulty, helps each kind of learner most, and it changes its own policy as it goes. It can suit each learner better, but it needs a lot of data and testing, and its choices are harder to explain.

**Key points:** fixed rule = same response every time; RL = actions, rewards and a policy that changes with experience; the reward is linked to later learning; it needs data and is less transparent.

### Pause & Try 5.16 — A smart city system

Model answer: the **smart water network**.
- **Sensor:** acoustic (sound) sensors on the water mains listen for the hiss of small leaks.
- **Network:** a long-range, low-power network such as LoRaWAN, or the mobile network, carries the readings to the water company's AI.
- **Actuator:** motorised valves that close to isolate the leaking pipe.
- **What the AI decides:** whether a sound really is a leak and not traffic noise, where the leak is, how serious it is, which valves to close and when to send a repair crew.

**One way it could fail:** a false alarm closes valves and cuts off water to homes or a hospital, or a sensor's battery dies and a real leak goes unnoticed. **Reducing the risk:** ask an engineer to confirm before closing valves for anything smaller than a major burst, and have every sensor send a regular "still working" message, so a silent sensor is noticed (a missing reading means "unknown", not "no leak"). Encrypting and authenticating valve commands also protects against attackers.

Also acceptable: adaptive traffic signals (cameras and road sensors; 5G; the traffic lights; the AI sets the green times; if a camera or the 5G link fails, the lights fall back to a safe fixed-timer plan).

### Pause & Try 5.17 — Bus-stop passenger cameras

**Opportunity:** extra buses go where people are actually waiting, so waits and crowding fall and fewer nearly empty buses run, saving fuel and cutting pollution.

**Privacy risk:** cameras at every stop record people's faces, so the data could be used to track where individuals go, or be stolen, sold or misused.

**Making it fairer or more transparent (one good answer):** count passengers on the camera itself (edge processing) and send only the number, never the video; delete the images at once, use no face recognition, and put up signs at each stop explaining what is collected and why. Also acceptable: publish the rule for sending extra buses; keep a minimum service on quieter routes so those areas are not left out; check that counting works equally well for everyone, e.g. wheelchair users, children and people waiting at night.

### Pause & Try 5.18 — The application I trust least

There is no single correct choice; a good answer names one application and gives a specific change for each pillar. Model answer for a **self-driving taxi**:
- **Fairness:** it must be shown to detect all road users equally well (children, wheelchair users, people of every skin tone, at night and in rain), and it should serve every neighbourhood, not only the most profitable ones.
- **Transparency:** it should tell passengers what it sees and what it is about to do, and why (e.g. "stopping: pedestrian ahead"); record its sensor data, like an aircraft's flight recorder, so accidents can be investigated; and its safety record should be published.
- **Accountability:** it must be clear who is responsible when something goes wrong. Under the UK's Automated Vehicles Act 2024, the company behind an approved self-driving system is responsible while it is driving; there should also be an easy way to report problems and an independent regulator to investigate.

**Key points:** one named application from the chapter; a concrete change for fairness, transparency and accountability; a reason why each change would increase trust.

## Practice

### Question 1 — Smart systems

A smart system combines hardware, networks and intelligent software so that a machine can sense its surroundings, share information, decide what to do and act, often within milliseconds and with little or no human help. Its four parts work as one loop, e.g. on a smart farm:
1. **Sense:** sensors (hardware) measure the physical world: soil-moisture sensors in every zone.
2. **Connect:** a network carries the readings to where the deciding happens and carries commands back: LoRaWAN to the farm's computer.
3. **Decide:** a processor running software or AI chooses the action: it combines the readings with the forecast.
4. **Act:** actuators (hardware) turn the decision into physical action: solenoid valves water Zone A for 12 minutes.

Acting changes the environment and the next readings show whether the action was right, so the loop is a feedback loop. Remove any part and the system fails: without sensors it is blind, without a network it is cut off, and without intelligent software it cannot adapt.

**Key points:** definition; sensors, network, processor and actuators, each with its job; the order sense → connect → decide → act; feedback loop; a real example.

### Question 2 — Real-time processing and automation

**(a)** Real-time processing means processing data immediately, or within a strict time limit (a deadline), so the result arrives in time: fast enough, every time, not just fast on average. Collision avoidance is hard real-time, because a late decision can kill. The car keeps moving while every stage adds delay: at 108 km/h it travels 30 m every second, which is 3 cm every millisecond.
- **Low network latency** matters because network delay adds directly to the distance travelled before braking: at 108 km/h a 500 ms cloud link means 15 m, a 5 ms onboard decision only 0.15 m. A busy or broken link could also make the system miss its deadline, so these decisions are made at the edge, in the car.
- **High-speed hardware** matters because the cameras, radar and lidar produce huge amounts of data that the onboard computer, with GPU and AI-accelerator chips, must process within a few milliseconds, and the brakes and steering must respond at once.

**Key points:** definition with deadline; hard real-time; distance = speed × delay; edge versus cloud latency; fast processors and sensors.

**(b)**
- Speed: 90 km/h = 90 × 1000 m ÷ 3600 s = 90 000 m ÷ 3600 s = **25 m/s**
- Cloud connection: 400 ms = 400 ÷ 1000 = 0.400 s, so 25 m/s × 0.400 s = **10 m**
- Onboard computer: 8 ms = 8 ÷ 1000 = 0.008 s, so 25 m/s × 0.008 s = **0.2 m** (20 cm)
- Deciding on board saves 10 − 0.2 = **9.8 m** before braking begins (the cloud decision takes 400 ÷ 8 = 50 times as long). The car then needs extra braking distance to stop.

**(c)** Automation is the use of technology to perform tasks with minimal human involvement.
- **Efficiency rises:** machines do not get tired or distracted, so a production line can run day and night; they respond in milliseconds instead of a person's 0.67 s; they repeat a task with the same precision thousands of times a day; and they use resources such as water and energy more precisely.
- **Error rates change:** random mistakes caused by tiredness fall (a robot does not miss the odd faulty part), but errors become systematic: if a camera is knocked out of line or the software has a bug, the robot repeats the same mistake on every product until someone notices. New risks also appear, such as sensor failures, cyber attacks and situations the system was never designed for.
- **People's role changes** from operator to supervisor: automated systems still need people to monitor them, without over-trusting them.

**Key points:** definition; at least one efficiency gain; fewer random errors but repeated, systematic ones; humans still monitor.

### Question 3 — Feedback and action

**(a)** The AI works in a loop. It observes the **state** through its sensors, uses its **policy** to choose an **action**, and the environment sends back feedback: a **reward** if the result was good or a **penalty** (a negative reward) if it was bad. Over many trials, actions that earned high rewards in a state become more likely and actions that earned penalties become less likely, so the policy improves by trial and error and the agent earns more reward over time. For example, a warehouse robot that scores +4 for a careful 12 s placement but −43 for a fast move that clips a shelf learns to make careful, collision-free moves. (Q-learning, from Chapter 2, is one way to do this: it updates an estimated value for each state and action after every result.)

**Key points:**
- state → action → reward or penalty → policy update, repeated many times;
- the reward defines what "good" means, so it must be designed carefully;
- each result must be matched to the right action (timestamps and sequence numbers); a lost report means the result is unknown, not a reward of zero;
- unlike reactive control, whose fixed rules never change, the behaviour changes with experience;
- training usually starts in simulation, and safety limits never depend on the reward.

**(b)** An actuator turns an electrical signal into physical action. Inside the computer a decision is only a number, e.g. "rotate joint 2 to 90°". The controller sends this target to a driver circuit, which turns it into a control signal (a voltage or PWM pulses) and switches the power the motor needs; the actuator then moves. A sensor such as an encoder measures the result (e.g. 87°) and the controller corrects the 3° error, so the actuator is part of a feedback loop. Examples: servo motors turn robot joints, solenoid valves open drip lines, a relay switches a boiler, a pump delivers insulin, and a car's steering motor and brakes carry out the AI's driving decisions. Without actuators, the AI's decisions would never change anything in the real world.

**Key points:** definition; decision → driver circuit → actuator → physical change; at least one example; sensor feedback lets the system correct errors.

### Question 4 — Humans and AI

**(a)** Human-AI interaction (HAI) is the ways humans communicate and interact with AI-powered systems. It differs from traditional human-computer interaction (HCI) in three ways:

| | Traditional HCI | Human–AI interaction |
|---|---|---|
| Behaviour | fixed: same input, same output | adapts to what it senses and learns |
| Human's role | operator giving every command | supervisor setting goals and checking |
| Unclear input | shows an error | makes a best guess, which may be wrong |

Example: driving a manual car is HCI; supervising a self-driving taxi is HAI. Because an AI can act on its own and can be wrong, HAI also needs the right level of trust: neither over-trust nor under-trust.

**(b)** The main challenge is confusion: if the user cannot see what the system is doing or why, they cannot predict its next action. They may over-trust it (a Level 2 driver stops watching the road) or under-trust it (switches off a useful safety feature), and if the system suddenly hands back control they may react too slowly or wrongly. On Air France Flight 447 in 2009, ice blocked the airspeed sensors, the autopilot handed control to pilots who did not understand why, and their confused responses led to a fatal crash. Automation must show clearly what it is doing and why, and warn the human early.

**Key points:** names the challenge (confusion, over-trust or under-trust, an unsafe handover); explains the effect on safety or usability; an example; a fix (clear status, explanations, early warnings).

**(c)** The screen should show why the AI raised the alert, not just "High risk". Put the risk level and the AI's confidence at the top, then the evidence, each item with its value, the normal range, its trend (a small chart) and the time it was measured, most important first. Add one-tap buttons to accept or reject the advice (with a reason, which also gives the system feedback) and a link to the full record. The doctor still makes the decision.

Three pieces of evidence (one good set):
1. **The vital signs that triggered the alert, with their trend:** e.g. heart rate rising from 92 to 125 beats per minute over three hours, blood pressure falling, fast breathing, high temperature.
2. **Supporting test results:** e.g. a raised blood lactate level or white-cell count, compared with the normal range.
3. **The AI's confidence and the main factors behind it:** e.g. "87% risk; main factors: falling blood pressure, rising lactate".

Also acceptable: what has changed since the last check, the patient's usual readings for comparison, and a warning about missing or out-of-date data.

### Question 5 — Ethics and society

**(a)** Ethical AI is the development and use of AI in ways that are fair, responsible and transparent. In complex smart systems each pillar is hard to keep:
- **Fairness** (people and groups are treated equally): AI learns from past data and repeats any bias hidden in it. In 2020 an algorithm used to award A-level grades in England lowered about 4 in 10 of teachers' predicted grades, and students at large state schools lost out more than those at private schools.
- **Transparency** (people can find out how a decision was made): many AI systems are black boxes whose outputs come from millions of calculations that even their developers cannot easily explain, and learning systems keep changing.
- **Accountability** (someone is clearly responsible when things go wrong): a hardware maker, software developer, network provider and user all play a part, so it is hard to say who is to blame. The law is only beginning to answer this: under the UK's Automated Vehicles Act 2024, the company is responsible while its approved self-driving system is driving.

**Key points:** definition; one reason for each pillar; at least one real example.

**(b)** **Opportunity:** resource optimisation, e.g. smart water networks find leaks so less clean water is lost, adaptive traffic signals shorten queues and cut pollution, and a smart grid balances demand using stored solar energy. **Risk:** every connected device is a possible way in for an attacker, and many cheap devices ship with weak or default passwords: in 2016 the Mirai malware took over hundreds of thousands of cameras and routers and used them in an attack that made websites such as Twitter and Netflix hard to reach for hours. Also acceptable as the risk: privacy, because city sensors collect data constantly about where people go, which could be stolen, sold or misused.

### Question 6 — Smart homes

**(a)**

| Device | One sensor | One actuator or output |
|---|---|---|
| Learning thermostat | temperature sensor | relay that switches the boiler on and off |
| Smart door lock | magnetic contact sensor (door open or shut) | motor that moves the bolt |
| Security camera | camera (image sensor) | speaker or siren that sounds an alarm |

Also acceptable: a PIR motion sensor in the thermostat or camera; a keypad or fingerprint reader on the lock; a microphone in the camera; the camera's alert and video sent to the phone app as its output.

**(b)** The thermostat treats every manual change as feedback. Each time the family changes the temperature, it records the day, the time and the setting. When it spots a pattern, e.g. the heating turned up from 17 °C to 21 °C at about 06:30 on weekdays, it changes its own schedule and starts heating earlier, at 06:00, so the house is warm when they get up. If the family corrects it, the correction works like a penalty for its last choice and the schedule shifts again; a day with no corrections suggests it got things right, so it keeps that schedule.

**Key points:** records manual changes; spots a pattern; adjusts its schedule by itself; corrections act as penalties, and no corrections confirm the schedule.

**(c)** Two steps (one good answer):
1. **Change every default password** to a strong, unique one and turn on two-factor authentication for the apps. Attackers try factory passwords automatically: this is how Mirai took over hundreds of thousands of devices.
2. **Install software (firmware) updates** as soon as they are released, or turn on automatic updates, because updates fix security holes that attackers use.

Also acceptable: use encryption (secure WPA2 or WPA3 Wi-Fi, encrypted video); put smart devices on a separate guest network; choose devices that collect only the data they need; turn off remote features that are not used.

### Question 7 — Healthcare

**(a)** The watch's **optical heart-rate sensor** (green LEDs and a light sensor) measures the heart rate throughout the day, its **ECG sensor** records the heart's electrical signal to check the rhythm, and its **accelerometer and gyroscope** track activity and sleep and detect a hard fall. The watch processes these readings itself and sends summaries over **Bluetooth** to the phone, which uploads them, encrypted, over the **mobile network** (or home Wi-Fi and the internet) to the clinic's dashboard. The doctor can follow trends over days and weeks, and the system flags unusual readings, e.g. a very fast or irregular heartbeat, so a nurse can phone the patient that day instead of the patient arriving at hospital later as an emergency. After a hard fall, the watch can call the emergency services if the wearer does not respond.

**Key points:** at least two named sensors; Bluetooth and the mobile network; processing on the watch; the doctor reviews trends or receives an alert; problems are caught early.

**(b)** It is a feedback loop. A glucose sensor measures the blood sugar every few minutes and sends the reading over Bluetooth to an algorithm, which decides the insulin dose, and the pump delivers it. The next reading shows how the body responded to that dose, and the algorithm uses this result to choose the next dose and, over time, to learn this person's insulin needs. So the dose is not fixed: it changes according to the measured results. It is called hybrid because the user still enters meals.

**Key points:** sensor → algorithm → pump → new reading; each result changes the next dose; it learns the person's needs over time.

### Question 8 — Transportation

**(a)** In fog, a driver cannot see the car ahead braking until it may be too late. With V2V, the car ahead that brakes hard sends a wireless message (its position, speed and "hard braking") to the vehicles around it. The message arrives in milliseconds, even at cars several vehicles back that cannot see it, and the car behind warns its driver at once (or brakes automatically). Braking starts sooner, so the car travels less distance before braking begins: at 90 km/h (25 m/s), each second saved is 25 m. That can be the difference between stopping in time and a crash.

**Key points:** the braking car broadcasts a warning; it arrives in milliseconds and does not need a clear view; the car behind warns or brakes earlier; less distance travelled before braking.

**(b)**
- **Level 2 (partial):** the car steers and controls its speed at the same time (e.g. lane-keeping plus adaptive cruise control), but the human is still the driver: they must watch the road constantly and be ready to take over immediately.
- **Level 4 (high):** the car drives itself within a defined area, e.g. a driverless taxi in part of a city. Inside that area the human is not needed to drive or watch the road; outside it, the car cannot drive itself.
- **The key difference:** at Level 2 the human is responsible for watching the road; at Level 4 the system is responsible inside its area.

### Question 9 — Industry and manufacturing

**(a)** One good set:
- **State:** a camera image showing the parcel's position, size and orientation; the arm's joint angles from its encoders; whether the gripper is holding the parcel; the free space on the conveyor belt.
- **Action:** move or rotate the arm, open or close the gripper, place the parcel.
- **Reward:** +20 when a parcel is placed correctly on the belt.
- **Penalty:** −100 for hitting a shelf, the belt or a person (also −30 for dropping a parcel and −1 for each second taken).

**(b)** Reward table (own values; any sensible table is acceptable):

| Event | Reward |
|---|---|
| parcel placed on the belt | +20 |
| each second taken | −1 |
| parcel dropped | −30 |
| collision with a shelf, the belt or a person | −100 |

- **Slow, safe move:** 10 s, parcel placed. Total = +20 − (1 × 10) = **+10**
- **Fast move that hits a shelf:** 4 s, parcel placed, one collision. Total = +20 − (1 × 4) − 100 = **−84**
- The safe move scores +10 − (−84) = **94 more**, so even though it is 6 s slower, the robot learns to prefer it. This works because the collision penalty (100) is much larger than the reward for the seconds saved (6 × 1 = 6).

**(c)** The robot learns exactly what it is rewarded for, not what people meant. Rewarded for speed only, it would learn to rush: throwing or dropping parcels, damaging goods, and crashing into shelves, the belt or people, because nothing in its reward says these are bad. It might even end each attempt as quickly as possible without placing the parcel properly. For example, with +1 for every second under 15 s, the 4 s crash earns 15 − 4 = 11 and beats the safe 10 s move, which earns only 15 − 10 = 5. The fix is to reward correct placement, penalise drops and collisions, practise in simulation, and keep safety limits such as emergency stops that never depend on the reward.

**Key points:** the AI optimises the reward it is given; rushing, drops, damage, collisions, injuries; a speed-only reward can make crashes score higher; balanced rewards, simulation and fixed safety limits.

### Question 10 — Education

**(a)** The app runs a feedback loop: **ask** a question → **observe** whether the answer is right or wrong → **update** its estimate of what the student seems to know → **choose** the next question. If the student is doing well, it gives harder questions; if they are struggling, it gives easier ones, a hint or a review. A simple app uses a fixed rule, e.g. 3 right in a row → up one level, 2 wrong in a row → down one level with a hint. A learning app uses thousands of students' results to find which question helps most, rewarded when a learner gets a similar question right a week later. Feedback flows both ways: the student's correct answers are reinforced at once, as with Skinner's teaching machines, and the system learns whether its question was too easy, too hard or just right.

**Key points:** ask → observe → update → choose; difficulty goes up or down with performance; fixed rule versus learning from rewards; feedback both ways.

**(b)**
- **Fairness concern:** an algorithm can repeat bias hidden in past data and treat groups unequally: in 2020 the A-level grading algorithm in England lowered about 4 in 10 of teachers' predicted grades, and students at large state schools lost out more than those at private schools. Also acceptable: an app that decides early that a student is weak may keep them on easy work; students without a good device or internet access at home fall behind.
- **Privacy concern:** adaptive systems record every answer and mistake (and school devices have cameras and microphones), so children's data could be stolen, shared or misused. Schools must protect it, collect only what they need and tell students and parents what is kept.

### Question 11 — How the technologies shape everyday life

In every setting the pattern is the same: hardware senses the world and changes it, networks carry information, and behaviourist AI chooses actions and improves them from feedback.
- **Smart home:** a learning thermostat's temperature sensor and relay (hardware) connect over Wi-Fi or Zigbee (network), and it learns the family's heating times from their corrections (behaviourist AI). The house is warm when they wake and empty rooms are not heated, saving energy. But every connected device is a way in for attackers, as Mirai showed, and its data reveal when the house is empty.
- **Transportation:** cameras, radar and lidar sense the road, and motors steer and brakes stop the car; V2V, V2I and 5G connect vehicles and signals. Adaptive signals share the green time to match the queues (45 s instead of 30 s for the busy road), and signals trained with rewards for short queues learn better timings still. At 108 km/h, deciding on the car's own computer instead of over a slow cloud link means travelling 0.15 m instead of 15 m before braking begins. This saves time, fuel and lives, but over-trust, black-box decisions and the question of who is responsible are real problems.

**Evaluation:** together the three technologies make everyday life safer, more convenient and less wasteful, usually without people noticing. But the benefit depends on every part working: without sensors the system is blind, without a network it is cut off, and without intelligent software it cannot adapt. It also depends on good design: safety-critical decisions at the edge, strong security and data protection, and AI that is fair, transparent and accountable. Not every "smart" system learns (many follow fixed rules), and people still choose the goals and rewards these systems learn from, so people remain responsible for them. Overall the effect is mainly positive, but only where these safeguards are in place.

**Key points:**
- examples from at least two settings, each naming its hardware, network and AI;
- the sense → connect → decide → act feedback loop;
- benefits with evidence (safety, efficiency, convenience, saving resources);
- drawbacks (security, privacy, fairness, transparency, accountability, dependence on networks);
- a balanced, justified conclusion.
