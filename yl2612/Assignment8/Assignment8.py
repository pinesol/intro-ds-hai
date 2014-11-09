from simulation import simulation
import matplotlib.pyplot as plt
import numpy as np

def main():
    '''This program stimulates each position, plot the results, store the means and standard deviations in a text file.'''
    position = [1, 10, 100, 1000]
    num_trials = 10000
    results = open('results.txt','w') #open a file to store mean and standard deviation
    
    for position in position:
        daily_ret = simulation(position, num_trials)
        plt.figure()
        plt.hist(daily_ret, 100, range=[-1, 1])
        plt.xlim(-1,1)
        plt.xlabel('Daily Return')
        plt.ylabel('Frequency in Number')
        plt.title('Daily Return of Position{}'.format(position))
        plt.savefig('histogram_{}_pos.pdf'.format(str(position).zfill(4)))
        
        mean = np.mean(daily_ret)
        std = np.std(daily_ret)
        results.write('Position: ' + str(position) + '\n')
        results.write('Mean: ' + str(mean) + '\n')
        results.write('Standard Deviation: ' + str(std) + '\n')
        
    results.close()

if __name__ == '__main__':
    main()
