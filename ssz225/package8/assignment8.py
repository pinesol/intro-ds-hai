import numpy as np
import matplotlib.pyplot as plt
  
def main():
    #obtain user input for number of shares to buy
    positions_raw = raw_input('Input a list of the number of shares to buy in parallel e.g. [1, 10, 100, 1000]: ')
    positions = [int(x) for x in positions_raw.strip('[]').split(',')]
    num_trials = int(raw_input('Input how many times to randomly repeat the test:'))
    
    #write results in "results.txt"
    results = open('results.txt', 'w')
    #loop through each position through invest function and store mean and standard deviation for each position in results.txt
    for position in positions:
        daily_ret = invest(position, num_trials)
        mean = np.mean(daily_ret)
        standard_deviation = np.std(daily_ret)
        results.write('For position ' + str(position) \
                      + '\n Mean is: ' + str(mean) \
                      + ' Standard Deviation is: ' + str(standard_deviation) + '\n')
        
        #draw histograms for each position
        histogram = plt.figure()
        plt.hist(daily_ret,100,range=[-1,1])
        plt.title('The Histogram of the Result for {} position'.format(position))
        plt.xlabel('Daily Return')
        plt.ylabel('Frequency')
        histogram.savefig('histogram_{}_pos.pdf'.format(str(position).zfill(4)))
    results.close()
    
def invest(positions, num_trials):
    cumu_ret = []
    daily_ret = []
    for trial in range(num_trials):
        position_value = 1000 / positions
        #probabiliy of losing = 0.49 and winning is 0.51
        probability_lose = 0.49
        win = np.random.uniform(0, 1, size = positions) > probability_lose
        #position_value doubles if win
        cumu_ret.append(win.sum() * 2 * position_value)
        #save result of each day to daily_ret
        daily_ret.append((cumu_ret[trial] / float(1000)) - 1)
    return daily_ret
  
if __name__=='__main__':
    main()
