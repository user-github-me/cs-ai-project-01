# Chapter 4 — Networking

**Learning outcome:** Compare network architectures, clients and clouds; identify communication hardware and media; trace URLs, DNS and TCP/IP; explain application protocols, switching and network performance; distinguish data protection goals, encryption, signatures and TLS.

**Prerequisites:** Read the relevant earlier chapters; this chapter connects those ideas to networking.

## Connect a room, a city, a world

### What a network provides

A network connects devices so they can exchange data and share services, storage or hardware. A connected device is a node. Networks differ in scale, ownership, transmission media and management. Geographic size alone does not determine speed: a particular WAN link can be faster than a particular local wireless connection.

### Names describe the scope

| Network | Typical scope |
| --- | --- |
| PAN / WPAN | A person’s nearby devices; a WPAN is wireless. |
| LAN / WLAN | A home, office or building; a WLAN uses wireless links. |
| MAN | A metropolitan area or several sites across a city. |
| WAN | Widely separated sites, regions or countries. |

### A practical analogy

A personal conversation resembles a PAN, a building intercom resembles a LAN, and an inter-city transport network resembles a WAN. Real networks can contain smaller networks inside them. The Internet is a global interconnection of networks, built from links and equipment operated by many organisations.

### Apply and check

**Try before reading feedback:** Does lab LAN versus city WAN alone determine which has greater throughput?

**Feedback:** No. Link technology, capacity, congestion and endpoints determine actual performance; geography contributes propagation delay but is not a throughput specification.

**Practice connection:** Exercise 4.1a in exercises.md; explained answer in solutions.md.

## Clients, servers & peers

### Two ways to organise services

| Client–server | Peer-to-peer |
| --- | --- |
| Clients request services from servers. | Peers can both request and provide resources. |
| Central management can simplify permissions and backup. | Resources can be distributed among participating peers. |
| Capacity and resilience require deliberate design. | Coordination and consistent security can be harder. |

### Servers are roles, not magic boxes

A file server provides access to shared files. One physical machine can host several server programs, and a service can run across many machines. A server failure need not stop an entire network if replication or failover is provided. A small P2P setup can be inexpensive, while large P2P systems can also scale when their protocols are designed for it.

### A service request

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Client request |
| 2 | Network |
| 3 | Server response |

A peer may act as a client for one exchange and as a server for another. Describe the role being performed.

### Apply and check

**Try before reading feedback:** If the only campus dispatch server fails, what dependency has the architecture exposed?

**Feedback:** A central service can be a single point of failure unless replicated or supported by an appropriate local fallback.

**Practice connection:** Exercise 4.1b in exercises.md; explained answer in solutions.md.

## Where does the work happen?

### Thin and thick clients

| Thin client | Thick client |
| --- | --- |
| Relies heavily on remote applications or services. | Performs substantial processing locally. |
| Can simplify central administration. | Can support more offline work. |
| Network and server availability affect its main tasks. | Needs suitable local hardware and maintenance. |

### Public and private clouds

A public cloud provides services using infrastructure operated by a provider for multiple customers. A private cloud is dedicated to one organisation and can be on-site or hosted elsewhere. Public cloud can reduce initial capital cost and offer flexible capacity; private cloud can provide greater direct control but requires resources to manage.

### Compare actual responsibilities

Neither deployment is automatically secure. Consider access control, configuration, backups, data location, operational expertise and ongoing cost. Replication improves availability but is not a substitute for a recoverable backup. A thin client still performs some local processing, such as displaying an interface; “thin” does not mean it has no CPU.

### Apply and check

**Try before reading feedback:** What breaks first if a thin client loses its server connection?

**Feedback:** Remote-dependent work may stop or degrade. A thick client may retain more local capability, though local storage and computation have costs.

**Practice connection:** Exercise 4.1d in exercises.md; explained answer in solutions.md.

## The devices along a network path

### Recognise the job

