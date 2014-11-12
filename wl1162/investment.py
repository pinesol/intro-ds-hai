import numpy as np

class investment:
	"""create a class that represents investment instruments"""
	def __init__(self, asset_value):
		"""constructor that takes in a numeric value"""
		self.asset_value=asset_value

	def simulation(self, num_trails, positions):
		"""given the shares to purchase, simulates this event and returns return rate"""
		position_value = self.asset_value/positions  # calculates the value per share on particular position
		cumu_ret=[]
		
		for i in range(num_trails):
			value_gain=np.random.uniform(size=positions) > 0.49 # situations that will gain
			cumu_ret.append(value_gain.sum()*position_value*2)

		daily_ret=[x/float(1000)-1 for x in cumu_ret]
		return daily_ret

