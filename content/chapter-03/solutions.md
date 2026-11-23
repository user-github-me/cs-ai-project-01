# Chapter 3 — Answers and expected outcomes

> Attempt each activity in draft.md before reading its answer. Calculations show every step; open questions list the
> points a good answer contains. Numbering matches draft.md.

## Pause & Try

### Pause & Try 3.1 — Smart speaker hardware jobs

| Part | Class | What it does here |
|---|---|---|
| Microphone | input | turns your voice into an electrical signal and then into digital data |
| Processor | processing | runs the program that handles your question |
| Flash memory | storage | keeps the program and settings when the power is off |
| Loudspeaker | output | plays the spoken answer |
| Ring of lights | output | shows that the speaker is listening or answering |

**Why it needs both:** the hardware can only capture, process, store and play sound; it does nothing useful until software tells it what to do. The software (kept in the flash memory) tells the processor how to pick out your question, work out an answer (often with help from a server over the internet) and turn it into speech. But a program needs hardware to run on, and to hear you and speak to you.

Key points:
- hardware is the physical parts: microphone, processor, memory, speaker, lights;
- software is the set of instructions that tells the hardware what to do;
- each is useless without the other: hardware without software is silent electronics, and software without hardware has nothing to run on.

### Pause & Try 3.2 — Self-checkout input devices

| Input device | Data it captures |
|---|---|
| Barcode reader (scanner) | the pattern of bars on each item, decoded into the product's number |
| Weighing scale (a weight or pressure sensor) | the item's weight, so the checkout can check that it matches the scanned product |
| Touchscreen (its touch sensor) | the position of your touch, i.e. your choices such as "Pay now" |
| Contactless card reader | the card's payment details, read by radio from the chip in the card |

Also acceptable: a camera that watches the bagging area, or a keypad for your PIN (the digits you type). The touchscreen is also an output device, because it shows the prices.

### Pause & Try 3.3 — 4K pixels and OLED black

**Pixels on the 4K screen:** 3840 × 2160 = **8 294 400 pixels**.

**Compared with Full HD:** 8 294 400 ÷ 2 073 600 = **4 times as many**. (There are twice as many pixels across, 3840 ÷ 1920 = 2, and twice as many down, 2160 ÷ 1080 = 2, and 2 × 2 = 4.)

**Why OLED black is deeper:** in an OLED screen each pixel **gives out its own light**, so a black pixel is simply switched off and gives out no light at all: true black. An LCD has a white **backlight** shining behind every pixel; the liquid-crystal cells cannot block it completely, so a little light leaks through and black looks dark grey.

### Pause & Try 3.4 — Touchscreen for gloved nurses

**Choice: a resistive touchscreen.** It detects pressure: pressing pushes the flexible plastic layer onto the glass layer, so their coatings touch and complete a circuit. Anything can press it, including a gloved finger. A capacitive screen needs a bare finger (or a special stylus) to change its electric field, so it is the wrong choice here.

- **Advantage:** it works with gloves, a pen or any other object, so nurses never have to take their gloves off.
- **Disadvantage:** the picture is less clear and the plastic top layer scratches easily. (Also acceptable: it usually senses only one touch at a time, so multi-touch gestures such as pinch-to-zoom do not work.)

### Pause & Try 3.5 — Parking sensor and the ADC

**Distance:** the sound travels to the wall **and back**, so distance = speed of sound × time ÷ 2.
- time: 2.9 ms = 0.0029 s
- distance travelled by the sound: 343 m/s × 0.0029 s = 0.9947 m
- distance to the wall: 0.9947 m ÷ 2 ≈ **0.50 m** (about 50 cm)

**Why an ADC is needed:** a temperature sensor produces an **analogue** signal: a voltage that can take any value in a range. A processor can only work with **digital** (binary) data. The ADC measures the voltage many times a second and turns each measurement into a binary number that the processor can use (for example, an 8-bit ADC turns 0–5 V into a number from 0 to 255).

### Pause & Try 3.6 — Automated greenhouse watering scenario

Model answer (watering the plants in a greenhouse):
- **Sensor:** a moisture sensor in the soil; an ADC turns its analogue reading into binary for the microcontroller.
- **Processing condition:** IF the soil moisture is below 30 % THEN start watering; IF it rises above 60 % THEN stop.
- **Actuator action:** a solenoid opens the water valve (or a relay switches a pump on), and closes it again when the soil is wet enough.
- **Feedback:** the sensor is read again every few seconds, so each new reading shows the result of the last action and the loop repeats.

