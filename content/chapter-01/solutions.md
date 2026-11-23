# Chapter 1 — Answers and expected outcomes

> Attempt each activity in draft.md before reading its answer. Calculations show every step; open questions list the
> points a good answer contains. Numbering matches draft.md.

## Pause & Try

### Pause & Try 1.1 — Binary and decimal prefixes

**a)** 1 MiB = 2²⁰ bytes = 1 048 576 bytes, so 3 MiB = 3 × 1 048 576 bytes = **3 145 728 bytes**.

**b)** **Model answer:** the maker counts in decimal gigabytes (10⁹ bytes), but the operating system counts in binary gibibytes (2³⁰ bytes), so the same number of bytes gives a smaller number of GiB.

- Sold as: 16 GB = 16 × 10⁹ bytes = 16 000 000 000 bytes.
- Counted as: 1 GiB = 2³⁰ bytes = 1 073 741 824 bytes.
- 16 000 000 000 bytes ÷ 1 073 741 824 = **14.9 GiB** (to 1 decimal place).
- No space is missing: a GiB is about 7% bigger than a GB, so fewer of them fit. (Windows shows this as "14.9 GB", even though it is counting in GiB.)

### Pause & Try 1.2 — Denary to 8-bit binary

**200:** 200 − 128 = 72; 72 − 64 = 8; 8 − 8 = 0. The 1s go in the 128, 64 and 8 columns: **200 = 1100 1000**.

**99:** 128 does not fit. 99 − 64 = 35; 35 − 32 = 3; 3 − 2 = 1; 1 − 1 = 0. The 1s go in the 64, 32, 2 and 1 columns: **99 = 0110 0011** (the leading 0 keeps it 8 bits long).

| Column value | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|
| 200 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| 99 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |

Check by converting back: 128 + 64 + 8 = 200 and 64 + 32 + 2 + 1 = 99.

### Pause & Try 1.3 — Binary to denary and hex

| Column value | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|
| Bit | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 |

- **Denary:** 128 + 32 + 16 + 4 + 2 = **182**.
- **Hexadecimal:** split into nibbles and use the column values 8, 4, 2, 1 inside each one: 1011 = 8 + 2 + 1 = 11 = B and 0110 = 4 + 2 = 6, so 1011 0110 = **B6**.
- Check: B6 = 11 × 16 + 6 × 1 = 176 + 6 = 182.

### Pause & Try 1.4 — Two's complement of −53

1. Write the positive number: +53 = 32 + 16 + 4 + 1 = 0011 0101
2. Flip every bit: 1100 1010
3. Add 1: **1100 1011** = −53

Check with the −128 column: 1100 1011 = −128 + 64 + 8 + 2 + 1 = −128 + 75 = **−53**.

### Pause & Try 1.5 — Binary addition and subtraction

**a)** Add column by column from the right. The Carry row shows each 1 that was carried into a column.

| Column value | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|
| Carry | | | | 1 | 1 | 1 | | |
| 0100 1010 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 0 |
| 0010 0111 | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 1 |
| Sum | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 |

- 1s: 0 + 1 = 1. 2s: 1 + 1 = 2 → write 0, carry 1. 4s: 0 + 1 + 1 = 2 → write 0, carry 1. 8s: 1 + 0 + 1 = 2 → write 0, carry 1. 16s: 0 + 0 + 1 = 1. 32s, 64s and 128s: 1, 1, 0.
- Answer: **0111 0001**.
- Check in denary: 0100 1010 = 64 + 8 + 2 = 74 and 0010 0111 = 32 + 4 + 2 + 1 = 39; 74 + 39 = 113, and 0111 0001 = 64 + 32 + 16 + 1 = 113.

**b)** 45 − 27 = 45 + (−27).

1. Write 27: 0001 1011
2. Make it negative with two's complement: flip → 1110 0100, add 1 → 1110 0101 (check: −128 + 64 + 32 + 4 + 1 = −27)
3. Add it to 45 = 0010 1101:

| Column value | 9th bit | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|---|
| Carry | 1 | 1 | 1 | | 1 | 1 | | 1 | |
| 45 | | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 1 |
| −27 | | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 1 |
| Sum | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |

