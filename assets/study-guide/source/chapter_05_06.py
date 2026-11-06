def add_chapters(P,B,T,D):
    P(5,'smart-system','A system that senses and acts',[
      B('Combine the parts','An integrated smart system connects physical hardware, communication and software to carry out a useful task. Sensors collect information; processing interprets it and selects an output; actuators change the world. A network lets components exchange data or use remote services. Some systems use fixed rules, some use learned models, and some combine both.'),
      D('Follow one complete workflow',['Sense','Communicate','Decide','Act'],'The changed environment supplies the next observation. The communication step may be local, remote or partly unnecessary for a self-contained controller.',kind='loop'),
      B('Use the body analogy carefully','Sensors resemble senses, actuators resemble muscles and communication links resemble nerves. Software coordinates the response. This is an analogy for the roles, not a claim that the machine has a human mind. Explain the actual mechanism: what is measured, what message is sent, what computation runs and what physical output follows.')
    ],'5.1','5.1–5.3')

    P(5,'smart-irrigation','Example: an irrigation system',[
      T('Trace the flow of information',['Stage','Illustrative design'],[['Measure','Soil-moisture sensors report readings and timestamps.'],['Communicate','A low-power network sends readings to a local gateway.'],['Decide','A controller selects a watering action using targets and constraints.'],['Act','A driver energises a valve; later readings show the effect.']]),
      B('Add learning only when it has a role','A fixed threshold can open a valve when soil is dry. A learned policy might instead use moisture, recent rain and other state variables to trade off water use and crop needs. Reinforcement learning would require a defined reward and a process for updating the policy from experience. Merely connecting a sensor to Wi-Fi does not make the system learn.'),
      B('Check assumptions before action','Sensors can drift; messages can arrive late; a valve can fail. Timestamp readings, detect implausible values and monitor the effect of each action. A real deployment needs domain-specific limits and testing. This example explains an architecture rather than prescribing watering durations for a particular crop.')
    ],'5.3b','5.3')

    P(5,'real-time','Real-time means meeting a deadline',[
      B('Correctness includes timing','A real-time system must produce the required response within a specified deadline. “Real-time” does not simply mean very fast. Missing a hard deadline can make a system fail its requirements; missing a soft deadline reduces service quality. Batch work, such as a monthly report, usually has different timing needs.'),
      T('Illustrative delay distance at 30 m/s',['Delay before response','Distance travelled'],[['500 ms = 0.500 s','30 × 0.500 = 15 metres'],['50 ms = 0.050 s','30 × 0.050 = 1.5 metres'],['5 ms = 0.005 s','30 × 0.005 = 0.15 metres']]),
      B('Interpret the calculation correctly','Distance during delay = speed × delay. This is only the distance travelled before a response begins, not total stopping distance. Sensing, processing, communication, actuation and physical braking all contribute to a real system. Moving a critical computation locally removes some communication delay, but it does not guarantee a particular safe outcome.')
    ],'5.2a','5.4')

    P(5,'networked-ai','Networking for a behaviour-based agent',[
      B('Separate the fast loop from shared services','A useful architecture keeps time-critical sensing, policy evaluation and actuator control near the device. A network can carry telemetry, coordinate multiple devices or distribute reviewed model updates. Training may occur centrally while a fixed policy runs locally. A system can continue its local task during a link outage only if it was designed to do so.'),
      D('Two connected responsibilities',['Device: observe / act','Network: data + updates','Server: analyse / train'],'Local action does not have to wait for every cloud exchange. This is an architectural choice, not a property of all AI systems.',kind='bidirectional'),
      B('Make messages interpretable','Include a device identity, timestamp, sequence number, units and model or policy version where needed. Reject stale or unauthorised commands. Delayed feedback must be associated with the action that produced it before a learning update is made. Network loss can reduce the evidence available for training; it should not silently become a reward of zero.')
    ],'6.5','5.3, 5.5, 5.8')

    P(5,'automation','Automation changes work and errors',[
      T('A spectrum of responsibility',['Mode','Who does what?'],[['Manual','A human performs the task directly.'],['Assistance','The system supports selected actions or provides alerts.'],['Partial automation','The system handles parts of the task; the human supervises.'],['Higher autonomy','The system acts within a defined operating domain.']]),
      B('Benefits depend on the setting','Automation can improve repeatability, throughput and availability for suitable work. It can also shift errors from isolated human mistakes to systematic software, sensor or model failures affecting many operations. Do not assume that automation gives zero errors, unlimited uptime or a fixed percentage improvement.'),
      B('Keep the operating domain explicit','A warehouse robot may work well on a mapped, maintained floor but fail on an unfamiliar surface. A human must understand what the system can handle, what it cannot handle and how a handover works. Formal driving-automation levels describe a specific domain; they should not be treated as a universal ladder for every smart appliance.')
    ],'5.2b','5.6–5.7')

    P(5,'policy-feedback','Feedback can change a policy',[
      B('Describe the learning mechanism','An RL agent collects transitions: a state, an action, a reward and a next state. A learning algorithm uses those transitions to update values or policy parameters. A positive reward does not mechanically guarantee that an action becomes more likely in every algorithm; updates depend on the method and its estimates of future return.'),
      T('Design an illustrative delivery task',['Element','Possible definition'],[['State','Location, remaining energy and relevant obstacle information.'],['Action','Choose a permitted move.'],['Reward','Score progress and successful completion; penalise undesirable outcomes.'],['Constraint','Disallow unsafe actions even if a reward would favour them.']]),
      B('A deployment may stop learning','A trained policy can be evaluated repeatedly on new observations without changing its parameters. Online learning requires a controlled update process and evidence that changes improve performance. Separate “the action changed because the observation changed” from “the policy changed because the agent learned”.')
    ],'5.3a','5.8')

    P(5,'actuators','Turn a decision into an action',[
      D('A command needs an execution path',['Policy output','Controller','Power driver','Actuator'],'Feedback from position, current or other sensors can confirm whether the requested action happened.'),
      T('Different physical outputs',['Actuator','Example role'],[['Electric motor / servo','Rotate a wheel or position a joint.'],['Solenoid valve','Open or close a fluid path.'],['Hydraulic actuator','Produce force using pressurised liquid.'],['Pneumatic actuator','Produce movement using compressed air.']]),
      B('Distinguish information from energy','A software value such as “target angle = 15 degrees” is information. Interface electronics convert it into a suitable control signal; a powered mechanism supplies the force. Some systems use analogue voltages, others PWM or digital commands. A DAC alone normally cannot supply motor power. Mechanical limits, response time and feedback all affect whether an intended action is achieved.')
    ],'5.3b','5.9')

    P(5,'human-ai','Help people understand the system',[
      B('Human-AI interaction is part of HCI','Human-computer interaction studies how people use computing systems. Human-AI interaction focuses on challenges raised by AI, including uncertainty, adaptation, delegation and trust. It is not a strict division between deterministic old interfaces and always-probabilistic new ones. The important question is what the person needs to understand and control.'),
      T('Useful interface information',['Show','Why it helps'],[['Current mode and operating limits','The user knows what the system is doing.'],['Relevant evidence and uncertainty','The user can judge an output appropriately.'],['Planned action and reason','The next behaviour is less surprising.'],['Override, handover and recovery','The user can respond when the system cannot continue.']]),
      B('Avoid over-trust and under-trust','Unclear automation can cause misuse through excessive reliance, or disuse when useful assistance is rejected. A handover should communicate the state of the task and why control is changing. A confident-looking score is not enough: the interface should support an informed decision and an appropriate human response.')
    ],'5.4b','5.10–5.11')

    P(5,'ethical-ai','Evaluate more than performance',[
      T('Three important ethical concerns',['Concern','Design question'],[['Fairness','Who benefits, who is disadvantaged, and how was this measured?'],['Transparency','Can affected people understand the system’s role and limitations?'],['Accountability','Who is responsible for deployment, oversight and correction?']]),
      B('Reward design can encode priorities','A reward that values only throughput can encourage neglect of other goals. Historical data can contain unequal representation or biased decisions. Evaluate outcomes across relevant groups and situations rather than assuming an algorithm is neutral because it uses numbers. The appropriate criteria depend on the task and the people affected.'),
      B('Make responsibility practical','Document the intended use, data sources, limitations and monitoring process. Provide channels to question or correct consequential outcomes. Ethical and legal requirements vary by context and jurisdiction; no single checklist proves a system is responsible. For high-stakes uses, performance testing and meaningful human oversight are essential parts of the deployment decision.')
    ],'5.5a','5.12')

    P(5,'smart-cities','Opportunities bring responsibilities',[
      T('Illustrative connected applications',['Application','Opportunity','Risk to consider'],[['Traffic signals','Respond to changing demand.','Unsafe control or unequal service.'],['Water monitoring','Detect leaks and reduce waste.','Faulty sensors or unauthorised commands.'],['Street lighting','Adjust lighting to local need.','Privacy, coverage and maintenance.'],['Connected health monitoring','Support timely review of measurements.','Sensitive data and incorrect alerts.']]),
      B('Measure outcomes, not just activity','More sensor readings or more automated actions do not necessarily mean better service. Compare meaningful outcomes such as resource use, reliability, accessibility and user experience. Any claimed improvement needs evidence from the particular deployment; percentages from an unspecified example are not general guarantees.'),
      B('Every connected device adds responsibilities','Connected cameras, locks, sensors and controllers need updates, access management and appropriate data protection. Minimise unnecessary personal data, limit retention and protect communication. Consider what happens if a device is compromised or the network is unavailable. Convenience should be assessed alongside maintainability, privacy and safe operation.')
    ],'5.5b','5.13–5.15')

    P(6,'system-tradeoffs','Judge the whole system',[
      T('Strengths and limitations interact',['Part','Strength','Limitation'],[['Hardware','Senses, computes and acts locally.','Power, heat, memory and physical reliability.'],['Networks','Share resources and coordinate devices.','Delay, loss, availability and security.'],['AI / control software','Selects actions and may learn from experience.','Model errors, limited evidence and unclear objectives.']]),
      B('There is no universally best architecture','Choose a design for its task, operating conditions and consequences of failure. A model with excellent offline accuracy may be unsuitable if it misses a deadline or requires too much memory. A highly connected system may be fragile if local operation depends on one remote service. A simple fixed-rule controller can be appropriate for a well-defined task.'),
      B('Make the comparison explicit','State the intended outcome, identify constraints, compare options and define measures for success. Evaluate the combination of hardware, networking, algorithms and human operation. A component’s specification is useful evidence, but it is not proof that the complete application meets its requirements.')
    ],'6.5','6.1, 6.9')

    P(6,'hardware-limits','Four physical budgets',[
      D('Every device has limits',['Power','Heat','Memory','Processing'],'A design must fit all four budgets, not just the model’s arithmetic requirement.',kind='tiles'),
      T('Understand the constraint',['Budget','What can go wrong'],[['Power','A battery drains too quickly for the required mission.'],['Heat','Thermal throttling reduces sustained performance.'],['Memory','Weights, inputs or intermediate results do not fit.'],['Processing','An inference or control computation misses its deadline.']]),
      B('Optimise with evidence','A smaller model, quantised representation, reduced input resolution or lower update rate can reduce cost, but may change accuracy or responsiveness. Measure the resulting behaviour. Dedicated accelerators can improve efficiency on supported workloads, but data conversion, memory movement and idle power remain relevant. Local computing removes a remote round trip; it does not mean zero total latency.')
    ],'6.1','6.2')

    P(6,'sensor-reliability','Reliable decisions need reliable inputs',[
      B('Sensors are imperfect','Noise creates random variation; drift changes a sensor’s behaviour over time. Obstruction, calibration error or environmental conditions can produce misleading observations. Sensor fusion combines information from multiple sources, often after time alignment and filtering. Different sensors can have complementary strengths, but they can also share common failure causes.'),
      D('A fusion pipeline',['Camera / range / motion','Align + check','Combine evidence','State estimate'],'Do not combine incompatible units or measurements from different times as if they described the same instant.'),
      B('Define reliability under conditions','Reliability concerns performing an intended function for a stated period under stated conditions. MTBF is a statistical measure for repairable systems, not a promise that a particular unit cannot fail earlier. Monitor drift, error rates, temperature and data quality. Redundancy can help when failures are sufficiently independent and the system can recognise and manage disagreement.')
    ],'6.1','6.3')

    P(6,'scalability','Grow without losing coordination',[
      T('Three network qualities',['Quality','Meaning'],[['Scalability','Handle more devices or work at acceptable performance.'],['Interoperability','Exchange data and use it correctly across different systems.'],['Resilience','Maintain or recover an acceptable service during disruption.']]),
      B('Capacity is only one part of scaling','Adding hundreds of IoT devices can increase addressing, authentication, message traffic, storage and maintenance work. Agree on data formats, units, timestamps and interface versions as well as the physical link. Two products using Wi-Fi do not automatically interpret one another’s messages correctly.'),
      B('Plan for failures','Redundant links, retry policies, local buffering and controlled reconnection can improve resilience. A mesh can route around some failures when an alternative path exists and the protocols support it. It does not guarantee communication through every outage. Test overload and partial failure, not just the normal case with every device online.')
    ],'6.2','6.4')

    P(6,'edge-cloud','Put each computation where it fits',[
      T('Three deployment patterns',['Location','Benefit','Cost or limit'],[['On-device edge','Low communication delay; local data.','Limited local resources and maintenance.'],['Nearby gateway / fog','Aggregates local devices.','Another service to size and manage.'],['Remote cloud','Shared compute and flexible capacity.','Network dependency, latency and transfer cost.']]),
      B('An illustrative warehouse design','Each robot handles immediate motion control locally. A shared service allocates tasks and coordinates inventory. Robots send selected telemetry and receive authorised updates. If the coordination service is unavailable, the design defines whether a robot pauses, completes a limited task or enters another safe state; continued operation must not be assumed.'),
      B('Optimise across the whole path','Compare local compute energy with transmission energy, available bandwidth, deadlines, privacy and model capacity. Summarising data locally can reduce transfer volume. Centralised analysis can reveal patterns across devices. The useful decision is which part of the workload belongs where, not whether edge or cloud is always superior.')
    ],'6.5','6.5')

    P(6,'prediction-behaviour','Predict an outcome or model behaviour?',[
      T('Two useful questions',['Predictive analytics','Behavioural modelling'],[['What is likely to happen?','How does an agent or system behave?'],['Forecasts, scores or probability estimates.','Rules, transitions, trajectories or action patterns.'],['Example: estimate a component’s failure risk.','Example: model a robot’s response to an obstacle.']]),
      B('The approaches can overlap','A behavioural model can be used to make predictions, and predictive features can inform an action policy. They are not mutually exclusive categories defined by one kind of data. Choose the model and evaluation method based on the question being asked and the evidence available.'),
      B('Adaptation is not guaranteed generalisation','Adaptive intelligence describes changing behaviour appropriately using new information or experience. Autonomy describes operating with limited direct human control. An autonomous device may use a fixed policy; an adaptive model may still need supervision. Performance in familiar conditions does not prove reliability in a new environment.')
    ],'6.4','6.6–6.7')

    P(6,'explainability','Understand why a policy acted',[
      B('Explainability is a practical capability','Explainability concerns making relevant aspects of a model’s behaviour understandable to people. A small rule set or Q table may be inspectable. A deep RL policy can be harder to interpret because many parameters contribute to each output. Complexity does not mean analysis is impossible, but a simple story about one decision may be incomplete or misleading.'),
      B('Look beyond one successful outcome','Inspect representative cases, counterexamples, changed conditions and failure logs. Separate a faithful explanation of the computation from a plausible narrative generated after the fact. An explanation does not establish that the action was correct; validation requires evidence about outcomes and requirements.'),
      B('Reward errors and bias','An agent rewarded only for speed may neglect an important constraint. Training environments can under-represent some conditions or groups. Distribution shift can reduce performance when deployment differs from training. Track both overall performance and relevant subsets. Correcting a reward or dataset requires re-evaluation of the resulting policy.')
    ],'6.6','6.8')

    P(6,'responsible-deployment','Balance benefit, risk & oversight',[
      T('Questions for a deployment review',['Area','Evidence to seek'],[['Security','Authenticated updates, restricted access and recovery plans.'],['Privacy','Necessary data collection, appropriate retention and access.'],['Fairness','Evaluation across relevant people and conditions.'],['Accountability','Named responsibilities, review and correction routes.'],['Reliability','Measured deadlines, failure handling and monitoring.']]),
      B('Physical effects raise the stakes','A connected controller can change the physical world, so a corrupted measurement or unauthorised command may have consequences beyond a damaged file. Protect sensor inputs, model updates and actuator commands according to the task. Test how the system responds to missing, stale and contradictory data.'),
      B('Finish with a justified judgement','State the benefit you expect, the evidence supporting it, the conditions under which it applies and the remaining limitations. Decide what a human must monitor or approve and how the system should respond when its assumptions fail. The strongest design is the one suited to its purpose, with limitations that are understood and managed.')
    ],'6.7','6.9')
