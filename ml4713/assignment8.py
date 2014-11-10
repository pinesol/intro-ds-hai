# -*- coding: utf-8 -*-
"""Programming for Data Science
   Assignment 8
   Menggfei Li
"""

from investment_instrument import *


def main():
    
        positions_input=input()
        repeated_times=input()
        
        #simulate the gambling and store the results in the variable 'final'
        final=strats(positions_input,repeated_times)    
        
        #generate results.txt
        statistics=stats(final,positions_input)
        with open('result.txt','w') as file:    
             file.write(str(statistics))
             
        #generate histograms        
        for p in positions_input:
            hist_generator(final,p)
            
            
            
            
if __name__=='__main__':
    main()