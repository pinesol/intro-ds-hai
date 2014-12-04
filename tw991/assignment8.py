import numpy as np
import matplotlib.pyplot as plt
from simulation import *


def main():
    """This program simulates each position, plots histogram of daily return and creates a file containing mean and
    standard variance
    """
    position = [1, 10, 100, 1000]
    num_trials = 10000
    result = simulation(position, num_trials)
    f = open('results.txt', 'w')  # open a file to write
    for x in position:
        mean = np.mean(result[str(x)])
        std = np.std(result[str(x)])
        f.write('Position is: '+str(x)+'\n')
        f.write('Mean: '+str(mean)+ '  Std: '+str(std)+'\n')
        f.flush()
        plt.figure()
        plt.hist(result[str(x)], 100, range = [-1, 1])
        plt.savefig('histogram_'+str(x).zfill(4)+'_pos.pdf', format = 'pdf', dpi = 72)
    f.close()

if __name__ == '__main__':
    main()