4. Ignore the carry out of the left-most bit: **0001 0010 = 16 + 2 = 18**. Check: 45 − 27 = 18.

### Pause & Try 1.6 — BCD and ASCII codes

**a)** Each denary digit gets its own nibble: 4 → 0100, 0 → 0000, 5 → 0101, 2 → 0010. So 4 052 = **0100 0000 0101 0010**. (The digit 0 still needs its own nibble, 0000.)

**b)** ASCII codes are in alphabetical order and G is 6 letters after A, so 'G' = 65 + 6 = **71**. In 8-bit binary: 71 = 64 + 4 + 2 + 1 = **0100 0111**.

### Pause & Try 1.7 — Bitmap colours and file size

**a)** 8 bits per pixel give 2⁸ = **256 colours**.

**b)**
- File size = width × height × colour depth = 800 × 600 × 8 bits = 3 840 000 bits
- 3 840 000 bits ÷ 8 = 480 000 bytes
- 480 000 bytes ÷ 1 024 = **468.75 KiB**

(The real file is slightly bigger, because it also stores a header.)

### Pause & Try 1.8 — Bitmap or vector graphic

**Model answer:** the logo should be a vector graphic, because it is made of simple shapes and colours that the computer can redraw sharply at 6 metres. The staff photo must be a bitmap, because a photo cannot be described as a list of shapes; it needs a high resolution so that it does not look pixelated when printed so large.

**Key points**
- **Logo → vector.** Lines, shapes, text and flat colours can be stored as a drawing list. The shapes are redrawn at any size, so the edges stay sharp even 6 m wide, and the file stays small. A bitmap logo enlarged that much would look jagged (pixelated).
- **Photo → bitmap.** In a photo neighbouring pixels can all be different colours, so it cannot be stored as a list of shapes. Every pixel gets bigger when the photo is enlarged, so it must be taken or scanned at a high resolution (many pixels).

### Pause & Try 1.9 — Converting sound for storage

**Model answer:** sound is analogue — the wave changes smoothly and continuously and can take endless values — but a computer can store only a limited list of binary numbers. So the wave must be sampled at regular intervals and each sample stored as a binary number.

**Key points**
- **Recording (analogue → digital): the ADC** (analogue-to-digital converter). The microphone first turns the sound into an analogue voltage; the ADC samples it and turns each sample into a binary number.
- **Playback (digital → analogue): the DAC** (digital-to-analogue converter). It turns the numbers back into a changing voltage, which an amplifier and speaker turn into sound.

### Pause & Try 1.10 — Sound file size and sampling

**a)** File size = sampling rate × sampling resolution × channels × seconds
- 8 000 Hz × 16 bits × 1 channel × 20 s = 2 560 000 bits
- 2 560 000 bits ÷ 8 = 320 000 bytes
- 320 000 bytes ÷ 1 000 = **320 kB**

(Dividing by 1 024 instead gives 312.5 KiB, which is the answer in kibibytes.)

**b)**
- **Advantage:** more samples are taken every second, so quicker changes in the wave (such as high-pitched sounds) are captured and the recording is closer to the real sound.
- **Disadvantage:** there are more samples to store, so the file is bigger: it needs more storage and takes longer to download or send.

### Pause & Try 1.11 — Choosing lossy or lossless

**a)** Program file: **lossless**. Every bit of every instruction matters; if any data were removed or changed, the program would not run correctly, so it must be rebuilt exactly.

**b)** Holiday photo for social media: **lossy** (e.g. JPEG). The photo is only for people to look at, so removing detail the eye hardly notices does no harm, and the much smaller file uploads and loads faster and uses less mobile data.

**c)** Spreadsheet of exam results: **lossless**. Every name and mark must be exactly right; losing or changing any data could give a student the wrong result.

### Pause & Try 1.12 — Run-length encoding in practice

- AAAABBBBBBCCDDDDD has runs of 4 A, 6 B, 2 C and 5 D: 17 values.
- RLE: **4A 6B 2C 5D**, which is 4 pairs = 8 values.
- Saved: 17 − 8 = **9 values**.

