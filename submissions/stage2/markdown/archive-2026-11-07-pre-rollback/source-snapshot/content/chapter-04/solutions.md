# Chapter 4 — Networking

## Explained answers

These are expected answers, not the only acceptable wording. Credit a correct alternative with clear assumptions and reasoning. Try the exercises before reading this section.

### Answer 4.1a

A LAN connects a local site, often under one organisation’s control. A WAN connects distant sites across wider geography and may depend on carriers. WAN paths often introduce longer propagation paths, but equipment, traffic and access links determine actual throughput and delay; scope alone does not guarantee a speed.

### Answer 4.1b

Client–server centralises a service, making policy and backup management easier but creating capacity and availability responsibilities. Peers can both request and provide resources, spreading work but complicating discovery, trust and consistency. Both can scale with suitable designs; neither is automatically unlimited.

### Answer 4.1c

A thick client performs substantial local processing and may keep local data. A thin client depends more on a remote server for computation and storage. Thin clients simplify some central management but depend more on network availability; actual systems can be hybrids.

### Answer 4.1d

A public cloud uses provider-operated shared infrastructure, often lowering up-front costs but adding provider dependence and shared security responsibilities. A private cloud is dedicated to one organisation and offers more direct control, but the organisation must fund and operate or contract capacity and security. Neither is inherently secure merely because of its label.

### Answer 4.2

Legacy shared, half-duplex Ethernet uses CSMA/CD to detect a collision and retry after backoff. Wi-Fi uses collision avoidance, including channel sensing, waiting and acknowledgements. Modern switched full-duplex Ethernet links normally avoid shared-medium collisions; congestion and queues can still occur.

### Answer 4.3a

In https://example.org/guide/chapter1, https is the scheme, example.org is the host name and /guide/chapter1 is the path. A URL can also include a port, query and fragment. It identifies how and where to request a resource, not necessarily a fixed physical machine.

### Answer 4.3b

DNS resolves names through a distributed hierarchy and caches. A resolver may return an address record for the requested host; the application can then use that address to contact a server. DNS does not itself download the web page, and cached records have limited lifetimes.

### Answer 4.4a

Application: services and application messages. Transport: communication between application endpoints, such as TCP streams or UDP datagrams. Internet: IP addressing and routing across networks. Link/network-access: delivery over a local link, such as Ethernet or Wi-Fi. Layer names vary slightly between teaching models.

### Answer 4.4b

HTTP requests and transfers web resources. FTP transfers files but its traditional form lacks confidentiality. POP3 retrieves email, often for local storage. IMAP manages and synchronises email kept on a server. Secure variants or TLS are required where credentials and content need protection.

### Answer 4.5a

Circuit switching reserves communication resources along a path for a session. Capacity can remain allocated even when no useful data is being sent, giving a different sharing trade-off from statistical packet multiplexing.

### Answer 4.5b

Under the stated reserved-capacity requirement, a circuit can provide predictable allocated capacity without competing for that same reservation during the call. It may waste idle capacity and needs setup. Modern Internet video calls normally use packet networks; the exercise is a hypothetical trade-off, not a claim about usual Internet practice.

### Answer 4.5c

Benefits: bursty users can share link capacity efficiently, and packets can be forwarded along available paths. Drawback: queueing, loss or reordering can create variable delay and require handling. No route change or reliability is guaranteed merely by using packets.

### Answer 4.6a

Security protects systems and data against unauthorised access or harm. Privacy concerns appropriate collection and use of personal information. Integrity concerns accuracy and resistance to unauthorised alteration. Encrypted personal data can still be collected without a legitimate purpose, so confidentiality alone does not settle privacy.

### Answer 4.6b

Validation checks whether data satisfies rules such as format or range; a plausible wrong date can pass. Verification checks agreement with an original or expected copy, such as double entry or a transfer checksum. A checksum detects some changes but does not establish authenticity against an active attacker.

### Answer 4.6c

Examples: least-privilege access controls, timely security updates, strong authentication, firewalls, encryption, protected backups and malware detection. Explain the threat addressed; no single mechanism stops every threat.

### Answer 4.7a

Symmetric cryptography uses a shared secret and is efficient for bulk data, but securely distributing and protecting that secret matters. Asymmetric mechanisms use a public/private key pair for particular tasks such as key establishment or signatures. Both require correct algorithms and key handling; a public key is not itself secret.

### Answer 4.7b

The sender signs with a private signing key; recipients verify with the matching public key. A valid signature supports origin and integrity relative to trust in that key, but does not hide the message. Encrypting for confidentiality is a distinct operation. A copied valid old signed message may still require replay protection.

### Answer 4.7c

SSL is the obsolete predecessor to TLS. TLS is used today for protected transport in HTTPS and other application protocols, providing confidentiality and integrity with authentication according to configuration. TLS does not make an endpoint safe or prevent a legitimate user from misusing received data.