Any scenario is acceptable if it names a sensor, a clear condition with a threshold and an actuator that changes the conditions. Examples: the greenhouse in draft.md (temperature sensor; IF below 22 °C THEN heater on, IF above 27 °C THEN a motor opens the roof window), or a smart thermostat (temperature sensor; IF below 20 °C THEN a relay switches the boiler on).

### Pause & Try 3.7 — Microwave embedded microcontroller

**Why a microcontroller:** a microwave oven only has one dedicated job: read the keypad and the door switch, run the timer, switch the heating part (the magnetron) and the turntable on and off, and show the time. A small, cheap microcontroller with its program in ROM or flash does exactly this. A general-purpose computer would be bigger, dearer and more power-hungry, would take time to start up, and its extra abilities (installing programs, browsing the web) would never be used.

- **Two benefits** (any two): small, light and cheap to mass-produce; uses very little power; starts instantly and responds in real time; reliable, because it does one job.
- **One drawback** (any one): hard or impossible to upgrade; limited memory and processing power; a fault often means replacing the whole board; a "smart", connected microwave could be hacked.

### Pause & Try 3.8 — Primary versus secondary storage

| | Primary storage | Secondary storage |
|---|---|---|
| Volatility | RAM and cache are volatile: they lose their data without power (ROM is the non-volatile exception) | non-volatile: keeps programs and files when the power is off |
| Speed | very fast: access in nanoseconds | slower: microseconds (SSD) to milliseconds (hard disk) |
| CPU accessibility | the CPU accesses it **directly** | the CPU **cannot** access it directly: data must first be copied into RAM |

Examples: primary storage = RAM, ROM, cache; secondary storage = hard disk, SSD, USB flash drive, DVD.

### Pause & Try 3.9 — SRAM versus DRAM structure

- **SRAM** stores each bit in a **flip-flop**: a small circuit of about six transistors that stays in one of two states while it has power. Nothing leaks away, so SRAM **never needs refreshing**.
- **DRAM** stores each bit as a **charge on a tiny capacitor**, switched by one transistor. The charge leaks away, so every cell must be **refreshed** (read and recharged) about every 64 ms.

**For a CPU cache: SRAM.** It is much faster (a few ns, compared with tens of ns for DRAM) and has no refresh delays, so the processor is not kept waiting. SRAM is expensive and holds fewer bits per chip, but that matters little because a cache is small (a few MB). Cheap, dense DRAM is used for the large main memory instead.

### Pause & Try 3.10 — ROM, PROM and EPROM

| Type | How data is written | How it is erased |
|---|---|---|
| ROM | built in when the chip is manufactured | it cannot be erased or changed |
| PROM | bought blank, then written **once** by a programmer that burns tiny fuses | it cannot be erased: one time only |
| EPROM | written electrically by a programmer | erased with strong **ultraviolet light** through a quartz window, with the chip out of the circuit; it can then be reprogrammed |

In short: ROM is fixed at the factory, PROM can be programmed after manufacture but only once, and EPROM can be erased and reprogrammed again and again (but not inside the circuit; EEPROM and flash can do that).

### Pause & Try 3.11 — Memory in a smart thermostat

**a)** Control program: **ROM or flash**. It is non-volatile, so the program is ready the moment the power comes on, and it is not normally changed (flash also lets the maker send a firmware update).

**b)** Current temperature reading: **RAM (the microcontroller's SRAM)**. The reading changes every few seconds, so it needs memory that is fast to read and write. Losing it in a power cut does not matter, because the sensor is simply read again.

**c)** Heating schedule: **EEPROM (or flash)**. It must survive a power cut, so it needs non-volatile memory, but the user must also be able to change it, and EEPROM can be rewritten electrically inside the circuit; saved settings are its typical use. (ROM or PROM could not be changed by the user; RAM would lose the schedule in a power cut.)

### Pause & Try 3.12 — Rotational latency at 5400 rpm

- revolutions per second: 5400 ÷ 60 = 90
- time for one revolution: 1 ÷ 90 s ≈ 0.0111 s ≈ **11.1 ms**
- average rotational latency (on average the sector is half a turn away): (1 ÷ 90 s) ÷ 2 = 1 ÷ 180 s ≈ 0.00556 s ≈ **5.6 ms**

**Why a fragmented file is slower to read:** its pieces sit in **non-consecutive sectors**, often on different tracks. Instead of reading one continuous run of sectors, the drive must move the read-write head to a new track for each piece (extra **seek time**) and wait again for the right sector to spin round under the head (extra **rotational latency**). A defragmentation utility moves the pieces back together.

### Pause & Try 3.13 — Choosing magnetic, optical, solid-state

