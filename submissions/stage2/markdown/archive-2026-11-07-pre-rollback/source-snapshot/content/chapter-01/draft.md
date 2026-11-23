# Chapter 1 — The Fundamentals

**Learning outcome:** Represent numbers, characters, images and sound; explain stored programs, registers and the fetch–execute cycle; compare translators; describe operating-system tasks, utilities, interrupts and peripheral connections.

**Prerequisites:** Basic arithmetic; Chapter 1 supplies representation and execution foundations.

## From bits to bytes

### Two states, many meanings

A bit is a binary digit: 0 or 1. Electronic circuits distinguish two ranges of voltage, allowing hardware to store and process bits reliably. Eight bits form one byte. A word is the group of bits a processor handles as a unit; its size depends on the architecture. The same pattern may represent a number, a character or an instruction: the interpretation supplies the meaning.

### Measure storage accurately

| Prefix | Bytes |
| --- | --- |
| kB / MB / GB | 1,000 / 1,000,000 / 1,000,000,000 |
| KiB / MiB | 1,024 / 1,048,576 |
| GiB / TiB | 1,073,741,824 / 1,099,511,627,776 |

### Units matter

Lowercase b means bit; uppercase B means byte. Divide bits by 8 to obtain bytes. Decimal prefixes use powers of ten; binary prefixes use powers of two. For example, 2 KiB = 2 × 1,024 = 2,048 bytes. A network speed in Mb/s is not the same unit as a file size in MB.

### Apply and check

**Try before reading feedback:** A log is 2 KiB. How many bits must be transferred, before protocol overhead?

**Feedback:** 2 × 1,024 × 8 = 16,384 bits. Keep binary storage prefixes separate from decimal link-rate prefixes.

**Practice connection:** Exercise 1.2b3 in exercises.md; explained answer in solutions.md.

## Binary, denary & hex

### Place value does the work

Denary uses powers of 10. Binary uses powers of 2, so the positions in an eight-bit number are 128, 64, 32, 16, 8, 4, 2 and 1. Add the positions containing 1: 00101101 = 32 + 8 + 4 + 1 = 45. To convert denary to binary, select those powers of two, or repeatedly divide by 2 and read the remainders backwards.

### Hexadecimal groups four bits

| Binary nibble | Hex | Denary |
| --- | --- | --- |
| 0000–1001 | 0–9 | 0–9 |
| 1010 / 1011 / 1100 | A / B / C | 10 / 11 / 12 |
| 1101 / 1110 / 1111 | D / E / F | 13 / 14 / 15 |

### Why engineers use hexadecimal

Group binary digits in fours from the right: 0010 1101 becomes 2D. Hexadecimal is a compact notation for the same value, useful in memory dumps, colour codes and hardware addresses. Binary addition carries when a column reaches 2: 1 + 1 = 10. With a fixed width, check whether a carry or signed overflow changes the interpretation.

### Apply and check

**Try before reading feedback:** Pip reports status 0x2D. Express the same unsigned value in binary and denary.

**Feedback:** 0010 1101 and 45; hexadecimal changes notation, not the stored value.

**Practice connection:** Exercise 1.1a1 in exercises.md; explained answer in solutions.md.

## Represent negative values

### Three eight-bit representations of −5

| Method | Representation | Rule |
| --- | --- | --- |
| Sign and magnitude | 10000101 | Sign bit + magnitude |
| One’s complement | 11111010 | Invert the bits of +5 |
| Two’s complement | 11111011 | Invert +5, then add 1 |

### Read two’s complement

The leftmost bit has a negative weight. In eight bits, 11111011 means −128 + 64 + 32 + 16 + 8 + 2 + 1 = −5. In n bits, the range is −2^(n−1) to 2^(n−1) − 1. Always state the width: a bit pattern has no unique signed meaning without a representation and a width.

### Subtract by adding the negative

To calculate 9 − 3 in eight bits, add 00001001 to the two’s complement of 00000011: 11111101. Keep the eight result bits, giving 00000110. A carry outside the width is discarded. Signed overflow occurs when the true result lies outside the representable range; it is not the same as an unsigned carry.