**Why RLE works badly on a photograph:** neighbouring pixels in a photo are almost always slightly different colours, so there are hardly any runs. Most runs are only 1 pixel long, and each pixel turns into two values (a count and a colour), so the file can get bigger instead of smaller — just as ABCD becomes 1A 1B 1C 1D.

### Pause & Try 1.13 — Stored program, CU and ALU

**Model answer:** in the stored-program concept, a program's instructions and its data are stored together in the same main memory, and the CPU fetches the instructions one at a time. The control unit decodes each instruction and sends control signals telling the other parts what to do; the ALU carries out the arithmetic and logic.

**Key points**
- **Stored program:** instructions and data share the same main memory, so a new job just means loading a different program; early computers such as ENIAC had to be rewired instead.
- **Control unit:** decodes instructions and sends control signals (along the control bus) to the ALU, registers, memory and I/O, timed by the system clock, so it controls the flow of data.
- **ALU:** does all the arithmetic (e.g. addition, subtraction) and logic operations (AND, OR, NOT, comparisons).

### Pause & Try 1.14 — Registers and buses

**a)** The **program counter (PC)**.

**b)** Each address wire doubles the number of addresses, so 24 wires give 2²⁴ = **16 777 216 memory locations**.

**c)** Data must travel both ways: from memory to the CPU when an instruction or data is read (fetched), and from the CPU to memory when a result is written (stored). Data also moves in both directions between the CPU and input/output devices. A one-way bus could do only one of these jobs.

### Pause & Try 1.15 — Order of the fetch–execute cycle

1. **PC → MAR:** the address in the PC is copied to the MAR and sent on the address bus.
2. **Memory → MDR:** the instruction stored at that address is copied to the MDR along the data bus.
3. **PC + 1:** the PC is incremented, so it holds the address of the next instruction.
4. **MDR → CIR:** the instruction is copied to the CIR.
5. **Decode:** the control unit splits it into the opcode and the operand.
6. **Execute:** the control unit sends signals so that the instruction is carried out.

**Model answer:** the PC is incremented first so that it already points at the next instruction while the CPU works on this one.

**Key points**
- The next fetch can start straight away from the address in the PC.
- If the instruction is a jump, the execute step simply puts the new address into the PC. If the PC were incremented after executing, 1 would be added to the jump address and the CPU would miss the instruction it should jump to.
- If an interrupt arrives, the saved PC already holds the address where the program must carry on.

### Pause & Try 1.16 — Handling a keyboard interrupt

**Model answer:** the CPU finishes its current cycle, saves where it was, runs the keyboard's interrupt service routine to read the key, then restores its registers and carries on with the program.

**Key points**
1. The keyboard sends an interrupt signal to the CPU (along the control bus).
2. The CPU finishes the fetch–execute cycle it is on; at the end of the cycle it checks for a waiting interrupt.
3. If the interrupt's priority is higher than the current task, the contents of the registers (including the PC) are saved. A lower-priority interrupt would have to wait.
4. The PC is loaded with the address of the keyboard's interrupt service routine (ISR).
5. The ISR runs: it reads the code of the key that was pressed (e.g. its ASCII code) and passes it on for the program to use.
6. The saved values are put back, so the PC again holds the address where the program stopped, and the program carries on.

### Pause & Try 1.17 — Peripherals, HDMI and VGA

A **peripheral** is a device connected to a computer that is not part of its core (the CPU and main memory). It plugs into a port, and the operating system controls it through a device driver.

- **Input:** a keyboard. Also acceptable: mouse, touchpad, microphone, webcam, scanner.
- **Output:** a monitor. Also acceptable: printer, speakers, headphones.
- **Storage:** a USB stick. Also acceptable: an external hard drive.

**Differences between HDMI and VGA (any two):**

| | HDMI | VGA |
|---|---|---|
| Signal | digital | analogue |
| What it carries | video and sound in one cable | video only |
| Picture | HD and 4K resolutions | loses sharpness at high resolutions and over long cables |
| Age and use | newer: TVs, monitors, projectors, games consoles | older, 15-pin plug: still found on older projectors |

