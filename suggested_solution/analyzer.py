import numpy as np
import pandas as pd
import pyshark

def test_pyshark():

    return
    


def process_pcaps(filename):
    opc_packets = pyshark.FileCapture(filename, display_filter='opcua')
    opc_read_response = pyshark.FileCapture(filename, display_filter='opcua.transport.type == "MSG" && ( opcua.Double  || opcua.Boolean)')
    num_packets = len([packet for packet in opc_read_response])
    
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

def main():

    df = process_pcaps('pcaps/BDV_short.pcapng')

    # TODO - remove, only for dev
    df_copy = df.copy()
    df_copy.iat[1, 1] = 10.0
    #print(df, df_copy)
    
    #--------------- RUN STATE COMPARISONS ----------------------
    compare_df(df, df_copy)

    return


if __name__ == '__main__':
    main()

# 1 Process pcaps
#  1.1 load files                            - DONE
#  1.2 remove tcp/ip header
#  1.3 parse opcua protocol                  - DONE
#  1.4 copy state values to separate dataset - DONE

# 2 Compare PCAPs
#  2.1 compare number of polls               - CHECK IF NUMBER OF ROWS EQUAL
#  2.2 compare number of messages per poll   - IF THIS IS NOT TRUE, I THINK THE CODE WILL CRASH   
#  2.3 compare values of states              - DONE

# 3 Check selected feature conditions
#  3.1 iterate dataset 
#  3.2 check conditions