### Apply and check

**Try before reading feedback:** An eight-bit signed sensor adds 100 and 40. Can the exact sum fit?

**Feedback:** No. The true sum 140 exceeds +127, so eight-bit signed overflow occurs. Do not reinterpret the wrapped result as the true physical value.

**Practice connection:** Exercise 1.1a3 in exercises.md; explained answer in solutions.md.

## Numbers, characters & codes

### BCD stores one decimal digit at a time

Binary-coded decimal allocates four bits to each decimal digit. Decimal 259 becomes 0010 0101 1001. This is different from converting the whole number 259 to ordinary binary. Patterns 1010–1111 are unused as decimal digits in ordinary BCD. Decimal representations are useful where exact decimal digits matter, including displays and some financial calculations.

### Characters need an agreed code

A character set defines the available characters. An encoding maps characters to stored values. ASCII defines 128 codes, covering English letters, digits, punctuation and control characters. Unicode assigns code points to characters from many writing systems. UTF-8 and UTF-16 are ways to encode those code points; Unicode does not mean every character occupies the same number of bytes.

### One pattern, different interpretations

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Bits |
| 2 | Encoding / format |
| 3 | Meaning |

An application must know the agreed format before it can interpret stored data.

### Apply and check

**Try before reading feedback:** A display sends digits 2 and 5 as BCD. Is 0010 0101 the ordinary binary value 25?

**Feedback:** No. The nibbles encode decimal digits 2 and 5. As one unsigned binary byte, the same pattern is 37.

**Practice connection:** Exercise 1.1b2 in exercises.md; explained answer in solutions.md.

## Build a digital image

### Pixels and colour depth

A bitmap is a grid of pixels. Pixel dimensions describe its width and height; resolution may also describe pixel density when an image is displayed or printed. Colour depth is the number of bits used per pixel. With b bits per pixel, up to 2^b different codes are available. More pixels preserve finer spatial detail; more bits per pixel allow more colour or intensity values.

### Uncompressed bitmap size

| Quantity | Example |
| --- | --- |
| Dimensions | 1,000 × 500 pixels |
| Colour depth | 8 bits per pixel |
| Raw pixel data | 1,000 × 500 × 8 = 4,000,000 bits |
| In bytes | 4,000,000 ÷ 8 = 500,000 bytes |

### Bitmap versus vector

A vector image stores shapes, paths and their properties. It can scale without pixelation, making it useful for diagrams and logos. Photographs are normally bitmaps. The size formula above excludes headers, palettes, metadata and compression; an actual file may have a different size.

### Apply and check

**Try before reading feedback:** Halve both dimensions of a 1,000 × 500 eight-bit bitmap. What happens to raw pixel size?

**Feedback:** 500 × 250 × 1 byte = 125,000 bytes, one quarter of 500,000. Halving two dimensions quarters the pixel count.

**Practice connection:** Exercise 1.2b2 in exercises.md; explained answer in solutions.md.

## Sample, store & compress

### Turn an analogue wave into numbers

An analogue-to-digital converter samples a sound signal. Sampling rate is the number of samples per second, in hertz. Sampling resolution, or bit depth, is the number of bits per sample. A higher rate can represent a wider range of frequencies; a greater bit depth provides finer amplitude steps. Both increase uncompressed storage requirements.

### Estimate audio size

Uncompressed audio size in bits = sampling rate × bit depth × channels × duration. For 10 seconds of mono audio at 8,000 samples/s and 16 bits/sample: 8,000 × 16 × 1 × 10 = 1,280,000 bits, or 160,000 bytes. Stereo requires two channels.

### Choose the right compression

| Lossless | Lossy |
| --- | --- |
| Reconstructs the original data exactly. | Permanently discards some information. |
| ZIP, run-length encoding, PNG. | JPEG images, MP3 audio. |
| Suitable for programs and exact records. | Useful when smaller media files justify reduced fidelity. |

### Apply and check

**Try before reading feedback:** Keep the duration and bit depth fixed but change mono to stereo. Predict raw audio size.