### Pause & Try 1.18 — Why computers need an OS

Any three of these reasons:
1. It gives the user an **interface** (windows, icons and menus, or a command line) to start programs and manage files.
2. It **hides the hardware's complexity**: a program just asks the OS to "save this file". Without an OS, every program would need its own code to drive the screen, the keyboard and the disk.
3. It **shares out resources** (CPU time, memory, storage and devices) between the running programs, so that several programs can run safely at the same time.

Also acceptable: it organises files into folders; it keeps the system and its users' data secure (logins and access rights); it controls devices through drivers.

### Pause & Try 1.19 — Multitasking and virtual memory

**Model answer:** the OS's scheduler gives each process the CPU for a very short time and then switches to the next one so quickly that all the programs seem to run at once. Virtual memory uses part of the disk as extra memory when RAM is full.

**Key points**
- Each process gets the CPU for a short **time slice** (a few milliseconds); then a timer interrupt passes the CPU to the next process.
- The switching is so fast that the programs appear to run together: **multitasking**.
- Processes have priorities, and a process waiting for input or output is **blocked**, so it does not waste CPU time.
- **Virtual memory:** when RAM is full, the OS moves pages that are not needed right now onto the disk and brings them back when they are needed, so more programs can run than RAM alone could hold.
- Disks are slow, so constant swapping (disk thrashing) makes the computer crawl.

### Pause & Try 1.20 — OS security and device drivers

**Two ways the OS keeps a computer secure:**
- **User accounts:** each user logs in with a username and a password, PIN or fingerprint, and the OS can lock the account after several wrong attempts.
- **Access rights:** every file and folder has permissions (such as read, write or delete), and only administrators can change system settings or install software.

Also acceptable: security updates (patches) that close weaknesses; a firewall that blocks unwanted network traffic; built-in virus checking; encrypting the whole disk.

**Device driver:** a small program that lets the OS control one particular device. It translates the OS's general commands, such as "print this page", into the exact signals that this device understands. When a new USB device is plugged in, the OS identifies it and loads the right driver (plug-and-play).

### Pause & Try 1.21 — Utilities for a slow disk

- **Defragmentation software** (for the slowness): as files are created, deleted and grow, a file's blocks get scattered over the disk, so the read head has to jump around to load it. Defragmenting moves each file's blocks next to each other, so files load faster.
- **Repair software** (for the files that will not open), e.g. Check Disk in Windows or Disk Utility in macOS: it checks the disk for damaged areas and errors in the file system's records, fixes them where it can, and marks bad areas so that they are not used again.

Also acceptable: a **virus checker** (malware can slow a computer down and damage files; it finds infected files and deletes or quarantines them), or **back-up software** (files that will not open can be restored from a back-up copy).

### Pause & Try 1.22 — Source code and translators

**Model answer:** source code is the program as the programmer writes it, in a language people can read; machine code is the binary instructions the processor can execute directly. For a short script that is still being tested, use an interpreter.

**Key points**
- **Source code:** written in a programming language (e.g. Python); people can read and edit it, but the processor cannot run it directly.
- **Machine code:** binary instructions from the processor's own instruction set, executed directly. A translator converts source code into machine code.
- **Interpreter, because** it translates and runs one statement at a time, so the script runs straight away after every change without compiling the whole program first.
- It stops at the first error and shows where it is, which makes debugging easier; speed does not matter much for a short script.

### Pause & Try 1.23 — Compiler or interpreter choice

**Games company — compiler**
- The game is translated once into an executable file of machine code, which runs fast — important for a game.
- Players run the executable without needing the compiler or the source code.
- The source code stays private, so the company's work is harder to copy or change.

**Student — interpreter**
- Each statement runs straight away, so the student sees the result of every change immediately.
- It stops at the first error and shows where it is, so mistakes are easier to find and fix while learning.
- Speed and keeping the code private do not matter for practice programs.

### Pause & Try 1.24 — Machine code for LOAD #9

- Opcode of LOAD #n: 0001.
- Operand: 9 as a 12-bit binary number = 0000 0000 1001 (8 + 1 = 9).
- Machine code: **0001 0000 0000 1001**.

