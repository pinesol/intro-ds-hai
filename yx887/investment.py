from __future__ import division
import numpy as np

class Invest(object):
    """ Investment instrument class """
    def __init__(self, asset):
        """ Constructor of the class. 

        Args:
            asset (int): Total asset possessed. 

        """
        self.asset = asset

    def simulate(self, ntrials, position):
        """ Simulate the investment given number of shares to purchase.

        Args:
            ntrials (int): number of trials to simulate.
            position (int): number of shares to purchase.

        Returns:
            (float): daily return rate calculated from the simulation results.

        """
        position_value = self.asset / position    # Value per share given position
        cumu_ret = []
        for trial in xrange(ntrials):
            gain = np.random.uniform(size=position) > 0.49    # Gain money?
            cumu_ret.append(gain.sum() * position_value * 2)

        daily_ret = [ret/1000-1 for ret in cumu_ret]
        return daily_ret

    
