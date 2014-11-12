'''
Created on 2014.11.8

@author: apple
'''

import numpy as np

class Investment():
    def __init__(self,total_investment):
        """
        construct the class of investment.
        
        attribute:
        total_investment: the capital used for investment.
        
        """
        self.total_investment = total_investment
        
    def simulation(self, position, num_trials):
        """
        This function can simulate the investment when the number of shares to buy varies in several times.
        
        input:
        position(int): the number of shares to buy
        num_trials(int): how many times to randomly repeat the test
        
        return:
        daily_ret(float): a list of the daily profit from the investment 
         
        """
        #position_value represents the size of each investment for every position
        position_value = self.total_investment/position
        cumu_ret = []

        for trial in range(1,num_trials+1):
            cumu = (np.random.choice([0,2],position,p=[0.49,0.51]).sum())*position_value
            cumu_ret.append(cumu)
        
        daily_ret = [it/1000.0-1 for it in cumu_ret]
        return daily_ret

if __name__ == '__main__':
    pass