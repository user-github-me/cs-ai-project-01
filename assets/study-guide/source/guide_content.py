"""Edited teaching content; each page links to the team's source exercises.

The six supplied chapter PDFs define the scope. Explanations clarify technical
overstatements without adding answers to the assessment exercises.
"""
PAGES = []

def B(title, text):
    return {'kind':'text','title':title,'text':text}

def T(title, headers, rows):
    return {'kind':'table','title':title,'headers':headers,'rows':rows}

def D(title, labels, caption='', kind='flow'):
    return {'kind':'diagram','title':title,'labels':labels,'caption':caption,'diagram':kind}

def P(ch, key, title, blocks, exercise, source):
    PAGES.append(dict(chapter=ch,key=key,title=title,blocks=blocks,exercise=exercise,source=source))

# CHAPTER 1 · DAWN
P(1,'bits-bytes','From bits to bytes',[
 B('Two states, many meanings','A bit is a binary digit: 0 or 1. Electronic circuits distinguish two ranges of voltage, allowing hardware to store and process bits reliably. Eight bits form one byte. A word is the group of bits a processor handles as a unit; its size depends on the architecture. The same pattern may represent a number, a character or an instruction: the interpretation supplies the meaning.'),
 T('Measure storage accurately',['Prefix','Bytes'],[['kB / MB / GB','1,000 / 1,000,000 / 1,000,000,000'],['KiB / MiB','1,024 / 1,048,576'],['GiB / TiB','1,073,741,824 / 1,099,511,627,776']]),
 B('Units matter','Lowercase b means bit; uppercase B means byte. Divide bits by 8 to obtain bytes. Decimal prefixes use powers of ten; binary prefixes use powers of two. For example, 2 KiB = 2 × 1,024 = 2,048 bytes. A network speed in Mb/s is not the same unit as a file size in MB.')
],'1.2b3','1.1')

P(1,'binary-hex','Binary, denary & hex',[
 B('Place value does the work','Denary uses powers of 10. Binary uses powers of 2, so the positions in an eight-bit number are 128, 64, 32, 16, 8, 4, 2 and 1. Add the positions containing 1: 00101101 = 32 + 8 + 4 + 1 = 45. To convert denary to binary, select those powers of two, or repeatedly divide by 2 and read the remainders backwards.'),
 T('Hexadecimal groups four bits',['Binary nibble','Hex','Denary'],[['0000–1001','0–9','0–9'],['1010 / 1011 / 1100','A / B / C','10 / 11 / 12'],['1101 / 1110 / 1111','D / E / F','13 / 14 / 15']]),
 B('Why engineers use hexadecimal','Group binary digits in fours from the right: 0010 1101 becomes 2D. Hexadecimal is a compact notation for the same value, useful in memory dumps, colour codes and hardware addresses. Binary addition carries when a column reaches 2: 1 + 1 = 10. With a fixed width, check whether a carry or signed overflow changes the interpretation.')
],'1.1a1','1.1')

P(1,'signed-binary','Represent negative values',[
 T('Three eight-bit representations of −5',['Method','Representation','Rule'],[['Sign and magnitude','10000101','Sign bit + magnitude'],["One’s complement",'11111010','Invert the bits of +5'],["Two’s complement",'11111011','Invert +5, then add 1']]),
 B('Read two’s complement','The leftmost bit has a negative weight. In eight bits, 11111011 means −128 + 64 + 32 + 16 + 8 + 2 + 1 = −5. In n bits, the range is −2^(n−1) to 2^(n−1) − 1. Always state the width: a bit pattern has no unique signed meaning without a representation and a width.'),
 B('Subtract by adding the negative','To calculate 9 − 3 in eight bits, add 00001001 to the two’s complement of 00000011: 11111101. Keep the eight result bits, giving 00000110. A carry outside the width is discarded. Signed overflow occurs when the true result lies outside the representable range; it is not the same as an unsigned carry.')
],'1.1a3','1.1')

