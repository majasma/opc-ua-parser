import numpy as np
import pandas as pd
import pyshark
    
def pcap_to_opcua(filename):
    opc_packets = pyshark.FileCapture(filename, display_filter='opcua')

    return opc_packets

def pcap_to_state(filename):
    opc_read_response = pyshark.FileCapture(filename, display_filter='opcua.transport.type == "MSG" && ( opcua.Double  || opcua.Boolean)')
    opc_read_response.load_packets()
    
    
    num_packets = len(opc_read_response)
    
    data_arr = []
    for pkt in opc_read_response:
        data_arr.append(float(pkt.opcua.double))

    df = pd.DataFrame(columns=["Level Transmitter","Return Pumps","Level Switch", "BDV", "PRV", "Drain Valve", "Temperature liquids", "Temperature gas"])

    # TODO - remove, only under dev: make the array divisible by 8 by cutting excess
    num_elements = len(data_arr) - (len(data_arr) % 8)
    data_arr = data_arr[:num_elements]


    for i in range(0, num_packets, 8):
        df.loc[i//8] = data_arr[i:i+8]

    return df


def compare_df(df1, df2):
    # compare the datasets
    comparison_values = df1.values == df2.values
    rows,cols = np.where(comparison_values==False)

    # output the irregularities
    for row,col in zip(rows,cols):
        print(f'Data at position ({row+1},{col+1}) is different')
        print(f'Dataset 1 value: {df1.iloc[row,col]}')
        print(f'Dataset 2 value: {df2.iloc[row,col]}')


def control_features(df):

    for i in df.index:
        if df['BDV'][i] == 1.0 and df['PRV'][i] == 0.0:
            print('BDV open and PRV closed, check ESD status')
        
        if df['BDV'][i] == 1 and df['Drain Valve'][i] == 0.0 and df['Return Pumps'][i] == 0.0 and df['Level Transmitter'][i] >= 50:
            print('BDV open while RP/drain closed and level high')

        if df['Level Transmitter'][i] >= 50.0 and df['Temperature gas'][i] <= 20.0:
            print('Liquid filling but not large gas flow')

    return

def control_communications(cap1, cap2):

    cap1.load_packets()
    cap2.load_packets()

    if len(cap1) != (len(cap2)+1):
        print("Mismatch length between capture 1 and 2")
    

    return

def main():

    #------------------- PROCESS PCAPS -------------------------
    df = pcap_to_state('pcaps/BDV_short.pcapng')
    opc_packets = pcap_to_opcua('pcaps/BDV_short.pcapng')

    #--------------------- CHECK PCAPS -------------------------
    control_communications(opc_packets, opc_packets)
    print("------------------------------------------------")


    #-----------------------------------------------------------
    # TODO - remove, only for dev
    df_copy = df.copy()
    df_copy.iat[1, 1] = 10.0
    #print(df, df_copy)
    
    #--------------- RUN STATE COMPARISONS ----------------------
    compare_df(df, df_copy)
    print("-------------------------------------------------")
    

    #------------------- FEATURE CHECKS -------------------------
    control_features(df)

    return


if __name__ == '__main__':
    main()

# 1 Process pcaps
#  1.1 load files                            - DONE
#  1.2 remove tcp/ip header                  - problems
#  1.3 parse opcua protocol                  - DONE
#  1.4 copy state values to separate dataset - DONE

# 2 Compare PCAPs
#  2.1 compare number of polls               - DONE
#  2.2 compare number of messages per poll   - IF THIS IS NOT TRUE, I THINK THE CODE WILL CRASH: problems 
#  2.3 compare values of states              - DONE

# 3 Check selected feature conditions
#  3.1 iterate dataset                       - DONE
#  3.2 check conditions                      - STARTED