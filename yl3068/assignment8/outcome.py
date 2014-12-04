import numpy as np
import matplotlib.pyplot as plt

#Define a function to calculate investment outcome for everyday

def outcome(investment, position, num_trails):

    """
    Arguments:
    investment: the total money you invested
    position: number of shares to purchase
    num_trails: number of trails to randomly repeat the test
     
    Returns:
    daily_ret: daily investment outcome rate from this simulation test

    """

    position_value = investment/position
    
    daily_ret = []

    for trail in xrange(num_trails):
        
        #Generate random numbers between 0 to 1 for each position
        outcome = np.random.uniform(low = 0, high = 1, size = position)

        #Calculate the numbers of positions that make revenues 
        revenue_counts = (outcome > 0.49).sum()

        cumu_ret = revenue_counts * position_value * 2
        daily_ret.append((float(cumu_ret)/1000) - 1)
    
    return daily_ret
