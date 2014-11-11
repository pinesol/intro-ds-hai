'''
Created on Nov 11, 2014

@author: ds-ga-1007
'''
import numpy as np
from numpy import *

def simulation(position, num_trials):
    """
    The simulation function will run the investment simulations given number of shares to buy
    """
    
    position_value = 1000/position
    daily_ret = []
    cumu_ret = []
    #Run simulations to determine how to make investment 
    for trial in xrange(num_trials):
        cumu_ret = (np.random.choice([0,2],position,p=[0.49,0.51]).sum())*position_value
        daily_ret.append(cumu_ret/1000.0-1)
    return daily_ret