| Category | Example | Best-choice situation | Why |
|---|---|---|---|
| Magnetic | hard disk drive (HDD), e.g. a removable hard disk | a weekly back-up of a family's photos and videos | cheapest per terabyte, with very large capacities |
| Optical | Blu-ray disc | selling a film to thousands of customers | cheap to mass-produce and light to post; 25 GB per layer |
| Solid-state (flash) | solid-state drive (SSD) | the main drive of a laptop carried to classes every day | very fast loading, silent, light, low power and survives being dropped |

Other examples are acceptable when the situation matches the technology's strengths, e.g. a CD or DVD for handing out software, a USB flash drive for carrying files between home and school, a memory card in a camera, or HDDs in a server that stores huge amounts of data.

### Pause & Try 3.14 — CPU parts and clock cycle

Any three of:
- **Control unit (CU):** decodes each instruction and sends control signals to the other parts to carry it out.
- **Arithmetic logic unit (ALU):** does arithmetic (add, subtract) and logic (AND, OR, compare).
- **Registers:** tiny, ultra-fast storage locations inside the CPU for the instruction, addresses and data in use right now.
- **Cache:** fast SRAM on the chip holding data that the CPU will need again.
- **Clock:** sends regular pulses that keep every step in time.

**One clock cycle at 2.5 GHz:**
- 2.5 GHz = 2.5 × 10⁹ pulses per second
- one cycle = 1 ÷ (2.5 × 10⁹) s = 4 × 10⁻¹⁰ s = **0.4 ns**

### Pause & Try 3.15 — PC, ACC and MDR

- **Program counter (PC):** holds the address of the **next** instruction to be fetched. At the start of the fetch its value is copied into the MAR (MAR ← PC); then it is increased (PC ← PC + 1) so that it points to the following instruction.
- **Accumulator (ACC):** holds the value being worked on and receives the results from the ALU. For example, ADD 51 does ACC ← ACC + MDR, so 5 becomes 5 + 7 = 12.
- **Memory data register (MDR):** holds the data or instruction just read from memory (from the address in the MAR), or data about to be written to memory. A fetched instruction is copied from the MDR into the CIR; fetched data goes from the MDR to the ALU and the ACC.

### Pause & Try 3.16 — Bus directions and addressing

- **Address bus, unidirectional:** only the CPU decides which memory location or device it wants, so addresses travel one way only: from the MAR to memory and I/O. Memory never sends an address back.
- **Data bus, bidirectional:** data must travel both ways: into the CPU when it reads from memory, and out of the CPU when it writes to memory.

**24-bit address bus:** 2²⁴ = **16 777 216 memory locations** (with one byte at each address, that is 16 MiB).

### Pause & Try 3.17 — RISC versus CISC instructions

- **RISC:** a small set of **simple instructions that all have the same (fixed) length**, e.g. 32 bits. Every instruction has the same simple format, so **decoding is simple and fast** and is done by a hard-wired control unit; most instructions take one clock cycle.
- **CISC:** a large set of **complex instructions of variable length**, some of which do several steps at once (`MULT 200, 201` loads, multiplies and stores). The CPU must work out how long each instruction is and what it does, so **decoding is complex** and needs a microprogrammed control unit; many instructions take several clock cycles.
- **The core difference:** RISC keeps the hardware simple and gives more work to the compiler (more, simpler instructions per program); CISC puts the complexity into the hardware (fewer, more powerful instructions).

### Pause & Try 3.18 — Six loads of laundry

- **Without a pipeline:** 6 loads × 3 hours = **18 hours**.
- **With a pipeline:** the first load takes 3 hours, then one more load finishes every hour: 3 + (6 − 1) = **8 hours**.

**Latency** is the time one load (one instruction) takes from start to finish: still 3 hours, with or without a pipeline. **Throughput** is how many loads (instructions) are finished per unit of time: with a full pipeline it rises to one load every hour (one instruction every clock cycle). Pipelining raises the throughput; it does not shorten the latency.

### Pause & Try 3.19 — Pipelining in RISC processors

**Model answer:** a RISC processor splits each instruction into five stages (IF, ID, OF, IE and WB), each done by a different part of the processor in one clock cycle. Pipelining overlaps these stages: while one instruction is being executed, the next is fetching its operands, the one after that is being decoded, and so on, so up to five instructions are being worked on at the same time. Once the pipeline is full, one instruction finishes every clock cycle: 5 instructions take 5 + (5 − 1) = 9 cycles instead of 5 × 5 = 25. RISC suits this because its fixed-length, simple instructions take one cycle per stage, and its many registers mean fewer slow trips to memory.

