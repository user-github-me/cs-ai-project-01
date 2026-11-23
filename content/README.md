# Hardware, Networks & Behaviorist AI — module content (V2.0)

**Team Blue Impulse** · Beginner's Guide: *How Machines Sense, Connect, and Act*

This folder is the shared Markdown source of the module. It is written for **high-school students and university
freshmen who already know some basic computer science**. The six chapters build one connected story: how a machine
represents and processes information (Chapter 1), how behaviour can be learned from consequences (Chapter 2), the
hardware that senses and computes (Chapter 3), the networks that connect machines (Chapter 4), how the three ideas
combine in real applications (Chapter 5), and where they succeed or fail (Chapter 6).

## Module learning outcomes

By the end of the module you should be able to:

1. **Represent and process data** — convert between binary, denary and hexadecimal; explain how numbers, text, images and sound are stored and compressed; trace the fetch–execute cycle; describe the roles of the operating system and language translators.
2. **Explain behaviour-based intelligence** — relate classical and operant conditioning to Behaviourist AI and reinforcement learning; define states, actions, rewards, value and policy; calculate a Q-learning update and an expected reward in an MDP.
3. **Describe and compare hardware** — classify input, output, storage and processing devices; compare memory and storage types; explain CPU registers, buses, pipelining and parallel architectures; build and simplify logic circuits; explain how hardware enables AI.
4. **Explain how networks work** — compare network types and models; trace how data finds its destination (IP, DNS, TCP/IP layers, switching); handle collisions; explain the main threats and protection methods, including encryption and digital certificates.
5. **Apply the three topics together** — analyse smart homes, healthcare, transport, industry and education systems as sense–connect–decide–act loops, including their timing and safety needs.
6. **Evaluate strengths and limitations** — judge where hardware, networks and behaviourist AI are suitable, using evidence about cost, reliability, bias, security, privacy and accountability.

Each chapter's detailed learning goals are in its `Learning_Outcomes*.md` file and at the start of its `draft.md`.

## Learning sequence

| Chapter | Subtopics | Builds on | Leads to |
| --- | --- | --- | --- |
| [1 · The Fundamentals](chapter-01/README.md) | 1.1 Number systems · 1.2 Multimedia & compression · 1.3 Von Neumann model & process execution · 1.4 Operating systems · 1.5 Language translators | basic arithmetic | binary data and the CPU are used in every later chapter |
| [2 · Behaviorism & Behaviorist AI](chapter-02/README.md) | 2.1 Foundations of behaviorism · 2.2 Behaviorist AI & behaviour-based robotics · 2.3 Reinforcement learning · 2.4 Markov decision processes | Ch. 1 (a program runs as steps) | the agents in Chapters 5–6 |
| [3 · Hardware](chapter-03/README.md) | 3.1 Input, processing & output hardware · 3.2 Memory & storage · 3.3 CPU architecture · 3.4 Parallel processing · 3.5 Logic & Boolean algebra · 3.6 How hardware enables AI | Ch. 1 (Von Neumann model, registers) | the sensors and limits in Chapters 5–6 |
| [4 · Networking](chapter-04/README.md) | 4.1 Network types & topologies · 4.2 Clients & clouds · 4.3 LAN hardware · 4.4 Media & collisions · 4.5 Internet, URLs & DNS · 4.6 TCP/IP · 4.7 Security · 4.8 Switching · 4.9 Cryptography | Ch. 1 (binary, addresses) and Ch. 3 (hardware) | connected systems in Chapters 5–6 |
| [5 · Applications](chapter-05/README.md) | 5.1 Real-life applications · 5.2 Smart homes · 5.3 Healthcare · 5.4 Transportation · 5.5 Industry & manufacturing · 5.6 Education · 5.7 Conclusion | Chapters 2–4 | evaluation in Chapter 6 |
| [6 · Strengths & Limitations](chapter-06/README.md) | 6.1 Integrated smart systems · 6.2 Embedded hardware · 6.3 Sensors & reliability · 6.4 Network architectures · 6.5 Edge vs cloud · 6.6 Adaptive agents · 6.7 Predictive vs behavioural modelling · 6.8 Limitations of behaviourist AI · 6.9 Ethical, security & practical concerns | Chapters 1–5 | — |

## How to study with these files

1. Read the chapter's **`draft.md`** in order. Each page-sized section introduces one idea, explains it step by step and works an example.
2. Stop at every **Pause & Try N.k** and answer it before reading on. Then check yourself against **`solutions.md`**, which uses the same numbers.
3. At the end of the chapter, complete the **Practice** questions (they include the team's `exercises.md` set) and mark them with `solutions.md`.
4. Use **`Key_Terms_*.md`** as a glossary while reading, and **`references.md`** to see where facts, dates and case studies come from.

## Files

| Path | Contents |
| --- | --- |
| `chapter-0N/draft.md` | Complete chapter text (V2.0): goals, key terms, explanations, worked examples, diagrams, Pause & Try activities, Practice |
| `chapter-0N/solutions.md` | Checked answers and expected outcomes for every activity and Practice question |
| `chapter-0N/Learning_Outcomes*.md`, `Key_Terms_*.md`, `exercises.md`, `UseOfAI.md` | The team's learning outcomes, glossary, original exercise set and AI-use record |
| `chapter-0N/images/`, `chapter-0N/figures/` | Photographs and diagrams used by `draft.md` |
| `chapter-01/Chapter-01-sample.md` | The Stage 1 sample excerpt, kept as development evidence |
| [`references.md`](references.md) | Sources and attribution |

## The same content in the other learning resources

The chapter text is identical to the [Blue Impulse Study Guide V2](../assets/study-guide/v2/BlueImpulse_Study_Guide_V2.pdf)
(exported from `assets/study-guide/v2/source/content/chN.sg`). The [Test Bank V1](../assets/study-guide/BlueImpulse_Stage2_TestBank_V1.docx)
has four true/false questions, four multiple-choice questions and one open task per chapter. The team presentation applies
Chapters 2–5 to NASA's Sojourner rover (`assets/presentations/final-presentation/`). Each chapter README maps its
subtopics to these resources and to the planned video tutorials. If you correct an error here, correct it in every
affected resource too.
