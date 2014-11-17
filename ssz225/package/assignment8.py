import matplotlib.pyplot as plt
from package.invest import *
import sys
from package.exceptions import *
"""This program is to simulate an investment instrument with the following properties:
    Can purchase in $1, $10, $100, and $1000 denominations
    Holding time is one day
    51% of the time return is 1.0 (value doubles)
    49% of the time return is 1.0 (all value is lost)
    Investor is given $1000 to invest.
    
    Program takes two user inputs:
        positions_raw = list of number of shares to buy in parallel
        trials = how many times to randomly repeat the test
    Program produces:
        results.txt containing mean and standard deviation of daily return simulations for each position input
        Historgram histogram_POSITION_pos.pdf for each position input"""
        
def main():
    while True:
        try:
            #obtain user input for number of shares to buy in parallel given $1000
            positions_raw = raw_input('Input a list of the number of shares to buy in parallel e.g. [1, 10, 100, 1000]: ')
        #quit program if user inputs ^C
        except KeyboardInterrupt:
            print 'KeyboardInterrupt. Bye!'
            sys.exit()
        #quit program if user inputs 'quit' in any letter case
        if positions_raw.lower() == 'quit':
            print 'Quitting. Bye!'
            sys.exit()
        else:
            try:
                #check if user input is in valid format of [int, int, ...] where int = 1, 10, 100, or 1000'
                positions = isValidPositionsInput(positions_raw)
                break
            except InvalidListError:
                print 'Invalid positions list, must be in [int, int, ...] format where int = 1, 10, 100, or 1000'
                
    while True: 
        try:  
            #obtain user input for number of simulations of first day investments   
            input_num_trials = raw_input('Input how many times to randomly repeat the test:')
        #quit program if user inputs %C
        except KeyboardInterrupt:
            print 'KeyboardInterrupt. Bye!'
            sys.exit()
        #quit program if user inputs 'quit' in any letter case
        if input_num_trials.lower() == 'quit':
            print 'Quitting. Bye!'
            sys.exit()
        else:
            try: 
                #check if user input is an integer
                num_trials = checkTrialsValidity(input_num_trials)
                break
            except InvalidTrialsError:
                print 'Invalid Trials. Must input an integer.'
                
    results = open('results.txt', 'w')
    results.write('List of number of shares to buy in parallel: {} \n'.format(positions_raw) \
                  + 'Times test is repeated: {} \n'.format(num_trials))
    
    #loop through each position through invest function and store mean and standard deviation for each position in results.txt
    for position in positions:
        daily_ret = invest(position, num_trials)
        daily_ret_mean = np.mean(daily_ret)
        daily_ret_std = np.std(daily_ret)
        results.write('For position ' + str(position) \
                      + '\n Mean is: ' + str(daily_ret_mean) \
                      + ' Standard Deviation is: ' + str(daily_ret_std) + '\n')
         
        #draw histograms of daily return for each position
        histogram = plt.figure()
        plt.hist(daily_ret,100,range=[-1,1])
        plt.title('The Histogram of the Result for {} position'.format(position))
        plt.xlabel('Daily Return')
        plt.ylabel('Frequency')
        histogram.savefig('histogram_{}_pos.pdf'.format(str(position).zfill(4)))
    results.close()
    
if __name__=='__main__':
    main()