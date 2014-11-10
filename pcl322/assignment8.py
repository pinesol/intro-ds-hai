import sys
import os
import numpy as np
import scipy as sp
import pandas as pd
import re
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

#Simulation
def Question_2(position, num_trials):

	result = {}

	for pos in position:

		position_value = 1000 / pos

		cumu_ret = []
		for i in range(num_trials):
			cumu_ret.append(np.sum(np.random.choice([0, 2*position_value], \
				pos, p=[0.49, 0.51])))
	
		result[pos] = np.array(cumu_ret)/1000.0 - 1

	return result

#Check input is int
def valid_int(input):

	if re.match(r"^\d+$", input) == None:
		return False
	return True

#Check position is in right format
def valid_position(input):

	if re.match(r"^\[(\d+\,)*\d+\]$", input) == None:
		return False
	return True

#Initialize the list of position
def init_position(position):

	pos = position.split(",")

	pos[0] = pos[0].replace("[", "")
	pos[-1] = pos[-1].replace("]", "")

	return [int(i) for i in pos]

#Compute the mean and std of each position
def stats_results(position, results):

	df = pd.DataFrame(index=position, columns=["mean", "std"])

	df["mean"] = [np.mean(results[p]) for p in position]
	df["std"] = [np.std(results[p]) for p in position]

	return df

if __name__ == "__main__":

	#Read number of trials from user
	while True:
		num_trials = raw_input("Please enter the number of trials ")
		if not valid_int(num_trials):
			print "Invalid number of trials: " + num_trials
			continue
		break

	#Read position from user
	while True:
		position = raw_input("Please enter the list of the number of shares ").replace(" ", "")
		if not valid_position(position):
			print "Invalid shares"
			continue
		break

	#Initialize position
	position = init_position(position)

	#Run simulation
	daily_ret =  Question_2(position, int(num_trials))

	#Calculate mean and std
	statsDataFrame =  stats_results(position, daily_ret)

	#Write results.txt
	fp = open("results.txt", "w")
	fp.write(statsDataFrame.to_string())
	fp.close()

	#Plot
	for p in position:
		plt.hist(daily_ret[p], 100, range=[-1,1])
		plt.savefig("histogram_"+"%04d" % (p)+"_pos.pdf", format="pdf")
		plt.close()
