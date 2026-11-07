# Chapter 3 — Hardware

## Explained answers

These are expected answers, not the only acceptable wording. Credit a correct alternative with clear assumptions and reasoning. Try the exercises before reading this section.

### Answer 3.1a

Primary storage includes working memory and, in some classifications, ROM; it is accessed through the processor’s memory system. Main RAM is normally volatile and relatively fast. Secondary storage such as SSD or HDD is non-volatile and usually slower to access. Data normally moves into working memory before ordinary processing. “All primary storage is volatile” is false.

### Answer 3.1b

Magnetic: hard disk drive or magnetic tape. Optical: CD, DVD or Blu-ray. Solid-state: SSD or USB flash drive.

### Answer 3.2a

SRAM uses a bistable transistor cell and does not need periodic refresh while powered. DRAM stores charge that leaks and needs refresh. Both normally lose data without power. SRAM is fast but less dense and costlier per bit; DRAM supports larger main memories.

### Answer 3.2b

Mask ROM is fixed during manufacture. PROM can normally be programmed once. EPROM can be erased with ultraviolet light and reprogrammed; EEPROM and flash instead use electrical erasure. These names refer to different technologies, not one universal write process.

### Answer 3.3

Touchscreen = output display plus touch input. SSD = storage, with read/write data transfers. Barcode reader = input. A device can legitimately have more than one role.

### Answer 3.4

For a greenhouse, a temperature sensor provides readings to a controller; when the temperature exceeds a defined threshold, the controller drives a fan actuator. Measure again to close the loop. A lower switch-off threshold can prevent rapid on/off chatter. This is fixed-rule control unless a learning method actually updates the decision policy.

### Answer 3.5a

RISC families traditionally emphasise relatively regular, simple instruction encodings and load/store operations. CISC families traditionally provide more varied encodings and operations. Modern implementations blur boundaries and may translate complex instructions into micro-operations. Neither label alone proves speed or efficiency.

### Answer 3.5b

Pipelining overlaps stages of different instructions to increase throughput. In an ideal four-stage pipeline, three independent instructions need 4 + 3 − 1 = 6 cycles, rather than 12 sequential stage cycles. A data dependency, resource conflict or branch can cause stalls; one instruction still traverses all four stages.

### Answer 3.5c

PC holds the next instruction address; ACC holds an intermediate arithmetic result in the teaching model; MDR holds a value or instruction being transferred between memory and the processor. A store address belongs in MAR, not automatically in ACC.

### Answer 3.6

A hardware interrupt is a request from hardware for service. When an enabled request is accepted, the system saves the execution state it needs, transfers control to an interrupt service routine, then restores state and resumes. Masking, priorities and architecture affect when this occurs.

### Answer 3.7

AND: 00→0, 01→0, 10→0, 11→1. OR: 00→0, 01→1, 10→1, 11→1. NOT: 0→1, 1→0. The usual AND symbol has a flat input side and rounded output side; OR has a curved input side; NOT is a triangle with an inversion circle. Named rectangular gate symbols are also valid if used consistently.