**One hazard** (any one): a **data hazard** (an instruction needs a result that an earlier one has not yet written back); a **control hazard** (after a branch, the instructions already fetched are the wrong ones and are thrown away); a **structural hazard** (two stages need the same hardware at the same time).

Key points: stages overlap, so several instructions are in progress at once; one instruction completes per cycle once the pipeline is full (higher throughput); one hazard correctly named and explained.

### Pause & Try 3.20 — Handling a hardware interrupt

**Hardware interrupt:** a signal from a hardware device (e.g. a key press, a printer that has run out of paper, a timer) asking the CPU to stop what it is doing and deal with an event.

**What happens, step by step:**
1. The CPU finishes the current instruction, then checks for interrupt signals (it does this at the end of every fetch–execute cycle).
2. It checks the priority: a lower-priority interrupt has to wait.
3. It saves the context: the PC and the other registers are pushed onto the stack.
4. The address of the interrupt service routine (ISR) is loaded into the PC.
5. The ISR runs and deals with the event.
6. The saved registers are restored from the stack, and the interrupted program carries on where it stopped.

**Why a pipelined RISC processor needs an extra step:** its pipeline may hold up to five partly finished instructions, so saving the PC alone would lose track of them. Before running the ISR the CPU must deal with the pipeline: usually it lets the instruction in the write-back stage finish, **discards** the others, and after the ISR **restarts** from the next instruction. (Less often, the contents of all five stages are saved in registers so that no work is lost.)

### Pause & Try 3.21 — SIMD versus MIMD

- **SIMD (single instruction, multiple data):** many processing units carry out the **same instruction** on different data items at the same moment. Example: a GPU brightening a photo by adding 20 to many pixels at once (also acceptable: the vector units in a modern CPU).
- **MIMD (multiple instruction, multiple data):** several processors each run **their own instructions on their own data** at the same time. Example: a multi-core CPU (also acceptable: a cluster or a supercomputer).
- **A quad-core laptop running four different programs is MIMD:** each core follows a different instruction stream (its own program) on its own data.

### Pause & Try 3.22 — Massively parallel computers

**Two characteristics** (any two):
- thousands of processors work on parts of the same problem at the same time (MIMD);
- each processor usually has its own memory and works on its own share of the data;
- the processors are joined by a high-speed interconnect and coordinate by passing messages to each other;
- the software must split the task into parts that can run independently, then combine the results.

**Time on 5 processors:**
- part that can be split: 200 s − 50 s = 150 s
- split between 5 processors: 150 s ÷ 5 = 30 s
- total: 50 s + 30 s = **80 s**

That is 200 ÷ 80 = 2.5 times faster, not 5 times, because the 50 s part still runs in sequence.

### Pause & Try 3.23 — AND, OR and NOT

**Symbols** (inputs on the left, output on the right):
- **AND:** a flat back and a round, D-shaped front; two inputs.
- **OR:** a curved back and a pointed front; two inputs.
- **NOT:** a triangle with a small circle at the output; one input. The small circle means "invert the output".

**Truth tables:**

| A | B | AND: A.B | OR: A + B |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 |

| A | NOT: A̅ |
|---|---|
| 0 | 1 |
| 1 | 0 |

AND gives 1 only if both inputs are 1; OR gives 1 if at least one input is 1; NOT gives the opposite of its input.

### Pause & Try 3.24 — NAND, NOR and NOT

| A | B | NAND: A̅.̅B̅ | NOR: A̅ ̅+̅ ̅B̅ |
|---|---|---|---|
| 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 0 |

To remember them: NAND is AND with every output flipped (0 only when both inputs are 1); NOR is OR with every output flipped (1 only when both inputs are 0).

**NAND with both inputs joined:** the same signal A goes into both inputs, so the only possible input pairs are 0, 0 and 1, 1:

| A | Inputs | A.A | Output: A̅.̅A̅ |
|---|---|---|---|
| 0 | 0, 0 | 0 | 1 |
| 1 | 1, 1 | 1 | 0 |

The output is always the opposite of A, which is exactly the NOT truth table (0 → 1, 1 → 0). (In Boolean algebra: A.A = A by the idempotent law, so A̅.̅A̅ = A̅.)

### Pause & Try 3.25 — Drawing and tracing a circuit

In the chapter's notation the expression is X = A.B + C̅.

**The circuit:**
- A and B go into an **AND** gate, whose output is A.B;
- C goes into a **NOT** gate, whose output is C̅;
- both outputs go into an **OR** gate, whose output is X.

