# -*- coding: utf-8 -*-
"""
Created on Fri Nov 07 16:40:52 2014

@author: Israel
"""

import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame

def runner(positions,num_trials):
  '''Simulation of one-day returns given position stategy, repeated num_trails times'''
  daily_ret=DataFrame(columns=positions,index=np.arange(1,num_trials+1))
  for p in positions:
    cumu_return=(np.random.random((num_trials,(1000/p)))>0.49).sum(axis=1)*2*(p)
    result=DataFrame(cumu_return,index=np.arange(1,num_trials+1),columns=['cumu_ret'])
    daily_ret[p]=(result['cumu_ret']/1000)-1
  return daily_ret

results=runner([1,10,100,1000],10000)

##summary stats
means=DataFrame(results.mean(),columns=["Mean by Position"])
stddev=DataFrame(results.std(),columns=["Std Dev by Position"])

f = open('results.txt','w')
f.write(str(means))
f.write('\n')
f.write(str(stddev))
f.flush()
f.close()


##plots
for p in [1,10,100,1000]:
 label = "%04d" % (p,)
 plt.figure(p)
 plt.hist(np.array(results[p]),100,range=[-1,1])
 plt.title(str(p)+" Positions")
 plt.plot()
 plt.savefig('histogram_'+label+'_pos.pdf')
