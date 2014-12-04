import numpy as np
import matplotlib.pyplot as plt
positions=[1,10,100,1000]

def simulate(denomination):
    """ simulates the return (return included the initial value) of one day investment 
        with chosen denomination inputed
    """
    shares=1000/denomination
    #shares indicate numbers of share we can buy  with $1000
    cum=0
    expectRet=[]
    for num_share in range(shares): 
        expect_Prob=np.random.choice([-1,1],p=[.49,.51])
        #specify the probability of two possible returns with corresponding probability
        expected_return= denomination*(1+expect_Prob)# expected_return included original amount of investment
        cum+=expected_return#add up all the returns from different shares
    expectRet.append(cum)#append total return into a list
    return expectRet[0]#return the value of denomination



def simulate_ret(position,num_trials):
    """returns a dictionary of daily return per each dollar invested,
        the daily return will be net return, which is the expected net profit for each dollar invested
    """
    cumu_ret={}
    daily_ret={}
    #create a dictionary for daily return with key be the specific single day, 
    #value be the corresponding expected return
    position_value=1000/position
    positionRet=0
    for trial in range(1,num_trials+1):
        positionRet=simulate(position_value)
        cumu_ret[trial]=positionRet
        daily_ret[trial]=(cumu_ret[trial]/1000.0-1)
        #"Normalize" the return value to be net profit value in each dollar units. 
        #Therefore, the net profit for each dollar invested will be between -1 and 1. 
    return daily_ret

def visualizeRet_to_pdf(positions,num_trails):
    """generate the histograms with X axis from -1.0 to +1.0, Y axis as number of trails with freq results
        and save each histogram of result for each positions into corresponding pdf . 
    """
    for position in positions:
        daily_ret=[]
        #create a list of daily return values for each positions ,which will be used for generating figures.
        dailyRet=simulate_ret(position,num_trails)
        for i in dailyRet: daily_ret.append(dailyRet[i])
        #append each single daily return value into list 
        plt.hist(daily_ret,100,range=[-1.0,1.0])
        plt.ylabel("number of trails")
        plt.xlabel("daily net-return")
        #plt.show()
        if position==1:plt.savefig('histogram_0001_pos.pdf')
        elif position==10:plt.savefig('histogram_0010_pos.pdf')
        elif position==100:plt.savefig('histogram_0100_pos.pdf')
        elif position==1000:plt.savefig('histogram_1000_pos.pdf')
        else: print "error: check position value"
        print position # just for testing the progress 
        plt.close()
        

def stat_to_file(position,num_trails):
    """return a text file ,which contains the results of expected value of daily return 
        and standard deviation of daily return for each position. 
    """
    result=open("results.txt",'w') 
    for position in positions:
        daily_ret=[]
        dailyRet=simulate_ret(position,num_trails)
        for i in dailyRet: daily_ret.append(dailyRet[i])
        ret_array=np.array(daily_ret)
        ret_mean=np.mean(ret_array)
        ret_std=np.std(ret_array)
        #print position,ret_std,ret_mean
        result.write('\n\nSome basic statistics of the daily return for  position of %s:\n expected value: %s, standard deviation:%s \n'%(position,ret_mean,ret_std))
    result.close()
    
    


if __name__=='__main__':
    
    stat_to_file(positions,10000)
    visualizeRet_to_pdf(positions,10000)


    
    
    
    
    