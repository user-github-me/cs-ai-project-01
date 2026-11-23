# Chapter 4 — Answers and expected outcomes

> Attempt each activity in draft.md before reading its answer. Calculations show every step; open questions list the
> points a good answer contains. Numbering matches draft.md.

## Pause & Try

### Pause & Try 4.1 — Classifying networks by size

- **a) PAN** (a WPAN): a few devices around one person, linked wirelessly, e.g. by Bluetooth.
- **b) LAN**: one building or site, owned and run by the school.
- **c) MAN**: offices spread across one town or city.
- **d) WAN**: links across countries and continents.

### Pause & Try 4.2 — LAN versus Internet transfer times

**a)** As in the chapter, 1 GB = 8 000 megabits, so 2 GB = 2 × 8 000 = **16 000 megabits**.

- Over the 1 Gbps LAN: 16 000 Mb ÷ 1 000 Mbps = **16 seconds**
- Over the 40 Mbps link: 16 000 Mb ÷ 40 Mbps = **400 seconds** (6 minutes 40 seconds)
- The Internet copy takes 400 ÷ 16 = **25 times** longer.

These are best-case estimates: headers, other traffic and resends make real transfers a little slower.

**b)** Any two of:

- **Bandwidth:** the school's own cables and switch carry 1 Gbps; the Internet link carries only 40 Mbps.
- **Distance and hops:** on the LAN the data travels at most a few hundred metres; the Internet copy crosses many kilometres and many routers, which adds delay.
- **Ownership and sharing:** the LAN belongs to the school alone; the Internet links belong to other companies and are shared with many other users, so the school gets only a share.
- **Fewer errors:** short LAN links pick up little interference, so fewer frames have to be resent.

### Pause & Try 4.3 — LANs and WAN of a bank

- **LANs:** each branch's 30 computers in one building form a LAN, so there are **200 LANs**, one per branch.
- **WAN:** the links that join the 200 branch LANs across the country, through routers and lines leased from telecom companies. The whole system is **one WAN made of 200 LANs**.

| | Each branch LAN | The bank's WAN |
|---|---|---|
| Ownership | Owned and managed by the bank: its own cables, switches and access points | Links leased from telecom providers; no single owner |
| Speed | Fast: typically 1 Gbps per device over short cables | Each branch gets a smaller share; longer delays across hundreds of kilometres and many routers |
| Reliability | High: short links, few errors; the bank's IT staff fix faults directly | More points of failure and other owners' equipment, so backup routes are needed |

### Pause & Try 4.4 — Choosing a reliable topology

**Star topology** (for several rooms, a hybrid of stars joined by a backbone).

- **Reason:** each node has its own cable to the central switch, so one broken cable stops only that one node and everyone else keeps working. A star also costs far less than a mesh and is easy to extend.
- **Weakness:** the central switch is a single point of failure: if it fails, the whole star stops. (It also needs more cable than a bus.)

Not suitable: a bus (one break in the backbone stops everyone); a full mesh is very reliable but too expensive for "a reasonable cost".

### Pause & Try 4.5 — When the file server fails

Students' documents, and usually their logins and the shared exam files, are stored on the file server, not on the PC in front of them. When it crashes:

- students cannot log in, or cannot open or save files on the server, so exam papers and coursework are unavailable and unsaved work may be lost;
- every client is affected at once, because the server is a **single point of failure**;
- the exam is delayed, or moved to paper, until the server is repaired and its data restored.

Ways to reduce the risk (any two):

- a **backup (standby) server** that takes over automatically when the main one fails;
- regular, e.g. nightly, **backups** with an off-site copy, so data can be restored quickly;
- a second copy of the exam materials elsewhere (e.g. cloud storage or local drives), and a test of the system the day before;
- maintenance and monitoring of the server, and an uninterruptible power supply (UPS) against power cuts.

### Pause & Try 4.6 — Network model for an architecture firm

**Client-server.** Three reasons:

1. **Strict user permissions:** access rights for every account are set and enforced centrally on the server by IT staff. In a peer-to-peer network each user secures their own computer, so rules cannot be enforced consistently.
2. **Daily off-site backups:** all files sit on the server, so one central backup can run automatically every night and be copied off-site. Peer-to-peer would need 40 separate backups.
3. **Size and large shared files:** 40 staff is too many for peer-to-peer, which suits homes and small offices. A powerful file server holds the large 3D rendering files centrally, so everyone opens the latest version from any computer, and the network grows simply by adding clients.

The higher cost (servers and IT staff) is justified. Also acceptable: central antivirus updates and security.

### Pause & Try 4.7 — Thick and thin clients

| | Thin client | Thick client |
|---|---|---|
| Processing | On the server | On its own CPU, GPU and RAM |
| Storage | Little or none locally; programs and files live on the server | On its own SSD or hard disk |

**When the server fails:** the thin client cannot do its main job. The software runs on the server, so the user's session stops, any unsaved work held on the server may be lost, and saved files are unavailable until the server is restored (they are safe if the server's disks or backups survive). A thick-client user could carry on working offline.

### Pause & Try 4.8 — Choosing public or private cloud

**Hospital: private cloud.**

- **Security:** patient scans are sensitive personal data; a private cloud is used by the hospital only, so the data is isolated from other customers.
- **Control:** full control over where the data is stored and how it is secured, which helps the hospital meet strict data-protection laws such as GDPR.
- **Cost:** high (servers and staff), but justified by how sensitive the data is.

**Start-up: public cloud.**

- **Cost:** low upfront cost and pay only for what you use: affordable for a small new company.
- **Growth:** almost unlimited capacity within minutes if the app suddenly becomes popular; a private cloud is limited by the hardware the company owns.
- **Security and control:** the provider secures the shared hardware, so the start-up needs no security staff; in return it accepts little say over location and setup.

### Pause & Try 4.9 — Hardware for a classroom LAN

