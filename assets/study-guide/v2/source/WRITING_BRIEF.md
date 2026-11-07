# Blue Impulse Study Guide V2 — writer's brief (one chapter per writer)

You are writing ONE chapter of a printed A4 study guide for the module **Hardware, Networks and Behaviorist AI**, aimed at
high-school students and university freshmen with some basic computer-science knowledge. The design system is finished;
your job is the chapter's content file, which the builder turns into designed pages.

Repository root: `/Users/abdullah/Desktop/Study/CS & AI/semester 01/cs-ai-project-01` (quote paths — they contain spaces).
Your file: `assets/study-guide/v2/source/content/chN.sg` (N = your chapter). Edit ONLY your file.
Do not edit `build.py`, `style.css`, other chapters, `front.sg` or `appendix.sg`. Do not commit.

## 1. Build and check loop (do this often)

```sh
cd "/Users/abdullah/Desktop/Study/CS & AI/semester 01/cs-ai-project-01/assets/study-guide/v2/source"
/private/tmp/claude-501/-Users-abdullah-Desktop-Study-CS---AI-semester-01-cs-ai-project-01/5b85d5a3-e48c-40a5-b6e0-62f90d927131/scratchpad/sg/bin/python -W ignore build.py --only chN --preview
```
- It prints JSON. `"problems"` lists pages whose content does not fit (`over` = pixels too tall) or is too wide. **Every page must fit: fix every problem** (cut words, split the page, narrow a table) — never leave overflow.
- Previews (8 pages per sheet) are written to `assets/study-guide/v2/build/preview/chN-01.jpg …`. **Look at them with the Read tool** after each build. To inspect one page at full size, render it with PyMuPDF from `assets/study-guide/v2/build/only-chN.pdf` (same python as above; `import pymupdf`).
- Each `@page` is exactly one printed page. Content does not flow to the next page automatically.

## 2. Markup (full reference at the top of `build.py`)

Study `content/ch1.sg` first — those pages were reviewed and set the house style.

