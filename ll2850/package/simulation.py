__author__ = 'leilu'
from numpy import *
import numpy as np
import matplotlib.pyplot as plt


def investment(positions, num_trails):
    '''
    This function will simulate the investment by taking two arguments:
    1)positions: a list of the number of shares
    2)num_trails times: an integer, the number of times that the process will be repeated

    The output return will be a list of lists; each list consists of num_trails elements
    '''
    daily_ret=[] # create a list for daily return
    for position in positions:
        position_value = 1000/position
        cumu_ret=[] # create a list for cumulative return
        for trail in range(num_trails):
            cumu_ret.append(position_value*(np.random.choice([0, 2], position, p=[0.49, 0.51]).sum()))
            # specify the return values and their corresponding probability
            # return a list of cumulative return
        daily = [cumu/float(1000) - 1 for cumu in cumu_ret]
        daily_ret.append(daily)

    return daily_ret



