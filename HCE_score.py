
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl

def HCE_impact_points( beta, delta, gamma,epsilon, D, S, C, E):
    return (beta*D)+(delta*S)+(gamma*C)+(epsilon*E)


def HCE_maximum_impact_points( beta, delta, gamma, epsilon):
    return  (beta*5) +(delta*5) + (gamma*5) + (epsilon*5)

#returns relative severity score in percent
def HCE_severity_score(HCE_name):
    D = int(input("Enter duration score: "))
    S = int(input("Enter safety score: "))
    C = int(input("Enter cost score: "))    
    E = int(input("Enter environment score: ")) 

    IP = HCE_impact_points( beta, delta, gamma, epsilon, D, S, C, E)
    MIP = HCE_maximum_impact_points( beta, delta, gamma, epsilon)

    D_scaled = ((beta*D)/MIP)*100
    S_scaled = ((delta*S)/MIP)*100
    C_scaled = ((gamma*C)/MIP)*100
    E_scaled =  ((epsilon*E)/MIP)*100
    SIP = (IP/MIP)*100 
    return [HCE_name, D_scaled, S_scaled ,C_scaled, E_scaled, SIP]



if __name__ == "__main__":
    beta = int(input("Enter beta (weighting coefficient for duration): "))
    delta = int(input("Enter delta (weighting coefficient for safety): "))
    gamma = int(input("Enter gamma (weighting coefficient for cost): "))
    epsilon = int(input("Enter epsilon (weighting coefficient for environment): "))
    
    HCE_array = []

    while 1:
        HCE_name = input("Enter name of HCE, if finished press 'enter': ")
        
        if HCE_name == "": 
            break

        HCE = HCE_severity_score(HCE_name)
        print(HCE_name, " severity score =", round(HCE[5], 2), "%")
        print('--------------------------------------------------------------')
        HCE_array.append(HCE)

    
    HCE_array = np.array(HCE_array)
    HCE_data = HCE_array[:,:5]
    
   
    df = pd.DataFrame(HCE_data,
				    columns=['HCE', 'Duration', 'Safety','Cost', 'Environment'])
    # view data

    print(df)
    df['Duration']=df['Duration'].astype(float) 
    df['Safety']=df['Safety'].astype(float) 
    df['Cost']=df['Cost'].astype(float) 
    df['Environment']=df['Environment'].astype(float) 

    mpl.rcParams['font.family'] = 'serif'

    # plot data in stack manner of bar type
    ax = df.plot(x= 'HCE', kind='bar', stacked=True, rot=0)
    font = {'family': 'serif', 'size': 11}
    #plt.rc('font', family='serif', size=11)
    ax.set_title('HCE Severity Score Composition', fontdict=font)
    ax.set_ylabel('Severity Score', fontdict=font)

    plt.show()
    
    
