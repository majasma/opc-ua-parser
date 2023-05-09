import numpy as np
import pandas as pd
import pyshark
import datetime
import logging

# Note: If tshark uses an ascii encoding to decode packets, filtering will not work. The line
# version_output = subprocess.check_output(parameters, stderr=null).decode("ascii") in tshark.py must therefore be changed to
# version_output = subprocess.check_output(parameters, stderr=null).decode("utf-8")

opcua_filter = '(tcp.port==4840 || tcp.port==4841) && (opcua.transport.type == "MSG") && (opcua.variant.ArraySize == 3 || opcua.Double ) && !(frame.len >= 220) '

# This filter removes all the Temperature Liquid readings
opcua_filter2 = '(tcp.port==4840 || tcp.port==4841) && (opcua.transport.type == "MSG") && (opcua.variant.ArraySize == 3 || opcua.Double ) && !((frame.len == 192) || (frame.len >= 220) || (opcua.security.rqid == 18))'


def pcap_to_opcua(filename, demo=0):
    #filters out to keep only translate requests and read responses
    opc_packets = pyshark.FileCapture(filename, display_filter=opcua_filter2)
    opc_packets.load_packets()
    num_packets = len(opc_packets)
    print(num_packets)

    df = pd.DataFrame(columns=["Level Transmitter","Return Pumps","Level Switch", "BDV", "PRV", "Drain Valve", "Temperature liquids", "Temperature gas"])

    if demo == 1:
        print('demo')

    last_col_idx = -1
    row_idx = 0
    first_column = True

    for i in range(0,num_packets, 2):
        # the translatenode packet
        sensor_name = str(opc_packets[i].opcua.qualname_name.fields[2])

        # Find the indices of the colon and greater than characters
        colon_index = sensor_name.index(": ")
        greater_than_index = sensor_name.index(">")

        # Extract the substring between the colon and greater than characters
        sensor_name = sensor_name[colon_index + 1:greater_than_index].lstrip()

        col_idx = df.columns.get_loc(sensor_name)

        if col_idx > 0:
            first_column = False

        
        if col_idx == last_col_idx + 1:

            df.at[row_idx, sensor_name] = opc_packets[i+1].opcua.double

            last_col_idx = col_idx 
            # Update the last value of name seen
            if (col_idx % 7 == 0 and first_column == False):
                row_idx += 1
                last_col_idx = -1
                first_column = True        
            
            
        else:
            # Insert a None value in the corresponding column
            df.at[row_idx, sensor_name] = np.nan

            logging.warning("%s Missing value, expected state update for %s", datetime.datetime.now().strftime("%H-%M-%S"), df.columns[last_col_idx+1])
            
            # Update the last value of name seen
            last_col_idx = col_idx

            if (col_idx % 7 == 0 and first_column == False):
                row_idx += 1
                last_col_idx = -1
                first_column = True 


        i +=2 

    return df



def compare_df(df1, df2):
    # compare the number of rows of the two dataframes
    if df1.shape[0] > df2.shape[0]:
        # remove the excessive rows from df1
        df1 = df1.head(df2.shape[0])
    elif df2.shape[0] > df1.shape[0]:
        # remove the excessive rows from df2
        df2 = df2.head(df1.shape[0])

    # compare the datasets
    comparison_values = df1.values == df2.values
    rows,cols = np.where(comparison_values==False)

    # output the irregularities
    for row,col in zip(rows,cols):
        df1_loc = df1.iloc[row,col]
        df2_loc = df2.iloc[row,col]
        name = df1.columns[col]
        logging.warning("%s Inconsistent data between levels for state %s values are: %s and %s", datetime.datetime.now().strftime("%H-%M-%S"), repr(name), repr(df1_loc), repr(df2_loc))
        
        #print(f'Data at position ({row+1},{col+1}) is different')
        #print(f'Dataset 1 value: {df1.iloc[row,col]}')
        #print(f'Dataset 2 value: {df2.iloc[row,col]}')


def control_features(df):

    count_1 = 0
    count_2 = 0
    count_3 = 0

    for i in range(len(df.index)):

        if float(df.loc[i]['BDV']) == 1.0 and float(df.loc[i]['PRV']) == 0.0:
            count_1 += 1
            if count_1 == 10:
                logging.warning("%s BDV open and PRV closed, check ESD status", datetime.datetime.now().strftime("%H-%M-%S"))
                count_1 = 0
        
        if float(df.loc[i]['BDV'] == 1) and df.loc[i]['Drain Valve'] == 0.0 and float(df.loc[i]['Return Pumps']) == 0.0 and float(df.loc[i]['Level Transmitter']) >= 50:
            count_2 += 1
            if count_2 == 10:
                logging.warning("%s BDV open while RP/drain closed and level high", datetime.datetime.now().strftime("%H-%M-%S"))
                count_2 = 0

        if float(df.loc[i]['Level Transmitter']) >= 50.0 and float(df.loc[i]['Temperature gas']) <= 20.0:
            count_3 += 1
            if count_3 == 10:
                logging.warning("%s Liquid filling but not large gas flow", datetime.datetime.now().strftime("%H-%M-%S"))
                count_3 = 0

    return

def integrity_check(df1, df2):
    print("-------------------------------------------------")
    print("Check: Packet integrity between levels - STARTED")    
    compare_df(df1, df2)
    print("Check: Packet integrity between levels - COMPLETED")

    return

def content_check(df):
    print("-------------------------------------------------")
    print("Check: State analysis - STARTED")    
    control_features(df)
    print("Check: State analysis - COMPLETED")

    return


def main():

    # Initialize logging
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # set up the logging module with a file handler
    logging.basicConfig(filename=f"log_files/log_{timestamp}.txt", level=logging.INFO)
    logging.info("Started script")

    #------------------- PROCESS PCAPS -------------------------
    print("Processing pcap files - STARTED")
    df1 = pcap_to_opcua('../pcaps/BDV_Level1.pcapng', 1)
    #df2 = pcap_to_opcua('../pcaps/PRV_Level0.pcapng', opcua_filter)
    print("Processing pcap files - COMPLETED")

    #print("------------------ PACKAGE LOSS DEMO ----------------")
    #df1 = pcap_to_opcua('./pcaps/BDV_Level1.pcapng')
    
    #integrity_check(df1, df2)
    #content_check(df1)

    return


if __name__ == '__main__':
    main()

