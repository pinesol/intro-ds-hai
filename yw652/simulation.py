import numpy as np
import sys
import os

def simulation(positions, num_trials):

    retList = []

    for position in positions:
        #Set up value "position_value" to represent the size of each investment
        position_value = 1000 / position

        cumu_ret = []
        for n in range(int(num_trials)):
            probList = []
            for n in range(position):
                prob = np.random.sample()
                probList.append(prob)

            cumu_ret.append(position_value * 2 * np.sum((prob > 0.51) * 1 for prob in probList))

        daily_ret = []

        for trial in range(len(cumu_ret)):
            daily_ret.append((cumu_ret[trial]/float(1000)) - 1)

        retList.append(daily_ret)

    return retList






