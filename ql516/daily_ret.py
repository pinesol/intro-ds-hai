# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 16:20:58 2014

@author: LaiQX
"""

import numpy as np

def daily_ret(position,num_trials):
    """
    input the position and num_trials, compute the daily return of the investment
    then repeat it "num_trials" times. return the result as a list
    
    position belong to [1,10,100,1000]
    
    """
    ret_list = []     # the list of the result
    for i in range(num_trials):         
        total = 0     # calculate each trial's total return 
        for j in range(position):
            # 0.51 chance to get 1.0 return and 0.49 chance to get -1.0 return
            return_rate = np.random.choice([0,2],p=[0.49,0.51])
            total = total + (1000/position)*return_rate
        total_ret = (total/1000.0) - 1
        ret_list.append(total_ret)
    return ret_list
