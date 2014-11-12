import investment
import matplotlib.pyplot as plt
import numpy as np

def main():
	positions_input = raw_input('a list of the number of shares to buy in parallel: e.g. [1, 10, 100, 1000]? ')
	positions = [int(x) for x in positions_input.strip('[]').split(',')]
	num_trials = int(raw_input('how many times to randomly repeat the test? '))
	mean_list = []
	std_list = []
	results = open('results.txt','w')
	for position in positions:
		daily_ret = investment.investment(position,num_trials)
		mean = np.mean(daily_ret)
		std = np.std(daily_ret)
		results.write('{}	mean:{},std:{} \n'.format(position,mean,std))
		p = plt.figure()
		plt.hist(daily_ret,100,range=[-1,1])
		plt.title('Histogram of Daily Return with position {}'.format(position))
		plt.xlabel('daily return')
		p.savefig('histogram_{}_pos.pdf'.format(str(position).zfill(4)))	
	
	results.close()

if __name__ == '__main__':
	main()
