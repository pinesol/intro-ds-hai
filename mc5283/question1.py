import numpy as np

def simulation(num_trials,position):
    '''
    this function runs a simulation to find the position combination
    of treasure notes with face values of 1, 10, 100, and 1000 UDS.
    The best combination maximizes daily investment return under the budget
    constraint of 1000USD
    a, b, c, d denote the position of 1000, 100, 10, 1USD treasure notes
    '''
    a = []
    b = []
    c = []
    d = []

    for i in range(2):
        for j in range(11):
            for l in range(101):
                for k in range(1001):
                    if 1000*i + 100*j + 10*l + 1*k <= 1000:
                        a.append(i)
                        b.append(j)
                        c.append(l)
                        d.append(k)
                    else:
                        break
    positionCombo = np.array([a,b,c,d]).T #position combination within budeget constraint

    bestPosition = []
    cumu_ret = []
    for trial in range(num_trials):
        returns = np.random.choice([1,-1], size = (len(positionCombo)*4), p = [0.51,0.49])
        returns = np.reshape(returns,(len(positionCombo), 4))
        value = position*positionCombo*(returns+1)
        totalValue = np.sum(value, axis = 1)
        maxValue = max(totalValue)
        ix = np.argmax(totalValue)
        bestPosition.append(positionCombo[ix])
        cumu_ret.append(maxValue)
        averagePosi = np.mean(bestPosition, axis = 0)
    return averagePosi

if __name__ == '__main__':
    position = np.array([1000,100,10,1])
    print simulation(100,position)
