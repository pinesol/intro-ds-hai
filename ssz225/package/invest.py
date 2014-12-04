import numpy as np
from exceptions import *

def invest(positions, num_trials):
    #run investment simulation for each position num_trials times
    cumu_ret = []
    daily_ret = []
    for trial in range(num_trials):
        position_value = 1000 / positions
        #probabiliy of losing = 0.49 and winning is 0.51
        probability_lose = 0.49
        win = np.random.uniform(0, 1, size = positions) > probability_lose
        #position_value doubles if win
        cumu_ret.append(win.sum() * 2 * position_value)
        #save result of each day to daily_ret
        daily_ret.append((cumu_ret[trial] / float(1000)) - 1)
    return daily_ret

def isValidPositionsInput(positions_raw):
    """Checks if user input of positions is in proper form"""
    #check if positions_raw is a string 
    if isinstance(positions_raw, str):
        try:
            #ensure input contains []
            lower_bracket = positions_raw[0]
            upper_bracket = positions_raw[-1]
            if lower_bracket == '[' and upper_bracket == ']':
                #create a list of int(position) and store in the variable positions
                positions = [int(x) for x in positions_raw.strip('[]').split(',')]
                final_positions = []
                valid = [1, 10, 100, 1000]
                #test that each int from user input is a valid input equal to 1, 10, 100, or 1000
                for position in positions:
                    if position in valid:
                        final_positions.append(position)
                    else:
                        raise InvalidListError('Invalid list input')
                return final_positions
            else:
                raise InvalidListError('Invalid list input')
        except:
            raise InvalidListError('Invalid list input')
    else:
        return False

def checkTrialsValidity(input_num_trials):
    #check that user input num_trials is an int
    try:
        num_trials = int(input_num_trials)
        return num_trials
    except:
        raise InvalidTrialsError('Invalid Trials') 