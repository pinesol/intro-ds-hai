import pandas as ps
import numpy as np
import sys
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 8, 6


def investment(positions, num_trials):
    position_value = 1000/np.array(positions)
    daily_mean = np.zeros(len(positions))
    daily_std = np.zeros(len(positions))
    
    #progress bar
    steps = num_trials/10

    with open('results.txt', 'w') as f:
        #loop over different positions
        for i, pos in enumerate(positions):
            cumu_ret = np.zeros(num_trials)
            print '\b.',
            sys.stdout.flush()

            # simulare returns for num_trials number of days
            for trial in xrange(num_trials):
                
                flip_results = coinFlip(pos)
                
                investment = position_value[i]
                
                returns = profits(investment, flip_results)
                
                cumu_ret[trial] = returns
            
            # normalize and graph a histogram
            daily_ret = (cumu_ret/1000)-1
            generateGraph(daily_ret, num_trials, pos)
            
            #calculate daily statistics
            daily_mean[i] = daily_ret.mean()
            daily_std[i] = daily_ret.std()
    
            
            #write statistics to file
            f.write('Statistics for normalized daily returns for %s days \n with %s parallel investments per day \n' %(num_trials,pos))
            f.write("mean: %s \n" %daily_ret.mean())
            f.write("standard deviation %s \n" %daily_ret.std())
            f.write("\n")
            
        print '\b]  Done!',   
    return #end of investment()

''' flips a biased coin num_investments # of times.
returns array of 1s and 0s determining where 1 is a successful flip'''
def coinFlip(num_investments):
   
    #flip a coin n times. n = num_investments
    coins = np.random.random(num_investments)
    
    #convert results according to baised coin (.51 , .49)
    flip_results = map(lambda x: 1 if x <= 0.51 else 0, coins)
    
    return flip_results


''' takes in in of position values and array of coin flips.
calculates return on investment`'''
def profits(investment, coin_flips ):
    returns = np.sum(investment*coin_flips*2)
    return returns


'''draw a histogram of daily returns for a given number of trials and parallel investments '''

def generateGraph(daily_ret, num_trials, pos):
    plt.figure()
    plt.hist(daily_ret, bins = 100, range = [-1,1])
    plt.title("Histogram of normalized daily returns for %s days \n %s parallel investments per day" %(num_trials,pos) )
    plt.savefig('histogram_%s_pos.pdf' %pos)
    
    return

positions = [1,10,100,1000]
num_trials = 10000


if __name__ == "__main__":

    try:
        print "running 10,000 simulations for each possible investment portfolio!"
        print 'Starting [    ]',
        print '\b'*6,
        sys.stdout.flush()

        investment(positions, num_trials)
    except KeyboardInterrupt as k:
            print "  You chose to terminate the program ... Goodbye now!"
            sys.exit()