| Hardware | Its job |
|---|---|
| **NIC** in every device (wired NICs in the 25 PCs and the printer; wireless NICs built into the 5 tablets) | Connects the device to the network and turns data into signals and back; each has a unique MAC address |
| **Twisted-pair Ethernet cables** (about 28: 25 PCs, the printer, the router and the access point) | Carry the signals between each wired device and the switch |
| **Switch** with at least 28 ports (e.g. one 48-port switch, or two linked 24-port switches) | The centre of the star: joins the wired devices and forwards each frame only to its destination, using MAC addresses |
| **Wireless access point** | Lets the 5 tablets join the LAN by Wi-Fi |
| **Router with a modem** | Connects the LAN to the ISP and so to the Internet; the router forwards packets in and out, the modem carries the signals over the line |

Optional: a file or print server, to store work centrally and queue print jobs. Also acceptable: connecting the printer by Wi-Fi.

### Pause & Try 4.10 — Hub versus switch traffic

Assume one node on each port, A to F (as in the chapter's worked example).

- The hub copies A's 6 MB to all **5** other ports: B, C, D, E and F.
- Only D needs it, so **4 nodes × 6 MB = 24 MB** reaches nodes that did not need it (30 MB is sent out in total).

**With a switch:** it reads D's MAC address, looks it up in its MAC address table and forwards the frames to D's port only, so **0 MB** is wasted.

**Why the LAN is faster for everyone:** the other ports stay free, so other pairs (e.g. B to C and E to F) can send at the same time, whereas on a hub only one node can send at a time. Nodes no longer receive and discard data they do not need, and the switch's private links have no collisions.

### Pause & Try 4.11 — Re-routing after a cost change

- Route via R3: 12 + 5 = **17**
- Route via R2: 10 + 10 = **20** (unchanged)
- 17 < 20, so R1 **still sends head-office packets to R3**, at a total cost of **17** (up from 6).

**How R1 finds out:** routers regularly swap information with their neighbours about the networks they can reach and what it costs. The new cost of the R1–R3 link (12) arrives in these updates (and R1 is at one end of that link). R1 recalculates the total for each route, keeps the cheapest and updates its routing table: head office, next hop R3, cost 17.

Common mistake: switching to R2. That route only becomes cheaper if the R1–R3 cost rises above 15 (15 + 5 = 20).

### Pause & Try 4.12 — Choosing transmission media

- **a) Fibre-optic cable.** 400 m is too far for twisted pair (about 100 m at most); fibre stays very fast over many kilometres and is immune to electrical interference, which suits a cable running between buildings.
- **b) Wi-Fi from wireless access points.** Customers move around with their own phones, so cables are impractical; Wi-Fi's range of about 30–50 m covers a café. The signals leak outside, so the network should be encrypted.
- **c) Bluetooth.** It is made for short-range WPANs around one person, using radio in the 2.45 GHz band; frequency hopping across 79 channels avoids interference, and it uses little power.

### Pause & Try 4.13 — What happens in a collision

- **The signals:** both frames travel along the cable; where they meet, the two signals overlap and add together (the voltage rises), so the nodes in between receive a garbled mixture that nobody can read. This is a **data collision**: both frames are destroyed and must be sent again.
- **Why not resend straight away:** both nodes would start again at the same moment and collide again, over and over. Instead each stops, a **jam signal** tells every node about the collision, and each node waits a **random** back-off time. The node with the shorter wait sends first; the other then hears a busy cable and waits its turn.

### Pause & Try 4.14 — Back-off after a third collision

- Each node chooses one of 8 slots (0–7), so there are 8 × 8 = **64** equally likely pairs of choices.
- They collide again only if both pick the same slot: (0, 0), (1, 1), … (7, 7) = **8** pairs.
- Chance = 8 ÷ 64 = **1/8 = 12.5%** (the pattern is 1/2, then 1/4, then 1/8).

**Why the range doubles:** each further collision shows that the cable is busy, perhaps with several nodes competing. Doubling the range spreads the retries over more slots and halves the chance of another clash, while the waits stay short when the network is quiet. After 16 failed attempts the frame is abandoned.

**Why a jam signal is needed:** it makes sure **every** node, not just the two senders, notices the collision, so the damaged frame is ignored and both senders stop and back off.

### Pause & Try 4.15 — Handling collisions: CSMA/CD and CSMA/CA

**Wired network: CSMA/CD (collision detection)**

1. **Listen** (carrier sense): send only when the cable is idle; otherwise wait.
2. **Send** the frame and keep **monitoring** the voltage on the cable.
3. **Collision?** If the voltage is too high, stop and send a **jam signal** so that all nodes know.
4. **Back off** for a random time (the range doubles after each collision), then start again at step 1; give up after 16 attempts.

**Wi-Fi: CSMA/CA (collision avoidance)**

1. **Listen** until the channel is clear.
2. **Count down** a random back-off time, so that devices which were waiting do not all start together.
3. **Reserve (optional):** send RTS; the access point replies CTS, which tells all other devices, including hidden nodes, to stay quiet.
4. **Send** the frame and wait for an **acknowledgement (ACK)**: no ACK means assume a collision, back off and retry.

Wi-Fi avoids collisions instead of detecting them because a radio cannot hear other signals while it transmits, and hidden nodes cannot hear each other at all. On a switched Ethernet LAN each cable is a private link to the switch, so collisions do not happen there.

### Pause & Try 4.16 — Internet, Web and hardware

Differences (any two):

- The **Internet** is the infrastructure: a global network of networks made of cables, routers and servers. The **Web** is a collection of linked web pages: one service that runs on the Internet.
- The Internet works with TCP/IP protocols and packets; the Web is used through browsers, URLs and HTTP/HTTPS.
- The Internet carries many services (the Web, email, calls, games); the Web is web pages only.
- The Internet began as ARPAnet in 1969; Tim Berners-Lee created the Web in 1989.

Hardware, in order: **laptop** (its wired or Wi-Fi NIC) → **router + modem** → **ISP** → **backbone** (routers on fibre-optic and undersea cables) → **web server**.

