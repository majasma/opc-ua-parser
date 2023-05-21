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

    plots = {
    'Level Transmitter, % of capcity': plt.plot(df['Level Transmitter'], color='tab:blue')[0],
    'Gas Temp Sensor, \u00b0C': plt.plot(df['Temperature Gas'], color='tab:red')[0],
    'Liquid Temp Sensor, \u00b0C': plt.plot(df['Temperature Liquid'], color='tab:green')[0],
    'PRV, % of capcity': plt.plot(df['PRV'], color='tab:pink')[0],
    }

    plt.xlabel('Time')

    lines = {
    'BDV on': plt.axvline(x=4, color='purple', linestyle='-'),
    'LS/Drain on': plt.axvline(x=5, color='orange', linestyle='-'),
    'LS/Drain on': plt.axvline(x=12, color='orange', linestyle='-'),
    'LS/Drain on': plt.axvline(x=20, color='orange', linestyle='-'),
    'BDV off': plt.axvline(x=23, color='purple', linestyle='--'),
    'Drain off': plt.axvline(x=11, color='orange', linestyle='--'),
    'Drain off': plt.axvline(x=18, color='orange', linestyle='--'),
    'Drain off': plt.axvline(x=24, color='orange', linestyle='--'),
    }

    unique_labels = {}
    for label, line in lines.items():
        if label not in unique_labels:
            unique_labels[label] = line

    for label, plot in plots.items():
        if label not in unique_labels:
            unique_labels[label] = plot

    plt.legend(unique_labels.values(), unique_labels.keys())
    

    plt.title('BDV Scenario')


    # Show the plot
    plt.show()

def plot_prv(filename):

    # Read CSV file into a DataFrame
    df = pd.read_csv(filename, header=0)
    df.columns = ['Level Transmitter', 'Return Pumps', 'Level Switch', 'BDV', 'PRV', 'Temperature Liquid', 'Temperature Gas', 'Drain' ]
    print(df)
    plt.rc('font', family='serif', size=11)

    plots = {
    'Level Transmitter, % of capcity': plt.plot(df['Level Transmitter'], color='tab:blue')[0],
    'Gas Temp Sensor, \u00b0C': plt.plot(df['Temperature Gas'], color='tab:red')[0],
    'Liquid Temp Sensor, \u00b0C': plt.plot(df['Temperature Liquid'], color='tab:green')[0],
    'PRV, % of capcity': plt.plot(df['PRV'], color='tab:pink')[0],
    }

    plt.xlabel('Time')

    lines = {
    'LS/RP on': plt.axvline(x=0, color='orange', linestyle='-'),
    'LS/RP on': plt.axvline(x=48, color='orange', linestyle='-'),
    'LS off': plt.axvline(x=22, color='orange', linestyle='--'),
    'LS off': plt.axvline(x=49, color='orange', linestyle='--'),
    'RP off': plt.axvline(x=27, color='Purple', linestyle='--'),
    'RP off': plt.axvline(x=57, color='Purple', linestyle='--')
    }

    unique_labels = {}
    for label, line in lines.items():
        if label not in unique_labels:
            unique_labels[label] = line

    for label, plot in plots.items():
        if label not in unique_labels:
            unique_labels[label] = plot

    plt.title("PRV Scenario")
    plt.xlabel('Time')

    plt.legend(unique_labels.values(), unique_labels.keys())


    # Show the plot
    plt.show()

def plot_attack_masked(filename):

    # Read CSV file into a DataFrame
    df = pd.read_csv(filename, header=0)
    df.columns = ['Level Transmitter', 'Return Pumps', 'Level Switch', 'BDV', 'PRV', 'Temperature Liquid', 'Temperature Gas', 'Drain' ]
    print(df)
    plt.rc('font', family='serif', size=11)


    plots = {
    'Level Transmitter, % of capcity': plt.plot(df['Level Transmitter'], color='tab:blue')[0],
    'Gas Temp Sensor, \u00b0C': plt.plot(df['Temperature Gas'], color='tab:red')[0],
    'Liquid Temp Sensor, \u00b0C': plt.plot(df['Temperature Liquid'], color='tab:green')[0],
    'PRV, % of capcity': plt.plot(df['PRV'], color='tab:pink')[0],
    }

    plt.xlabel('Time')

    lines = {
    'LS/RP on': plt.axvline(x=30, color='orange', linestyle='-'),
    'LS off': plt.axvline(x=33, color='orange', linestyle='--'),
    'RP off': plt.axvline(x=61, color='Purple', linestyle='--')
    }

    unique_labels = {}
    for label, line in lines.items():
        if label not in unique_labels:
            unique_labels[label] = line

    for label, plot in plots.items():
        if label not in unique_labels:
            unique_labels[label] = plot




    plt.xlabel('Time')
    plt.legend(unique_labels.values(), unique_labels.keys())

    

    plt.title("Masked Attack Scenario")
    # Show the plot
    plt.show()


def plot_attack_real(filename):

        # Read CSV file into a DataFrame
    df = pd.read_csv(filename, header=0)
    df.columns = ['Level Transmitter', 'Return Pumps', 'Level Switch', 'BDV', 'PRV', 'Temperature Liquid', 'Temperature Gas', 'Drain' ]
    print(df)
    plt.rc('font', family='serif', size=11)


    plots = {
    'Level Transmitter, % of capcity': plt.plot(df['Level Transmitter'], color='tab:blue')[0],
    'Gas Temp Sensor, \u00b0C': plt.plot(df['Temperature Gas'], color='tab:red')[0],
    'Liquid Temp Sensor, \u00b0C': plt.plot(df['Temperature Liquid'], color='tab:green')[0],
    'PRV, % of capcity': plt.plot(df['PRV'], color='tab:pink')[0],
    }

    plt.xlabel('Time')

    lines = {
    'BDV on': plt.axvline(x=29, color='orange', linestyle='-'),
    'LS on': plt.axvline(x=30, color='Purple', linestyle='-')
    }

    unique_labels = {}
    for label, line in lines.items():
        if label not in unique_labels:
            unique_labels[label] = line

    for label, plot in plots.items():
        if label not in unique_labels:
            unique_labels[label] = plot


    plt.xlabel('Time')
    plt.legend(unique_labels.values(), unique_labels.keys())
    plt.title("Real Attack Scenario")

    # Show the plot
    plt.show()


def main():

    #plot_bdv("./test_infrastucture/log_files/BDV_scenario_Level1.csv")
    #plot_prv("./test_infrastucture/log_files/PRV_scenario_Level1.csv")
    #plot_attack_masked("./test_infrastucture/log_files/attack_scenario_masked_Level1.csv")
    plot_attack_real("./test_infrastucture/log_files/attack_real_scenario_Level1.csv")


    return

if __name__ == '__main__':
    main()