```
       ┌─────┐
 A ────┤     │
       │ AND ├─── A.B ───┐
 B ────┤     │           │   ┌─────┐
       └─────┘           └───┤     │
                             │ OR  ├─── X
       ┌─────┐           ┌───┤     │
 C ────┤ NOT ├── NOT C ──┘   └─────┘
       └─────┘
```

**Trace for A = 1, B = 0, C = 0:**
- AND gate: 1 AND 0 = 0
- NOT gate: NOT 0 = 1
- OR gate: 0 OR 1 = 1
- so **X = 1**

### Pause & Try 3.26 — Truth table for a circuit

| A B C | A.B | C̅ | X = A.B + C̅ |
|---|---|---|---|
| 0 0 0 | 0 | 1 | 1 |
| 0 0 1 | 0 | 0 | 0 |
| 0 1 0 | 0 | 1 | 1 |
| 0 1 1 | 0 | 0 | 0 |
| 1 0 0 | 0 | 1 | 1 |
| 1 0 1 | 0 | 0 | 0 |
| 1 1 0 | 1 | 1 | 1 |
| 1 1 1 | 1 | 0 | 1 |

**X = 1 in 5 of the 8 rows:** the four rows where C = 0 (so C̅ = 1), plus the row A = B = C = 1 (where A.B = 1). Row 5 (A = 1, B = 0, C = 0) gives X = 1, the same result as the trace in Pause & Try 3.25.

### Pause & Try 3.27 — Simplifying with Boolean algebra

1. **Distributive law**, take out the common factor A.B: Z = A.B.(C + C̅)
2. **Inverse law**, C + C̅ = 1: Z = A.B.1
3. **Identity law**, A.B.1 = A.B: **Z = A.B**

**Check with a truth table:**

| A B C | A.B.C | A.B.C̅ | Z = A.B.C + A.B.C̅ | A.B |
|---|---|---|---|---|
| 0 0 0 | 0 | 0 | 0 | 0 |
| 0 0 1 | 0 | 0 | 0 | 0 |
| 0 1 0 | 0 | 0 | 0 | 0 |
| 0 1 1 | 0 | 0 | 0 | 0 |
| 1 0 0 | 0 | 0 | 0 | 0 |
| 1 0 1 | 0 | 0 | 0 | 0 |
| 1 1 0 | 0 | 1 | 1 | 1 |
| 1 1 1 | 1 | 0 | 1 | 1 |

The Z column and the A.B column match in all 8 rows, so Z = A.B. (C makes no difference: when A = B = 1, one of the two terms is always 1.) The circuit shrinks from two three-input AND gates, a NOT gate and an OR gate to a single AND gate.

### Pause & Try 3.28 — Why GPUs train neural networks

**Model answer:** training a neural network is mostly **matrix** maths: each layer multiplies its inputs by a matrix of weights and adds up the results. A layer with 1000 inputs and 1000 outputs needs 1000 × 1000 = 1 000 000 multiplications for every example, and training repeats this for a huge number of examples. These multiplications do not depend on each other, so they can be done in **parallel**. A GPU has **thousands of small cores** that carry out the same maths on lots of data at once (SIMD style), so it does thousands of multiplications at the same moment. A CPU has only a few powerful **cores**, designed for varied, step-by-step tasks, so it gets through far fewer at a time. That is why a GPU trains a network many times faster.

Key points: training is mostly matrix multiplication; the multiplications are independent, so they can run in parallel; a GPU has thousands of cores doing the same operation on different data, a CPU only a few cores built for varied tasks; so the GPU is much faster.

### Pause & Try 3.29 — AI limits on a drone

- **Memory capacity:** all of the model's weights must fit in memory. A model with 7 billion weights of 2 bytes each needs 7 × 10⁹ × 2 bytes = 14 GB, more than a small drone's computer usually has, so the drone has to use a much smaller model, which may be less accurate.
- **Memory bandwidth:** to produce each result the processor must read every weight from memory. Even at 1 TB/s, reading 14 GB takes 14 ms, and a small device's memory is much slower. At 100 GB/s it would take 14 GB ÷ 100 GB/s = 0.14 s, and a drone flying at 10 m/s would travel 10 m/s × 0.14 s = 1.4 m before it could react: too slow to dodge an obstacle.
- **Power:** a big model keeps the processor and memory working hard, which drains the drone's small battery (which also has to power the motors), so the flight time gets shorter; a bigger battery would add weight.
- **Heat:** a chip working hard gets hot, and a small, light drone has little room for heatsinks or fans, so the chip must slow down to avoid overheating, which makes the model even slower.

