import investment
import matplotlib.pyplot as plt
import numpy as np

def main():
    #take user input for a list of the number of shares to buy and put them into a list
    positions_input = raw_input('a list of the number of shares to buy in parallel: e.g. [1, 10, 100, 1000]? ')
    positions = [int(x) for x in positions_input.strip('[]').split(',')]
    #take user input for the number of times to repeat the test
    num_trials = int(raw_input('how many times to repeat the test?'))

    #open a file to write
    results = open('results.txt', 'w')
    for position in positions:
        daily_ret = investment.investment(position, num_trials)
        mean = np.mean(daily_ret)
        std = np.std(daily_ret)
        results.write('Position is: '+ str(position) + '\n')
        results.write('Mean: '+ str(mean) + ' Std: '+ str(std) + '\n')
        
        #plot a histogram with x = [-1, 1] and y as the number of trials
        p = plt.figure()
        plt.hist(daily_ret, 100, range = [-1, 1])
        plt.title('Histogram of Daily Return with Position {}'.format(position))
        plt.xlabel('Daily Return')
        p.savefig('histogram_{}_pos.pdf'.format(str(position).zfill(4)))	

    results.close()

if __name__ == '__main__':
    main()
        