**LOAD #9 or LOAD 9:** the # means "use this number itself", so LOAD #9 puts the number 9 into ACC. Without the #, 9 is an address: LOAD 9 (opcode 0010, machine code 0010 0000 0000 1001) copies the value stored at memory address 9 into ACC, and that value could be any number.

### Pause & Try 1.25 — The two-pass assembler

**Model answer:** pass 1 reads the program to build a symbol table of every label and its address; pass 2 reads it again and uses the table to turn every line into machine code.

**Pass 1 — find the labels**
- Reads the program one line at a time and removes comments.
- Counts addresses, so it knows where each line will be stored.
- Checks that every mnemonic is in the instruction set.
- Adds each label to the symbol table with its address (LOOP 101, DONE 105, COUNT 106). A forward reference is added first and given its address when the label is found.

**Pass 2 — produce machine code**
- Reads the program again from the start.
- Replaces each mnemonic with its opcode and each label with its address from the symbol table: JUMPZ DONE becomes JUMPZ 105.
- Converts every operand to binary and outputs the object code, or reports errors such as a label that was never defined.

**Why one pass cannot translate line 103:** JUMPZ DONE uses the label DONE, but DONE is not defined until line 105 — a forward reference. When a one-pass assembler reaches line 103 it does not yet know DONE's address, so it cannot write the operand of the machine-code instruction. (Line 100, LOAD COUNT, has the same problem: COUNT is not defined until line 106.)

### Pause & Try 1.26 — Tracing the changed countdown

COUNT = 5, and line 102 is now SUB #2:

| Address | Instruction | ACC | Output |
|---|---|---|---|
| 100 | LOAD COUNT | 5 | |
| 101 | OUT | | 5 |
| 102 | SUB #2 | 3 | |
| 103 | JUMPZ DONE | | |
| 104 | JUMP LOOP | | |
| 101 | OUT | | 3 |
| 102 | SUB #2 | 1 | |
| 103 | JUMPZ DONE | | |
| 104 | JUMP LOOP | | |
| 101 | OUT | | 1 |
| 102 | SUB #2 | −1 | |
| 103 | JUMPZ DONE | | |
| 104 | JUMP LOOP | | |
| 101 | OUT | | −1 |
| … | … | … | … |

**Output:** 5, 3, 1, −1, −3, −5, … and the program never stops.

**Problem — an infinite loop:** starting at 5 and subtracting 2 gives only odd numbers, so ACC goes from 1 straight to −1 and is never exactly 0. JUMPZ jumps only when ACC is 0, so the program never reaches HALT at line 105. (Even in a fixed-size register that wraps round, the value stays odd, so it still never becomes 0.) One fix is an even starting value: with COUNT = 6 the output is 6, 4, 2 and then the program halts.

### Pause & Try 1.27 — IDE features for debugging

Any three of these features:
- **Error highlighting:** syntax errors are underlined as you type, so they can be fixed before the program is run.
- **Breakpoints:** the program pauses at a chosen line, so you can check the values at that point.
- **Single stepping:** the program runs one line at a time, so you can see exactly which line goes wrong.
- **Variable watch window:** shows each variable's value as it changes — like a trace table filled in for you — so you can spot the moment a value becomes wrong.

Also acceptable: the built-in run-time environment, which shows the output and any error messages straight away.

## Practice

### Question 1 — Two's complement integers

**(a)** [2 marks]
- 0100 1111: the left-most bit is 0, so it is positive: 64 + 8 + 4 + 2 + 1 = **79**.
- 1001 1010: the left-most bit is 1, so it is negative: −128 + 16 + 8 + 2 = **−102**.

**(b)** [1 mark] **1100 1011**. Working: +53 = 0011 0101 → flip every bit: 1100 1010 → add 1: 1100 1011. Check: −128 + 64 + 8 + 2 + 1 = −53.

**(c)** [2 marks] From **−128** (1000 0000) to **+127** (0111 1111).

### Question 2 — Binary-coded decimal (BCD)