### Pause & Try 4.17 — IPv4 binary and IPv6 shortening

**a)** Write each denary number as 8 bits:

| Denary | 10 | 0 | 255 | 7 |
|---|---|---|---|---|
| Binary | 00001010 | 00000000 | 11111111 | 00000111 |

Answer: **00001010.00000000.11111111.00000111** (check: 10 = 8 + 2; 255 = all eight bits set; 7 = 4 + 2 + 1).

**b)**

- Rule 1, drop leading zeros: `2001:db8:0:0:0:0:0:1`
- Rule 2, replace the one run of five zero groups with `::`: **`2001:db8::1`**

Common mistake: using `::` twice, which would make the address ambiguous.

**c)** One reason (any one): IPv4 addresses have run out. The central pool of free IPv4 addresses emptied in 2011, because 2³² ≈ 4.3 billion addresses are fewer than the number of devices online; IPv6 has 2¹²⁸ ≈ 3.4 × 10³⁸ addresses, so every device can have its own public address. Also acceptable: IPv6 devices configure their own address automatically; IPv6 headers are simpler, so routers process them quickly.

### Pause & Try 4.18 — The parts of a URL

| Part | In this URL | How it helps |
|---|---|---|
| Protocol | `https://` | Fetch the page with HTTP Secure, over an encrypted connection; no port is shown, so the HTTPS default, 443, is used |
| Domain name | `shop.example.org` | Which server: DNS turns the name into the server's IP address. Read right to left: `.org` is the top-level domain, `example` the organisation's registered name, `shop` one particular host (server) |
| Path | `/books/` | Which folder on the server |
| Resource | `networking.html` | Which file the server should send back |
| Fragment | `#reviews` | Which part of the page to show: the browser jumps to the reviews section; the fragment stays in the browser |

The browser uses the parts in order: protocol → DNS lookup → request `/books/networking.html` → display the page at `#reviews`. Treating `/books/networking.html` as one path is also acceptable.

### Pause & Try 4.19 — A DNS lookup, step by step

First visit:

1. The browser and operating system check their own **cache**: on a first visit the address is not there.
2. The computer asks a **recursive resolver**, a DNS server run by the ISP or school.
3. The resolver asks a **root server**, which replies: "ask the .org TLD server".
4. The resolver asks the **.org TLD server**, which replies: "ask example.org's authoritative server".
5. The **authoritative server** holds the official record and returns the IP address, **203.0.113.25**.
6. The resolver **caches** the answer and passes it back to the computer, which caches it too.
7. The browser connects to 203.0.113.25 and requests the page using HTTPS.

**A second visit minutes later is faster** because the address is still cached on the computer (and at the resolver), so the lookup ends at step 1. No messages go to the resolver, root, TLD or authoritative servers, which saves several round trips across the network. (Cached answers are kept only for a while, then looked up again.)

### Pause & Try 4.20 — The four TCP/IP layers

| Layer (top to bottom) | Core responsibility | Protocols |
|---|---|---|
| Application | Gives applications network services: web pages, email, file transfer | HTTP, HTTPS, FTP, SMTP, POP3, IMAP, DNS |
| Transport | Splits data into numbered segments, adds port numbers, checks every segment arrives and puts them back in order | TCP, UDP |
| Internet | Adds the source and destination IP addresses and routes packets across networks | IP (IPv4, IPv6) |
| Link | Adds MAC addresses and sends the bits over the physical medium as frames | Ethernet, Wi-Fi |

**One benefit of a stack** (any one): each layer does one job and only uses the layer below, so one layer can change without affecting the others (a browser works the same over Wi-Fi or a cable); devices and software from different manufacturers can work together; each layer is simpler to design, test and fix.

### Pause & Try 4.21 — A web request through the layers

**Your computer** (down the layers):

1. **Application:** the browser creates an HTTP request, e.g. "GET /notes.html".
2. **Transport:** TCP splits it into segments, numbers them and adds the port number of the web service.
3. **Internet:** IP adds your IP address and the server's IP address, making a **packet**.
4. **Link:** Ethernet or Wi-Fi adds MAC addresses and an error check, making a **frame**, and sends it as signals.

**A router on the way:** it reads only as far as the internet layer. It removes the frame, checks the destination IP address, finds the next hop in its routing table and wraps the packet in a **new frame** for the next link.

**The web server** (up the layers): each layer checks and removes its own header in reverse order (link, internet, transport, application). TCP checks that all the segments arrived and puts them in order, so the web-server program receives exactly the request that was sent. The reply makes the same journey back.

### Pause & Try 4.22 — Segments and headers

- 3 000 ÷ 1 460 ≈ 2.05, so 2 full segments are not enough: **3 segments** are needed.
- 1 460 + 1 460 + 80 = 3 000, so the last segment carries 3 000 − 2 × 1 460 = **80 bytes**.

Headers in each frame, from the outside in:

1. **Frame (Ethernet) header:** source and destination MAC addresses
2. **IP header:** source and destination IP addresses
3. **TCP header:** port numbers and the segment's sequence number

Then comes the data, and the frame ends with a **trailer** (an error check). Extra: with 58 bytes of headers and trailer per frame, as in the worked example, 3 000 + 3 × 58 = 3 174 bytes are sent.

### Pause & Try 4.23 — HTTP and FTP

- **HTTP** sets the rules for requesting and sending web pages between a browser and a web server, by request and response. Example: the browser sends `GET /courses/notes.html` and the server replies `200 OK` with the page (or `404 Not Found`). Other good examples: submitting a search form (a POST request); opening any web page.
- **FTP** sets the rules for uploading and downloading files, both text and binary, between a client and a server. Example: a web designer uploads the new version of a website's files to the hosting server. Other good example: a researcher downloads a 2 GB data set from a university archive.
- **Uploading a 2 GB file from a command-line terminal:** **FTP**, e.g. with the `put` command. In practice a secure version, **SFTP** or **FTPS**, is used, because plain FTP sends passwords unencrypted.

