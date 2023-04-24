import pandas as pd
import matplotlib.pyplot as plt

def plot_csv(filename):

    # Read CSV file into a DataFrame
    df = pd.read_csv(filename, header=0)
    df.columns = ['Level Transmitter', 'Return Pumps', 'Level Switch', 'BDV', 'PRV', 'Temperature Liquid', 'Temperature Gas', 'Drain' ]
    print(df)

    # Create the first subplot for Level Transmitter, Temperature Gas and Temperature Liquid
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))

    #axs[0].plot(y=df['Level Transmitter','Temperature Gas', 'Temperature Liquid'])
    axs[0].plot(df['Level Transmitter'], label='Level Transmitter', color='tab:blue')
    axs[0].plot(df['Temperature Gas'], label='Temperature Gas', color='tab:red')
    axs[0].plot(df['Temperature Liquid'], label='Temperature Liquid', color='tab:green')

    axs[0].set_xlabel('Time')
    axs[0].legend()

    # Create the second subplot for the remaining columns
    axs[1].plot(df['Return Pumps'], label='Return Pumps', color='tab:orange')
    axs[1].plot(df['Level Switch'], label='Level Switch', color='tab:purple')
    axs[1].plot(df['BDV'], label='BDV', color='tab:brown')
    axs[1].plot(df['PRV'], label='PRV', color='tab:pink')
    axs[1].plot(df['Drain'], label='Drain', color='tab:gray')

    axs[1].set_xlabel('Time')
    axs[1].legend()

    # Adjust spacing between subplots
    fig.subplots_adjust(hspace=0.4)

    # Show the plot
    plt.show()


def main():
    plot_csv("test_scenarios/log_files/BDV_scenario.csv")
    plot_csv("PRV_scenario.csv")
    plot_csv("attack_real_scenario.csv")
    plot_csv("attack_masked_scenario.csv")
    return

if __name__ == '__main__':
    main()