So drones run small, efficient models on an NPU or another accelerator (edge AI), or send some of the work to the cloud, which needs a network connection and adds delay.

## Practice

### Question 1 — Classifying hardware

**(a)** Touchscreen display: **both input and output** (a dual role). As an input device, its touch sensor detects where you touch and sends that position to the processor (1 mark); as an output device, its display shows images and text (1 mark).

**(b)** SSD: **storage** (secondary storage); it keeps programs and files in non-volatile flash memory.

**(c)** Barcode reader: **input**; it shines light on the bars, senses the reflected light (dark bars reflect less) and decodes the pattern into a number for the computer.

### Question 2 — Output devices

**(a)** Each pixel of an OLED screen is an organic LED that **gives out its own light**, so no separate light (a backlight) is needed behind the screen; a black pixel is simply switched off.

**(b)** Model answer: the sound is stored as numbers. A **digital-to-analogue converter (DAC)** turns these numbers into a smoothly changing analogue voltage. An **amplifier** makes this signal strong enough to drive the speaker. The changing current flows through a **coil**, which moves a **cone** back and forth; the cone pushes the air back and forth, creating sound waves.

Mark points (one each):
- the DAC is named as the part that converts the digital data into an analogue signal;
- an amplifier makes the signal stronger;
- the current moves a coil and a cone, which vibrates the air to make sound waves.

### Question 3 — Automated control system scenario

Model answer: a smart thermostat.

**(a)** Sensor: a **temperature sensor** in the room (an ADC turns its analogue reading into binary for the processor).

**(b)** Threshold condition: **IF the room temperature is below 20 °C** (the temperature the user has set) THEN the heating must come on; otherwise it must be off.

**(c)** Actuator action: a **relay switches the boiler on**, and off again once the room reaches 20 °C. The temperature is read again every few seconds, so each reading is feedback and the loop repeats.

Any scenario with a named sensor, a clear numerical threshold and a matching actuator earns the marks, e.g. a greenhouse: (a) temperature sensor; (b) IF the temperature is above 27 °C; (c) a motor opens the roof window.

### Question 4 — Embedded systems

**(a)** An embedded system is **a computer built into a larger device to do one dedicated job**, for example the microcontroller that runs a washing machine's valve, heater, motor and pump.

**(b)** Benefits (any two, 1 mark each):
- small, light and cheap to mass-produce;
- uses very little power;
- starts instantly and responds in real time (e.g. it closes the valve as soon as the water-level sensor reads full);
- reliable, because it only does one job.

Drawback (any one, 1 mark):
- hard or impossible to upgrade;
- limited memory and processing power;
- a fault often means replacing the whole control board;
- a "smart", connected machine can be hacked.

### Question 5 — Storage classification

**(a)** One mark per property:
- **Volatility:** primary storage is mostly volatile (RAM and cache lose their data when the power is off; ROM is the exception); secondary storage is non-volatile.
- **Access speed:** primary storage is much faster (nanoseconds); secondary storage takes microseconds (SSD) to milliseconds (hard disk).
- **Direct CPU accessibility:** the CPU accesses primary storage directly; it cannot access secondary storage directly, so programs and data are first copied into RAM.

**(b)** One mark each:
- **Magnetic:** a hard disk drive (HDD); a removable hard disk or magnetic tape is also acceptable.
- **Optical:** a DVD; a CD or a Blu-ray disc is also acceptable.
- **Solid-state (flash):** a solid-state drive (SSD); a USB flash drive or a memory card is also acceptable.

### Question 6 — Memory technologies

**(a)** Mark points (one each):
- SRAM stores each bit in a **flip-flop** made of about six transistors;
- a flip-flop keeps its state as long as there is power, so SRAM **needs no refreshing**;
- DRAM stores each bit as a **charge on a capacitor**, with one transistor;
- the charge leaks away, so DRAM must be **refreshed** (read and recharged) constantly, about every 64 ms.

(As a result SRAM is faster but more expensive and less dense, so it is used for cache; DRAM is cheap and dense, so it is used for main memory.)

**(b)** Mark points (any four):
- ROM: the data is written in during manufacture;
- ROM cannot be erased or changed;
- PROM: bought blank and written once, after manufacture, by a programmer that burns tiny fuses;
- PROM cannot be erased, so it is one time only;
- EPROM: written electrically by a programmer;
- EPROM can be erased with strong ultraviolet light through a quartz window (out of the circuit) and then reprogrammed.

