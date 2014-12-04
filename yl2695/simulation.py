import numpy as np


def simulation(positions, num_trials):
    '''
    Define a simulation function that takes postions and number of trials as inputs and returns the revenue rate of every trial.
    '''

    # use simulationResult to store the final simulation result
    simulationResult = {}
    
    # do loop for every position in the positions list
    for position in positions:
        simulationResult[position] = []

        for trial in range(num_trials):
            position_value = 1000 / position

            # generate a random number which is in (0, 1) and find whether it is more than 0.49.
            result = np.random.uniform(0, 1, size=position) > 0.49

            daily_ret = (result * position_value * 2).sum() / 1000.0 - 1
            simulationResult[position].append(daily_ret)

    return simulationResult
