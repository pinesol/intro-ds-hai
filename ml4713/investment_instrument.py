# -*- coding: utf-8 -*-
"""Investment Strategy
   Mengfei Li
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def single_bet(pos_val):
    """Imitate a single 'flip' in this gambling problem
    """
    value=np.random.binomial(1,0.51)
    if value==1:
        res=pos_val*2
    else:
        res=0
    
    return res


def simulation(pos):
    """According to different positions, experiemnt related trials.
       For example, if we buy 10 shares with $100 for each of shares, then
       we experiment 10 single_bet and store the output as result.
    """
    result=[None]*pos
    pos_val=1000/pos
    for j in np.arange(pos):
        result[j]=single_bet(pos_val)
    return result        
        

def strats(positions,num_trials):
    """Take positions as a list of numer of shares to buy, and num_trials as int
       represents the size of each investment
    """

    cumu_ret=[None]*num_trials
    daily_ret=[None]*num_trials
    summary=pd.DataFrame(index=positions,columns=np.arange(num_trials))
    
    for p in positions:
        for i in np.arange(num_trials):                 
            cumu_ret[i]=sum(simulation(p))            
            daily_ret[i]=(cumu_ret[i]/float(1000))-1   
        summary.loc[p,:]=daily_ret    

    return summary


def stats(summary,positions_input):
    """Calculate the mean and std for each position and return the statistics 
       report
    """
    mean=pd.DataFrame(index=['mean value'],columns=positions_input)
    std=pd.DataFrame(index=['Standard Deviation'],columns=positions_input) 
    for p in positions_input:
        mean[p]=np.mean(summary.loc[p,:])
        std[p]=np.std(summary.loc[p,:])  
    
    stats_report=pd.concat([mean,std])
        
    return stats_report



def hist_generator(summary,pos):
    """Generate histogram for each position
    """
    ax=plt.figure()  
    plt.hist(summary.loc[pos,:],100,range=[-1,1])  
    ax.savefig('histogram_{}_pos.pdf'.format(str(pos).zfill(4)))
  
    
    

