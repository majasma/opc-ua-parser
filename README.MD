# Master Thesis Code Part
This repository contains all code used for planning, implementation and testing. 

## Diagrams
Diagrams are used to illustrate the use case and plan implementation. 
The directory contains:
- Network architecture
- Process drawing
- Process drawing with PLC info lines

## Implementation

## Testing
The test environment is set up using a Python script acting as a OPC-UA server. The server represents the PLC which receives input from the flare system. The client is implemented using UaExpert. Wireshark is used to capture packets. 

How to run the environment:
1. Run python script
2. Connect OPC UA client in UaExpert to url provided in python script
3. Capture packets with wireshark
    1. Open Wireshark and select the network interface that corresponds to the loopback interface on your machine. This interface is typically named "Loopback: lo" or "Loopback: localhost".
    2. In the Wireshark menu, go to "Capture" and then "Options".
    3. In the "Capture Interfaces" window, select the loopback interface and click on "Options".
    4. In the "Interface Options" window, enter **`port 4840`** or **`opcua`** in the "Capture filter" field.

Current issues:
 - [ ] Currently communication is encrypted 
 - [ ] Unsure how to incorporate Ethernet-APL