```
@page Heading outside the boxes          (DIN Condensed, automatic)
@section 1.1 Exact subtopic name          first page of a subtopic → Contents, bookmarks, running label
Plain markdown lines = text sitting directly on the background (use this on most pages — the team asked for
text outside the window boxes, not only inside them).
@box light|dark|alt [w=60] [right|center] [small] | Box title (Smiley Sans, automatic)
  markdown body: paragraphs, lists, **bold**, tables (pipe tables), <sup>/<sub>, inline HTML/SVG allowed
  @image FILE w=40 | caption      (inside a box: picture floats right of the text; add @clear after if needed)
  @flow A > B > C   /  @stack A > B > C    (diagrams can sit inside boxes)
@end
@image FILE [w=45] [right|center] | caption      folder-style picture box (art page 7 look)
@flow A :: small second line > B > C              pill diagram, horizontal (art page 8 look)
@stack Step 1 :: detail > Step 2 :: detail          vertical pill flowchart with arrows
@cycle Observe > Act > Feedback > Update            loop
@row … @endrow                                       put two blocks side by side
@video Title | URL                                   tutorial link
@h2 Small heading outside boxes
@try … @end                                          Pause & Try (always the LAST block on a content page)
@goals … @end   @terms … @end   @practice … @end
@plane none | @plane climb|side|top tl|tr|bl|br     airliner decoration (default automatic; use none on dense pages)
```
- Box variants: `light` and `dark` are the chapter's two colours from the art; `alt` is the second light colour. Mix them; do not use the same layout on every page. Use `@row` for side-by-side comparisons, `w=` + `right` for staggered boxes like the art examples.
- Images: refer to the supplied picture by its file name (e.g. `@image 4.1 LAN.PNG w=48 right | caption`). Supplied images live in `temp contents/ai proj stage2/` (already converted in `assets/study-guide/v2/art/images/`).
- Diagrams: prefer `@flow` / `@stack` / `@cycle`, tables and, where a picture is needed but none was supplied, a clean inline SVG inside a box (flat shapes, the chapter's colours, labels ≥ 11px). Keep SVGs simple and correct.

## 3. Rules from the team (all chapters)

1. **Order inside the chapter:** page 1 = `@goals` (the learning goals, copied as bullet points — do NOT summarise; take them from `content/chapter-0N/Learning_Outcomes*.md`, fixing only spelling) plus a 2–3 sentence chapter introduction; then the **key terms** (`@terms`) on the next page(s), all together, before any content. Then the numbered subtopics. Then a **Practice** page (or two) at the end.
2. **Keep the subtopic numbers and names exactly as given in section 5 below** (from the chapter PDFs, except where the team restructured). Use `@section` on the first page of each subtopic. Page headings (`@page`) are your own short headings for the idea on that page.
3. **Explain, don't summarise.** The team's main complaint about the old guide: "it looks like a quick summary, not a textbook". Each page teaches one idea in beginner-friendly prose: define the term, explain how it works step by step, give a concrete example or worked example with numbers, then the Pause & Try. Concise and not redundant, but complete. Check every fact, number and calculation.
4. **Every content page ends with a `@try`** (Pause & Try) that tests *that page's* idea — use questions from `content/chapter-0N/exercises.md` or the chapter PDF's questions where they fit, otherwise write a good new one. **Never print answers or solutions anywhere.** Never write "Adapted from GitHub exercises" or any source note on exercises. The goals page, key-terms pages and practice pages have no `@try`.
5. **Practice page(s):** one `@practice` box per page, questions numbered 1, 2, 3 with sub-parts as nested numbered items (they print as a), b), c)). Include the chapter's exercises from `content/chapter-0N/exercises.md` and the chapter PDF's end-of-chapter questions (merge duplicates), plus anything section 5 asks for. Keep marks like `[2 marks]` where given.
6. **Tables** get white cell borders automatically — keep tables to ≤ 4 columns and short cell text.
7. **Analogies:** every analogy in the chapter must have a picture: use the supplied image where section 5 lists one; otherwise draw a simple inline SVG or a pill diagram that shows the analogy.
8. **Video tutorial links** go at the end of the topic they teach (see section 5) with `@video`.
9. **Keep it in British/international English, friendly second person ("you").** No emoji. No "Pause & Try" outside content pages.
10. Aim for the page count in section 5; it is a guide, not a limit — quality and completeness come first.

## 4. Your sources (read before writing)

- Team chapter PDF text (scope + numbering): `assets/study-guide/v2/source/notes/chN.txt`
- Team's revision notes for the old guide: `temp contents/ai proj stage2/1STUDY GUIDE REVISION/STUDY GUIDE FIX FIX.md` — read the section `[ Chapter N revision ]` (Chapter 3: `notes/ch3improve.txt`). Page numbers in those notes refer to the OLD guide; its text, page by page, is in `notes/old_guide_chN.txt`. Every point in your chapter's notes must be addressed.
- Repo chapter materials: `content/chapter-0N/` → `Learning_Outcomes*.md`, `Key_Terms_*.md`, `exercises.md`, `draft.md`.
- Supplied images: `temp contents/ai proj stage2/*.PNG` (open the ones for your chapter with Read to see them).

## 5. Chapter specifics

Video URLs: `https://github.com/user-github-me/cs-ai-project-01/blob/main/assets/tutorials/stage2/videos/<FILE>`

