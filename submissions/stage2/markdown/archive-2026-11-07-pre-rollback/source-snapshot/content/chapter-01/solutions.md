# Chapter 1 — The Fundamentals

## Explained answers

These are expected answers, not the only acceptable wording. Credit a correct alternative with clear assumptions and reasoning. Try the exercises before reading this section.

### Answer 1.1a1

79. The sign bit is 0, so add the weights 64 + 8 + 4 + 2 + 1.

### Answer 1.1a2

−102. In eight-bit two’s complement, −128 + 16 + 8 + 2 = −102. Alternatively invert 10011010 and add 1 to obtain 01100110 = 102, then negate.

### Answer 1.1a3

11001011. +53 is 00110101; invert to 11001010 and add 1. Check: −128 + 64 + 8 + 2 + 1 = −53.

### Answer 1.1a4

−128 through +127 inclusive: −2^7 to 2^7 − 1. There are 256 distinct eight-bit patterns.

### Answer 1.1b1

0111 1001 1000. Encode the decimal digits 7, 9 and 8 separately; do not convert the entire value to ordinary binary.

### Answer 1.1b2

9776. The four nibbles represent decimal 9, 7, 7 and 6.

### Answer 1.1c

A decimal digital display can store each displayed digit as one BCD nibble. Some decimal arithmetic systems also use BCD; it uses more bits than ordinary binary for most multi-digit values.

### Answer 1.2a1

Sampling resolution (bit depth) is the number of bits used to encode the amplitude of each audio sample.

### Answer 1.2a2

More bits per sample provide more quantisation levels, reducing amplitude quantisation error for a given signal range. This increases raw storage and does not itself increase the number of time samples per second.

### Answer 1.2b1

For a stored bitmap, pixel dimensions describe the number of pixels across and down. In display or print contexts, resolution can also mean pixel density. State the intended meaning and units.

### Answer 1.2b2

4 bits per pixel, because 2^4 = 16 colour codes.

### Answer 1.2b3

256 colours require 8 bits = 1 byte per pixel. 16,384 × 512 = 8,388,608 bytes. Divide by 1,073,741,824 bytes/GiB to obtain 0.0078125 GiB (8 MiB). This excludes palette, header and compression.

### Answer 1.3

PC → MAR; memory[MAR] → MDR; increment PC; MDR → CIR; decode; execute. This is the supplied one-word teaching model. Implementations can overlap operations and use different instruction lengths.

### Answer 1.4

A backup permits recovery after accidental deletion, corruption, device failure or an attack. Keep a separate recoverable copy with appropriate access controls and test restoration; synchronisation alone can also synchronise a deletion.

### Answer 1.5

An assembler translates assembly operations and labels into machine instructions. A compiler translates source into another representation, such as native instructions or bytecode. An interpreter executes operations through a runtime. Real implementations can combine these approaches; a language is not inherently limited to one.