**(a)** [1 mark] 7 → 0111, 9 → 1001, 8 → 1000, so 798 = **0111 1001 1000**.

**(b)** [1 mark] 1001 = 9, 0111 = 7, 0111 = 7, 0110 = 6, so the number is **9776**.

**(c)** [1 mark] Digital clocks, calculators and meters: each 4-bit group drives one digit of the display, so no conversion is needed. Also acceptable: storing amounts of money in banking systems, where keeping each decimal digit avoids small rounding errors (a value such as 0.1 cannot be stored exactly in pure binary).

### Question 3 — Sampling and image resolution

**(a)** [1 mark] The number of bits used to store each sound sample (also called the bit depth).

**(b)** [2 marks]
- More bits per sample give more levels: n bits give 2ⁿ levels (8 bits give 256, 16 bits give 65 536).
- So each sample is rounded less, the stored values are closer to the real sound wave and the sound is more accurate, with less hiss (but the file is bigger). A lower resolution means more rounding, so the stored sound is less accurate.

**(c)** [1 mark] The number of pixels in an image, written as width × height (for example 1920 × 1080).

**(d)** [1 mark] 16 = 2⁴, so **4 bits** per pixel.

**(e)** [3 marks]
- 256 colours = 2⁸, so each pixel needs 8 bits.
- 16 384 × 512 = 8 388 608 pixels; 8 388 608 × 8 bits = 67 108 864 bits.
- 67 108 864 bits ÷ 8 = 8 388 608 bytes.
- 8 388 608 bytes ÷ 1 024 = 8 192 KiB; ÷ 1 024 = 8 MiB; ÷ 1 024 = **0.0078125 GiB** (exactly 1/128 GiB).

### Question 4 — Order of the fetch–execute cycle

[6 marks]
1. The address contained in the PC is copied to the MAR.
2. The instruction is copied from the memory location in the MAR and placed in the MDR.
3. The value in the PC is incremented by 1.
4. The instruction is copied from the MDR and placed in the CIR.
5. The instruction is decoded.
6. The instruction is executed.

This is the order the chapter teaches. Some books put the PC increment straight after stage 1, because the PC can be increased while memory is being read; either way, it must come after the PC is copied to the MAR and before the instruction is executed.

### Question 5 — Why files must be backed up

[3 marks]

**Model answer:** files can be lost or damaged in many ways, and some — photos, coursework, business records — cannot be made again. A back-up is a separate copy on another device or in the cloud, so the files can be restored if anything happens to the originals. Utilities such as File History and Time Machine make the copies automatically on a schedule, so the back-up is always recent.

**Key points (any three)**
- Files can be deleted or overwritten by accident.
- The disk can fail, or files can become corrupted.
- The computer can be lost, stolen or destroyed, for example by fire or flood.
- Malware such as ransomware can lock or damage files.
- Restoring from a back-up saves work that would take a long time, or be impossible, to recreate; earlier versions of a file can also be recovered.

### Question 6 — Roles of the three translators

[6 marks]

**Model answer:** a processor can execute only machine code, so a program written in any other language must be translated first. An assembler translates low-level assembly language into machine code, one instruction for one instruction. Compilers and interpreters both translate high-level languages: a compiler translates the whole program once and produces an executable file, while an interpreter translates and runs the program one statement at a time, every time it runs.

**Key points (about one per mark)**
- **Assembler:** translates assembly language (mnemonics and labels) into machine code, one-to-one: each assembly instruction becomes one machine-code instruction. It usually works in two passes, using a symbol table for the labels.
- An assembler is used for low-level programs that control the hardware directly, e.g. device drivers and embedded systems.
- **Compiler:** translates the whole high-level program before it runs and saves an executable file, which runs fast and can be run again and again without the compiler.
- A compiler lists all the errors together and nothing runs until they are fixed; users get only the executable, so the source code stays private. Best for finished programs given to users.
- **Interpreter:** translates and executes one statement at a time, every time the program runs; no executable is saved, so it runs more slowly and users need the interpreter and the source code.
- An interpreter stops at the first error, which makes debugging easier: best for writing, learning and testing code, and for short scripts. Developers often test with an interpreter, then compile the finished version (Java mixes the two, using bytecode).