### Pause & Try 4.24 — Choosing email protocols

- **a) IMAP:** the emails stay on the server and are kept in sync, so every device shows the same inbox and read or unread status. (With POP3 the laptop would download them and usually delete them from the server.)
- **b) SMTP** sends the email, with **MIME** packaging the PDF (a binary file) so that it can travel with the text.
- **c)** SMTP is a **push** protocol because the sender starts the transfer: the email app opens a connection to the mail server and pushes (uploads) the message to it, and the servers push it on until it reaches the recipient's mail server. SMTP cannot fetch mail out of a mailbox; the recipient pulls it with POP3 or IMAP.

### Pause & Try 4.25 — Security, privacy and integrity

| | Meaning | A failure in a school's student-records system |
|---|---|---|
| **Data security** | Protecting data and systems from unauthorised access, theft, loss, damage or corruption | A student guesses a teacher's weak password and logs in to the records; or the server's disk fails and there is no backup |
| **Data privacy** | The right of people to control how their personal data is collected, used and shared | The school gives pupils' home addresses to an advertising company without consent |
| **Data integrity** | Data staying accurate, complete and unchanged during entry, storage and transfer | A date of birth typed as 2091, or a mark of 9 entered instead of 90 |

Security is the set of tools; privacy and integrity are two of the things those tools protect. Any failure that clearly matches each definition is acceptable.

### Pause & Try 4.26 — Phishing and pharming

- **Phishing:** fake emails or messages that look genuine, with a link to a fake website. It needs the victim to **act**: click the link and type their details.
- **Pharming:** malicious code on the computer, or a tampered DNS server, redirects the user to a fake website **even when they type the correct address**. No click is needed.

Protection (one each):

- **Phishing:** check the sender and the real web address before clicking, and never give a password in reply to a message (spam filters and staff training also help).
- **Pharming:** antivirus software to find and remove the malicious code; check for the padlock and the site's certificate; keep software updated.

**Why antivirus alone cannot stop phishing:** phishing is a trick, not a program. The message contains no virus for the antivirus to detect, and the victim types their details into the fake website themselves, so only the user's care (helped by filters and training) can stop it.

### Pause & Try 4.27 — Cracking a short password

- Combinations: 26 choices for each of 6 positions, so 26⁶ = **308 915 776 ≈ 3.1 × 10⁸**.
- Time: 308 915 776 ÷ 10 000 000 000 guesses per second ≈ **0.031 seconds**: about three hundredths of a second.

Ways to make it stronger (any two):

- **Make it longer:** 12 or more characters; every extra character multiplies the number of combinations.
- **Mix character types:** upper and lower case letters, digits and symbols. With 94 possible symbols, 12 characters give 94¹² ≈ 4.8 × 10²³ combinations: about 1.5 million years at the same speed (the chapter's table).
- Avoid words and personal details, and use a different password for every site.

Also acceptable: adding two-factor authentication, which protects the account even if the password is guessed.

### Pause & Try 4.28 — Matching security mechanisms to problems

- **a) Encryption** (e.g. encrypted Wi-Fi, HTTPS): captured traffic is meaningless ciphertext without the key.
- **b) A digital signature**, backed by the supplier's digital certificate: it proves who sent the contract and that nobody changed it.
- **c) A firewall:** its rules block traffic to known malicious websites. (Antivirus only helps once something harmful has already been downloaded.)

### Pause & Try 4.29 — Parity, validation and verification

**a)** 1100101 contains 1 + 1 + 0 + 0 + 1 + 0 + 1 = **4** ones, already an even number, so the parity bit is **0**: the byte is **01100101** (parity bit first, as in the chapter's worked example). If your course puts the parity bit at the end, 11001010 is equally correct.

**b)** 01110101 contains 0 + 1 + 1 + 1 + 0 + 1 + 0 + 1 = **5** ones, an odd number, so **yes, an error has been detected** and the byte is resent. (Compared with the byte in a), the 4th bit has flipped from 0 to 1. Parity shows that an error happened, not which bit changed.)

**c)**

- **Validation** is an automatic check, made as data is entered, that the data is sensible and follows set rules. Example: a **range check** (age must be 11–19, so 42 is rejected). It cannot prove the data is correct: a 15-year-old who types 16 still passes.
- **Verification** checks that data entered or transferred **matches the original**. Examples: **double entry** (typing a new password twice) during entry, or a **parity check** during transfer.

Also acceptable: format, length, type or presence checks for validation; a visual check or a checksum for verification.

### Pause & Try 4.30 — Circuit switching for video conferencing

**a)** In circuit switching a **dedicated path** (circuit) is set up between the sender and the receiver **before** any data is sent. The whole path and all of its bandwidth belong to that one communication until it ends, when the path is released (set up → transfer → tear down). Example: a landline telephone call.

**b)** A video conference is live, so it needs a steady data rate and a short, constant delay:

- the whole bandwidth of the circuit is reserved, so the data rate never drops, even when the network is busy;
- all the data follows the same path, so delay is low and constant and data arrives in order: no jitter and no reassembly, so picture and sound do not stutter or freeze;
- the call sends data continuously, so little of the reserved capacity is wasted.

### Pause & Try 4.31 — Routers and packet reassembly

**What a router does with each packet:**

1. Reads the destination IP address in the header.
2. Looks it up in its routing table and chooses the best next hop **at that moment** (the lowest cost).
3. Lowers the hop limit by 1, and discards the packet if it reaches 0.
4. Forwards the packet, in a new frame, to the next hop.

**How the receiver rebuilds the message:**

- **Wrong order:** every packet carries a **sequence number**. The receiver holds the packets that have arrived and puts them back in number order, e.g. arrived 1, 2, 4, 3 → rebuilt 1, 2, 3, 4.
- **Missing or damaged:** a gap in the sequence numbers shows that a packet is missing, and the error check in the trailer shows if one is damaged. The receiver asks for only that packet to be sent again, then completes the message.