| Device | Primary role |
| --- | --- |
| NIC | Connects a host to a network interface. |
| Switch / bridge | Forwards frames between LAN ports or segments. |
| Router | Forwards IP packets between networks. |
| Wireless access point | Connects wireless stations to a network. |
| Hub / repeater | Repeats signals; a hub sends them to multiple ports. |
| Gateway / modem | Translates between systems / modulates and demodulates signals. |

### Addresses serve different scopes

An Ethernet switch learns which MAC addresses are reachable through which ports. A router uses IP routing information to select a next hop. MAC addresses can be changed or randomised; they are not always permanently fixed identifiers. A modem’s modulation depends on the medium, rather than being limited to old telephone lines.

### A switch is selective, not omniscient

Known unicast frames can be sent to a selected port. Broadcasts and unknown destinations may be flooded within the relevant LAN. A router chooses a route using its routing table and policies; it does not always measure the least congested possible path for every packet.

### Apply and check

**Try before reading feedback:** A packet leaves the campus subnet for another network. Is a switch alone the same as an IP router?

**Feedback:** No. A typical switch forwards local link-layer frames; a router forwards IP packets between networks. Some products combine roles.

**Practice connection:** Exercise 4.4a in exercises.md; explained answer in solutions.md.

## Sharing a communication medium

### Choose a link for its conditions

Twisted-pair copper reduces some electromagnetic interference by twisting paired conductors. Optical fibre carries light and supports high-capacity links. Wi-Fi uses shared radio channels; Bluetooth connects nearby devices using its own radio protocols. Range, speed and frequency-hopping behaviour depend on the version, equipment and environment, not one universal distance or channel count.

### Collision detection and avoidance

| CSMA/CD | CSMA/CA |
| --- | --- |
| Historically used on shared, half-duplex Ethernet. | Used by Wi-Fi to manage shared radio access. |
| Listen, transmit, detect collision, back off and retry. | Listen, wait/back off, transmit and use acknowledgements. |
| Modern switched full-duplex Ethernet has no collisions on the link. | RTS/CTS is an optional mechanism, not a compulsory step every time. |

### Use the conversation analogy

At a busy table, people listen before speaking and pause if they talk over each other. Random backoff reduces repeated clashes. Avoidance reduces the chance of a collision; it cannot guarantee one never happens. Interference, hidden stations and missing acknowledgements can still cause retries and delay.

### Apply and check

**Try before reading feedback:** A modern full-duplex switched Ethernet link slows under load. Is collision detection necessarily the cause?

**Feedback:** No. That link does not normally use shared-medium collisions. Queueing, bottleneck capacity or endpoint limits can explain the delay.

**Practice connection:** Exercise 4.2 in exercises.md; explained answer in solutions.md.

## Internet, web & addresses

### The web is one Internet service

The Internet carries many kinds of communication. The World Wide Web uses linked resources accessed through web protocols. Email and other services also use the Internet. IPv4 addresses have 32 bits; IPv6 addresses have 128 bits. An address helps identify a network interface for communication, while routing determines how packets are forwarded.

### Read a URL: https://example.org:443/course/notes?q=ai#part2

| Part | Meaning |
| --- | --- |
| https | Scheme: how the resource is accessed. |
| example.org / :443 | Host name / port number. |
| /course/notes | Path interpreted by the server. |
| ?q=ai | Query supplied to the application. |
| #part2 | Fragment identifying a location within the resource. |

### A URL is not just an IP address

The host name may be resolved through DNS. The path selects a resource on that host and need not correspond to a physical directory. Default ports can be omitted. A browser normally handles the fragment locally rather than sending it as part of an HTTP request.

### Apply and check

**Try before reading feedback:** In https://campus.example/rover?id=7, which part is the host and which is the query?

**Feedback:** Host: campus.example. Query: id=7. HTTPS is the scheme; /rover is the path.

**Practice connection:** Exercise 4.3a in exercises.md; explained answer in solutions.md.

## Find a host with DNS

### Names are easier to remember