**Feedback:** It doubles because channels change from 1 to 2. Compression and headers can change the actual file size.

**Practice connection:** Exercise 1.2a2 in exercises.md; explained answer in solutions.md.

## The stored-program computer

### Instructions and data share memory

In the introductory Von Neumann model, memory holds both instructions and data. The CPU fetches instructions, decodes them and performs the required operations. The arithmetic logic unit (ALU) performs calculations and comparisons. The control unit coordinates the operation of the CPU, memory and input/output devices. Registers hold small amounts of immediately needed information.

### The main connections

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | CPU |
| 2 | System buses |
| 3 | Memory / I/O |

Address bus: identifies a location. Data bus: carries instructions or values. Control bus: carries signals such as read and write.

### Timing and the bottleneck

The system clock coordinates operations. A clock frequency of 3 GHz means three billion clock cycles per second, not necessarily three billion completed instructions. Cache and pipelining reduce some delays, but moving instructions and data through shared resources can still restrict throughput. Real processors extend this simplified model in many ways.

### Apply and check

**Try before reading feedback:** Pip has a 3 GHz processor. A friend says it therefore finishes exactly three billion instructions each second. Find the error.

**Feedback:** GHz counts clock cycles, not completed instructions. Work per instruction, parallel issue, stalls and workload all affect instruction throughput.

**Practice connection:** Exercise 1.3 in exercises.md; explained answer in solutions.md.

## Fetch / decode / execute

### Follow one instruction

| Step | Register transfer or action |
| --- | --- |
| 1 | Copy the address in PC to MAR. |
| 2 | Read the memory instruction into MDR. |
| 3 | Advance PC to the next instruction address. |
| 4 | Copy the instruction from MDR to CIR. |
| 5 | Decode the operation and its operand. |
| 6 | Execute; store a result or change control flow. |

### Give each register a job

PC is the program counter: the next instruction address. MAR identifies the memory location being accessed. MDR holds data moving to or from memory. CIR holds the current instruction. ACC is an accumulator for intermediate arithmetic results in this teaching model. A branch instruction may replace the normal next value of PC.

### A useful analogy

Think of a recipe: PC marks the next recipe line, MAR selects its location, MDR carries the line, CIR holds the instruction being followed, and ACC is a temporary mixing bowl. In this simplified one-word instruction model PC advances by 1; actual instruction sizes and timing depend on the processor.

### Apply and check

**Try before reading feedback:** While fetching the instruction at address 100, which register identifies the address and which carries the instruction from memory?

**Feedback:** MAR contains 100; MDR carries the fetched instruction. CIR holds the current instruction after the relevant transfer.

**Practice connection:** Exercise 1.3 in exercises.md; explained answer in solutions.md.

## From source code to execution

### Three translator roles

| Tool | Input and result |
| --- | --- |
| Assembler | Assembly mnemonics and labels become machine instructions. |
| Compiler | Source program becomes another representation, often native code or bytecode. |
| Interpreter | Runs program operations through a runtime, sometimes using bytecode. |

### Choose the right level

Machine code contains the instructions a processor executes. Assembly exposes architecture-specific operations and registers. High-level languages offer abstractions such as variables, functions and data structures. They improve portability, but some translation or runtime support is still needed. A language may have both compiled and interpreted implementations.

### Trade-offs are implementation-dependent

Ahead-of-time compilation can support fast execution and catch some errors before running. Interpretation can support rapid experimentation and interactive debugging. Many modern systems combine compilation, interpretation and just-in-time compilation. It is too simple to say that all interpreters translate one source line at a time or that all compilers produce a standalone executable.

### Apply and check

**Try before reading feedback:** A language runs through bytecode in a virtual machine. Must it be called either compiled or interpreted, never both?

**Feedback:** No. A compiler may produce bytecode and a runtime may interpret or just-in-time compile it. Describe the implementation stages.

**Practice connection:** Exercise 1.5 in exercises.md; explained answer in solutions.md.

## Trace a tiny program

### Teaching assembly: one instruction per address

