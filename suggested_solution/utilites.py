import pandas as pd
import numpy as np 
import pstats

def results_processing(filename):

    df = pd.read_csv(filename)
    print(df.columns)
    df['var_diff'] = ((df['var1'] + df['var2'])/2)


    # define the list of possible names
    names = ['Level Transmitter', 'Return Pumps', 'Level Switch', 'BDV', 'PRV', 'Drain Valve', 'Temperature liquids', 'Temperature gas']

    # initialize a dictionary to store the results
    results = {}

    # loop through the possible names
    for name in names:
        # filter the dataframe for the current name
        name_df = df[df['name'] == name]
        name_df.columns = ['name', 'var1', 'var2', 'delta', 'var_diff']
        
        # calculate the number of occurrences of the current name
        count = len(name_df)
        
        # calculate the minimum, maximum, and average delta for the current name
        delta_min = name_df['delta'].min()
        delta_max = name_df['delta'].max()
        delta_avg = name_df['delta'].mean()
        variance = name_df['var_diff'].var()
        

        print(name, ': count ', count, 'delta_min ', delta_min, '%', 'delta_max ', delta_max, '%', 'delta_avg ', round(delta_avg,2), '%', 'variance', round(variance,2))
        
        # add the results to the dictionary
        results[name] = {'count': count, 'delta_min': delta_min, 'delta_max': delta_max, 'delta_avg': delta_avg, 'variance': variance}

    # create a new dataframe from the results dictionary
    table_df = pd.DataFrame(results).transpose()

    # format the delta columns to have 2 decimal places
    table_df['delta_min'] = table_df['delta_min'].apply(lambda x: '{:.2f}'.format(x))
    table_df['delta_max'] = table_df['delta_max'].apply(lambda x: '{:.2f}'.format(x))
    table_df['delta_avg'] = table_df['delta_avg'].apply(lambda x: '{:.2f}'.format(x))

    # set the index name
    table_df = table_df.rename_axis('Name')

    # create a LaTeX table string 
    table_str = table_df.to_latex(column_format='lccc')

    # print the LaTeX table string
    print(table_str)


    return

def read_analysis(filename):
    p = pstats.Stats(filename)
    p.sort_stats('cumulative').print_stats(10)

def main():

    #results_processing('./data_inconsistensies_attack.csv')
    read_analysis('./runtime_analysis.txt')

    return 

if __name__ == '__main__':
    main()