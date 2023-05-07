import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


def plot_bdv(filename):

    # Read CSV file into a DataFrame
    df = pd.read_csv(filename, header=0)
    df.columns = ['Level Transmitter', 'Return Pumps', 'Level Switch', 'BDV', 'PRV', 'Temperature Liquid', 'Temperature Gas', 'Drain' ]
    print(df)




    # Specify the font family and size
    plt.rc('font', family='serif', size=11)

    #axs[0].plot(y=df['Level Transmitter','Temperature Gas', 'Temperature Liquid'])
    plt.plot(df['Level Transmitter'], label='Level Transmitter, % of capcity', color='tab:blue')
    plt.plot(df['Temperature Gas'], label='Gas Temp Sensor, C', color='tab:red')
    plt.plot(df['Temperature Liquid'], label='Liquid Temp Sensor, C', color='tab:green')
    plt.plot(df['PRV'], label='PRV, % of capcity', color='tab:pink')

    plt.xlabel('Time')
    
    
    plt.axvline(x=10, color='black', linestyle='-', label='Drain on')
    plt.axvline(x=18, color='purple', linestyle='-', label='BDV off')
    plt.axvline(x=21, color='grey', linestyle='-', label='Drain off')
    plt.axvline(x=18.1, color='orange', linestyle='-', label='LS off')

    plt.title('BDV Scenario')
    plt.legend()

    # Show the plot
    plt.show()

def plot_prv(filename):

    # Read CSV file into a DataFrame
    df = pd.read_csv(filename, header=0)
    df.columns = ['Level Transmitter', 'Return Pumps', 'Level Switch', 'BDV', 'PRV', 'Temperature Liquid', 'Temperature Gas', 'Drain' ]
    print(df)
    plt.rc('font', family='serif', size=11)

    #axs[0].plot(y=df['Level Transmitter','Temperature Gas', 'Temperature Liquid'])
    plt.plot(df['Level Transmitter'], label='Level Transmitter, % of capcity', color='tab:blue')
    plt.plot(df['Temperature Gas'], label='Temperature Gas, \u00b0C', color='tab:red')
    plt.plot(df['Temperature Liquid'], label='Temperature Liquid, \u00b0C', color='tab:green')
    plt.plot(df['PRV'], label='PRV, % of capcity', color='tab:pink')

    plt.axvline(x=6, color='orange', linestyle='-', label='RP on')
    plt.axvline(x=30, color='indigo', linestyle='-', label='RP off')
    plt.axvline(x=6.1, color='yellow', linestyle='-', label='LS on')
    plt.axvline(x=8, color='grey', linestyle='-', label='LS off')

    plt.title("PRV Scenario")
    plt.xlabel('Time')
    plt.legend()


    # Show the plot
    plt.show()

def plot_attack_masked(filename):

    # Read CSV file into a DataFrame
    df = pd.read_csv(filename, header=0)
    df.columns = ['Level Transmitter', 'Return Pumps', 'Level Switch', 'BDV', 'PRV', 'Temperature Liquid', 'Temperature Gas', 'Drain' ]
    print(df)
    plt.rc('font', family='serif', size=11)



    #axs[0].plot(y=df['Level Transmitter','Temperature Gas', 'Temperature Liquid'])
    plt.plot(df['Level Transmitter'], label='Level Transmitter', color='tab:blue')
    plt.plot(df['Temperature Gas'], label='Temperature Gas', color='tab:red')
    plt.plot(df['Temperature Liquid'], label='Temperature Liquid', color='tab:green')
    plt.plot(df['PRV'], label='PRV', color='tab:pink')

    plt.axvline(x=70, color='orange', linestyle='-', label='RP on')
    plt.axvline(x=123, color='indigo', linestyle='-', label='RP off')


    plt.xlabel('Time')
    plt.legend()

    

    plt.title("Masked Attack Scenario")
    # Show the plot
    plt.show()


def plot_attack_real(filename, filename2):

    # Read CSV file into a DataFrame
    df1 = pd.read_csv(filename, header=0)
    df1.columns = ['PRV', 'Temperature Liquid', 'Temperature Gas', 'Drain' ]

    df2 = pd.read_csv(filename2, header=0)
    df2.columns = ['Level Transmitter', 'Return Pumps', 'Level Switch', 'BDV']
    print(df1)
    print(df2) 


    #axs[0].plot(y=df['Level Transmitter','Temperature Gas', 'Temperature Liquid'])
    plt.plot(df2['Level Transmitter'], label='Level Transmitter, % of capcity', color='tab:blue')
    plt.plot(df1['Temperature Gas'], label='Temperature Gas, \u00b0C', color='tab:red')
    plt.plot(df1['Temperature Liquid'], label='Temperature Liquid, \u00b0C', color='tab:green')
    plt.plot(df1['PRV'], label='PRV, % of capcity', color='tab:pink')

    plt.axvline(x=0, color='purple', linestyle='-', label='BDV on')
    plt.axvline(x=6.1, color='orange', linestyle='-', label='LS on')
    plt.rc('font', family='serif', size=11)
    plt.xlabel('Time')
    plt.title("Real Attack Scenario")
    plt.legend()

    # Show the plot
    plt.show()


def main():

    #plot_bdv("./test_infrastucture/log_files/BDV_scenario_Level1.csv")
    #plot_prv("./test_infrastucture/log_files/PRV_scenario_Level1.csv")
    plot_attack_masked("./test_infrastucture/log_files/attack_scenario_masked_Level1.csv")


    #plot_attack_real("./test_infrastucture/log_files/attack_scenario_Level0_1.csv", "./test_infrastucture/log_files/attack_scenario_Level0_2.csv")


    return

if __name__ == '__main__':
    main()