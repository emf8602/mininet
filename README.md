# Mininet 
In a tool called mininet, you will design subnets that satisfy specified requirements. There are three routers A, B, and C, each of which is connected to two hosts. Also, the three routers themselves are connected to each other with IP addresses 20.10.100.0/24. You need to design subnets (LAN A, B, and C) that connect the two hosts to each router.

## How to Install Dependencies
All the dependencies added were related to Mininet so if you are within the correct virtual box, no additional dependencies are needed.

## How to Run
Detailed below is how to run the custom network.

### Assumptions
This was all tested using `mininet-2.3.0-210211-ubuntu-20.04.1-legacy-server-amd64` on Oracle VirtualBox.  
While I think this would work on other VM Software, that is what I used.

### Execution
First, run run the Mininet Ubuntu Virtual Machine  
Login with username:`mininet`, password:`mininet`  
Copy layer3_network_code.py into the VM  
- I did this by just copying layer3_network_code.py's text and pasting it into a new file on the VM.
- But however you get the code into the VM is fine (scp was giving me issues).

Now run the file with 
```cmd 
$ sudo python layer3_network_code.py
```

Once all the set-up of the network finishes the Mininet CLI executes.  
Here you can run your own commands like `pingall`

## Examples of command-line usage
Detailed below is the command-line input and expected output.  
While in the folder with the layer3_network_code.py code 
```cmd
$ sudo python layer3_network_code.py
```
**Output before Task 3:**
```cmd
*** Adding routers
*** Adding LAN hosts
*** Creating switches
*** Connecting LANs to routers
*** Connecting routers to each other
*** Creating network
*** Adding controller
*** Adding hosts:
hA1 hA2 hB1 hB2 hC1 hC2 rA rB rC
*** Adding switches:
s1 s2 s3
*** Adding links:
(hA1, s1) (hA2, s1) (hB1, s2) (hB2, s2) (hC1, s3) (hC2, s3) (rA, rB) (rA, s1) (rB, rC) (rB, s2) (rC, rA) (rC, s3)
*** Configuring hosts
hA1 hA2 hB1 hB2 hC1 hC2 rA rB rC
*** Starting Network
*** Starting controller
c0
*** Starting 3 switches
s1 s2 s3 ...
*** Waiting for switches to connect
s1 s2 s3
*** Assigning IPs

--- Testing LAN A ---
hA1 -> hA2
hA2 -> hA1
*** Results: 0% dropped (2/2 received)

--- Testing LAN B ---
hB1 -> hB2
hB2 -> hB1
*** Results: 0% dropped (2/2 received)

--- Testing LAN C ---
hC1 -> hC2
hC2 -> hC1
*** Results: 0% dropped (2/2 received)
*** Opening Mininet CLI
*** Starting CLI:
```
The network has been set up as per the requirements and we see that hosts can talk to the other hosts within their LAN. 

Now we get access to the Mininet CLI.
To test that the hosts to talk to the hosts in their subnet and not outside of it, we run pingall.
```cmd
$ pingall
```
```
*** Ping: testing ping reachability
hA1 -> hA2 X X X X rA X X
hA2 -> hA1 X X X X rA X X
hB1 -> X X hB2 X X X rB X
hB2 -> X X hB1 X X X rB X
hC1 -> X X X X hC2 X X rC
hC2 -> X X X X hC1 X X rC
rA -> hA1 hA2 X X X X X X
rB -> X X hB1 hB2 X X X X
rC -> X X X X hC1 hC2 X X
*** Results: 75% dropped (18/72 received)
```
The Xs indicate that it was unable to ping.  
We see that the hosts are unable to ping outside their LAN and routers are only able to talk to their 2 hosts.

**Output after Task 3:**

Note that we will use the command tracepath rather than traceroute