### Chapter 1 — The Fundamentals (Dawn) · ~26 pages
Subtopics: 1.1 Number Systems & Data Representation · 1.2 Multimedia Representation & Compression · 1.3 Computer Architecture & The Von Neumann Model · 1.4 Operating Systems & Software Architecture · 1.5 Language Translators & Code Execution.
`ch1.sg` already contains reviewed sample pages (goals, key terms, Binary system, Binary/Denary/Hexadecimal, Representing negative values, Fetch–execute cycle, Practice) — keep their style, extend and complete the chapter around them (you may refine them). Address revision items 4–23 (items 1–3 are front matter, handled elsewhere): binary system + KiB vs KB; three systems + "why engineers use hexadecimal"; detailed negative values; separate "Binary-coded decimal system (BCD)" and "ASCII system" on one page; replace "one pattern, different interpretations" with a clear explanation; "Digital images" (pixels, colour depth); bitmap vs vector; "Multimedia" with a Sound section (conversion, sampling in detail); keep the compression table and explain all lossy and lossless types; "Process execution" with much more explanation, a picture, what the fetch–execute cycle is doing and what comes next; translators (what a translator is, types, what each suits); "Utility software" (disk formatter, virus checker, defragmentation, repair, file compression, back-up) and detailed OS jobs (memory, hardware, security, process management); peripherals (what they are, common ones, USB/HDMI/VGA); interrupts; two-pass assembler, assembly vs machine code, tracing a short program; IDE features. Practice: cohesive, one box per page.
Images: `1.1 hexadecimal` (under hexadecimal — already placed), `1.2 compression methods` (under compression methods), `1.4 OS` (under operating system), `1.5 computer language` (under language translators).
Video: Program execution → end of the process-execution topic (1.3): `BlueImpulse_Video05_Program_Execution.mp4` (already on the sample page; keep it at the end of the topic).

