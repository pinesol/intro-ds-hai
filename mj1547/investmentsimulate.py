'''
Created on Nov 8, 2014

@author: jiminzi
'''
import numpy as np
#position=[1,10,100,1000]
def investment(positions,n_trials):
    '''
    method to simulate
    arguement: 
    positions:a list of the number of shares to buy in 
              parallel: e.g. [1, 10, 100, 1000]
    num_trials :how many times to randomly repeat the test
    '''
    #invest={{str(x):[] for x in positions}}
    #result={'position':[],'daily':[]}
    results={}
    #create a empty result dict
    for num_position in positions:
        daily_ret=[]#create a new daily_ret list
        position_value=1000/num_position#position_value function
        for trail in range(1,n_trials):
            expect_prob=np.random.choice([-1,1],num_position,p=[0.49,0.51])
            '''
            51% of the time the return is exactly 1.0 (the value doubles).
            49% of the time the return is exactly -1.0 (all value is lost).
            '''
            #for this investment, there is 0.49 posibility lost ,and 0.51 posibility win
            cumu_return=position_value*np.sum(expect_prob + 1)
            #the cumu_return functuon for trails
           #the function to calculate the daily return by cumu_teyurm
            daily_return=(cumu_return/1000.)-1
            # add each daily_returm value to daily_return list
            daily_ret.append(daily_return)
        if (results.has_key(num_position)):
            results[num_position].append(daily_ret)
        else:
            results[num_position]=daily_ret
            #write the daily_ret to results dictionary
    #print result 
    #print results
    return results
