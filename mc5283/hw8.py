import numpy as np
import matplotlib.pyplot as plt

def simulation(position, num_trials):
    '''
    this function simulate the return of a list of positions for num_trials times
    '''
    returns = {str(i):[] for i in position}
    for i in position:
        position_value = 1000/i
        daily_ret = []
        for trial in range(num_trials):
            cumu_ret = position_value*(np.random.choice([0,2], i, p = [0.49,0.51]).sum())
            ret = (cumu_ret/float(1000)) - 1
            daily_ret.append(ret)
        returns[str(i)].append(daily_ret)
    return returns

def main():
    '''
    this function caculate the mean and standard deviation of return 
    in different positions
    '''
    position = [1,10,100,1000]
    num_trials = 10000
    returns = simulation(position, num_trials)
    file = open('results.txt', 'w')
    for i in position:
        mean = np.mean(returns[str(i)])
        std = np.std(returns[str(i)])
        file.write('Position:'+str(i)+'\n'+'mean:'+str(mean)+'\t'+'std:'+str(std)+'\n')
        file.flush()
        plt.figure()
        plt.hist(returns[str(i)], 100, range = [-1,1])
        plt.savefig('histgram_'+str(i)+'pos.pdf', format = 'pdf', dpi = 72)
        file.close

if __name__ == '__main__':
    main()