| Address | Instruction | Meaning |
| --- | --- | --- |
| 100 | LOAD #3 | Put the literal value 3 in ACC. |
| 101 | ADD #4 | Add the literal value 4 to ACC. |
| 102 | STORE 200 | Copy ACC to memory address 200. |
| 103 | HALT | Stop this teaching program. |

### Watch state change

Start with PC = 100. After LOAD, ACC = 3. After ADD, ACC = 7. STORE copies 7 to address 200; it does not mean “store the number 200”. The # sign denotes an immediate value in this invented teaching notation. The example illustrates execution; it is not the instruction set of a particular real CPU.

### Two passes and a helpful editor

A two-pass assembler first builds a table connecting labels to addresses, then uses it to resolve operands and encode instructions. An integrated development environment (IDE) combines editing, syntax highlighting, completion, translation and debugging. Breakpoints and single-stepping let you inspect the changing PC, registers and memory.

### Apply and check

**Try before reading feedback:** Change ADD #4 to ADD #9 in the supplied program. Predict ACC and memory[200] after STORE.

**Feedback:** Both are 12: LOAD sets ACC to 3, ADD makes 12, and STORE copies the result. PC finally reaches 104 in this model after HALT is fetched.

**Practice connection:** Exercise 1.5 in exercises.md; explained answer in solutions.md.

## The operating system’s jobs

### Coordinate shared resources

| Management task | Purpose |
| --- | --- |
| Processes | Schedule CPU time and coordinate running programs. |
| Memory | Allocate and protect memory; manage virtual memory. |
| Devices and files | Use drivers, organise storage and provide I/O services. |
| Security | Authenticate users and enforce access permissions. |

### Utilities support maintenance

Backup software creates recoverable copies; test restoration as well as copying. Antivirus checks for known and suspicious malware activity. A formatter prepares a file system and may destroy access to existing data. Repair tools check file-system structures. Compression tools reduce storage or transfer size. Defragmentation helps some hard disks; it is not routine maintenance for SSDs.

### Software does not replace hardware

The OS provides a managed interface to physical resources. A program still needs CPU time, working memory and access to its files. Good resource management improves sharing and responsiveness, but it does not remove limits in memory capacity, processing speed or storage performance.

### Apply and check

**Try before reading feedback:** Pip loses its main drive after a backup was made yesterday. What should the team test before promising recovery?

**Feedback:** Restore the backup to a safe target and check required files and versions. A successful copy log alone does not establish recoverability.

**Practice connection:** Exercise 1.4 in exercises.md; explained answer in solutions.md.

## Events, interrupts & peripherals

### Respond without checking everything constantly

An interrupt requests the processor’s attention. For an enabled interrupt, the processor and operating system preserve the required execution state, transfer control to an interrupt service routine, then restore state and resume. Exact timing and saved registers depend on the architecture. Not every request is handled immediately; priorities and masking affect when it is serviced.

### Interrupt service, conceptually

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Running task |
| 2 | Save context |
| 3 | Service event |
| 4 | Restore / resume |

A timer interrupt helps an OS share CPU time; an input device may interrupt when data becomes available.

### Common peripheral connections

| Connection | Typical purpose |
| --- | --- |
| USB | Serial data, plug-and-play peripherals; many versions also provide power. |
| HDMI | Digital video and audio for a display. |
| VGA | Legacy analogue video connection. |

### Apply and check

**Try before reading feedback:** A sensor interrupt arrives while a calculation is running. Why save context?

**Feedback:** The system needs enough state to resume the interrupted calculation correctly after the interrupt service routine.

**Practice connection:** Exercise 3.6 in exercises.md; explained answer in solutions.md.

## Chapter review

Complete ACT-01 using the supplied mission instructions. Then choose two related terms and explain a mechanism using both; identify one limitation of the teaching model and one condition that could change the result.

## Reference support

- R2: Nand to Tetris — Project 5: Computer Architecture — Project overview, proposed computer architecture and hardware simulator guidance. https://www.nand2tetris.org/project05
- R6: The Unicode Standard — technical introduction — Unicode design principles and character encoding model. https://www.unicode.org/standard/principles.html

Full resource introductions, optional tasks and access alternatives are in ../references.md.