P(1,'characters-bcd','Numbers, characters & codes',[
 B('BCD stores one decimal digit at a time','Binary-coded decimal allocates four bits to each decimal digit. Decimal 259 becomes 0010 0101 1001. This is different from converting the whole number 259 to ordinary binary. Patterns 1010–1111 are unused as decimal digits in ordinary BCD. Decimal representations are useful where exact decimal digits matter, including displays and some financial calculations.'),
 B('Characters need an agreed code','A character set defines the available characters. An encoding maps characters to stored values. ASCII defines 128 codes, covering English letters, digits, punctuation and control characters. Unicode assigns code points to characters from many writing systems. UTF-8 and UTF-16 are ways to encode those code points; Unicode does not mean every character occupies the same number of bytes.'),
 D('One pattern, different interpretations',['Bits','Encoding / format','Meaning'],'An application must know the agreed format before it can interpret stored data.')
],'1.1b2','1.1')

P(1,'images','Build a digital image',[
 B('Pixels and colour depth','A bitmap is a grid of pixels. Pixel dimensions describe its width and height; resolution may also describe pixel density when an image is displayed or printed. Colour depth is the number of bits used per pixel. With b bits per pixel, up to 2^b different codes are available. More pixels preserve finer spatial detail; more bits per pixel allow more colour or intensity values.'),
 T('Uncompressed bitmap size',['Quantity','Example'],[['Dimensions','1,000 × 500 pixels'],['Colour depth','8 bits per pixel'],['Raw pixel data','1,000 × 500 × 8 = 4,000,000 bits'],['In bytes','4,000,000 ÷ 8 = 500,000 bytes']]),
 B('Bitmap versus vector','A vector image stores shapes, paths and their properties. It can scale without pixelation, making it useful for diagrams and logos. Photographs are normally bitmaps. The size formula above excludes headers, palettes, metadata and compression; an actual file may have a different size.')
],'1.2b2','1.2')

P(1,'sound-compression','Sample, store & compress',[
 B('Turn an analogue wave into numbers','An analogue-to-digital converter samples a sound signal. Sampling rate is the number of samples per second, in hertz. Sampling resolution, or bit depth, is the number of bits per sample. A higher rate can represent a wider range of frequencies; a greater bit depth provides finer amplitude steps. Both increase uncompressed storage requirements.'),
 B('Estimate audio size','Uncompressed audio size in bits = sampling rate × bit depth × channels × duration. For 10 seconds of mono audio at 8,000 samples/s and 16 bits/sample: 8,000 × 16 × 1 × 10 = 1,280,000 bits, or 160,000 bytes. Stereo requires two channels.'),
 T('Choose the right compression',['Lossless','Lossy'],[['Reconstructs the original data exactly.','Permanently discards some information.'],['ZIP, run-length encoding, PNG.','JPEG images, MP3 audio.'],['Suitable for programs and exact records.','Useful when smaller media files justify reduced fidelity.']])
],'1.2a2','1.2')

P(1,'stored-program','The stored-program computer',[
 B('Instructions and data share memory','In the introductory Von Neumann model, memory holds both instructions and data. The CPU fetches instructions, decodes them and performs the required operations. The arithmetic logic unit (ALU) performs calculations and comparisons. The control unit coordinates the operation of the CPU, memory and input/output devices. Registers hold small amounts of immediately needed information.'),
 D('The main connections',['CPU','System buses','Memory / I/O'],'Address bus: identifies a location. Data bus: carries instructions or values. Control bus: carries signals such as read and write.',kind='bidirectional'),
 B('Timing and the bottleneck','The system clock coordinates operations. A clock frequency of 3 GHz means three billion clock cycles per second, not necessarily three billion completed instructions. Cache and pipelining reduce some delays, but moving instructions and data through shared resources can still restrict throughput. Real processors extend this simplified model in many ways.')
],'1.3','1.3')

P(1,'fetch-execute','Fetch / decode / execute',[
 T('Follow one instruction',['Step','Register transfer or action'],[['1','Copy the address in PC to MAR.'],['2','Read the memory instruction into MDR.'],['3','Advance PC to the next instruction address.'],['4','Copy the instruction from MDR to CIR.'],['5','Decode the operation and its operand.'],['6','Execute; store a result or change control flow.']]),
 B('Give each register a job','PC is the program counter: the next instruction address. MAR identifies the memory location being accessed. MDR holds data moving to or from memory. CIR holds the current instruction. ACC is an accumulator for intermediate arithmetic results in this teaching model. A branch instruction may replace the normal next value of PC.'),
 B('A useful analogy','Think of a recipe: PC marks the next recipe line, MAR selects its location, MDR carries the line, CIR holds the instruction being followed, and ACC is a temporary mixing bowl. In this simplified one-word instruction model PC advances by 1; actual instruction sizes and timing depend on the processor.')
],'1.3','1.3')

