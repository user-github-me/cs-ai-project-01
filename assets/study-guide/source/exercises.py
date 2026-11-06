"""Questions from content/chapter-XX/exercises.md at repository revision 9a645d0.

Subquestions are split for page placement. Minor wording/notation is normalised;
the circuit-switching and signature questions have their technical premises clarified.
No answer key is included.
"""
EXERCISES = {
 '1.1a1': 'The byte 01001111 represents an eight-bit two’s complement integer. State its equivalent denary value.',
 '1.1a2': 'The byte 10011010 represents an eight-bit two’s complement integer. State its equivalent denary value.',
 '1.1a3': 'Write the integer −53 in eight-bit two’s complement form.',
 '1.1a4': 'State the range of integers that can be represented by an eight-bit two’s complement number. Give the endpoints in denary.',
 '1.1b1': 'Write the denary integer 798 in binary-coded decimal (BCD) format.',
 '1.1b2': 'Write the denary number represented by the BCD sequence 1001 0111 0111 0110.',
 '1.1c': 'Give one use of the binary-coded decimal system.',
 '1.2a1': 'A developer records sounds for a game. State what is meant by sampling resolution.',
 '1.2a2': 'Describe how sampling resolution affects the accuracy of stored digitised sound.',
 '1.2b1': 'A developer includes bitmap images in a game. Explain the term image resolution.',
 '1.2b2': 'A developer uses 16-colour bitmap images. State the number of bits required to encode the data for one pixel.',
 '1.2b3': 'An image is 16,384 pixels wide and 512 pixels high. It is saved as a 256-colour bitmap. Calculate the raw image-data size in gibibytes, excluding headers and compression.',
 '1.3': 'Put these fetch–execute stages in order: copy MDR to CIR; execute the instruction; decode the instruction; copy PC to MAR; increment PC by 1; copy the instruction at the memory location in MAR into MDR.',
 '1.4': 'File History and Time Machine are examples of backup utilities. Explain why it is important to back up files on a computer.',
 '1.5': 'Assemblers, compilers and interpreters are all used to translate or execute programs. Discuss the different roles played by each translator.',
 '2.1': 'Differentiate between classical conditioning (Pavlov) and operant conditioning (Skinner) in terms of how learning occurs.',
 '2.2': 'Give an example of a simple reflex-based agent, such as a robotic vacuum or thermostat, and identify its stimulus, response and environment.',
 '2.3': 'Explain how subsumption architecture organises robot behaviours into layered modules without requiring a centralised internal map.',
 '2.4a': 'What are the roles of the environment, the agent and the policy in a Markov decision process (MDP)?',
 '2.4b': 'Explain the difference between exploration (trying new actions) and exploitation (using the best current estimates). Why must an agent balance both?',
 '3.1a': 'Differentiate between primary storage and secondary storage in terms of volatility, speed and CPU accessibility.',
 '3.1b': 'Give an example of a secondary-storage technology for each category: magnetic, optical and solid-state (flash).',
 '3.2a': 'Explain the structural difference between SRAM and DRAM regarding how they store data and their need for refreshing.',
 '3.2b': 'Contrast ROM, PROM and EPROM in terms of how data is written and erased.',
 '3.3': 'Classify the following as input, output or storage, noting dual roles where relevant: a touchscreen display, a solid-state drive and a barcode reader.',
 '3.4': 'Outline an automated environmental control system, such as a greenhouse or thermostat. Specify the sensor, the processing condition and the resulting actuator action.',
 '3.5a': 'Explain the main design difference between RISC and CISC architectures regarding instruction encoding and decoding complexity.',
 '3.5b': 'Explain the role of pipelining in overlapping instruction execution, and name one hazard that can stall a pipeline.',
 '3.5c': 'State the functions of the program counter, accumulator and memory data register during instruction execution.',
 '3.6': 'What is a hardware interrupt, and what happens to program execution when an enabled interrupt is serviced by the CPU?',
 '3.7': 'Draw or describe the logic-gate symbols and write the truth tables for AND, OR and NOT.',
 '4.1a': 'Contrast LANs and WANs in geographic scale, ownership and typical transmission conditions. Avoid assuming that scale alone fixes speed.',
 '4.1b': 'Compare the client–server and peer-to-peer models in resource management and scalability.',
 '4.1c': 'Differentiate between a thick client and a thin client based on where processing and storage take place.',
 '4.1d': 'What are the main trade-offs in cost, security responsibilities and control between a public cloud and a private cloud?',
 '4.2': 'How do network systems handle simultaneous transmissions on a shared medium, using collision detection or collision avoidance?',
 '4.3a': 'Break down the parts of a URL, such as scheme, domain and path, and explain how it identifies a resource.',
 '4.3b': 'Describe the role of DNS when resolving the host name in a URL to an IP address.',
 '4.4a': 'Outline the four TCP/IP layers in order and give the core responsibility of each.',
 '4.4b': 'State the purpose of HTTP, FTP, POP3 and IMAP.',
 '4.5a': 'Explain what is meant by circuit switching.',
 '4.5b': 'Assume a video-conferencing scenario specifically requires reserved communication capacity. Explain why circuit switching could be preferred in that scenario. This is the source question’s assumed context, not a claim that modern Internet video calls generally use circuits.',
 '4.5c': 'List two benefits and one drawback of packet switching.',
 '4.6a': 'Differentiate between data security, data privacy and data integrity.',
 '4.6b': 'Contrast validation, such as range and format checks, with verification, such as double entry and transfer checks, when protecting data quality.',
 '4.6c': 'Name three mechanisms used to protect computer systems against threats.',
 '4.7a': 'Compare symmetric and asymmetric cryptography in key management, typical performance and the handling of plaintext and ciphertext.',
 '4.7b': 'Explain how a private signing key and matching public verification key support a digital signature that checks message origin and integrity. Distinguish signing from encryption.',
 '4.7c': 'What are SSL and TLS, and where is TLS used to secure network traffic today?',
 '5.1': 'Define a smart system and explain how it integrates physical hardware, network connectivity and software into one workflow.',
 '5.2a': 'Define real-time processing and explain why communication delay and hardware performance matter for tasks such as collision avoidance.',
 '5.2b': 'What is automation, and how can moving from manual operation to automated systems change efficiency and error patterns?',
 '5.3a': 'Explain how an RL-based system uses feedback or reward signals from its environment to update its behavioural policy or value estimates.',
 '5.3b': 'Describe the role of actuators in translating a computed decision into a physical change.',
 '5.4a': 'Define human-AI interaction and explain the additional challenges it introduces within human-computer interaction.',
 '5.4b': 'Identify a usability or safety challenge that can occur when a smart system’s autonomous behaviour lacks transparency.',
 '5.5a': 'Define ethical AI and discuss the challenges of maintaining transparency, fairness and accountability in smart systems.',
 '5.5b': 'Identify one opportunity and one security or privacy risk associated with connecting everyday physical devices to networks.',
 '6.1': 'Explain how thermal limits, power consumption, memory capacity and processing speed constrain complex AI models on small embedded devices.',
 '6.2': 'Define scalability and interoperability. Explain why both matter when adding hundreds of IoT devices from different manufacturers.',
 '6.3': 'Define adaptive intelligence and explain how it can help an agent respond to changing conditions, without assuming that adaptation guarantees success.',
 '6.4': 'Compare predictive analytics and behavioural modelling in how they use evidence to inform future decisions or actions.',
 '6.5': 'Explain resource optimisation when balancing local hardware processing against network transmission costs.',
 '6.6': 'Define explainability and explain why some deep reinforcement-learning models are difficult to interpret.',
 '6.7': 'Identify two security concerns and two ethical implications when a network of smart devices makes high-stakes decisions with limited human oversight.'
}

def source_path(key):
    return f'content/chapter-{int(key.split(".")[0]):02d}/exercises.md'

def label(key):
    ch,number=key.split('.',1)
    return f'Chapter {ch} · Question {number}'
