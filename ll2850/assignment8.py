__author__ = 'leilu'
import numpy as np
import matplotlib.pyplot as plt
from package.simulation import *

def main():
    '''
    main function will carry out the investment function, taking argument that positions = [1,10,100,1000] and num_trails = 10000
    The result daily_return is a list contain 4 sub-lists where each sub-list contains 10000 floats.
    '''
    positions = [1, 10, 100, 1000]
    num_trials = 10000
    daily_return = investment(positions, num_trials)
    f = open('results.txt', 'w')
    # open a file to write numerical results
    for i in range(len(daily_return)):
    #start a loop to describe results for each position
        mean = np.mean(daily_return[i])
        std = np.std(daily_return[i])
        f.write('When position is '+str(10**i)+ ':' + '\n')
        f.write('mean average daily return is: '+str(mean)+ '  and the standard deviation: '+str(std)+'\n')
        f.flush()
        plt.figure()
        plt.hist(daily_return[i], 100, range = [-1, 1])
        plt.savefig('histogram_'+str(10**i).zfill(4)+'_pos.pdf', format = 'pdf', dpi = 72)
    f.close()

if __name__ == '__main__':
    main()
