
import numpy as np
def simulation(position, num_trials):
    '''
    Args:
        position: a list of the number of shares to buy in parallel
        num_trials: how many times to randomly repeat the test
    Returns:
        daily_ret_list: a list of daily return rate
    '''
    position_value = 1000 / position
    daily_ret = []
    for trial in range(num_trials):
        ret = np.random.choice([0,2], position, p=[0.49,0.51]) #one time return
        cumu_ret = ret.sum() * position_value #cumulative return
        daily_ret.append(cumu_ret/1000.-1) #store daily return results in a list
        
    return daily_ret