### Chapter 2 — Behaviorism & Behaviorist AI (Morning) · ~20 pages
Subtopics: 2.1 Foundations of Behaviorism · 2.2 Behaviorist AI & Behavior-Based Robotics · 2.3 Introduction to Reinforcement Learning (RL) · 2.4 Markov Decision Processes (MDPs) Made Simple.
The revision notes are long and specific (pages 23–33): make the central principle of behaviourism prominent; develop classical vs operant conditioning; add "From Operant Conditioning to Reinforcement Learning"; explicitly DEFINE Behaviourist AI and distinguish it from psychological behaviourism; reactive control vs learned behaviour as a central distinction; simplify subsumption with the obstacle-avoidance / target-seeking / basic-movement example; explain every part of Sensor → Behaviour rule → Actuator → Environment; grid-world worked example; one complete RL interaction step by step; reward vs value vs return vs policy with numbers; penalties = negative rewards; epsilon-greedy with Q = 5 / 8 / 3; exploration improves estimates; a real robot safety example; correct Q-learning notation Q(s,a) ← Q(s,a) + α[r + γ max<sub>a'</sub> Q(s',a') − Q(s,a)] with every symbol defined and terminal states explained; purpose of an MDP; Markov property with the position-vs-speed example; S, A, P, R, γ tied to one example; transition probabilities compared across two actions (risky vs predictable); adaptation to new environments, training vs deployment; behaviour-based robotics vs RL vs neural networks. Fix the Pause & Try questions exactly as the notes ask (numerical Q-update question; the 70% +10 / 30% −4 expected-reward question). Key terms must include classical conditioning, operant conditioning, Behaviourist AI, behaviour-based robotics, reactive control, sensor, actuator, reinforcement, punishment (plus the existing ones).
Images: `2.1 living organisms` (foundations of behaviourism), `2.2 robot` (under the GOFAI paragraph), `2.4 analogy boardgame` (the board-game / Snakes & Ladders analogy). Other analogies (restaurant, vacuum cleaner…) need a simple drawn picture.
Video: Basic reinforcement learning → end of 2.3: `BlueImpulse_Video01_Basic_Reinforcement_Learning.mp4`.

### Chapter 3 — Hardware (Midday) · ~26 pages
The team RESTRUCTURED this chapter (`notes/ch3improve.txt`) — use exactly these subtopics, in this order:
3.1 Input, Processing and Output Hardware · 3.2 Computer Memory and Storage · 3.3 Processing Devices and CPU Architecture · 3.4 Parallel Processing and Computer Systems · 3.5 Logic Circuits and Boolean Algebra · 3.6 How Hardware Enables AI.
Key terms all together at the start. 3.1 opens with text elaborating what hardware is (with window boxes and a Pause & Try), then "Input and Output" (key input/output devices with examples: keyboards, headphones, speakers, sensors, touchscreens …; as many pages as needed). 3.2 "Computer Memory and Storage": primary vs secondary, RAM, ROM, SRAM, DRAM, PROM, EPROM (and EEPROM/flash), their uses in a range of devices and their differences, magnetic/solid-state/optical storage — small sections with mini headings. 3.3 "Processing Devices and CPU Architecture": inside the CPU, registers (MAR, PC, MDR, CIR, ACC…), the buses and their directions, beginner-friendly. 3.4 "Parallel Processing & Computer Systems": RISC vs CISC, pipelining and registers in RISC (laundry analogy with a clear diagram), SISD/SIMD/MISD/MIMD, massively parallel computers, interrupt handling on CISC and RISC, parallel processing. 3.5 "Logic Circuits and Boolean Algebra": each gate in steps (AND, OR, NOT, NAND, NOR, XOR with symbols drawn in SVG and truth tables), logic circuits, Boolean algebra, and a worked truth-table example walked through. 3.6 "How Hardware Enables AI": short separate text sections (software needs hardware; CPU/GPU/RAM/VRAM/SSD roles; matrix maths; memory bandwidth; sensors & edge AI; limits & accelerators) and a Pause & Try. Also cover embedded systems/microcontrollers, sensors/actuators/ADC/DAC and control loops, touchscreens/OLED/3D printing from the PDF where they fit (3.1).
Images: `3.1 CPU` (in the CPU / processing architecture topic), `3.2 RAM` (where RAM is explained), `3.2 CD` (where CDs / optical storage are explained), `3.3 input hardware` (where input hardware is introduced), `3.3 input hardware, sensor` (where sensors are input hardware).
Video: How hardware enables AI → end of 3.6: `BlueImpulse_Video02_How_Hardware_Enables_AI.mp4`.

### Chapter 4 — Networking (Afternoon) · ~28 pages
Subtopics: 4.1 Network Architecture & Topologies · 4.2 Client Computations & Cloud Technologies · 4.3 Hardware Required to Support a LAN · 4.4 Transmission Media & Collision Handling · 4.5 Internet Infrastructure, URLs & DNS · 4.6 Protocols & The TCP/IP Protocol Stack · 4.7 Network Security, Privacy & Data Integrity · 4.8 Switching Mechanisms: Circuit vs. Packet Switching · 4.9 Cryptography, Quantum Security & Digital Certificates. (The PDF's 4.10 exercises become the Practice pages.)
Address every revision note (old pages 52–70): LAN/WAN characteristics in detail (ownership, speed, reliability, media) and keep MAN/PAN/WPAN brief; real-world examples + cost/security differences for client-server vs P2P; thin vs thick client storage; public/private cloud examples; how routers choose routes; the hardware needed to build a LAN; CSMA/CD and CSMA/CA step by step with a collision illustration; IPv4 vs IPv6 formats and practical differences; a DNS lookup example and a complete resolution diagram; TCP/IP layer interaction and an encapsulation illustration; HTTP, FTP, POP3, IMAP, SMTP with practical examples (SMTP properly explained); packet-switching benefits and drawbacks; bandwidth/latency only briefly; protection methods (digital signatures, user accounts, passwords, antivirus, anti-spyware, access rights, encryption); encryption/decryption demonstrated; public/private keys sending a secure message; obtaining a digital certificate and how certificates, public keys and signatures relate; block/stream/CBC kept brief; QKD eavesdropping detection explained simply. Key terms must separately include IP address, DNS, URL, HTTP, FTP, POP3, IMAP, phishing, pharming, hacking, virus, spyware, encryption, decryption, public key, private key (plus the existing ones). Practice must cover LAN/WAN, cloud, DNS, TCP/IP layers, collision handling, QKD, SSL/TLS, digital certificates and creating/verifying digital signatures.
Images: `4.1 analogy whispering` (the people-whispering analogy), `4.1 LAN` (where LAN is introduced), `4.4 analogy party` (the dark-room party analogy for collisions), `4.6 analogy mail` (the mail/postal encapsulation analogy), `4.7 security` (security topic).
Video: Network challenges → after collision handling (4.4) or the TCP/IP layers (4.6): `BlueImpulse_Video03_Network_Challenges.mp4`.

### Chapter 5 — Applications (Dusk) · ~16 pages
The team RESTRUCTURED this chapter (revision notes "[Chapter 5 revision]"). Use these subtopics, numbered in order:
5.1 Applications of Hardware, Networks and Behaviorist AI in Real-Life Situations · 5.2 Smart Homes · 5.3 Healthcare · 5.4 Transportation · 5.5 Industry & Manufacturing · 5.6 Education · 5.7 Conclusion.
More explanatory text, fewer "smart-sounding" boxes; short example situations may use window boxes, longer ones become paragraphs. 5.1: how the three topics come together in real life (use the PDF's smart-system anatomy: sensors, network, processor, actuators; real-time processing). 5.2 connected devices, sensors, AI-driven automation. 5.3 wearables, patient monitoring, intelligent health systems. 5.4 smart traffic systems, connected vehicles, autonomous technology (use the PDF's braking/latency worked example). 5.5 robotics, automated production, smart factories (reward design / RL in robots fits here). 5.6 smart learning devices, connected classrooms, adaptive learning. 5.7 how the three technologies combine to shape everyday life and future innovation. Bring in the PDF's valuable ideas (real-time constraints, automation spectrum, human-AI interaction, transparency, ethics, smart cities, security/privacy risks) where they fit.
Images: `5.1 smart system` (5.1/5.2 where smart systems are introduced), `5.2 workexamplebraking` (the braking worked example), `5.7 reader activity emergency room` (the emergency-room activity, Healthcare), `5.8 reward system` (where rewards/reinforcement are discussed), `5.13 smartcity` (the smart-city paragraph).
Video: Networking for behaviorist AI → in 5.1 or 5.4: `BlueImpulse_Video04_Networking_for_Behaviorist_AI.mp4`.

### Chapter 6 — Strengths & Limitations (Midnight) · ~18 pages
Subtopics (from the PDF): 6.1 Introduction to Integrated Smart Systems · 6.2 Embedded Hardware: Capabilities & Limitations · 6.3 Deep Dive: Sensor Integration and Hardware Reliability · 6.4 Network Architectures: Connectivity & Infrastructure · 6.5 Resource Optimization: Edge vs. Cloud Trade-Offs · 6.6 Behaviorist AI & Adaptive Agents · 6.7 Predictive Analytics vs. Behavioral Modeling · 6.8 Key Limitations of Behaviorist AI Models · 6.9 Ethical, Security, and Practical Concerns.
Address every revision note (old pages 85–94): advantages/disadvantages of each technology with real-world examples and how they complement each other; hardware limits across different devices (not only AI); sensor reliability and fusion compared practically, MTBF with a simple example; scalability/interoperability/resilience with practical examples and multi-vendor challenges; edge/fog/cloud with concrete examples and suitability; predictive analytics vs behavioural modelling with clear examples, adaptive intelligence vs behaviourist AI; ethical implications with real-world examples of a wrong reward function and biased data; trade-offs between automation, human oversight, reliability and safety. This chapter must EVALUATE (strengths, weaknesses, suitability) — use comparison tables and case studies. Key terms must add sensor fusion, energy efficiency, processing limitations, hardware performance, reinforcement, rewards, penalties, trial and error, learning from feedback, and clarify autonomy / adaptive intelligence / behavioural modelling. Mention that Chapter 3's video and RoverLab show limits in action where useful.
Images: `6.1` (in 6.1), `6.5 autonomous robot` (where autonomous warehouse robots are mentioned), `6.7 predictive analytics` (predictive analytics topic), `6.8 system bias` (where system bias is discussed).

## 6. When you finish

Run the build one last time: zero problems. Then reply with ≤ 12 lines: number of pages, the subtopics with their page ranges, which revision notes were addressed and any you could not, and anything the design could not express.