The Domain Name System maps names to records, including records that provide IP addresses. A browser and operating system may already have a cached answer. If not, a recursive resolver can obtain an answer using the DNS hierarchy. Cached answers remain usable for their permitted lifetime, reducing repeat lookups.

### A simplified lookup

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Client |
| 2 | Recursive resolver |
| 3 | Root / TLD |
| 4 | Authoritative server |

The resolver follows referrals, receives the requested record, caches it and returns the answer to the client.

### The lookup is only one step

After resolving a host, a client still needs to establish suitable communication with the service. DNS does not deliver the web page itself, and it does not translate an entire URL, including its path, into an address. Failures in DNS, connectivity, transport, security negotiation or the application can each prevent a page from loading.

### Apply and check

**Try before reading feedback:** DNS successfully returns an address but the web page still fails. Is that contradictory?

**Feedback:** No. Name resolution and application transfer are separate stages; routing, server availability or application errors can still fail.

**Practice connection:** Exercise 4.3b in exercises.md; explained answer in solutions.md.

## Give each protocol layer a job

### The four-layer TCP/IP model

| Layer | Responsibility | Examples |
| --- | --- | --- |
| Application | Application messages and services. | HTTP, DNS, SMTP |
| Transport | Communication between application endpoints. | TCP, UDP |
| Internet | IP addressing and routing between networks. | IPv4, IPv6, ICMP |
| Link | Local network delivery and access to the medium. | Ethernet, Wi-Fi |

### Encapsulation is packaging

Application data is carried inside transport data, which is carried inside IP packets, which are carried by link-layer frames. Each layer has its own fields and scope. A frame’s MAC addresses are not the same thing as an IP packet’s addresses; the frame can change at the next link while the packet continues its journey.

### Reliable ordering is a service choice

TCP provides an ordered byte stream with reliability and flow/congestion control. UDP provides datagrams without those guarantees by itself. Applications may build additional mechanisms over UDP. Not every IP packet contains a sequence number that allows a router to rebuild a file: reconstruction belongs to the relevant endpoint protocol.

### Apply and check

**Try before reading feedback:** At which TCP/IP layer does IP routing belong?

**Feedback:** The Internet layer. TCP belongs to transport; HTTP belongs to application; Wi-Fi is a link technology.

**Practice connection:** Exercise 4.4a in exercises.md; explained answer in solutions.md.

## Web, files, email & sharing

### Identify the application protocol

| Protocol | Purpose |
| --- | --- |
| HTTP / HTTPS | Web requests and responses; HTTPS protects HTTP using TLS. |
| FTP | Traditional file transfer; plain FTP is not encrypted. |
| SMTP | Submitting and relaying email. |
| POP3 | Retrieving email, with retention behaviour set by the client. |
| IMAP | Accessing and synchronising server-held mailboxes. |
| MIME | Structures message content and attachments; not a transport protocol. |

### A BitTorrent example

BitTorrent divides a file into pieces that peers exchange. A swarm is the participating group. A seed has the complete content and can upload pieces. A downloading peer may upload too; the word “leecher” does not necessarily mean a malicious user. Trackers can help peers discover one another, while distributed discovery is also possible.

### Security is part of the choice

A protocol name alone may not guarantee confidentiality or authenticity. Use protected versions or secure alternatives where appropriate. File-transfer tools such as SFTP use a different protocol from FTP. A networked application must also authenticate users and apply access controls at the service.

### Apply and check

**Try before reading feedback:** A student wants the same mailbox state on a laptop and phone. Which course protocol is the best fit?

**Feedback:** IMAP is designed to manage server-held mail across clients. Use an appropriately secured connection.

**Practice connection:** Exercise 4.4b in exercises.md; explained answer in solutions.md.

## Reserve a path or share capacity?

### Circuit and packet switching

| Circuit switching | Packet switching |
| --- | --- |
| Reserves communication capacity for a session. | Shares links by sending discrete packets. |
| Can provide predictable allocated capacity. | Uses capacity efficiently across variable traffic. |
| Reservation can be idle during pauses. | Queues, loss and variable delay need management. |

