import numpy as np
import matplotlib.pyplot as plt


def simulation(positions, num_trials):
    """This program runs num_trials times simulations for position allocation provided by input list positions.
    Return a dictionary with str(positions) as key name and a list of daily return simulation results as value
    """
    result = {str(x):[] for x in positions}  # dictionary to store result of each position simulation
    for position in positions:
        position_value = 1000/position
        daily_ret = []  # list to store daily return
        for trials in range(num_trials):
            cumu = position_value*(np.random.choice([0,2], position, p=[0.49,0.51]).sum())
            daily = (cumu/float(1000)) - 1
            daily_ret.append(daily)
        result[str(position)].append(daily_ret)
    return result