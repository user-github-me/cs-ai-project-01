# Sources and scope — Blue Impulse Stage 2 teaching slides

The presentation adapts the checked six-chapter project content into classroom explanations. All diagrams, tables and the fictional Pip rover are original editable shapes. No third-party photographs, video clips, stock graphics or prior-student material are used.

The slides and presenter notes contain the actual explanations, activities and answers. The following are references and further reading, not substitutes for submitted content.

| Source | Relevant explanation |
| --- | --- |
| Blue Impulse, six-chapter Markdown V2.0 and *Blue Impulse Study Guide* (2026), chapter/subtopic titles listed in `Learning_Resource_Map.md`. | Module scope, terminology, common examples and practice connections. |
| Richard S. Sutton and Andrew G. Barto, *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press, 2018. ISBN 978-0-262-03924-6. Chapters 3–6. Publisher: https://mitpress.mit.edu/9780262039246/reinforcement-learning/ | Agent/environment interaction, policy, return, value, MDPs, exploration and Q-learning. The publisher blocked automated access during the current link check; the bibliographic reference is provided directly. |
| Rodney A. Brooks, “A Robust Layered Control System for a Mobile Robot,” *IEEE Journal of Robotics and Automation*, RA-2(1), 14–23, 1986. DOI: 10.1109/JRA.1986.1087032. MIT AI Memo 864 preprint: https://people.csail.mit.edu/brooks/papers/AIM-864.pdf | Layered behavior coordination through suppression and inhibition; the classroom priority diagram is a simplified illustration. |
| Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*. Free author text: https://pages.cs.wisc.edu/~remzi/OSTEP/ | OS virtualization, processes, memory, scheduling, persistence and I/O. |
| Noam Nisan and Shimon Schocken, *The Elements of Computing Systems*, and Nand2Tetris course projects: https://www.nand2tetris.org/course | Logic, stored-program architecture and execution. The supplied toy instruction set is original and is not the Hack ISA. |
| Python Software Foundation, “Unicode HOWTO”: https://docs.python.org/3/howto/unicode.html | Code points, encodings and variable-length UTF-8. |
| R. Braden, ed., RFC 1122, *Requirements for Internet Hosts—Communication Layers*, 1989: https://www.rfc-editor.org/rfc/rfc1122 | Internet layering, link/network/transport responsibilities. |
| P. Mockapetris, RFC 1034, *Domain Names—Concepts and Facilities*, 1987: https://www.rfc-editor.org/rfc/rfc1034 | DNS names, records, distributed lookup and caching. |
| T. Berners-Lee, R. Fielding and L. Masinter, RFC 3986, *Uniform Resource Identifier (URI): Generic Syntax*, 2005, §3: https://www.rfc-editor.org/rfc/rfc3986 | Scheme, authority, path, query and fragment. |
| W. Eddy, ed., RFC 9293, *Transmission Control Protocol (TCP)*, 2022, §2.2: https://www.rfc-editor.org/rfc/rfc9293 | Reliable in-order byte-stream service and retransmission. |
| J. Postel, RFC 768, *User Datagram Protocol*, 1980: https://www.rfc-editor.org/rfc/rfc768 | Datagram transport without guaranteed delivery or duplicate protection. |
| E. Rescorla, RFC 8446, *The Transport Layer Security (TLS) Protocol Version 1.3*, 2018: https://www.rfc-editor.org/rfc/rfc8446 | Authenticated key establishment, confidentiality and integrity in modern secure transport. |
| NIST, “Cryptographic Standards and Guidelines”: https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines | Standards-based cryptography and its scope. These slides are conceptual, not cryptographic implementation instructions. |

Link-check evidence is included in `review/source-link-check.json`. Short technical excerpts checked against the TCP, UDP and URI standards are in `review/source-excerpts.json`. A successful URL response is not treated as proof that every claim is correct; calculations and demonstration outcomes were checked separately.

Inter is by Rasmus Andersson and contributors, used under the SIL Open Font License 1.1. The complete license and the regular/bold fonts are included in `fonts/`. Both font weights are embedded in the PowerPoint. Text uses one family; lines and arrowheads are native PowerPoint geometry.

## Teaching-model limits

- The stored-program trace uses an invented one-instruction-per-address ISA, not a particular physical CPU.
- The four-stage pipeline assumes independent instructions, one cycle per stage and no stalls.
- Q-learning arithmetic shows one non-terminal update and one terminal alternative. It does not establish convergence or safe deployment.
- The network calculation gives distance during delay only, not total stopping distance. The 30 m/s example is hypothetical and is not Pip’s recommended operating speed.
- The packet validator uses an illustrative 200 ms freshness threshold and a simplified clock/sequence model. Authentication is checked elsewhere; setting a Boolean does not authenticate a sender. The code never controls equipment.
- Local-versus-remote placement is a design proposal. The slides do not claim a validated robot safety case, measured performance, actual classroom feedback or completed rehearsal.

## Significant AI assistance

NeoGPT/Codex generated substantial content, editable diagrams, notes and build code on 7 November 2026 under the user's instruction to apply `rules/Stage2_All_Instructions.md`. `AI_Use_Evidence.md` preserves the relevant request, production decisions and concrete verification results. AI assistance does not establish that a student has mastered the material; individual reflection and demonstration remain the student's responsibility.