### Packets move hop by hop

A sender divides or packages data according to its protocols. Routers forward IP packets using destination information. Packets may follow different routes or arrive out of order, although this is not required for every transfer. Endpoint protocols handle the reliability or ordering their applications need.

### Apply the comparison carefully

A reserved circuit still has propagation and processing delay; it does not mean zero latency or perfect reliability. Modern Internet video calls commonly use packet-switched networks, buffering, congestion control and other techniques. The source exercise about a preferred circuit assumes a scenario valuing reserved capacity; it is not a universal description of today’s video conferencing.

### Apply and check

**Try before reading feedback:** Why can packet switching use a quiet user’s spare capacity while a dedicated circuit cannot automatically do so?

**Feedback:** Packets statistically share links; a reserved circuit keeps allocated resources for its session even during idle periods.

**Practice connection:** Exercise 4.5c in exercises.md; explained answer in solutions.md.

## Capacity is not responsiveness

### Four problems to distinguish

| Metric | What it tells you |
| --- | --- |
| Bandwidth / capacity | How much data a link can carry per second. |
| Throughput | The successful transfer rate actually achieved. |
| Latency | How long a transfer or response takes. |
| Jitter / loss | Variation in delay / missing packets. |

### Why a fast link can still feel slow

A wide road carries many cars, but a long journey still takes time. Similarly, high bandwidth does not remove propagation delay, queueing or server processing. Retransmitting lost data can add delay; interference and contention can reduce throughput. Measure the entire task, not just the advertised link rate.

### Choose a response to the problem

Compress or summarise data when capacity is limited. Reduce unnecessary round trips when latency matters. Use timestamps to identify stale measurements. Buffering can smooth jitter for playback, but adds delay. Redundancy and reconnect logic can improve resilience, while local control keeps a time-critical action from depending on an unavailable remote link.

### Apply and check

**Try before reading feedback:** A 100 Mb/s link has 200 ms command delay. Does the high capacity guarantee a responsive control loop?

**Feedback:** No. Capacity and latency are different. At 30 m/s, 0.2 s contributes 6 m of delay distance before response.

**Practice connection:** Exercise 6.5 in exercises.md; explained answer in solutions.md.

## Protect data and its meaning

### Three different goals

| Goal | Question |
| --- | --- |
| Security | Who can access, change or disrupt the system? |
| Privacy | How is personal data collected, used and shared? |
| Integrity | Has the data remained correct and unaltered? |

### Validation versus verification

Validation checks whether an input meets rules: range, type, length or a valid calendar date. It cannot prove a plausible value is true. Verification checks that data agrees with a source or expected copy, such as double entry or a transfer checksum. Checksums detect some errors; a cryptographic authentication mechanism is needed to resist deliberate modification by an attacker.

### Use layers of protection

Strong authentication, least-privilege access, updates, backups and network filtering address different risks. Malware can damage or steal data; spyware monitors activity; phishing tricks a user; pharming redirects a user to an unintended destination. A firewall is not a substitute for secure software, and antivirus cannot promise to detect every threat.

### Apply and check

**Try before reading feedback:** A temperature is validly formatted as 99°C but the true reading is 29°C. Did format validation establish correctness?

**Feedback:** No. Validation establishes conformance to rules; verification against a reliable source or other checks is needed to find a plausible wrong value.

**Practice connection:** Exercise 4.6b in exercises.md; explained answer in solutions.md.

## Keep messages confidential

### From plaintext to ciphertext

Encryption uses an algorithm and a key to transform readable plaintext into ciphertext. Correctly implemented cryptography can protect confidentiality, but key management and authentication remain essential. Encryption alone does not prove who sent a message or ensure that a device receiving it is trustworthy.

### Two approaches

| Symmetric | Asymmetric |
| --- | --- |
| Uses a shared secret key. | Uses a related public/private key pair. |
| Efficient for bulk data encryption. | Supports mechanisms such as key establishment and signatures. |
| Both parties must obtain the secret securely. | The public key must be authenticated to its owner. |

