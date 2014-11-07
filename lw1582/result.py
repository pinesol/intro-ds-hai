'''import Investment module for calculation
numpy for statistical calculations
matplotlib for the plots'''
from Investment import investment
import numpy as np
from matplotlib import pyplot as plt

def result(positions, num_trials):

  '''this result first calculate the mean and std for the oucomes of every position and write into a txt file'''
  final_result = investment(positions,num_trials)
  
  ret_mean = np.mean(final_result,axis = 0)
  ret_std = np.std(final_result,axis = 0)
  
  f = open("results.txt","w")
  
  i = 0
  while i < len(positions):
    f.write("position: " + str(positions[i]) + "\nmean: " + str(ret_mean[i]) + "\nstd: " + str(ret_std[i]) + "\n")
    i = i + 1

  f.close()

  i = 0

  '''for each position, the outcomes are plotted in a histogram'''
  while i < len(positions):
    plt.figure()
    plt.hist(final_result[:,i],100,range=[-1,1])
    plt.savefig("histogram_{0:04}_pos.pdf".format(positions[i]))
    i +=1
  return "completed"

def main():
  positions = [1,10,100,1000]
  num_trials = 10000

  result(positions, num_trials)

if __name__ == "__main__":
  main()

