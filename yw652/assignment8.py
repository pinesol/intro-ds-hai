import numpy as np
import matplotlib.pyplot as plt
from simulation import *

def main():
    positions = [1,10,100,1000]
    num_trial = 10000
    return_list = simulation(positions, num_trial)

    outputF = open('result.txt', 'w')
    for i in range(len(return_list)):
        mean = np.mean(return_list[i])
        std = np.std(return_list[i])
        outputF.write("Position is " + str(positions[i]) + '\n')
        outputF.write("The mean of the return is " + str(mean)+ ', ' + "and the standard deviation is " + str(std)+"\n")
        outputF.flush()
        plt.hist(return_list[i], 100, range=[-1,1])

        plt.show()

if __name__ == "__main__":
    main()

