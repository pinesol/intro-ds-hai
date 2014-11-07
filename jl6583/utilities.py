'''
Created on Nov 6, 2014

@author: luchristopher
'''

import sys
import re
from exceptions import *
from userexcps import *

def isList(str_name):
    '''
        returns True if the input string is a valid 'list' string with format like '  [   1,   2  ,3  ]  ',
        inputs with unacceptable formats, symbols(except',','[]'and 0-9) and values(e.g.negative numbers, decimals)
        are recognized as illegal
    '''
    if type(str_name) == str:
        list_pattern = re.compile(r'^\s*\[(\s*\d+\s*,)*\s*\d+\s*\]\s*$')
        return bool(re.match(list_pattern,str_name))
    else:
        return False
        

def listParser(str_name):
    '''
        list string object validation
    '''
    if isList(str_name):
#         delimiter = re.compile(r'(?<=\d)\s*,\s*(?=\d)')
        numstr_pattern = re.compile(r'\d+')    #find all numbers in the string
        numstr_list = numstr_pattern.findall(str_name)
        num_list = map(int,numstr_list) #convert the parsed numbers in strings to integers
        if 0 in num_list:
            raise InvalidInputError()
            return None
        return num_list
    else:
        raise InvalidInputError()
        return None
    
def numIdentifier(str_name):
    '''
        returns False if input string has characters except 0-9 and spaces
    '''
    if type(str_name) != str:
        raise InvalidInputError()
        return None 
    pattern = re.compile(r'^\s*\d+\s*$')
    if bool(re.match(pattern,str_name)):
        return int(re.search(re.compile(r'\d+'),str_name).group())
    else:
        raise InvalidInputError()
        return None


            
        