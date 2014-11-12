'''
Created on Nov 11, 2014

@author: ds-ga-1007
'''
import matplotlib.pyplot as plt
import numpy as np
from simulation import *

def main():
    """ 
    Main function that simulate through the position [1,10,100,100] and plot the histograms of daily return.
    The function will simulate 10000 trials for each position to get the results and then store it in a text file.
    """
    file_txt = open('results.txt','w+')
    positions = [1,10,100,1000]
    num_trials = 10000
    
    # Simulate the investment and plot histogram for different positions
    for position in positions:
        daily_ret = simulation(position, num_trials)
        plt.figure()
        plt.hist(daily_ret, 100, range=[-1,1])
        plt.title('The histogram of daily return for position ={}'.format(position))
        plt.xlabel('Daily return')
        plt.ylabel('The number of trials')
        plt.savefig('histogram_{}_pos.pdf'.format(str(position).zfill(4)))
        
        # Save the results of the simulation into a txt file 
        file_txt.write('Position: {}\n'.format(position))
        file_txt.write('Mean: {}; Std: {}\n'.format(np.mean(daily_ret),np.std(daily_ret)))
        file_txt.write('\n')
    file_txt.close() 
    
if __name__ == '__main__':
    main()