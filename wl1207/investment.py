import numpy as np
def investment(position, num_trials):
    cumu_ret = []
    daily_ret = []
    for trial in range(num_trials):
        position_value = 1000/position
        gain = np.random.uniform(size=position)>0.49 #with probability 51% win, 49 lose.
        cumu_ret.append(gain.sum()*position_value*2)
        daily_ret.append((cumu_ret[trial]/1000.)-1)
    return daily_ret
