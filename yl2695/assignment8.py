import numpy as np
from simulation import *
import matplotlib.pyplot as plt


def main():
    '''
    Main function of the simulation. The positions is [1, 10, 100, 1000] and the number of trials is 10000
    '''
    positions = [1, 10, 100, 1000]
    num_trials = 10000

    # simulate the different investment.
    investResult = simulation(positions, num_trials)

    # plot histogram for different position
    for position in positions:
        plt.figure()
        plt.hist(investResult[position], 100, range=[-1.0, 1.0], color='red')
        plt.xlabel('Daily Ret')
        plt.ylabel('Numbers')
        plt.title("Histogram of position-{}'s daily ret".format(position))
        plt.savefig('histogram_{}_pos.pdf'.format(str(position).zfill(4)))

    # set up a file called 'result.txt' and save the mean and std of different position
    f = open('result.txt', 'w')
    f.write('position' + '\t' + 'mean' + '\t' + 'std' + '\n')
    for position in positions:
        f.write(str(position) + '\t' + str(np.array(investResult[position]).mean()) + '\t' + str(np.array(investResult[position]).std()) + '\n')
    f.close()


if __name__ == '__main__':
    main()
