'''
Created on Nov 7, 2014

@author: luchristopher
'''
import sys
from userexcps import *



def safeInput(prompt,termination_command,str_parser):
    '''
        Provide general input string checking and additional validations with user defined functions,
        if illegal input string is received, it will flush the input and request a new valid input
    '''
    while True:
        try:
            input_string = raw_input(prompt)
        except (KeyboardInterrupt, EOFError):
            print >> sys.stderr, 'Program terminated by unexpected operations\n'
            sys.exit()
        
        if input_string in termination_command:
            print 'Program terminated by user\n'
            sys.exit()
            
        try:
            secured_input = str_parser(input_string)
            break
        except (InvalidInputError):
            continue
    return secured_input