**(c)** One mark each:
- **DRAM:** the main working memory (several GB of low-power DRAM) that holds the operating system and the apps that are running;
- **SRAM:** the cache inside the processor, holding data and instructions that it will need again soon;
- **Flash:** non-volatile storage for the operating system, apps, photos and other files, which stay there when the phone is switched off.

### Question 7 — Registers and buses

**(a)** One mark each:
- **PC:** holds the address of the next instruction to be fetched; its value is copied into the MAR and it is then increased by 1.
- **ACC:** holds the data being processed and the results from the ALU.
- **MDR:** holds the data or instruction just read from memory, or data about to be written to memory.

**(b)** Only the CPU sends addresses (from the MAR) to memory and the I/O devices, and no address ever has to travel back to the CPU, so the address bus carries signals in one direction only.

**(c)** An n-bit address bus can carry 2ⁿ addresses: 2²⁰ = 2¹⁰ × 2¹⁰ = 1024 × 1024 = **1 048 576 memory locations** (1 MiB if each location holds one byte).

### Question 8 — Processor design

**(a)** Mark points (any three):
- RISC instructions have a **fixed length** (e.g. 32 bits); CISC instructions have a **variable length**;
- RISC has a small set of **simple instructions**, most taking one clock cycle; CISC has many **complex instructions**, often taking several cycles;
- RISC instructions are **simple and fast to decode** (hard-wired control unit); CISC instructions are **complex to decode** (microprogrammed control unit);
- RISC programs are longer (more work for the compiler); CISC programs are shorter (more work for the hardware).

**(b)** Mark points (one each):
- each instruction is split into stages (IF, ID, OF, IE, WB), each done by different hardware in one clock cycle;
- while one instruction is in one stage, the following instructions are in the earlier stages, so up to five instructions are processed at the same time and, once the pipeline is full, one finishes every cycle (5 instructions in 9 cycles instead of 25);
- one hazard named: a data hazard (an instruction needs a result not yet written back), a control hazard (after a branch, the instructions already fetched are wrong and are thrown away) or a structural hazard (two stages need the same hardware at once).

### Question 9 — Hardware interrupts

**Model answer:** a hardware interrupt is a signal from a hardware device, such as a key press, a printer that has run out of paper or a timer, asking the CPU to stop what it is doing and deal with an event. The CPU finishes its current instruction and checks for interrupts at the end of each fetch–execute cycle. If an interrupt is waiting and its priority is high enough, the CPU saves the context (pushes the PC and the other registers onto the stack), loads the address of the interrupt service routine (ISR) into the PC and runs the ISR. When the ISR has finished, the saved registers are restored from the stack and the original program carries on where it stopped.

Mark points (any four):
- definition: a signal from a device asking the CPU to stop and deal with an event;
- the CPU finishes the current instruction and checks for interrupts at the end of the fetch–execute cycle, then checks the priority (a lower-priority interrupt waits);
- the context is saved: the PC and the other registers are pushed onto the stack;
- the address of the ISR is loaded into the PC and the ISR runs;
- the registers are restored from the stack and the program continues where it stopped.

(On a pipelined RISC processor, the partly finished instructions in the pipeline must also be discarded and restarted afterwards, or saved.)

### Question 10 — Parallel processing

**(a)** Mark points (one each):
- **SIMD:** one instruction is carried out on many data items at the same moment by many processing units;
- SIMD example: a GPU applying the same operation to every pixel of an image (or the vector unit of a modern CPU);
- **MIMD:** several processors each run their own instructions on their own data at the same time;
- MIMD example: a multi-core CPU (or a cluster or a supercomputer).

**(b)** Any two (1 mark each):
- thousands of processors work on parts of the same problem at the same time;
- each processor usually has its own memory and its own share of the data;
- the processors are joined by a high-speed interconnect and coordinate by passing messages;
- the task must be split into parts that can run independently, and the results combined.

### Question 11 — AND, OR and NOT gates

Mark points: one mark for each correct symbol (3) and one mark for each correct truth table (3).

**Symbols** (inputs on the left, output on the right):
- **AND:** a flat back and a round, D-shaped front; two inputs.
- **OR:** a curved back and a pointed front; two inputs.
- **NOT:** a triangle with a small circle on its output; one input.

**Truth tables:**

| A | B | AND: A.B | OR: A + B |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 |

| A | NOT: A̅ |
|---|---|
| 0 | 1 |
| 1 | 0 |

### Question 12 — Designing a logic circuit

**(a)** X = A.B̅ + B.C ("A AND NOT B, OR B AND C").

