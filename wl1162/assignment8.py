from investment import investment
import numpy as np
import matplotlib.pyplot as plt

def main():
	"""main program that will simulate at each position and generate histograms of daily return rate"""
	positions = [1, 10, 100, 1000]  # initialize four positions
	num_trails = 10000 # number of trails the program will repeat the process
	instrument = investment(1000)  # initialize this instrument with asset amount 1000
	results = ['position mean std']  # initialize a list to store result

	for i in positions:
		print 'Position = {} simulation'.format(i)
		daily_ret=instrument.simulation(num_trails, i)  # simulate the event given the position i
		results.append(' '.join(map(str, [i, np.mean(daily_ret), np.std(daily_ret)])))  # append the results to results list

		plot=plt.figure()
		plt.hist(daily_ret, 100, range=[-1, 1], color='blue')
		plt.title('Daily return histogram with position {}'.format(i))
		plt.xlabel('Daily return')
		plt.ylabel('Frequency')

		plt.savefig('histogram_{}_pos.pdf'.format(str(i).zfill(4)))
	
	with open('results.txt', 'w') as function:  # set a write function to write out result
		function.write('\n'.join(results))


if __name__=='__main__':
	main()