P(1,'translators','From source code to execution',[
 T('Three translator roles',['Tool','Input and result'],[['Assembler','Assembly mnemonics and labels become machine instructions.'],['Compiler','Source program becomes another representation, often native code or bytecode.'],['Interpreter','Runs program operations through a runtime, sometimes using bytecode.']]),
 B('Choose the right level','Machine code contains the instructions a processor executes. Assembly exposes architecture-specific operations and registers. High-level languages offer abstractions such as variables, functions and data structures. They improve portability, but some translation or runtime support is still needed. A language may have both compiled and interpreted implementations.'),
 B('Trade-offs are implementation-dependent','Ahead-of-time compilation can support fast execution and catch some errors before running. Interpretation can support rapid experimentation and interactive debugging. Many modern systems combine compilation, interpretation and just-in-time compilation. It is too simple to say that all interpreters translate one source line at a time or that all compilers produce a standalone executable.')
],'1.5','1.5')

P(1,'program-trace','Trace a tiny program',[
 T('Teaching assembly: one instruction per address',['Address','Instruction','Meaning'],[['100','LOAD #3','Put the literal value 3 in ACC.'],['101','ADD #4','Add the literal value 4 to ACC.'],['102','STORE 200','Copy ACC to memory address 200.'],['103','HALT','Stop this teaching program.']]),
 B('Watch state change','Start with PC = 100. After LOAD, ACC = 3. After ADD, ACC = 7. STORE copies 7 to address 200; it does not mean “store the number 200”. The # sign denotes an immediate value in this invented teaching notation. The example illustrates execution; it is not the instruction set of a particular real CPU.'),
 B('Two passes and a helpful editor','A two-pass assembler first builds a table connecting labels to addresses, then uses it to resolve operands and encode instructions. An integrated development environment (IDE) combines editing, syntax highlighting, completion, translation and debugging. Breakpoints and single-stepping let you inspect the changing PC, registers and memory.')
],'1.5','1.5')

P(1,'operating-system','The operating system’s jobs',[
 T('Coordinate shared resources',['Management task','Purpose'],[['Processes','Schedule CPU time and coordinate running programs.'],['Memory','Allocate and protect memory; manage virtual memory.'],['Devices and files','Use drivers, organise storage and provide I/O services.'],['Security','Authenticate users and enforce access permissions.']]),
 B('Utilities support maintenance','Backup software creates recoverable copies; test restoration as well as copying. Antivirus checks for known and suspicious malware activity. A formatter prepares a file system and may destroy access to existing data. Repair tools check file-system structures. Compression tools reduce storage or transfer size. Defragmentation helps some hard disks; it is not routine maintenance for SSDs.'),
 B('Software does not replace hardware','The OS provides a managed interface to physical resources. A program still needs CPU time, working memory and access to its files. Good resource management improves sharing and responsiveness, but it does not remove limits in memory capacity, processing speed or storage performance.')
],'1.4','1.4')

P(1,'interrupts-ports','Events, interrupts & peripherals',[
 B('Respond without checking everything constantly','An interrupt requests the processor’s attention. For an enabled interrupt, the processor and operating system preserve the required execution state, transfer control to an interrupt service routine, then restore state and resume. Exact timing and saved registers depend on the architecture. Not every request is handled immediately; priorities and masking affect when it is serviced.'),
 D('Interrupt service, conceptually',['Running task','Save context','Service event','Restore / resume'],'A timer interrupt helps an OS share CPU time; an input device may interrupt when data becomes available.'),
 T('Common peripheral connections',['Connection','Typical purpose'],[['USB','Serial data, plug-and-play peripherals; many versions also provide power.'],['HDMI','Digital video and audio for a display.'],['VGA','Legacy analogue video connection.']])
],'3.6','1.3–1.4')

