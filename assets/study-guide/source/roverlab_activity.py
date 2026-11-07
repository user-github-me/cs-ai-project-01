"""Optional game activity shared by the ebook and Markdown content."""
ACTIVITY = '''# ROVERLAB — Build, Connect, Train

**Interactive companion:** [Play ROVERLAB](https://roverlab-blue-impulse.vercel.app)

**Provider:** Blue Impulse. **Time:** approximately 5–10 minutes per experiment. **Preparation:** read Chapter 2 — Behaviorism & Behaviorist AI, Chapter 3 — Hardware, and Chapter 4 — Networking; use Chapter 5 — Applications to connect the systems. No programming experience or account is required.

## Your challenge

Build an exploration rover that can sense obstacles, visit a research site, send its findings to base and return. Predict how one changed component or response will affect the mission, then compare the prediction with the event log and results.

1. Choose Exploration rover. In Hardware, inspect the processor, memory, motors, wheels or tracks, sensors and power supply. You may try the starter build, then inspect what each part contributes. Remove the distance sensor once: read why sensing or mission readiness changes, then restore it.
2. Add a radio module and connect the base station. Run the network test. Explain why a connected base station is a different role from the robot's processor.
3. Train at least three rules: obstacle detected → stop, then turn; destination reached → return to base; low battery → return to base. Test a stimulus and give feedback. Compare competing associations by strength and order. The research sensor collects its reading at the site and queues it for transmission through your actual network route; the destination rule tells the drive system to return.
4. Select Survey & return. Resolve the readiness findings, then launch. Pause or step through an obstacle event. Identify the sensor observation, selected rule, actuator action and later packet transmission.
5. Record the result and four scores. Return to training and replace obstacle → stop, then turn with obstacle → move / run. Predict the outcome before launching again. Compare the actual event evidence rather than only the total score.

## Observe, explain and extend

Record two rows: configuration, prediction, observed event, result, and explanation. Which component detected the obstacle? Which rule selected the response? What made the wheels move? Which route delivered the report? Why can a compatible rule still be unhelpful?

Expected reasoning: an appropriate sensor makes the obstacle observable; the processor selects a supported rule; the drive system carries out the command. Continuing toward the obstacle can cause a collision. A module alone does not establish a usable route, and a route that works at the start may fail as the robot moves. Feedback changes which competing association wins; it does not make an unsafe command safe or supply missing hardware.

For another experiment, use Search & assist to combine person sensing and a control computer, or Monitor & protect to detect high temperature, stop the process and send a server alert. Chapter 6 — Strengths & Limitations helps explain why a successful toy mission is insufficient evidence for a real autonomous deployment.

## Access and offline alternative

Open the link in a modern desktop or mobile browser. After a complete first visit, the local game cache supports offline reloads where service workers are available. Progress is saved in this browser; private browsing or blocked storage can limit persistence. The repository also provides a source ZIP that can be extracted and opened at public/index.html without internet: https://github.com/user-github-me/cs-ai-project-01/tree/main/apps/roverlab

If the game cannot load, draw this trace on paper: obstacle → distance sensor → processor selects rule → motor response → research reading → radio link → base. Compare stop-and-turn with continuing forward; remove the sensor or radio and mark the exact missing link. This supplies the same core reasoning task without the website.

ROVERLAB uses explicit player-authored stimulus–response associations and simplified feedback. It is not a neural network or a full reinforcement-learning trainer. Range, power and environmental values are fictional teaching values. The source and automated checks are public; a student or teacher playtest remains separate evidence.
'''
