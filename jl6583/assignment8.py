'''
Created on Nov 6, 2014

@author: luchristopher
'''
from userinterface import *
from investsim import *
import sys

def main():
    positions, num_trials = receiveInput()
    
    try:
        f = open('results.txt','a')
    except:
        print >> sys.stderr, 'Cannot open the file!\n'
    
    print >> f, 'position    mean    standard_deviation'
    
    #for each position build a simulator instance and run the simulation
    for pos in positions:
        invest_simulator = BinomialInvestSimulator(amount=1000,position=pos,p=0.51)
        invest_simulator.runSimulation(trial_nums=num_trials)
        print >> f, invest_simulator.describe()
        sys.stdout = sys.__stdout__
        invest_simulator.generateHistogram(100)
    
    f.close()

if __name__ == '__main__':
    main()