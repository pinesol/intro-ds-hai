import numpy as np
import matplotlib.pyplot as plt
import problem2


def problem3():
    daily_ret = problem2.investmentSimulation2([1, 10, 100, 1000], 10000)
    for i in range(4):
        plt.figure()
        plt.hist(daily_ret[i], 1000, range=[-1.1, 1.1])
        plt.savefig('picture' + str(i))

if  name__ == '__main__':
    problem3()