### Question 7 — Number systems and binary arithmetic

**(a)** [1 mark] 1110 = 8 + 4 + 2 = 14 = E and 0101 = 4 + 1 = 5, so 1110 0101 = **E5**.

**(b)** [1 mark] B = 11, so 3B = 3 × 16 + 11 × 1 = 48 + 11 = **59**.

**(c)** [2 marks]

| Column value | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|
| Carry | | 1 | 1 | 1 | 1 | | | |
| 0010 1101 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 1 |
| 0011 0110 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 0 |
| Sum | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |

- 1s: 1 + 0 = 1. 2s: 0 + 1 = 1. 4s: 1 + 1 = 2 → write 0, carry 1. 8s: 1 + 0 + 1 = 2 → write 0, carry 1. 16s: 0 + 1 + 1 = 2 → write 0, carry 1. 32s: 1 + 1 + 1 = 3 → write 1, carry 1. 64s: 0 + 0 + 1 = 1. 128s: 0.
- Answer: **0110 0011**.
- Check in denary: 45 + 54 = 99, and 0110 0011 = 64 + 32 + 2 + 1 = 99.

**(d)** [2 marks] Overflow happens when a result needs more bits than are available to store it. An 8-bit register can hold at most 1111 1111 = 255. For example, 200 + 100 = 300: 1100 1000 + 0110 0100 = 1 0010 1100, which needs 9 bits. The ninth bit is lost, so the register holds 0010 1100 = 44, which is wrong. The CPU sets a flag in the status register so that a program can detect the error.

### Question 8 — Text, images and sound

**(a)** [1 mark] E is 4 letters after A, so its code is 65 + 4 = 69 = 64 + 4 + 1 = **0100 0101**.

**(b)** [4 marks] Two differences, each describing both types:

| | Bitmap image | Vector graphic |
|---|---|---|
| What is stored | the colour of every pixel in a grid | a drawing list of objects (lines, circles, text) with properties such as position, size and colour |
| When enlarged | every pixel gets bigger, so edges look jagged (pixelated) | the shapes are redrawn at the new size, so they stay sharp |

Also acceptable: a bitmap's file size depends on resolution × colour depth, but a vector's depends on the number of objects; bitmaps suit photos, while vectors suit logos, diagrams and fonts.

**(c)** [3 marks]
- 3 minutes = 3 × 60 = 180 s.
- 22 050 Hz × 8 bits × 1 channel × 180 s = 31 752 000 bits.
- 31 752 000 bits ÷ 8 = 3 969 000 bytes.
- 3 969 000 bytes ÷ 1 000 000 = **3.969 MB** (≈ 3.97 MB). In binary units: 3 969 000 ÷ 1 048 576 ≈ 3.79 MiB.

**(d)** [2 marks] The row has runs of 4 W, 3 B, 6 W and 2 B, so it becomes **4W 3B 6W 2B**: 15 values become 8.

**(e)** [3 marks]

**Model answer:** music only has to sound right to human ears, so some data can be thrown away; a bank's records must be exactly right, so nothing can be lost.

**Key points**
- Lossy compression (e.g. MP3, AAC) makes songs about a tenth of their CD size by removing sounds people cannot hear, and quiet sounds masked by louder ones.
- Smaller files stream faster and use less bandwidth and mobile data, and listeners hardly notice the difference.
- One lost or changed digit in an account number or balance would be a serious error, so bank records must be compressed losslessly: the original can then be rebuilt exactly.

### Question 9 — The processor and its connections

**(a)** [2 marks]
- **MAR:** holds the address of the memory location to be read from or written to. In the fetch, the address in the PC is copied to the MAR and sent along the address bus.
- **MDR:** holds the data or instruction just read from memory, or about to be written to it. The fetched instruction arrives in the MDR along the data bus and is then copied to the CIR.

**(b)** [2 marks] The **address bus**. Addresses only ever travel from the CPU (the MAR) to memory or a device, to say which location is wanted. Memory never needs to send an address back, because the data it returns travels on the data bus.

