# Title: Synthesised flare system data
**DOI:** <br />
**Contact information:** Maja Simons Markusson, maja.markusson@gmail.com <br />
**Licensing:** This dataset is dedicated to the public domain.

This dataset was created to test an OPC-UA parser implemented in a master thesis project. It contains six packet capture next-generation files with OPC-UA traffic. The traffic is captured on the loopback interface using Wireshark. The state_references folder contains ten csv files with state references for the different nodes. The source code used to create the dataset and directions on how to do it is hosted on https://github.com/majasma/opc-ua-parser.

## Method:

The dataset is produced by several Python scripts representing different use case scenarios in a flare system. The system comprises eight sensors/actuators (Level 0) that sends readings to a PLC (Level 1). The PLC then forwards the readings to an HMI (Level 2). OPC-UA communication with client/server structure is used to communicate between levels.

For every other second in the test scenarios, the "OPC-UA server" writes values for the "OPC-UA client" to read. On level 0, the sensors are parted into two groups. This illustrates that a client would have to interact with several servers, but scaling it up to eight was unnecessary. Consequently, there are two different CSV files for each level 0 scenario. 

The states included in the datasets are: 'Level Transmitter [% of full  knock-out drum capacity]', 'Return Pumps[True/False]', 'Level Switch[True/False]', 'BDV[True/False]', 'PRV [% of full valve capacity]', 'Drain Valve [True/False]', 'Temperature liquids [degrees Celsius]', 'Temperature gas [degrees Celsius]'

**About the scenarios:**<br />
PRV: The PRV scenario comprises two parts. The end case where the level switch is not activated, but liquids are manually evaporated is not included. One illustrates the system behavior in the case of a considerable relief and one of a smaller relief. In the case of significant relief, the PRV is modeled to have a dynamic opening between 40-55%. This causes the level transmitter readings to increase. Following the large flow of gas to the flare, the temperature over the gas temperature sensor falls. When the level transmitter increases above the threshold, set to 10, the level switch turns on, and the return pumps open. After 180 seconds, the simulated large relief is over, and the PRV closes. The closing of the valve shuts off the gas flow, which in turn increases the temperature to normal. When the return pump is open, the tank level decreases. Once under 10, the level switch is turned off. The large relief scenario is terminated when the PRV is closed and the knock-out drum is empty (LT = 0). 

The termination of the large relief scenario initiates the small relief scenario. The goal is to illustrate the case where the PRV is opened slightly, and the level of the tank is also barely increased above the level switch threshold. For the 50 seconds, the PRV is opened in a dynamic interval between 3-5%. The level is only momentarily above 10 \% of tank capacity, but the return pumps are activated to empty the tank. The scenario is terminated when the PRV is turned off, the tank is empty, and the temperature sensor at the bottom of the tank returns to normal system temperature. 

BDV: The BDV scenario covers a process- or emergency-shutdown use case. The BDV is opened fully and releases gas and liquids into the system for 40 seconds. The large flow of gas and liquids decreases the temperature over the gas temperature sensor and increases the tank level. As the level increases above the threshold, the level switch is turned high. Given the prerequisite that the system performs an ESD/PSD, the drain system is turned on instead of the return pumps, like in the PRV scenario. This causes the level to decrease and the gas temperature to increase. The scenario is terminated when the BDV is turned off, and the tank is empty.

Attack: Producing the datasets for the attack scenario is more complex. In the former examples, the communication between sensors and PLC will be identical to that between the PLC and the HMI. As the attacker seeks to mask the attack by replaying old process measurements, the communication between levels will not be identical. Two separate scripts are implemented to represent this. The actual attack is a simple scenario to model. First, BDV is set to open, rapidly increasing the tank level. Simultaneously, the temperature over the gas temperature sensor decreases due to the large gas flow. The level switch measures the high level, but the return pumps or drain system is not activated. When the level transmitter reaches 100% (full capacity), the value is continuously repeated as the sensor cannot measure the amount of overflow. The overflow is set to occur after polls, corresponding to 92 seconds. The second is the communication received by the HMI - the masked traffic. As the increased gas flow will be visible on the CCTV camera system, it is favourable to pretend a minor relief occurs. Therefore, the server writes values for the PRV and level transmitter according to a sine curve alternating between 0 and 2. Previously recorded records would have been used as a replay attack in an actual attack. After one minute, the values for the level switch are written high, and the return pump value is written true. The server then goes on writing as if the level in the tank was decreasing. 

The ESD status of the facility is not taken into consideration. The data is intended to be used for pattern-matching tests. The sample size is not sufficient to perform machine learning techniques.


## Data- and file overview: 
- state_references
  - attack_scenario_Level0_1.csv
  - attack_scenario_Level0_2.csv
  - attack_scenario_masked_Level1.csv
  - attack_scenario_real_Level1.csv
  - BDV_scenario_Level0_1.csv
  - BDV_scenario_Level0_2.csv
  - BDV_scenario_Level1.csv
  - PRV_scenario_level0_1.csv
  - PRV_scenario_level0_2.csv
  - PRV_scenario_Level1.csv
- attack_scenario_masked.pcapng
- attack_scenario_real.pcapng
- BDV_scenario_Level0.pcapng
- BDV_scenario_Level1.pcapng
- PRV_scenario_Level0.pcapng
- PRV_scenario_Level1.pcapng
- README.md

### File specific information:
- state_references
  - attack_scenario_Level0_1.csv: Sensor states for sensor node 1, level 0, real attack scenario
  - attack_scenario_Level0_2.csv: Sensor states for sensor node 2, level 0, real attack scenario
  - attack_scenario_masked_Level1.csv: States for all sensors, level 1, masked attack scenario
  - attack_scenario_real_Level1.csv: States for all sensors, level 1, real attack scenario
  - BDV_scenario_Level0_1.csv: Sensor states for sensor node 1, level 0, BDV scenario
  - BDV_scenario_Level0_2.csv: Sensor states for sensor node 2, level 0, BDV scenario
  - BDV_scenario_Level1.csv: States for all sensors, level 1, BDV scenario
  - PRV_scenario_level0_1.csv: Sensor states for sensor node 1, level 0, BDV scenario
  - PRV_scenario_level0_2.csv: Sensor states for sensor node 2, level 0, BDV scenario
  - PRV_scenario_Level1.csv: States for all sensors, level 1, PRV scenario
- attack_scenario_masked.pcapng: Communication traffic from loopback interface, port 4840, masked attack scenario
- attack_scenario_real.pcapng: Communication traffic from loopback interface, ports 4840 and 4841, real attack scenario
- BDV_scenario_Level0.pcapng: Communication traffic from loopback interface, ports 4840 and 4841, BDV scenario
- BDV_scenario_Level1.pcapng: Communication traffic from loopback interface, port 4840, BDV scenario
- PRV_scenario_Level0.pcapng: Communication traffic from loopback interface, ports 4840 and 4841, PRV scenario
- PRV_scenario_Level1.pcapng: Communication traffic from loopback interface, port 4840, PRV scenario
- README.md: dataset decription