# CHAPTER 2 · MORNING
P(2,'conditioning','Learning from the environment',[
 B('Start with observable behaviour','Behaviourism studies the relationship between observable behaviour and environmental events. A stimulus is a detectable event; a response is an observable reaction. Pavlov, Watson and Skinner contributed to different strands of this tradition. The approach helped make learning measurable, although it is not a complete description of every kind of human learning.'),
 T('Two kinds of conditioning',['Classical conditioning','Operant conditioning'],[['A cue becomes associated with another stimulus.','An action becomes associated with its consequences.'],['A bell paired with food can trigger salivation.','Sitting followed by a treat can become more frequent.'],['Focus: an elicited response.','Focus: behaviour shaped by reinforcement or punishment.']]),
 B('Connect the analogy carefully','Reinforcement learning borrows the idea of learning from consequences, but an algorithm is not a human or animal mind. A numerical reward is a training signal. It does not imply feelings, understanding or consciousness. Use the analogy to identify a feedback relationship, then describe the computational mechanism precisely.')
],'2.1','2.1')

P(2,'reactive-agents','React first: behaviour-based robots',[
 B('A sensor can trigger a useful action','A simple robotic vacuum may move forward until a bumper is pressed, then reverse and turn. Its environment is the room, its stimulus is the bumper signal, and its response is the movement. These rules can produce useful behaviour without a detailed map. If the rules never change from experience, this is reactive control rather than reinforcement learning.'),
 D('A direct feedback path',['Sensor','Behaviour rule','Actuator','Environment'],'Situated systems act in an environment; embodied systems have a physical body that constrains and enables action.'),
 B('Layers and priorities','Brooks’ subsumption architecture coordinates relatively simple behaviour modules. A module can inhibit or suppress another module’s output under specified conditions. A designer might combine wandering, obstacle avoidance and task seeking while protecting a safety stop. This is one design approach, not a claim that all map-based planning is slow or unreliable; practical robots often combine reactive control and planning.')
],'2.3','2.2')

P(2,'rl-loop','The reinforcement-learning loop',[
 B('Learn a policy through experience','Reinforcement learning is a way for an agent to learn decisions through interaction. The agent observes a state or observation, selects an action, and receives feedback from the environment. A learning algorithm uses that experience to improve a policy: the rule or strategy for choosing actions. The objective is usually expected cumulative reward, not just the next reward.'),
 D('One interaction at time t',['Agent / policy','Action','Environment','Next state + reward'],'Repeat: observe, act, receive feedback, then update. The learning update may occur during training rather than every deployed action.',kind='loop'),
 T('Name the components',['Component','Grid-world example'],[['Agent / environment','A simulated rover / a grid with obstacles.'],['State / action','Current square / move up, down, left or right.'],['Reward / policy','Points for outcomes / a strategy for selecting moves.']])
],'2.4a','2.3')

P(2,'rewards-values','Rewards, policies & values',[
 B('Feedback evaluates an outcome','A reward is a numerical signal associated with an interaction. It may be positive, zero or negative. A reward of −1 is not a moral judgement: its role is defined by the task. Designers might reward reaching a goal, penalise a collision and charge a small cost per step. Poorly chosen rewards can encourage shortcuts that defeat the intended goal.'),
 B('Distinguish the three ideas','The reward says how an outcome scores now. A policy says what action to choose in a situation. A value estimate says how much future reward is expected from a state or a state–action choice. A good policy may accept a small immediate cost to achieve a larger long-term return. Q-learning estimates action values and derives choices from them.'),
 D('The learning question',['Experience','Value estimate','Policy improvement'],'A fixed rule such as “if hot, turn on fan” may control a system effectively without learning any values or changing a policy.')
],'5.3a','2.3')

P(2,'exploration','Explore or exploit?',[
 B('Use the restaurant analogy','Exploitation is ordering a dish you already believe is best. Exploration is trying another dish to learn more about it. In an RL task, exploitation chooses the action with the best current value estimate, including future return. Exploration gathers information about other actions. Early estimates can be wrong, so always exploiting can lock an agent into an inferior policy.'),
 T('An epsilon-greedy example',['Choice rule','With epsilon = 0.10'],[['Explore','With 10% probability, choose a random permitted action.'],['Exploit','Otherwise choose an action with the highest current Q value.'],['During training','Measure outcomes and update estimates; epsilon may change over time.']]),
 B('Think before choosing','Suppose one route has worked twice and another has never been tried. Is the first route certainly better? No: evidence is incomplete. Exploration can improve knowledge, but it also has a cost. In physical systems, experiments must respect safety constraints; training in a simulation does not automatically make every real-world action safe.')
],'2.4b','2.3')