**(c)** [4 marks]
- At the end of each fetch–execute cycle, the CPU checks for a waiting interrupt.
- If the interrupt's priority is higher than the current task, the contents of the registers (including the PC) are saved; a lower-priority interrupt has to wait.
- The PC is loaded with the address of the correct interrupt service routine (ISR), which runs and deals with the event.
- The saved values are restored, and the original program carries on from where it stopped.

**(d)** [3 marks]
- **USB:** connecting a keyboard, mouse, printer or flash drive (it can also charge a phone).
- **HDMI:** connecting a computer or games console to a TV, monitor or projector, carrying digital HD or 4K video and sound in one cable.
- **VGA:** connecting a computer to an older monitor or projector (analogue video only).

### Question 10 — Operating systems and utilities

**(a)** [2 marks] Any two:
- Allocates each program its own area of RAM when it starts, and frees it when the program closes.
- Protects each area, so that one program cannot read or overwrite another program's memory (or the OS's own).

Also acceptable: records which parts of memory are in use, and by which program; manages virtual memory, moving pages onto the disk when RAM is full.

**(b)** [3 marks]
- On a hard disk, files are saved in blocks. As files are created, deleted and grow, a file's blocks become scattered (fragmented).
- The read head then has to jump between many places to read one file, which slows loading down.
- Defragmentation moves each file's blocks next to each other, so the head moves less and files load faster.
- An SSD has no moving parts, so it reads every block equally fast wherever it is stored: fragmentation does not slow it down, and the extra rewriting would only wear out its flash memory.

**(c)** [4 marks] Two utilities, each named and described (about 2 marks each):
- **Virus checker:** scans files and memory for malware by comparing them with a database of known virus signatures and watching for suspicious behaviour; infected files are deleted or quarantined. It must be updated often.
- **Back-up software:** copies files to another device or to the cloud, often automatically on a schedule, so they can be restored if the originals are deleted, damaged, stolen or locked by ransomware.

Also acceptable: a disk formatter (sets up a file system on a new drive, or wipes a drive clean), repair software (finds and fixes disk errors and marks bad areas so they are not used), or file compression (makes files smaller, e.g. ZIP, and can pack several files into one archive).

### Question 11 — Translators and assembly language

**(a)** [1 mark] One-to-one: each assembly language instruction translates into exactly one machine-code instruction (a mnemonic stands for each binary opcode, and labels can stand for addresses).

**(b)** [4 marks]
- **Pass 1:** reads the program line by line, removes comments, counts addresses and checks that every mnemonic is in the instruction set.
- Pass 1 builds the **symbol table**: every label with its address. A forward reference is added first and given its address when the label is found.
- **Pass 2:** reads the program again, replacing each mnemonic with its opcode and each label with its address looked up in the symbol table.
- Pass 2 converts the operands to binary and outputs the object code (the machine code), or reports errors such as a label that was never defined.

**(c)** [4 marks]

| Address | Instruction | ACC | Output |
|---|---|---|---|
| 100 | LOAD #6 | 6 | |
| 101 | SUB #2 | 4 | |
| 102 | OUT | | 4 |
| 103 | JUMPZ 105 | | |
| 104 | JUMP 101 | | |
| 101 | SUB #2 | 2 | |
| 102 | OUT | | 2 |
| 103 | JUMPZ 105 | | |
| 104 | JUMP 101 | | |
| 101 | SUB #2 | 0 | |
| 102 | OUT | | 0 |
| 103 | JUMPZ 105 | | |
| 105 | HALT | | |

**Output: 4, 2, 0.** OUT runs before the JUMPZ test, so the 0 is output too; then ACC is 0, JUMPZ jumps to 105 and the program halts.

**(d)** [3 marks] Any three of these features:
- **Syntax highlighting** (pretty printing): keywords, names and text appear in different colours, so the code is easier to read and mistakes stand out.
- **Auto-completion:** the IDE suggests names and keywords as you type, which saves time and avoids spelling mistakes.
- **Automatic indentation and bracket matching:** keep the structure of the code clear.
- **Expanding and collapsing blocks of code:** lets you hide parts of the program and focus on one section.
