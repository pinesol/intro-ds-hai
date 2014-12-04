import numpy as np

class InvestSimulation(object):
	''' This is the class for the investment simulation'''

	def __init__(self, total_asset):
		'''Constructor of the class'''
		self.total_asset = total_asset 

	def simulation(self, position, num_trials):
		'''This is the function that checks the validity of inputs and 
		simulates the investment given the position and number of trials.'''

		cumu_ret = []
		daily_ret = []
		for trial in range(num_trials):
			#calculate the size of each investment
			position_value = self.total_asset / position
			#probability: 51% win and 49% lose
			gain = np.random.uniform(size = position) > 0.49
			cumu_ret.append(gain.sum()* position_value * 2)
			daily_ret.append((cumu_ret[trial] / 1000.) - 1)
		return daily_ret 








