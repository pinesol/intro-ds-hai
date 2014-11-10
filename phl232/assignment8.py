import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

'''

Function to simulate payout for investment described in assignment 
Returns an array of returns for each trial. pWin is a parameter of the investment

Example: Buy 100 shares of $10, 20 times

playGame(10, 100, 20)

'''

def playGame(denomination, shares, numTrials):
    
    pWin = 0.51    
    trials = np.random.rand(numTrials, shares)
    
    cumu_ret = np.zeros([numTrials, shares])    
    cumu_ret[trials <= pWin] = 2 * denomination
    
    daily_ret = (cumu_ret.sum(1) / (denomination * shares))-1
    
    return daily_ret
    
### Run HW Input ###


# Set plotting options
try:
    sns.set_palette("deep", desat=.6)
    sns.set_context(rc={"figure.figsize": (8, 5)})
except:
    pass

# Homework Case

numTrials = 10000
positions = [1, 10, 100, 1000]
numShares = 1000

resultsFile = open('results.txt', 'w')

for numShares in positions:
    
    returnOut = playGame(1000 / numShares, numShares, numTrials)
    
    # Make Histogram
    numstr = str(numShares)
    
    if numShares == 1:
        titleTxt = numstr + ' Share of $' + str(int(1000 / numShares)) + ', numTrials = ' + str(numTrials) 
    else:
        titleTxt = numstr + ' Shares of $' + str(int(1000 / numShares)) + ', numTrials = ' + str(numTrials)  
    
    plt.figure()
    plt.hist(returnOut, bins = 100, range = [-1,1])
    plt.xlim(-1,1)
    plt.ylabel('count'), plt.xlabel('return'), plt.title(titleTxt)
    
    # Save Histogram
    outName = 'histogram_'+numstr.zfill(4)+'_pos'
    pp = PdfPages(outName+'.pdf')
    pp.savefig()
    pp.close()
    
    # Save text file with summary statistics
    resultsFile.write(titleTxt + '\n' + 'mean :' + str(round(returnOut.mean(),4)) +
                        '\n' + 'stdev: ' + str(round(returnOut.std(),4)) + '\n\n')
    
resultsFile.close()