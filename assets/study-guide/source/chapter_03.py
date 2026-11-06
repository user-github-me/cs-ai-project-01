def add_chapter(P,B,T,D):
    P(3,'hardware-roles','Hardware gives software a body',[
      B('Classify by the job being performed','Hardware is the physical part of a computer system. An input device supplies data, a processing device transforms it, an output device communicates or acts on a result, and storage retains information. One device can have several roles: a touchscreen displays output and senses input. A barcode reader is input; an SSD is storage.'),
      D('From a physical event to a response',['Sensor / input','Processor + memory','Output / actuator'],'The processor follows instructions. Useful behaviour depends on the program, the data, the hardware and their connections.'),
      B('How hardware enables AI','An AI model must run as computations on hardware. Sensors provide observations, memory holds model parameters and working data, a processor evaluates the model, and an output device communicates the decision. A physical robot also needs a powered actuator to move. More powerful hardware can increase capacity or speed, but does not itself create a learning algorithm.')
    ],'3.3','3.1–3.3')

    P(3,'memory-hierarchy','Memory: capacity versus speed',[
      T('A useful hierarchy',['Resource','Role and trade-off'],[['Registers','Very small, very fast storage inside the processor.'],['Cache','Fast memory holding copies of recently or frequently used data.'],['Main RAM','Working storage for active programs and data; normally volatile.'],['Secondary storage','Larger, persistent storage; usually slower to access.']]),
      B('SRAM and DRAM','Static RAM stores bits using bistable circuits such as flip-flops. It needs power but no periodic refresh, and is commonly used for CPU caches. Dynamic RAM stores charge in cells that must be refreshed; its greater density and lower cost make it suitable for main memory. Both are volatile. Cache can be on the processor chip; it is not necessarily external.'),
      B('Why an AI workload needs memory','Model weights, input data and intermediate results must fit somewhere. A fast processor can spend time waiting for data if memory bandwidth is insufficient. Capacity answers “how much fits?” Bandwidth answers “how quickly can it move?” These are different constraints and both affect performance.')
    ],'3.2a','3.2')

    P(3,'rom-storage','Keep data when power is off',[
      T('ROM and flash families',['Type','Writing or erasing'],[['Mask ROM','Programmed during manufacture.'],['PROM','Programmed once after manufacture.'],['EPROM','Erased with ultraviolet light, then reprogrammed.'],['EEPROM','Electrically erasable and reprogrammable.'],['Flash','Electrically erasable memory, normally erased in blocks.']]),
      B('Magnetic, solid-state and optical media','A hard disk stores data magnetically on rotating platters. Seek time and rotational latency delay access; fragmentation can increase head movement. An SSD stores data in flash with no moving parts. It avoids mechanical seek and rotation delays, but still has nonzero access latency and finite write endurance. External drives can provide portable backup storage.'),
      B('Optical storage','CDs, DVDs and Blu-ray discs use laser light to read recorded features. Some discs have multiple recording layers. Material defects and optical effects, including birefringence, can disrupt reading. Choose a medium using capacity, access time, cost, durability and the need for long-term retention rather than assuming one technology is best for every purpose.')
    ],'3.2b','3.2')

    P(3,'risc-cisc','Processor instruction-set choices',[
      T('Introductory design tendencies',['RISC','CISC'],[['Regular, often simpler instruction encodings.','Can include more complex and variable-length instructions.'],['Typically separates loads/stores from register arithmetic.','May allow operations with memory operands.'],['Examples include ARM and RISC-V families.','A major example is the x86 family.']]),
      B('The distinction is not a speed guarantee','A reduced instruction set does not guarantee that every instruction takes one clock cycle. A complex instruction set does not prevent pipelining or high performance. Modern processors use caches, pipelines, prediction and other techniques; many translate instructions internally into simpler operations. Some RISC families also support compressed instruction encodings.'),
      B('Look at the workload','Performance depends on implementation, clock frequency, instructions per cycle, memory behaviour, software and energy constraints. A mobile device may prioritise power efficiency; a workstation may prioritise throughput. Compare measured work done under relevant conditions instead of judging a CPU from the RISC or CISC label alone.')
    ],'3.5a','3.1')

    P(3,'pipeline','Overlap work with a pipeline',[
      B('Use the laundry analogy','A laundry can wash one load while drying an earlier load. Similarly, a processor pipeline can fetch a new instruction while decoding or executing previous ones. This increases throughput after the pipeline fills; it does not necessarily reduce the latency of an individual instruction. Pipelining is used in both RISC and CISC implementations.'),
      T('A simplified four-stage pipeline',['Instruction','Cycle 1','2','3','4','5'],[['I1','Fetch','Decode','Execute','Write','—'],['I2','—','Fetch','Decode','Execute','Write'],['I3','—','—','Fetch','Decode','Execute']]),
      B('Why a pipeline can pause','A data hazard occurs when an instruction needs a result that is not ready. A control hazard occurs when a branch makes the next instruction uncertain. A structural hazard occurs when operations need the same resource. Stalling, forwarding, scheduling and prediction can help, depending on the processor. “Overlapping” does not mean every instruction is independent.')
    ],'3.5b','3.1')

    P(3,'parallel','One stream or many?',[
      T('Flynn’s classification',['Class','Instruction / data streams','Example idea'],[['SISD','Single / single','One instruction stream processes individual data.'],['SIMD','Single / multiple','One operation applied to many array elements.'],['MISD','Multiple / single','Rare; different processing of one data stream.'],['MIMD','Multiple / multiple','Independent cores or computers run different work.']]),
      B('Scale beyond one processor','A cluster connects computers, called nodes, so they can coordinate work. Massively parallel systems distribute large tasks across many processing units. Supercomputers are designed for demanding scientific or engineering computation; they are not simply a synonym for mainframes. Communication, synchronisation and data movement affect whether adding processors actually helps.'),
      B('Connect this to AI','Large arrays of multiplications can benefit from parallel hardware. Parts of an AI workload may still be sequential or limited by memory and communication. A GPU has its own execution model, often described using SIMT, and provides SIMD-like parallel arithmetic; the simple taxonomy is a starting point, not a complete description of every chip.')
    ],'3.5b','3.1')

    P(3,'hardware-interrupt','Let hardware request attention',[
      B('Events can change the schedule','A sensor, network interface or timer can raise an interrupt. The CPU responds when the request is enabled and eligible. It preserves enough context to resume the interrupted work and transfers execution to a handler. The handler deals with the event and returns. The hardware and operating system divide the responsibility for saving and restoring state.'),
      D('A simplified service sequence',['Event arrives','Preserve context','Run handler','Resume task'],'Context can include the program counter, status and required registers. Exact details vary by architecture.'),
      B('Predictability matters','A system with a timing deadline must account for interrupt priority, handler execution time and other sources of delay. RISC versus CISC alone does not determine interrupt latency. Long or frequent interrupt handling can delay useful work. A well-designed system measures worst-case behaviour rather than assuming every event will receive an immediate response.')
    ],'3.6','3.1')

    P(3,'logic-gates','Reason with logic gates',[
      B('Gates transform binary signals','AND produces 1 only when all inputs are 1. OR produces 1 when at least one input is 1. NOT inverts one input. XOR produces 1 when two inputs differ. NAND is the inverse of AND; NOR is the inverse of OR. A truth table lists every possible input combination and its corresponding output.'),
      T('Two-input truth table',['A','B','AND','OR','XOR','NAND','NOR'],[['0','0','0','0','0','1','1'],['0','1','0','1','1','1','0'],['1','0','0','1','1','1','0'],['1','1','1','1','0','0','0']]),
      B('Read symbols and conditions','NOT maps 0 to 1 and 1 to 0. An AND symbol has a flat input side and curved output side; an OR symbol has a curved input side and pointed output. A small output circle means inversion. In a control rule, “door closed AND start pressed” requires both conditions; “smoke OR manual alarm” requires either.')
    ],'3.7','3.4')

    P(3,'boolean-algebra','Simplify a logic expression',[
      T('Useful identities',['Law','Equivalent expressions'],[['Identity','A AND 1 = A; A OR 0 = A'],['Null','A AND 0 = 0; A OR 1 = 1'],['Idempotent','A AND A = A; A OR A = A'],['Complement','A AND NOT A = 0; A OR NOT A = 1'],['De Morgan','NOT(A AND B) = (NOT A) OR (NOT B)'],['De Morgan','NOT(A OR B) = (NOT A) AND (NOT B)']]),
      B('A worked simplification','Let X = (A AND B) OR (A AND NOT B). Factor out A: X = A AND (B OR NOT B). The term in brackets is always 1, so X = A AND 1 = A. A simpler equivalent circuit can reduce hardware and delay. Check equivalence by comparing truth-table outputs for every input combination.'),
      B('Keep the negation in the right place','De Morgan’s laws negate the whole grouped expression on the left. Dropping that outer NOT changes the meaning. Parentheses make the scope clear, especially when a printed overbar is difficult to see. In Boolean algebra, OR is not ordinary arithmetic addition: 1 OR 1 is still 1.')
    ],'3.7','3.4')

    P(3,'sensor-control','Sense, decide, act, sense again',[
      B('Monitoring versus control','A monitoring system records or displays measurements. A control system also acts on the environment. In a greenhouse, a temperature sensor supplies a reading, a processor compares it with a target, and a fan changes the temperature. A later measurement closes the feedback loop. This can be a fixed-rule controller; learning is not required.'),
      D('An environmental control loop',['Sensor','Input conversion','Decision','Driver + actuator'],'The changed environment is measured again. Analogue sensors may need an ADC; many sensors already provide digital data.',kind='loop'),
      B('Signals are not actuator power','An ADC converts an analogue signal to a digital value. A DAC converts a digital value to an analogue signal. Some actuators use PWM or digital interfaces instead of a DAC. PWM is a timed switching signal, not the same thing as analogue conversion. A motor driver or power stage supplies the current needed to move a motor or operate a valve.')
    ],'3.4','3.3')

    P(3,'embedded','Computing inside another device',[
      B('A dedicated purpose','An embedded system performs a particular role within a larger product, such as a washing-machine controller or a sensor node. A microcontroller typically combines a CPU, memory and input/output peripherals on one chip. An embedded system may use a microcontroller, a larger processor or specialised hardware, depending on its requirements.'),
      T('Benefits and constraints',['Potential benefit','Constraint to consider'],[['Compact, low-power operation.','Limited memory, processing capacity and battery energy.'],['Low cost for repeated tasks.','Upgrades and repairs may be difficult.'],['Predictable behaviour with careful design.','Timing and reliability must be tested, not assumed.'],['Local operation without a cloud link.','External data or remote management may still need a network.']]),
      B('Design around the task','A small fixed-rule controller may need only modest hardware. A vision model can require much more memory and computation. Choose sensors, processing capacity, interfaces and power together. Environmental temperature, moisture, vibration and expected service life also influence whether a design is suitable.')
    ],'6.1','3.3')

    P(3,'ai-hardware','The hardware behind an AI model',[
      T('Different processing strengths',['Hardware','Useful role'],[['CPU','General control, branching and diverse program tasks.'],['GPU','High-throughput parallel arithmetic for suitable workloads.'],['NPU / TPU-type accelerator','Specialised tensor operations with hardware-specific efficiency.'],['RAM and storage','Hold weights, inputs, intermediate results and saved models.']]),
      B('Training and inference have different costs','Training adjusts model parameters using data or experience. Inference uses a model to produce an output. A model may be trained on a large server and deployed on a smaller device. Simple tabular reinforcement learning can run on an ordinary CPU; AI does not always require a GPU, and a specialised chip is not automatically faster for every workload.'),
      B('Trace the whole path','For a camera-based robot, the sensor captures an image, memory buffers it, processing estimates a useful state, a policy selects an action, and control hardware drives the actuator. Delays in any stage matter. Model size, memory movement, power consumption and heat can be as important as the advertised arithmetic speed of the chip.')
    ],'6.1','3.1–3.3')

    P(3,'advanced-io','Interfaces you can see and touch',[
      T('Touch and display technologies',['Technology','Key idea'],[['Capacitive touch','Detects changes in an electric field; often supports multi-touch.'],['Resistive touch','Pressure brings conductive layers into contact.'],['OLED display','Organic light-emitting pixels produce their own light.'],['VR headset','Combines displays, optics and tracking to present an immersive view.']]),
      B('Display quality involves trade-offs','Screen resolution describes pixel dimensions. OLED can provide deep blacks because individual pixels can be off, but power use depends on displayed content and hardware. Capacitive and resistive touch differ in input methods, clarity, durability and cost. A touchscreen is both an input surface and an output display.'),
      B('Build physical objects layer by layer','In material-extrusion 3D printing, a nozzle deposits material to form successive layers. In binder-based printing, a binder joins selected regions of a powder bed. These are different additive-manufacturing methods; material properties and post-processing requirements differ. A printer turns digital instructions into physical output through controlled motion and material handling.')
    ],'3.3','3.3')