P(2,'q-learning','Update a Q value',[
 B('A table of learned action values','Q(s, a) estimates the return from taking action a in state s and then following a good policy. Q-learning is model-free: it learns from transitions without needing a supplied transition model. “Model-free” does not mean memory-free or that the agent lacks a table or neural network.'),
 B('The update rule','Q(new) = Q(old) + alpha × [reward + gamma × max Q(next state, next action) − Q(old)]. Alpha controls the size of an update. Gamma discounts future rewards. The quantity in square brackets is the temporal-difference error. For a terminal next state, use zero for the future-value term.'),
 T('Work through one illustrative update',['Quantity','Value'],[['Old Q / alpha','2 / 0.5'],['Reward / gamma / best next Q','1 / 0.9 / 4'],['Target','1 + 0.9 × 4 = 4.6'],['New Q','2 + 0.5 × (4.6 − 2) = 3.3']]),
 B('Interpret the result','This experience raised the estimate from 2 to 3.3. It did not prove the action is always best. Repeated experience, an appropriate learning schedule and sufficient exploration are important; one reward does not establish a reliable policy.')
],'2.4b','2.3')

P(2,'mdp','A decision problem as an MDP',[
 T('Five parts of a Markov decision process',['Symbol','Meaning'],[['S','Possible states.'],['A','Available actions.'],['P','Transition probabilities: where an action can lead.'],['R','Reward function: how outcomes are scored.'],['gamma','Discount factor: how future rewards are weighted.']]),
 B('The Markov property','A state is Markov when it contains the information needed to predict the next-state and reward distribution, given the current action. Earlier history adds no further predictive information once that state is known. A position alone may be insufficient: a robot may also need speed, battery level or whether it is carrying a package.'),
 B('Observation is not always state','Sensors can provide incomplete or noisy observations. A camera view may hide an obstacle or omit velocity. An agent may need memory or a state estimate to work with partial information. A simple grid world is useful because we can explicitly specify the state, actions, transitions and rewards instead of assuming the agent knows everything.')
],'2.4a','2.4')

P(2,'uncertainty','Actions can have uncertain outcomes',[
 B('A slippery grid square','Imagine an agent choosing “forward”. In this illustrative environment, it reaches the intended square with probability 0.8 and slips sideways with probability 0.2. The action is chosen by the agent; the transition outcome is sampled by the environment. The probabilities for all possible next outcomes must sum to 1.'),
 D('One action, two outcomes',['Choose forward','Target: probability 0.8','Slip: probability 0.2'],'For immediate rewards of +10 and −5, the expected immediate reward is 0.8 × 10 + 0.2 × (−5) = 7. Future rewards may change which action is best.',kind='branch'),
 B('Expected is not guaranteed','An expected value of 7 does not mean every attempt earns 7. It summarises the average implied by the model. A system that learns under one set of transition probabilities may perform poorly when its environment changes. Test across plausible conditions rather than judging a policy from a single successful run.')
],'2.4a','2.4')

P(2,'learning-deployment','Training is different from using a policy',[
 B('Separate two phases','During training, the system collects experience and updates estimates or policy parameters. During deployment, it may use a fixed learned policy without further learning. Some applications allow controlled online updates, but adaptation is not automatic. A robot can react to a new sensor reading while keeping exactly the same policy.'),
 B('Test what was actually learned','Check whether success persists with different starting states, sensor noise and changed conditions. Compare against a simple fixed-rule baseline. Examine failure cases as well as average reward. If the goal is “arrive safely”, a reward that only measures speed may produce an undesirable strategy even when the algorithm is working as specified.'),
 D('A responsible learning workflow',['Define the task','Train / explore','Evaluate','Deploy / monitor'],'Behaviour-based robotics, reinforcement learning and neural networks are related ideas, not interchangeable labels. A system can use one without using all three.')
],'2.2','2.2–2.4')

# Additional chapters are loaded as ordinary local Python modules for easy editing.
from chapter_03 import add_chapter as add03
from chapter_04 import add_chapter as add04
from chapter_05_06 import add_chapters as add0506
add03(P,B,T,D)
add04(P,B,T,D)
add0506(P,B,T,D)
