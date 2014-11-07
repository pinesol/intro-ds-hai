# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 19:16:43 2014

@author: LaiQX
"""

import matplotlib.pyplot as plt
from daily_ret import daily_ret
import numpy as np


def main():
    """
    main function 
    take the given positions and trials
    plot histogram of each position and save the image as pdf format
    calculate the mean and std of each position, save the result in a text file
    """
    
    positions = [1,10,100,1000]
    trials = 10000
    result = {}
    for position in positions:
        result[position] = daily_ret(position,trials)

    
    #plot histograms
    for position in positions:
        plt.figure()
        plt.hist(result[position],bins=100,range=[-1,1])
        file_name = "histogram_%04d_pos.pdf" % (position)
        plt.savefig(file_name)
        plt.close()


    # calculate means and stds
    f = open("result.txt","a+")   
    for position in positions:
        mean = np.mean(result[position])
        std = np.std(result[position])
        write_string = "position: "+str(position)+"\n"
        f.write(write_string)
        mean_string = "mean: %3.4f" % (mean) + "   std: %5.4f" % (std)+"\n"
        f.write(mean_string)
    f.close()
    
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
            
    


