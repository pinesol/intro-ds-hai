'''
Created on Nov 6, 2014

@author: luchristopher
'''
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class BinomialInvestSimulator():
    '''
    Class for a Binomial Investment Simulator
    In class BinomialInvestSimulator:
    >>>>
        Attributes:
            1) __daily_ret
            2) __total_investment
            3) __position
            4) __position_value
            5) __p : The probability of win at each time
        Methods:
            1) __getMean()
            2) __getStd()
            3) runSimulation()
            4) describe()
            5) generateHistogram()
    '''


    def __init__(self, amount, position, p):
        '''
        Constructor: check the validity of input and initialize the simulator instance
        '''
        if type(position) != int or (type(amount) != float and type(amount) != int):
            raise TypeError()
        if position == 0 or p > 1 or p < 0:
            raise ValueError()
        self.__daily_ret = None
        self.__total_investment = amount
        self.__position = position
        self.__position_value = self.__total_investment/self.__position
        self.__p = p
        
    
    def runSimulation(self,trial_nums):
        '''
            runs simulation for trial_nums times and generate the daily return
        '''
        cumu_ret = np.random.binomial(self.__position,self.__p,trial_nums)*2*self.__position_value
        self.__daily_ret = (cumu_ret/float(self.__total_investment))-1
        return self.__daily_ret
    
    def __getMean(self):
        '''
            Returns the mean of daily return
        '''
        return np.mean(self.__daily_ret)
    
    def __getStd(self):
        '''
            Calculate the standard deviation of the daily return 
        '''
        return np.std(self.__daily_ret)
    
    def describe(self):
        '''
            Returns the mean and standard deviation
        '''
        return [self.__position,self.__getMean(),self.__getStd()]
        
    def generateHistogram(self,bin_width=100):
        #setting the Latex Path so that labels and legends in the plot can be shown with Latex
        os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin'
        fig = plt.figure()
        #Use latex fonts for better appearance, but it might slow down the plotting process
        plt.rc('text',usetex=True)
        plt.rc('font',family='Computer Modern')
        N, BINS, PATCHES = plt.hist(self.__daily_ret,bins=bin_width,range=[-1,1],color='k')
        plt.xlim((-1,1))
        plt.xlabel(r'Daily Returns')
        plt.ylabel(r'Counts')
        plt.title(r"The Daily Return With Position = {} ".format(self.__position))
        plt.show()
        fig.savefig('histogram_{0:0>4}_pos.pdf'.format(self.__position_value))
        
        
        
        
        