### Pause & Try 4.32 — Packet switching benefits and drawbacks

**Benefits** (any two, with the reason):

- **Efficient:** links are shared, so while one user pauses, other people's packets use the line; no capacity is reserved and wasted.
- **Robust:** each packet is routed independently, so if a link or router fails the next packets are routed around it and the message still arrives.
- Also acceptable: no set-up delay (there is no path to reserve); only lost packets are resent; cheaper to run.

**Drawback** (any one, with the reason):

- **Variable delay (jitter):** packets wait in queues at busy routers and may take different routes, so they arrive at uneven intervals and out of order.
- Also acceptable: reassembly is needed; busy routers may drop packets, which must be resent; every packet carries header overhead; no fixed share of bandwidth is guaranteed.

**Live video call across a busy network: circuit switching.** The reserved circuit gives a steady data rate and a low, constant delay with data in order, so the call does not stutter; on a busy packet-switched network, router queues cause jitter and lost packets. (Today's Internet video calls actually use packet switching with buffering at the receiver; a well-argued answer on that trade-off is also acceptable.)

### Pause & Try 4.33 — Caesar cipher practice

**a)** Shift each letter forward 5 places: C → H, O → T, D → I, E → J, giving **HTIJ**.

**b)** Shift each letter back 3 places: K → H, H → E, O → L, O → L, R → O, giving **HELLO**.

**c)** With only 25 keys, an eavesdropper can simply try every shift (a **brute-force attack**): a computer does it in a fraction of a second, a person in a few minutes. Only one shift gives readable text, which reveals both the message and the key. (Also acceptable: each letter always becomes the same letter, so letter-frequency patterns show through.) A real 128-bit key has 2¹²⁸ ≈ 3.4 × 10³⁸ possible values instead.

### Pause & Try 4.34 — XOR encryption and key distribution

**a)** XOR gives 1 where the bits differ and 0 where they match:

| Step | Bits |
|---|---|
| Plaintext: the letter A | 0100 0001 |
| Key | 1100 1100 |
| Ciphertext = plaintext XOR key | **1000 1101** |
| Ciphertext XOR the same key | **0100 0001** = A again |

**b) The key distribution problem:** in symmetric encryption the sender and the receiver need the **same secret key**. If the key is emailed or sent across the network, an eavesdropper can intercept it and then decrypt every message from then on; meeting in person to swap keys is impossible with millions of websites. Asymmetric encryption solves this, because a public key can be sent openly and used to share the secret session key.

### Pause & Try 4.35 — Toy public-key encryption

**Encrypt** with the public key (n = 33, e = 3): 2³ = 8, and 8 ÷ 33 = 0 remainder 8, so 8 mod 33 = 8. **Ciphertext = 8.**

**Decrypt** with the private key (d = 7): 8⁷ = 2 097 152, and 2 097 152 ÷ 33 = 63 550 remainder 2 (33 × 63 550 = 2 097 150). So 8⁷ mod 33 = **2**: the original number.

Optional shortcut with smaller numbers: multiply by 8 and take mod 33 after every step.

| Power | Calculation | mod 33 |
|---|---|---|
| 8² | 8 × 8 = 64 | 31 |
| 8³ | 31 × 8 = 248 | 17 |
| 8⁴ | 17 × 8 = 136 | 4 |
| 8⁵ | 4 × 8 = 32 | 32 |
| 8⁶ | 32 × 8 = 256 | 25 |
| 8⁷ | 25 × 8 = 200 | **2** |

**Why Eve cannot decrypt with the public key:** the keys work as a pair: what the public key encrypts, only the private key can decrypt. Applying the public key again just gives 8³ mod 33 = 512 mod 33 = 17, not 2. To find d she would have to split n into its prime factors (33 = 3 × 11): easy for this toy key, but for a real n with over 600 digits no ordinary computer could do it in any useful time.

### Pause & Try 4.36 — How a digital signature works

**"In reverse":** to keep a message secret you encrypt with the receiver's public key; to sign it, the sender encrypts with her **own private key**, and anyone can check it with her **public key**.

Alice signs:

1. She hashes the message, producing a short, fixed-length hash.
2. She encrypts the hash with her private key: this is the **digital signature**.
3. She sends the message + the signature (+ her certificate).

Bob verifies:

4. He decrypts the signature with Alice's public key → hash A.
5. He hashes the message he received → hash B.
6. He compares: if A = B, the message is genuine.

- **Identity:** only Alice's private key could make a signature that her public key turns back into the right hash, so Alice sent it.
- **Integrity:** any change to the message gives a different hash B, and nobody can make a new matching signature without Alice's private key.

Toy check: hash 5; signature 5⁷ mod 33 = 78 125 mod 33 = 14; check 14³ mod 33 = 2 744 mod 33 = 5, which matches. A signature does not hide the message; to keep it secret as well, Alice also encrypts it with Bob's public key.

### Pause & Try 4.37 — Obtaining and trusting a certificate

**Obtaining a certificate:**

