import numpy as np

def investment(position, num_trials):
    #initiate empty lists for cumulative return and daily return
    cumu_ret = []
    daily_ret = []
    for trial in range(num_trials):
        position_value = 1000 / position
        #with probability 0.51 gain money and 0.49 lose money
        gain = np.random.uniform(size = position) > 0.49
        #append the sum of money gained to cumulative return and then daily return
        cumu_ret.append(gain.sum() * position_value * 2)
        daily_ret.append((cumu_ret[trial]/1000.) - 1)
    return daily_ret