**(b)** The circuit needs four gates:
- B goes into a **NOT** gate, giving B̅;
- A and B̅ go into the first **AND** gate, giving A.B̅;
- B (split off before the NOT gate) and C go into the second **AND** gate, giving B.C;
- both AND outputs go into an **OR** gate, whose output is X.

```
                 ┌─────┐
 A ──────────────┤     │
                 │ AND ├─── A.(NOT B) ──┐
       ┌─────┐   │     │                │
 B ──┬─┤ NOT ├───┤     │                │   ┌─────┐
     │ └─────┘   └─────┘                └───┤     │
     │                                      │ OR  ├─── X
     │           ┌─────┐                ┌───┤     │
     └───────────┤     │                │   └─────┘
                 │ AND ├─── B.C ────────┘
 C ──────────────┤     │
                 └─────┘
```

Mark points: a NOT gate on B feeding an AND gate together with A (1); an AND gate for B and C, with both AND outputs going into an OR gate (1).

**(c)**

| A B C | B̅ | A.B̅ | B.C | X = A.B̅ + B.C |
|---|---|---|---|---|
| 0 0 0 | 1 | 0 | 0 | 0 |
| 0 0 1 | 1 | 0 | 0 | 0 |
| 0 1 0 | 0 | 0 | 0 | 0 |
| 0 1 1 | 0 | 0 | 1 | 1 |
| 1 0 0 | 1 | 1 | 0 | 1 |
| 1 0 1 | 1 | 1 | 0 | 1 |
| 1 1 0 | 0 | 0 | 0 | 0 |
| 1 1 1 | 0 | 0 | 1 | 1 |

X = 1 in 4 rows. Check against the words: rows 1 0 0 and 1 0 1 have A = 1 and B = 0; rows 0 1 1 and 1 1 1 have B = 1 and C = 1. Roughly 1 mark for every two correct rows of X.

### Question 13 — Simplifying Q

1. **Distributive law**, take out the common factor A.B from the first two terms: Q = A.B.(C + C̅) + A.B̅
2. **Inverse law**, C + C̅ = 1: Q = A.B.1 + A.B̅
3. **Identity law**, A.B.1 = A.B: Q = A.B + A.B̅
4. **Distributive law**, take out the common factor A: Q = A.(B + B̅)
5. **Inverse law**, B + B̅ = 1: Q = A.1
6. **Identity law**, A.1 = A: **Q = A**

Marks: 1 for reaching A.B + A.B̅, 1 for A.(B + B̅), 1 for Q = A, with the laws named. (Steps 4–6 are the worked example in draft.md.) Check: Q = 1 in exactly the four rows where A = 1 and in none of the rows where A = 0, so Q = A.

### Question 14 — GPUs, VRAM and on-device NPUs

**Model answer:** training a neural network means carrying out huge numbers of matrix multiplications (inputs × weights). They are independent of each other, so a GPU's thousands of small cores can do thousands of them in parallel, carrying out the same maths on lots of data at once; a CPU, with only a few cores, is many times slower. A large amount of VRAM matters because it is the GPU's own fast memory: it holds the model's weights and the data being processed right next to the cores, so a big model fits and the data reaches the cores fast enough to keep them busy. A phone might run a model on its own NPU so that the data never has to leave the phone: it stays private (e.g. face unlock).

Mark points (one each):
- training is mostly matrix multiplication, and the multiplications can be done in parallel;
- a GPU has thousands of small cores doing the same maths on lots of data at once, so it is much faster than a CPU;
- large, fast VRAM holds the model's weights and the data being processed close to the GPU, so the model fits and the cores are kept supplied with data;
- one valid NPU reason: the data stays private; the answer comes faster (no network delay); it works without a network; the NPU runs AI efficiently, using little battery.

### Question 15 — Calculations

**(a)**
- time: 11.6 ms = 0.0116 s
- distance there and back: 343 m/s × 0.0116 s = 3.9788 m
- distance to the object: 3.9788 m ÷ 2 ≈ **1.99 m**

**(b)**
- revolutions per second: 10 000 ÷ 60 ≈ 166.7
- time for one revolution: 60 s ÷ 10 000 = 0.006 s = 6 ms
- average rotational latency (half a revolution): 6 ms ÷ 2 = **3 ms**

**(c)**
- k = 5 stages, n = 20 instructions
- without pipelining: n × k = 20 × 5 = **100 clock cycles**
- with pipelining: k + (n − 1) = 5 + (20 − 1) = **24 clock cycles**

**(d)**
- part that can be split: 60 s − 12 s = 48 s
- split between 4 processors: 48 s ÷ 4 = 12 s
- total: 12 s + 12 s = **24 s** (2.5 times faster than on one processor, not 4 times)