1. The shop creates a **key pair** and keeps the private key secret on its server.
2. It **applies** to a certificate authority (CA), sending its public key and its domain name.
3. The **CA checks** that the applicant really controls the domain (and, for some certificates, who the company is).
4. The **CA creates and signs** the certificate (domain name, public key, CA's name, serial number, valid dates) with the CA's private key.
5. The shop **installs** the certificate on its web server, which sends it to every visitor.

**How the browser decides to trust the shop's public key:**

- The browser and operating system already hold the **public keys of trusted CAs**.
- The browser checks the **CA's signature** on the certificate with the CA's public key: this proves the CA issued it and that nothing in it was changed.
- It checks that the **domain name** matches the shop's address and that today is within the **valid dates**.
- If every check passes, it trusts the shop's public key inside the certificate and uses it to set up an encrypted connection (the padlock); if any check fails, it warns the user.

### Pause & Try 4.38 — SSL, TLS and certificate checks

**What they are:** Secure Sockets Layer (SSL) and its successor, Transport Layer Security (TLS), are protocols that protect data travelling between two applications, such as a browser and a web server. They provide **encryption** (an eavesdropper sees only ciphertext), **authentication** (the certificate proves the server is the real website) and **integrity** (any change on the way is detected). SSL is out of date; TLS is what runs behind https:// and the padlock.

**Where they are used** (any two or three): online banking and shopping; logging in to websites and school portals; email (SMTP, IMAP or POP3 over TLS); video calls, messaging and cloud storage; some VPNs linking remote workers to an office.

**What the browser does with the certificate** (during the TLS handshake):

1. It receives the website's digital certificate.
2. It verifies the **CA's signature** on it with the CA's public key, which is already stored in the browser.
3. It checks that the **domain name** matches the site and the certificate is within its **dates**.
4. If the checks pass, it uses asymmetric cryptography to agree a new symmetric **session key** with the server, and all data in the session is encrypted with it (the key is thrown away at the end). If they fail, it shows a warning.

### Pause & Try 4.39 — Detecting an eavesdropper with QKD

**How QKD detects Eve:**

- Alice sends each bit of the key as a single **photon**, polarised with one of two settings chosen at random; Bob measures each photon with a setting he chooses at random.
- Over an ordinary channel they compare the **settings** (not the bits) and keep only the bits where their settings matched.
- Measuring a photon changes it, and a photon cannot be copied. Eve must measure each photon without knowing Alice's setting; she guesses wrongly half of the time and disturbs those photons, so about **1 in 4** of the kept bits that Alice and Bob compare disagree. Without Eve, almost none do.
- So they publicly compare a sample of the kept bits: almost no errors means the rest is their secret key; many errors means someone listened.

**The sample:** 49 ÷ 200 = 0.245 = **24.5%**, about 1 in 4. Eve measuring every photon would cause about 200 ÷ 4 = 50 disagreements, so this matches.

- **Conclusion:** an eavesdropper intercepted the photons, so the key is not secret.
- **Next:** discard the whole key (never use it to encrypt anything) and start again with new photons, ideally after checking the link. Only a key whose test sample shows almost no errors is kept, and it is then used with a symmetric cipher.

## Practice

### Question 1 — Network fundamentals and architectures

**(a)** [3 marks] A LAN covers a small area and is owned by one organisation, and it is very fast; a WAN covers countries or the world over links leased from telecom companies, and each user gets a smaller share of the speed with longer delays. One mark per row:

| | LAN | WAN |
|---|---|---|
| Geographic scale | One building or site | Towns, countries, the world |
| Ownership | Owned and managed by one organisation | Links leased from telecom providers; no single owner |
| Transmission speed | 100 Mbps – 10 Gbps per device (1 Gbps typical) | Fast backbones, but a smaller share per user and longer delays |

**(b)** [3 marks] In client-server, a central server manages the resources and the network grows easily; in P2P every peer manages its own resources, which is simple when small but hard to manage as it grows. Key points (any three):

- **Client-server, resource management:** files, printers, security, access rights and backups are managed centrally on servers by IT staff.
- **P2P, resource management:** there is no server; each peer stores, secures and backs up its own data and shares it directly with other peers.
- **Client-server, scalability:** it grows by adding clients or upgrading servers, and one IT team can manage hundreds of clients; but the server can become a bottleneck and is a single point of failure.
- **P2P, scalability:** cheap and simple for a few devices (homes, small offices), but harder to manage and secure as it grows. (File-sharing P2P such as BitTorrent spreads well, because every new peer also uploads pieces.)

**(c)** [2 marks]

- **Thin client:** data is processed on the server, and programs and files are stored on the server (little or no local storage).
- **Thick client:** data is processed on its own CPU, GPU and RAM, and stored on its own SSD or hard disk, so it also works offline.

**(d)** [3 marks] A public cloud is cheap to start and grows instantly but gives little control; a private cloud is costly but isolated and fully controlled. One mark each:

- **Cost:** public is low upfront and pay as you go; private needs high upfront spending on servers plus staff.
- **Security:** in a public cloud the provider secures hardware shared with other customers, so you rely on the provider; in a private cloud the data is isolated, but you must secure it yourself.
- **Control:** public gives little say over where data is stored and how things are set up; private gives full control of hardware, location and security settings, which helps meet strict data laws.

Also acceptable: growth (public is almost unlimited within minutes; private is limited by your own hardware).

**(e)** [4 marks] Any four, one mark each with its purpose:

- **NIC** in each computer and the printer: connects the device to the network; each has a unique MAC address.
- **Switch** (at least 17 ports, e.g. a 24-port switch, for 15 computers + printer + router): joins the devices in a star and forwards each frame only to its destination.
- **Twisted-pair Ethernet cables:** connect each device to the switch.
- **Router with a modem:** connects the LAN to the ISP and the Internet, routing packets between them; the modem carries the signals over the line.
- Also acceptable: a **wireless access point** (lets laptops and phones join by Wi-Fi); a **file or print server**.

### Question 2 — Medium access and collisions

**(a)** [4 marks] Devices first listen before sending; on a wired shared medium CSMA/CD detects collisions and recovers, and on Wi-Fi CSMA/CA tries to avoid them. Key points (one mark each):

- **Carrier sense:** a device listens and sends only when the medium is idle (multiple access: many devices share it).
- **CSMA/CD (wired):** while sending, the node monitors the voltage; a collision makes it too high, so the node stops and sends a **jam signal** so that every node knows.
- **Random back-off:** each sender waits a random time before trying again, and the range of waits doubles after each collision, so a repeat clash becomes unlikely; after 16 failed attempts the frame is abandoned.
- **CSMA/CA (Wi-Fi):** wait for a clear channel plus a random back-off countdown, optionally reserve it with RTS/CTS, send, then wait for an **ACK**; no ACK means assume a collision, back off and retry.

Also acceptable: a switched Ethernet LAN gives each node a private link to the switch, so collisions cannot happen.

**(b)** [2 marks]

- A Wi-Fi radio **cannot hear other signals while it is transmitting**, so it cannot detect a collision as it happens the way a cable's voltage rise is detected.
- **Hidden node problem:** two devices on opposite sides of an access point may be too far apart to hear each other at all, so their frames can clash at the access point without either sender noticing. Wi-Fi therefore tries to **avoid** collisions (random back-off, RTS/CTS) and uses acknowledgements to find out whether a frame got through.

### Question 3 — Web infrastructure and addressing

**(a)** [3 marks] Example: `https://www.example.com:443/courses/computer-science/notes.html#section2`

- **Protocol** `https://`: how to fetch the resource (HTTP Secure, encrypted).
- **Domain name** `www.example.com`: which server; DNS turns it into the server's IP address. An optional **port** (`:443`) names the service on that server.
- **Path** `/courses/computer-science/` and **resource** `notes.html`: which folder and which file on the server. An optional **fragment** `#section2` says which part of the page to show (and an optional query, e.g. `?q=networks`, passes extra information to the server).

How it locates the resource: the browser uses the protocol, looks up the domain name's IP address with DNS, connects to that server and requests the path and file, then displays the page and jumps to the fragment.

**(b)** [4 marks] One mark per step, up to four:

1. The browser and operating system check their **cache**; if the address is there, the lookup ends.
2. Otherwise the computer asks a **recursive resolver** (run by the ISP or school).
3. The resolver asks a **root server**, which refers it to the right **TLD server** (e.g. .org).
4. The TLD server refers it to the domain's **authoritative server**.
5. The authoritative server returns the **IP address**.
6. The resolver **caches** the answer and passes it to the computer (which caches it too); the browser then connects to that IP address.

Strictly, DNS translates the **domain-name part** of the URL (e.g. www.example.org), not the whole URL.

**(c)** [4 marks] One mark for each difference and one for each example:

- **Difference 1, size:** IPv4 addresses are 32 bits (2³² ≈ 4.3 billion addresses); IPv6 addresses are 128 bits (2¹²⁸ ≈ 3.4 × 10³⁸ addresses).
- **Difference 2, format:** IPv4 is four denary numbers from 0 to 255 separated by dots; IPv6 is eight groups of four hexadecimal digits separated by colons, which can be shortened.
- **IPv4 example:** `192.168.1.20`
- **IPv6 example:** `2001:0db8:0000:0000:0000:ff00:0042:8329`, shortened to `2001:db8::ff00:42:8329`

Also acceptable differences: IPv4 addresses have run out, so homes share one public address between private addresses, while IPv6 gives every device its own; IPv6 devices configure their own address automatically; IPv6 headers are simpler and fixed.

**(d)** [2 marks]

- The **Internet** is the infrastructure: a worldwide network of interconnected networks (cables, routers, servers) that carries data using TCP/IP.
- The **World Wide Web** is one service that runs on the Internet: the collection of linked web pages and resources, reached with browsers, URLs and HTTP/HTTPS. The Internet also carries other services, such as email, calls and games.

### Question 4 — Protocol stacks and applications

**(a)** [4 marks] One mark per layer, in order:

| Layer (top to bottom) | Core responsibility |
|---|---|
| Application | Gives applications network services (web pages, email, file transfer) using protocols such as HTTP, FTP, SMTP, POP3, IMAP and DNS |
| Transport | Splits data into numbered segments, adds port numbers, checks that every segment arrives and puts them back in order (TCP, UDP) |
| Internet | Adds the source and destination IP addresses and routes packets across networks (IP) |
| Link | Adds MAC addresses and sends the bits over the physical medium as frames (Ethernet, Wi-Fi) |

Listing them bottom to top (link, internet, transport, application) is equally correct.

**(b)** [3 marks]

- **Encapsulation:** each layer treats everything from the layer above as data and wraps it in its own header: the transport layer adds a TCP header (port numbers, sequence number) to make a segment, and the internet layer adds an IP header (source and destination IP addresses) to make a packet.
- The **link layer** adds a frame header (MAC addresses) and a trailer (an error check) to make a frame; the receiver unwraps the layers in reverse order.
- **A router** reads only as far as the internet layer: it removes the frame, reads the destination IP address, uses its routing table to choose the next hop (lowering the hop limit by 1) and wraps the packet in a new frame for the next link.

**(c)** [4 marks] One mark each:

- **HTTP:** the rules for requesting and sending web pages between a browser and a web server (request and response).
- **FTP:** the rules for uploading and downloading files, text or binary, between a client and a server.
- **POP3:** a pull protocol that downloads emails from the mail server to one device and, by default, deletes them from the server.
- **IMAP:** a pull protocol that keeps emails on the server and syncs them (inbox, folders, read status) across all your devices.

**(d)** [2 marks]

- SMTP is the **push protocol for sending** email: the sender's email app pushes (uploads) the message to the sender's outgoing mail server.
- That server uses DNS to find the recipient's mail server and **relays** the message to it, server to server, again by SMTP; the message is stored there until the recipient pulls it with POP3 or IMAP. (Attachments travel packaged with MIME; SMTP cannot fetch mail from a mailbox.)

### Question 5 — Switching paradigms

**(a)** [2 marks]

- A **dedicated path** (circuit) between sender and receiver is set up **before** any data is sent.
- The path and all its bandwidth are **reserved** for that one communication for its whole duration (data follows it in order), and are released when it ends. Example: a landline telephone call.

**(b)** [2 marks] Any two:

- The circuit's **whole bandwidth is reserved**, so the data rate never drops: important for a continuous live video stream.
- Delay is **low and constant** (no jitter), so picture and sound stay smooth in real time.
- All data takes the same path and **arrives in order**, so no reassembly or buffering is needed.

**(c)** [3 marks] Two benefits and one drawback, one mark each:

- **Benefit:** efficient: links are shared, so no capacity is wasted while a user is silent.
- **Benefit:** robust: packets are routed around a failed link or router, so the message still arrives.
- **Drawback:** variable delay (jitter): queues at busy routers make packets arrive at uneven intervals and out of order, so they must be reordered.

Also acceptable benefits: no set-up delay; only lost packets are resent; cheaper to run. Also acceptable drawbacks: lost packets must be resent; header overhead; no guaranteed bandwidth.

### Question 6 — Data security, validation and verification

**(a)** [3 marks] One mark each:

- **Data security:** protecting data and computer systems from unauthorised access, theft, loss, damage or corruption (e.g. passwords, firewalls, backups).
- **Data privacy:** the right of individuals to control how their personal data is collected, used and shared (protected by laws such as GDPR).
- **Data integrity:** data remaining accurate, complete and unchanged during entry, storage and transfer.

**(b)** [4 marks] Validation checks that data is **sensible**; verification checks that it **matches the original**. Key points (one mark each):

- **Validation** is an automatic check, made as data is entered, that it follows set rules: e.g. a **range check** (age 11–19 rejects 42) or a **format check** (dd/mm/yyyy rejects 2024-02-12).
- Validation **cannot prove data is correct**: a sensible but wrong value, such as 16 typed for 15, still passes.
- **Verification during entry:** **double entry** (typing the data twice so the computer compares the copies, e.g. a new password) or a visual check against the source document; neither catches the same mistake made twice.
- **Verification during transfer:** a **parity check** (even parity: an odd count of 1s shows an error, so the data is resent) or a checksum; parity misses an error if two bits flip.

**(c)** [3 marks] Any three, one mark each:

- **User accounts and strong passwords**, with **access rights** that limit what each user can do.
- A **firewall**, which checks traffic in and out against rules and blocks anything not allowed.
- **Antivirus software**, which scans files and quarantines or deletes infected ones.

Also acceptable: anti-spyware software, encryption, digital signatures, two-factor authentication.

**(d)** [2 marks]

- **Phishing:** fake emails or messages that look genuine trick the user into **clicking a link** to a fake website and entering personal details; it needs the user to act.
- **Pharming:** malicious code on the computer, or a tampered DNS server, **redirects** the user to a fake website even when they type the correct address; no click is needed.

### Question 7 — Encryption mechanics and certificates

**(a)** [4 marks] One mark for key management, one for speed and two for how each type turns plaintext into ciphertext:

| | Symmetric | Asymmetric |
|---|---|---|
| Key management | One shared secret key, which must be sent to the receiver secretly: the key distribution problem | A key pair: the public key can be shared openly and the private key never leaves its owner, which solves key distribution |
| Speed | Fast, so used for bulk data (Wi-Fi, disks, the main part of HTTPS) | Much slower, so used to share a symmetric session key and for digital signatures |
| Plaintext to ciphertext | The **same key** encrypts and decrypts, e.g. plaintext bits XORed with key bits, as a stream cipher or in fixed-size blocks | Encrypt with the **receiver's public key** (toy example: 4³ mod 33 = 31); only the matching **private key** can decrypt (31⁷ mod 33 = 4) |

**(b)** [3 marks]

- "In reverse": the sender **hashes** the message and encrypts the hash with her **own private key**; the result is the digital signature, sent with the message.
- The receiver decrypts the signature with the **sender's public key** and compares the result with his own hash of the message.
- If they match, the sender's **identity** is proven (only her private key could make that signature) and the message's **integrity** is confirmed (any change would give a different hash).

**(c)** [3 marks] One mark per step:

1. Decrypt the signature using the **sender's public key** (from the sender's certificate), which gives the hash the sender made (hash A).
2. Hash the received message with the **same hash function** (hash B).
3. **Compare** A and B: equal means the message is genuine and unchanged; different means it was changed or not signed by that sender, so it is rejected.

