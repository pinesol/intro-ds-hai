'''
Created on 2014.11.8

@author: apple
'''

from InvestmentClass import *
import matplotlib.pyplot as plt
import numpy as np

def plothist(daily_ret, position):
    """
    Plot of the result of the trials in the histogram with X axis from -1.0 to +1.0, 
    and Y axis as the number of trials with that result.
    Save each figure into a pdf.
    
    Input:
        daily_ret(float): a list of the daily return from the investment given by an exact position.
        position(int): the number of shares to buy.
    
    """
    plt.figure()
    plt.hist(daily_ret,100,range=[-1.0,1.0])
    plt.xlabel('Daily Return')
    plt.ylabel('The Number of Trials')
    plt.title('Histogram of Daily Return with Position = {}'.format(position))
    plt.savefig('histogram_{}_pos.pdf'.format(str(position).zfill(4)))

def resulttxt(daily_ret, position):
    """
    For each position, save the mean value and standard deviation of the daily return
    into a txt file.
    
    Input:
        daily_ret(float): a list of the daily return from the investment given by an exact position.
        position(int): the number of shares to buy.
    
    """
    mean = np.mean(daily_ret)
    std = np.std(daily_ret)
    
    #If we first write this 'result.txt' file, we should use 'w' and write a new file named 'result.txt'.
    #In this case, if 'result.txt' exists, we can rewrite it.
    if position == 1:
        f = open('result.txt','w')
    #If we want append something to 'result.txt',we should use 'a'. 
    #If we insist using 'w', we'll lose the former information.
    else:
        f = open('result.txt','a')
    f.write('Position: {}\n'.format(position))   
    f.write('    Mean: {}; Std: {}\n'.format(mean,std))
    f.close()
    
def main():
    """
    When we have $1000 to invest in $1, $10, $100, and $1000 positions. 
    We can simulate 10000 times for each position to get the value of daily return.
    Plot a histogram and calculate the mean and standard deviation.
    """
    positions = [1,10,100,1000]
    num_trials = 10000
    total_investment = 1000
    
    for position in positions:
        daily_ret = Investment(total_investment).simulation(position, num_trials)
        plothist(daily_ret, position)
        resulttxt(daily_ret, position)
    
if __name__ == '__main__':
    main()