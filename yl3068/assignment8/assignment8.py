from outcome import outcome
import numpy as np
import matplotlib.pyplot as plt

#Define a function to run investment simulation for each position and show the results

def main():

    investment = 1000
    positions = [1,10,100,1000]
    num_trails = 10000
    f = open('results.txt', 'w') #Open a file to write in mean and standard deviation results

    for position in positions:
        daily_ret = outcome(investment, position, num_trails)
        f.write('\nPosition:{}'.format(position))
        f.write('\nMean:{0}; Std:{1}\n'.format(np.mean(daily_ret), np.std(daily_ret)))
        fig = plt.figure()
        plt.hist(daily_ret, 100, range=[-1,1], color = 'silver', edgecolor = 'DarkGrey')
        plt.title('The histogram of the result for {0} position'.format(position))
        plt.xlabel('daily return')
        fig.savefig('histogram_{}_pos.pdf'.format(str(position).zfill(4)))
    f.close()


if __name__ == '__main__':
    main()
