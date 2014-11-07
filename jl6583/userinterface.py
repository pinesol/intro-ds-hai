'''
Created on Nov 6, 2014

@author: luchristopher
'''
import sys
from utilities import *
from superio import *

def receiveInput():
    '''
        Safely receives the input strings
    '''
    input_list = safeInput('Enter a list of positions:\n',['exit','quit'],listParser)
    input_num = safeInput('Enter the number of trials:\n',['exit','quit'],numIdentifier)
    return input_list,input_num


            
            
    