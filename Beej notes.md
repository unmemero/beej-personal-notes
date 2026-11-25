[Reference](https://beej.us/guide/bgnet0/html/split/foreword.html)
# Overview
- We receive arbitrary bytes exchanged between 2 or more nodes.
- We need away to identify those nodes, maintain data integrity, and route data between 2 nodes among millions
## Circuit switched network
- Need a dedicated blocking circuit per call
- Made of electro-mechanical relays and switches
- Limited number of wires
## Packet switched
- Data doesn't block a single line until send is complete
- Data is split into packets. 84 KB would be split into 50-60 packets
- These packets are sent over the lines as space permits
- Once arriving at the destination computer, it reconstructs the full message from the packets
- Packets may get sent to other places (instead of the post office in the town of your friend, may go to a DC further north), which allows for massive data transfers of many people.
- Data moves from computer to computer until getting to the destination
- Advantages:
	- Multiple PCs can use the same wire at the same time
	- No need for dedicated circuit between each computer
	- Wire can be used at full capacity (If unused, another person can use it)
## Client/Server Architecture
- Server listens, client sends requests
- Server sends back responses to the client based on the requests
## The OS, Network Programming, and Sockets
- To use network, must get perms from OS
- Modern API $\neq$ Network sockets interface in UNIX
- Can use original sockets API through C in Unix
## 2.5 Protocols
- A specific arrangement of bytes for computers to understand each other
- Examples: 
	- TCP: Reliable
	- UDP: Quick and unreliable
	- IP: For computers to find each other
	- HTTP: To make web requests and for websites
	- Ethernet: To send data over LAN
- These live at different layers of the network software.
## 2.6 Network Layers and Abstraction
- HTTP req $\rightarrow$ Headers wrapping with TCP/UDP $\rightarrow$ More header wrapping for IP $\rightarrow$ OS hands over to NIC $\rightarrow$ NIC wraps data in Ethernet protocol and sends package $\rightarrow$ Send to server via IP (OS verifies) $\rightarrow$ Remainder of resolution from server
- This is the protocol stack
- Each layer is swappable (as long as it's properly maintained and changes well documented) since it only concerns on its own responsibility
## 2.7 Wired versus Wireless
- Ethernet is a protocol, not a cable (that cable is just called wire)
- LAN is for both WiFi and Wired
- WiFi allows multiple connections to the same access point, while Ethernet: 1 cable, 1 connection
# Sockets API
- Allows for inter process communication (including internet).
- C version ins a blend of system calls and lib calls
- Python calls the C sockets API
## 3.1 Client Connection Process
Steps to connect to another computer(process):
1. **Ask OS for socket**. Python uses object, C uses File Descriptor (FD). No connection yet.
2. **Perform a DNS lookup**. DNS is the distributed DB that holds the mapping of domain$\rightarrow$ IP address. Perform lookup with
```python
socket.getaddrinfo()
```
In python (not C) this resolution is automatic when you use the domain name in:
```python
socket.connect()
```
3. **Connect to that socket**. Connect to that IP address and port. From 0 - 65635
	- Port 80 is usually for HTTP protocol
	- Server must be listening on that port
4. **Send and receive data** Send sequence of bytes
5. **Close connection**. Close when done, saying there is nothing else left to be said.
## 3.2 Server Listening Process
Process:
1. **Ask OS for socket**
2. **Bind socket to port** Assign port to server. Only root can assign ports under 1024. Ports are per computer. Clients are auto assigned a port
3.  **Listen to incoming connections**. OS knows we'll listen to connections in that port
4. **Accept connection**. Server sleeps until incoming or pending connection. 
	- Once the connection is received, it creates a new socket for that connection, so the OS can handle multiple clients at once
	- Some servers spawn a new thread or process with each new client (not mandatory).
5. **Send and receive data**. Receive requests, send responses.
6. **Go back and accept another connection**. May be a queue of requests waiting to be fulfilled.
7. **Close connections once server is shutdown**
## 3.3 Client API Code
```python
import socket

# 1. Create socket object
s = socket.socket()

# 2. Connecting to host and port (With auto DNS lookup)
s.connect(("google.com", 80)) # arg is tuple

# 3. Sending and receiving data
s.send(data) # may be partial send
s.sendall(data) # send all data
data = s.recv(128) # receive max 128 bytes

# 4. Close connection
s.close()
```

## 3.4 Server API Code
```python
import socket

# 1. Create socket
s = socket.socket()

# 2. Bind to address and port
s.bind(("localhost", 3490))

# 3. Start listening for incoming connections
s.listen()

# 4. Accept incoming connections (usually in a loop)
while True:
	client_socket, client_addr = s.accept() # server will block (sleep) until new incoming connection
	
	# 5. Send and receive data
	client_socket.send(data) # partial send
	client_socket.sendall(data) # full send
	data = client_socket.recv(128) # Only receive 128 bytes max
	
# 6. Close when done
s.close()
```
# 4 The Layered Network Model
==🟡IMPORTANT== terms
- **IP Address**: Computer ID on the internet. 4 bytes split by dots
- **Port:** Process listener identifier within a computer.
- **TCP**: Transmission Control Protocol. Identifies senders and receivers by port. Packets arrive correctly and in order.
- **UDP**: (Universal Datagram Protocol): Lightweight TCP that only promises if a package arrives, it arrives error free.
- **IPv6**: Goes from traditional 4 to 16 bytes. Examples:
```bash
`::1` or `2001:db8::8a2e:370:7334`, or even bigger.
```
- **NAT:** Network Address Translation. Allows organizations to have private subnets with non-globally unique addresses translated to globally unique addresses as they pass through a router. This private subnets usually start with: `192.168.X.X` or `10.X.X.X`
- **Router:** packet switching computer that switches packages through the package switching network. It "routes" the packages to the destination IP.
- **IP:**  Internet Protocol. Identifies computers by address and routes data to them through routers
- **Local Area Network:** A network where all computers are connected not via a router.
- **Interface:** Physical Networking Hardware. Can have many in one PC like Ethernet cable and WiFi.
- **Header:** Data prepended to the packet's main information as part of the protocols' requirements.
	- TCP includes error correction information and source and destination port number.
	- IP includes source and destination addresses
	- Ethernet source and destination MAC addresses
	- HTTP response includes data length, date modified, and success status
	- Think envelope in mail
- **Network Adapter:** Network card
- **MAC Address:** Media Access Control. 6 bytes separated by colon. Must be unique on the LAN. Device identifier in LAN (innermost network of the internet)
## 4.1 The Layered Network Model
- Each protocol is a layer performing a function
## 4.2 An example of Layering Protocols on Data
- Example HTTP request built by browser
```bash
GET / HTTP/1.1
Host: example.com
Connection: close
```
HTTP don't care of TCP or IP or the Ethernet
- The OS wraps HTTP request in TCP headers
- Then it wraps that with the IP protocol data
- Sends data to LAN, which includes the router. For this, the OS sends it to the MAC address corresponding to the next IP address. This mean, it's wrapped in the Ethernet header
	- This happens via a lookup via the ARP cache
- The data goes out the wire
- The computer with the MAC address listens and receives the packet, and the OS strips the Ethernet Header.
- If the IP address is correct, it strips the IP headers, else it discards the packet.
- TCP header inspection makes sure packet is correct, and the header is stripped. Requests resend  from sender if packet is not correctly formatted
- HTTP wakes up the listening server, and gives it the data
- If the destination address is an intermediate router, it strips the Ethernet headers. Router checks the IP address and determines where to forward the packet, then it sends it to that interface with another Ethernet packet (Could be other protocol than Ethernet)
## 4.3 The Internet Layer Model
| Layer       | Responsibility                                  | Example Protocols                             |
| ----------- | ----------------------------------------------- | --------------------------------------------- |
| Application | Structured application data                     | HTTP, FTP, TFTP, Telnet, SSH, SMTP, POP, IMAP |
| Transport   | Data Integrity, packet splitting and reassembly | TCP, UDP                                      |
| Internet    | Routing                                         | IP, IPv6, ICMP                                |
| Link        | Physical, signals on wires                      | Ethernet, PPP, token ring                     |
- All data requires 4 types of transmission:
	- App data, transport, routing, and physical transport
- There's another model. The OSI model.
# The ISO OSI Network Layer Model
- International Standards Organization Open Systems Interconnect model.
- Some traditional internet layers can map to multiple OSI layers

|ISO OSI Layer|Internet Layer|
|---|---|
|Application|Application|
|Presentation|Application|
|Session|Application|
|Transport|Transport|
|Network|Network|
|Data link|Link|
|Physical|Link|

|ISO OSI Layer|Responsibility|Example Protocols|
|---|---|---|
|Application|Structured application data|HTTP, FTP, TFTP, Telnet, SMTP, POP, IMAP|
|Presentation|Encoding translation, encryption, compression|MIME, SSL/TLS, XDR|
|Session|Suspending, terminating, restarting sessions between computers|Sockets, TCP|
|Transport|Data integrity, packet splitting and reassembly|TCP, UDP|
|Network|Routing|IP IPv6, ICMP|
|Data link|Encapsulation into frames|Ethernet, PPP, SLIP|
|Physical|Physical, signals on wires|Ethernet physical layer, DSL, ISDN|
- OSI is rarely used and not the focus of this book.
# 5 Project: HTTP Client and Server
- Program that can download files from a server
- Cannot use `socket.create_connection()`, `socket.create_server()`, or anything in the `urlib` modules
- Encoding must be in ISO-8859-1 for byte sequence, UTF-8 for string
- Use `.encode("format")` to encode bytes. similar for decode
- Always call loop for `recv()` while `\r\n` not received. Break the receive loop if data length is 0
- **301  or 302**: The resource has moved to a different URL
- **400 and 500**: client or server error, 404 not found
# The Internet Protocol (IP)
Protocol responsible for packet routing.
- **IP Address**: Routing identifier for a Host
- **Host**: A computer
## 6.2 Two Common Versions
- **IPv4**: 192.168.1.3
- **IPv6**: `fe80::c2b6:f9ff:fe7e:4b4`
## 6.3 Subnets
- The initial bits of the address identify  individual networks
- The trailing bits identify the hosts in that network
- These individual networks are called subnets
- Example where the first 6 bits identify the network:
	- `00010111`, the bits `000101` and `11` identify the host. This means only 4 possible hosts in this network, 2 in practice because hosts with all 0's or all 1's are reserved.
## 6.4 Additional IP-Layer Protocols
- **ICMP**: Internet Control Message Protocol. a mechanism for communicating IP nodes to talk about IP control metadata with one another
- **IPSec**: Internet Protocol Security. Encryption and Authentication. Mostly used on VPN
ICMP is the most common. `traceroute` util is using ICMP "time exceeded" messages to find out how packets are being routed
## 6.5 Private Networks
- There are networks within a LAN network with hosts with unique addresses (for this LAN network). This is possible through Network Address Translation (NAT, See further content).
## 6.6 Static vs Dynamic IP Addresses, and DHCP
- **Static IP**: Globally unique IP assigned to a host.
- IPv4 addresses are limited. May need to pay money for a static IP. ISP often has a subnet that dynamically allocates on demand.
- IP's are commonly dynamic (reset on device reboot typically)
- On a server on the LAN a program listens for requests which conform to DHCP (Dynamic Host Configuration Protocol)
- DHCP server keeps track of which IP's in a subnet are allocated for use, and which are free. It gets a client their address and returns it to them upon connection, and other data in the computer
# 7 The Internet Protocol version 4
Most common. First popular version
## 7.1 IP Addresses
32 bits, split into 4 bytes by dots
## 7.2 Subnets
- First set of bits in an address is the subnet number, the remainder identifies the hosts. This first set is variable
- When setting up a network with a public IP's you're allocated a subnet from your connection provider. More hosts = More cost.
### Example
- If you need 180 hosts, you need 182 addresses (reserved addresses are for all 0's and 1's). You need 8 bits to represent (0-255 hosts), and the remaining 24 bits are the network bits
- This means, if the address is `192.51.100.0`, `192.51.100` is the network, and `0` is the host.
- To abbreviate this, we type `198.51.100.0/24`
- The hosts (for this network) are identified by the last byte (`0` in this case)
- Address `0` is reserved. Address `255` is used for broadcast
- Can further subnet an address that has been subnetted (assign more bits to network, reducing the hosts)
## 7.3 Subnet Masks
- Number that when ANDed with an IP address will give you the subnet number
- Same format as IP (32 bits/4 bytes) with all subnet bits set to 1. In other words, `198.51.100.0/24` the mask is `255.255.255.0`. This mask is the same for all subnets. 
- This is done to determine the destination subnet
```
         24 network bits         | 8 host bits
  -------------------------------+---------
  11000110 . 00110011 . 01100100 . 01000011    198. 51.100.67
& 11111111 . 11111111 . 11111111 . 00000000  & 255.255.255. 0
-------------------------------------------  ----------------
  11000110 . 00110011 . 01100100 . 00000000    198. 51.100. 0
```
- In this case, the subnet for `198.51.100.67` with mask `255.255.255.0` is `198.51.100.0`
## 7.4 Historic subnets
There used to be class A, B, and C (8 bits on A, 16 B, 24 C). This caused uneven distributions, where some companies got large subnets (16 million) that they didn't fully need
## 7.5 Special Addresses
- `127.0.0.1`: localhost
- `0.0.0.0`: Reserved
- `255.255.255.255` Broadcast. No package incomes into this address
## 7.6 Special subnets
- **10.0.0.0/8** - Private network addresses (_very common_)
- **127.0.0.0/8** - This computer, via the _loopback_ device.
- **172.16.0.0/12** - Private network addresses
- **192.0.0.0/24** - Private network addresses
- **192.0.2.0/24** - Documentation
- **192.168.0.0/16** - Private network addresses (_very common_)
- **198.18.0.0/15** - Private network addresses
- **198.51.100.0/24** - Documentation
- **203.0.113.0/24** - Documentation
- **233.252.0.0/24** - Documentation
# 8 The Internet Protocol Version 6
- 4 byte addresses can only represent 4,294,967,296 addresses
- IPv6 uses 128 bits 79,228,162,514,264,337,593,543,950,336 addresses
- IPv4 is the most common, but IPv6 will eventually replace it
## 8.1 Representation
- 16 bits, splits into groups of 2 bytes separated by colons
```
2001:0db8:6ffa:8939:163b:4cab:98bf:070a
```
- For subnetting use slash notation like in IPv4
```
2001:0db8:6ffa:8939:163b:4cab:98bf:070a/64
```
- This example has 64 host bits
- Some shortcut rules for such a long string:
	- Leading 0's on any 16 bit number can be removed
	- Runs of multiple 0's after rule 1 can be replace with 2 sequential colons
- Example
```
2001:0db8:6ffa:0000:0000:00ab:98bf:070a
```
Gets reduced to
```
2001:db8:6ffa:0:0:ab:98bf:70a
```
Where the sequential zeroes then turning into `::`
```
2001:db8:6ffa::ab:98bf:70a
```
## 8.2 Link-Local Addresses
- Some addresses are reserved in the LAN like f`e80::/10`
 ```
fe80:0000:0000:0000:0000:0000:0000:0000
 ```
 Where the first 10 bits are the network portion, the next 54 are reserved (0), and the remaining 64 are used to identify hosts
 - When an IPv6 interface is brought up, it computes the link-local address based on the Ethernet Address and other things
 - Link-local addresses are unique to the LAN, but maybe not to the world
 - Routers do not forward link-local packets out of the LAN to prevent these issues
 - An interface might get a different IP later if a DHCP server hands one out, for example, in which case it’ll have two IPs.
## 8.3 Special IPv6 Addresses and Subnets
- `::1` is localhost
- `2001:db8::/32` for documentation
- `fe80::/10` for link-local address
## 8.4  IPv6 and DNS
- IPv6 also works with DNS
- Can use:
```bash
dig page.com AAAA
```
to get the IPv6 record, which is in `ANSWER SECTION`
```
; <<>> DiG 9.10.6 <<>> example.com AAAA
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 13491
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;example.com.            IN    AAAA

;; ANSWER SECTION:
example.com.        81016    IN    AAAA    2606:2800:220:1:248:1893:25c8:1946

;; Query time: 14 msec
;; SERVER: 1.1.1.1#53(1.1.1.1)
;; WHEN: Wed Sep 28 16:05:16 PDT 2022
;; MSG SIZE  rcvd: 68
```
## 8.5 IPv6 and URLs
- IP goes inside of `[]` in order to use the port `:` symbol still:
```
http://[::1]:33490/
```
# 9 Project: A better web server