### Combine their strengths

Secure protocols commonly use asymmetric mechanisms to authenticate or establish shared secrets, then symmetric authenticated encryption for application traffic. Keep private keys private. Do not invent an encryption scheme by substituting characters or treating a checksum as a secret; the design and implementation of cryptography require established protocols.

### Apply and check

**Try before reading feedback:** Does a confidential encrypted packet automatically contain a safe command?

**Feedback:** No. Confidentiality hides data in transit. Correct authorisation, integrity/authenticity, freshness and command validation remain necessary.

**Practice connection:** Exercise 4.7a in exercises.md; explained answer in solutions.md.

## Trust, signatures & certificates

### A signature protects authenticity and integrity

A sender signs a message, usually through a hash-based construction, using a private signing key. A verifier checks the signature with the matching public key. A valid signature supports a claim about the key used and whether the signed content changed. It does not encrypt the message or prove that the message’s claims are true.

### A simplified verification path

| Step / element | Meaning in the diagram |
| --- | --- |
| 1 | Message + signature |
| 2 | Trusted public key |
| 3 | Verify |
| 4 | Accept or reject |

Signing is not generally “encryption in reverse”; the operations depend on the signature algorithm.

### Certificates and TLS

A digital certificate binds an identity, such as a domain name, to a public key and is signed by an issuer. A client checks the trust chain, validity and expected name. TLS uses authentication and cryptography to protect communication, including HTTPS. SSL is obsolete and should not be deployed. A certificate can authenticate a domain without proving the site is honest in every other respect.

### Apply and check

**Try before reading feedback:** An attacker replays an old message with its valid signature. What does the signature fail to establish?

**Feedback:** It does not establish freshness. Use appropriate sequence/session and timestamp or nonce checks alongside trusted signature verification.

**Practice connection:** Exercise 4.7c in exercises.md; explained answer in solutions.md.

## Encryption modes & quantum ideas

### Blocks and streams

A block cipher operates on fixed-size blocks; a mode specifies how it is used for longer messages. A stream cipher combines data with a generated keystream. Reusing a key/nonce combination incorrectly can undermine security. Authenticated encryption also detects unauthorised changes, rather than providing confidentiality alone.

### Understand CBC as a historical example

Cipher block chaining combines a plaintext block with the previous ciphertext block before encryption, starting with an initialisation vector. Correct IV handling, padding and authentication matter. CBC is useful to understand, but a new application should use a vetted protocol and suitable authenticated-encryption construction rather than assembling its own cryptographic workflow.

### What quantum key distribution does

QKD uses quantum signals and classical communication to establish key material. Its security analysis detects disturbance statistically under stated assumptions; it does not make every device or message unhackable. It requires specialised infrastructure and authenticated classical communication. Post-quantum cryptography is a different approach: algorithms designed to resist quantum attacks on conventional computers.

### Apply and check

**Try before reading feedback:** Why is a homemade encryption mode risky even if the block cipher is strong?

**Feedback:** Incorrect nonce handling, integrity protection or composition can break the system. Use vetted protocols and libraries with their documented requirements.

**Practice connection:** Exercise 4.7a in exercises.md; explained answer in solutions.md.

## Chapter review

Complete ACT-04 using the supplied mission instructions. Then choose two related terms and explain a mechanism using both; identify one limitation of the teaching model and one condition that could change the result.

## Reference support

- R3: RFC 1122 — Requirements for Internet Hosts: Communication Layers — Section 1.1.3 (Internet protocol suite) and the link, IP and transport sections. https://www.rfc-editor.org/rfc/rfc1122
- R4: RFC 8446 — The Transport Layer Security (TLS) Protocol Version 1.3 — Section 1 (Introduction) and Section 8 (0-RTT and anti-replay). https://www.rfc-editor.org/rfc/rfc8446

Full resource introductions, optional tasks and access alternatives are in ../references.md.
