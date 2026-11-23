# Blue Impulse — References and resource introductions

The six team-supplied chapter PDFs defined the scope. Their notes credit Cambridge International AS & A Level Computer Science but do not identify a full edition or author bibliography; this remains a provenance limitation and no edition has been invented. The new activities, calculations and checkpoints are original AI-assisted teaching examples. The guide’s original artwork is user supplied and retains its own third-party rights.

The resources below were inspected as optional extensions and reference support. No external link replaces an explanation, input, question or answer in this snapshot. No student-created website or external platform is required.

## R1 — Reinforcement Learning: An Introduction, second edition

Richard S. Sutton and Andrew G. Barto, MIT Press, 2018.

http://incompleteideas.net/book/the-book-2nd.html

**Relevant section:** Chapter 3 (finite Markov decision processes) and Section 6.5 (Q-learning)

**Why use it:** Primary textbook support for the agent/environment distinction, expected return and the Q-learning update.

**Learner task:** After ACT-02, explain in your own words what the bootstrapped target includes, then compare it with the terminal-state case.

**Limits:** The book is mathematically deeper than this beginner guide. Start with the supplied worked calculation; do not treat the browser page as required activity content.

**Offline alternative:** The formula, both complete calculations and interpretation are included in ACT-02 and the chapter, so the task works offline.

**Access:** Optional public web resource; no account required to read the cited page. Signed-out HTTP access was checked on 7 November 2026. Availability on every campus network is not guaranteed. All essential task instructions and feedback are supplied locally.

## R2 — Nand to Tetris — Project 5: Computer Architecture

Noam Nisan and Shimon Schocken / Nand to Tetris.

https://www.nand2tetris.org/project05

**Relevant section:** Project overview, proposed computer architecture and hardware simulator guidance

**Why use it:** A concrete educational computer architecture connects logic, CPU state and memory.

**Learner task:** After ACT-01, compare the purpose of an instruction address and a data-memory address with the project’s computer model. Name one part the models share and one detail that differs.

**Limits:** The Hack computer is a different ISA; its instructions and registers must not be substituted directly into this guide’s toy program. Software installation is optional and not required for the paper task.

**Offline alternative:** ACT-01 includes its full program, trace and expected output. ACT-03 provides a complete paper pipeline grid specification.

**Access:** Optional public web resource; no account required to read the cited page. Signed-out HTTP access was checked on 7 November 2026. Availability on every campus network is not guaranteed. All essential task instructions and feedback are supplied locally.

## R3 — RFC 1122 — Requirements for Internet Hosts: Communication Layers

IETF / R. Braden, editor, 1989.

https://www.rfc-editor.org/rfc/rfc1122

**Relevant section:** Section 1.1.3 (Internet protocol suite) and the link, IP and transport sections

**Why use it:** An authoritative foundation for the layered Internet model used in Chapter 4.

**Learner task:** Draw the four teaching layers and place HTTP, TCP, IP and Ethernet/Wi-Fi by role. Explain why a large link capacity does not set an end-to-end response time.

**Limits:** This is a technical historical standards document; current protocols have later updates. Use it for layer roles, not as a complete modern security checklist.

**Offline alternative:** The chapter and ACT-04 contain the layer explanations and all delay inputs/results offline.

**Access:** Optional public web resource; no account required to read the cited page. Signed-out HTTP access was checked on 7 November 2026. Availability on every campus network is not guaranteed. All essential task instructions and feedback are supplied locally.

## R4 — RFC 8446 — The Transport Layer Security (TLS) Protocol Version 1.3

IETF / Eric Rescorla, 2018.

https://www.rfc-editor.org/rfc/rfc8446

**Relevant section:** Section 1 (Introduction) and Section 8 (0-RTT and anti-replay)

**Why use it:** Distinguishes transport confidentiality/integrity from application-level decisions, including replay considerations.

**Learner task:** After ACT-05, explain why authenticated transport alone does not decide whether an old command is still appropriate to execute.

**Limits:** The Python receiver is a validation demonstration, not a TLS implementation. Do not implement cryptography from this worksheet.

**Offline alternative:** ACT-05 includes the packet fields, state transitions and rejection explanations; no network service or account is needed.

**Access:** Optional public web resource; no account required to read the cited page. Signed-out HTTP access was checked on 7 November 2026. Availability on every campus network is not guaranteed. All essential task instructions and feedback are supplied locally.

## R5 — Artificial Intelligence Risk Management Framework (AI RMF 1.0)

NIST, NIST AI 100-1, January 2023.

https://www.nist.gov/itl/ai-risk-management-framework

**Relevant section:** Framework functions Govern, Map, Measure and Manage; trustworthy AI characteristics

**Why use it:** Connects measured performance with context, impacts, monitoring and responsibility.

**Learner task:** For ACT-06, assign one concrete action to each framework function: identify an owner, describe the operating domain, measure a relevant failure and plan a response.

**Limits:** A voluntary risk-management framework is not certification that a product is safe, fair or legally compliant. Context and evidence still matter.

**Offline alternative:** ACT-06 supplies the design table and expected trade-off reasoning. A suitable four-action response is: Govern — name an accountable operator; Map — define the campus operating domain; Measure — test missed deadlines and uneven accuracy; Manage — maintain fallback and an incident response process.

**Access:** Optional public web resource; no account required to read the cited page. Signed-out HTTP access was checked on 7 November 2026. Availability on every campus network is not guaranteed. All essential task instructions and feedback are supplied locally.

## R6 — The Unicode Standard — technical introduction

The Unicode Consortium.

https://www.unicode.org/standard/principles.html

**Relevant section:** Unicode design principles and character encoding model

**Why use it:** Supports the difference between a code point and a variable-length encoding such as UTF-8.

**Learner task:** Explain why one character is not necessarily one byte, and why BCD digits and text digits need an agreed representation.

**Limits:** Full text processing includes combining characters and grapheme clusters beyond this chapter. A displayed symbol is not always one code point.

**Offline alternative:** Chapter 1 defines character sets, code points and encodings and includes the BCD/ordinary-binary comparison.

**Access:** Optional public web resource; no account required to read the cited page. Signed-out HTTP access was checked on 7 November 2026. Availability on every campus network is not guaranteed. All essential task instructions and feedback are supplied locally.

## Responsible AI-use record

Neogpt/Codex assisted on 7 November 2026 with reconciling the guide into Markdown, developing activities and answers, drafting the Test Bank, generating PDFs/DOCX and verifying package structure. The user asked to follow rules/Stage2_All_Instructions.md. Calculations and supplied code outputs were checked locally; source/resource access and document checks are recorded in the submission evidence. These checks are not independent human peer review. Significant interaction excerpts belong in the project and personal logs.