**(d)** [3 marks]

- **What they are:** Secure Sockets Layer (SSL) and its successor, Transport Layer Security (TLS), are protocols that encrypt and authenticate data sent between two applications, e.g. a browser and a web server; SSL is out of date and TLS is used today.
- **What they provide:** encryption, authentication of the server by its certificate, and integrity (changes are detected).
- **Where they are used** (any two): HTTPS for online banking and shopping; logging in to websites; email (SMTP, IMAP or POP3 over TLS); video calls, messaging and cloud storage; some VPNs.

**(e)** [4 marks] One mark per step, up to four:

1. The company generates a **key pair** and keeps the private key secret.
2. It **applies** to a certificate authority, sending its public key and domain name (and company details).
3. The CA **checks** the applicant's identity and that it controls the domain.
4. The CA **creates the certificate** (owner's name or domain, public key, CA's name, serial number, valid dates) and **signs** it with the CA's own private key.
5. The company **installs** the certificate on its server, which sends it to every visitor (and renews it before it expires).

**(f)** [2 marks]

- The browser already holds the **public keys of trusted CAs**, and uses the CA's public key to check the **CA's signature** on the website's certificate (it also checks the domain name and the dates).
- If the signature is valid, the certificate was issued by a trusted CA and has not been changed, so the browser trusts that the **public key inside it belongs to that website**.

### Question 8 — Quantum cryptography

**(a)** [2 marks]

- Asymmetric encryption is safe only because some maths problems, such as **splitting a huge number n into its prime factors**, would take ordinary computers billions of years.
- A large enough **quantum computer** could solve them quickly (for factoring, using Shor's algorithm), so an attacker could work out the private key from the public key, then decrypt intercepted messages and session keys or forge digital signatures.

**(b)** [3 marks] One mark per point:

- Alice sends the key as single **photons**, each polarised with a randomly chosen setting; Bob measures each with a random setting, and they keep only the bits where their (publicly compared) settings matched.
- **Measuring a photon changes it** and a photon cannot be copied, so an eavesdropper must guess the settings; wrong guesses (half of them) disturb the photons and cause errors in about **1 in 4** of the kept bits.
- Alice and Bob publicly **compare a sample** of the kept bits: almost no errors means the key is safe to use; many errors means someone listened, so they discard the key and start again.
