import numpy as np
import matplotlib.pyplot as plt

def main():
	'''This program simulates the given position list by num_trials times.

	Returns a results.txt files and corresponding histograms'''
	
	# Setting initial parameters
	num_trials = 10000
	positions = np.array([1, 10, 100, 1000])
	Budget = 1000.0
	position_values = np.divide(Budget, positions)
	
	Return_List = []        # To store the return data for the final result
	Std_List = []			# To store the Std for the final result
	result = open('results.txt', 'w') # Create a txt file to write related results in
	result.write('Position'.ljust(10)+'Mean'.ljust(12)+'Std \n')
	
	# The following loop Computes the returns and plots corresponding histograms
	for i in xrange(len(positions)):
		daily_ret = []
		for j in xrange(num_trials):
			cumu_value = position_values[i] * sum(np.random.choice([0, 2], positions[i], p=[0.49, 0.51]))
			daily_ret.append(cumu_value/1000 - 1)  # computes each daily return
		Return_List.append(np.mean(daily_ret)) 
		Std_List.append(np.std(daily_ret))
        
        # Plotting
		plt.figure()
		plt.hist(daily_ret,100, range=[-1,1])
		plt.title('Daily return histogram of position {}'.format(positions[i]))
		plt.xlabel('Daily Return')
		plt.ylabel('Frequency')
		plt.savefig('histogram_'+str(positions[i]).zfill(4)+'_pos.pdf', format='pdf')
		result.write(str(positions[i]).ljust(10)+str(Return_List[i]).ljust(12)+str(Std_List[i]).ljust(12)+'\n')
	result.close()
if __name__ == '__main__':
	main()