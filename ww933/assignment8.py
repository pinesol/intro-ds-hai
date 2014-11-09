__author__ = 'chianti'

import numpy as np
import matplotlib.pyplot as plt


def generate_return(position, num_trials):
    # position: the number of shares to buy in parallel
    # num_trials: how many times to randomly repeat the test
    # This function returns the investment result of each day 

    cumu_ret = []
    position_value = 1000.0 / position
    # position_value represents the size of each investment

    for trial in xrange(num_trials):
        each_prob = np.random.binomial(1, .51, position)
        # each_prob determines whether each position would earn money or loss money
        # With a prob of .51, a position would earn money and give us a return of 1.0
        # With a prob of .49, a position would loss money and give us a return of -1.0

        cumu_ret.append(each_prob.sum() * position_value * 2)
        # cumu_ret gives the outcome of one day of investment

    daily_ret = [(each_ret/1000)-1 for each_ret in cumu_ret]
    # This is the result of each day showing the return of the investment

    return daily_ret


def show_return(positions, num_trials):
    # This function receives a list of positions and num_trials
    # and shows the result of generate_return(position, num_trials) for each position in the list
    # It will give us a txt file showing the numerical results for each position containing the mean and std value
    # and some pdf files showing the histogram of the result for each position in the list

    f = open('results.txt', 'w')

    for each_position in positions:
        daily_ret = generate_return(each_position, num_trials)
        ret_mean = np.mean(daily_ret)
        ret_std = np.std(daily_ret)
        f.write('For position:' + str(each_position) + '\n')
        f.write('The mean of the daily return is:' + str(ret_mean) + '\n')
        f.write('The standard deviation of the daily return is:' + str(ret_std) + '\n' + '\n')
        f.flush()
        plt.clf()
        plt.hist(daily_ret, 100, range=[-1, 1])
        plt.savefig('histogram_{}_pos.pdf'.format(str(each_position).zfill(4)))

    f.close



def main():
    # With positions set to [1, 10, 100, 1000] and num_trials set to 10000, this main function
    # shows the result of the investment for each position

    my_positions = [1, 10, 100, 1000]
    my_num_trials = 10000
    show_return(my_positions, my_num_trials)

if __name__ == '__main__' and True:
    main()




