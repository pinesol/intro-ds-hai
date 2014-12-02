import numpy as np
import pandas as pd

def loadData(file_name, index_col):
	"""Loads data and sets row index equal to value of index_col."""
	df = pd.read_csv(file_name)
	df = df.set_index(df[index_col])
	return df.drop(index_col, 1)

def getMeasureSplit(df, type_col, measure_name):
	"""Takes a measure (i.e. SIR), removes all entries unrelated to that measure,
		and then returns a dictionary where the keys are measure types (i.e. HAI_1)
		and the values are data frames corresponding only to that measure."""
	df = df[df[type_col].str.contains(measure_name)] # filter by measure_name
	types = np.unique(df[type_col])
	df_split = {}
	for i in types:
		df_split[i] = df[df[type_col] == i].drop(type_col,1)
	return df_split

def categoricalToIndicator(df, compare):
    """Replaces the string values in a compare column to numerical benchmarks
        -1: Worse than national average
        0: No different than national average
        1: Better than national average
        Nan: Not available"""
    benchmarks = pd.unique(df[compare])
    benchmarks.sort() # alphabetically sort the comparator labels
    benchmarks ={benchmarks[0]:1, benchmarks[1]:0, benchmarks[2]:np.nan, benchmarks[3]:-1}
    return df.replace({compare:benchmarks})

def convertToNumeric(df, col_label, missing_marker):
    """Converts missing values denoted by string missing_marker to Nan 
    	and casts column data as float."""
    df[col_label][df[col_label]==missing_marker] = np.nan
    df[col_label] = df[col_label].astype(float)
    return df		

def plotScoresByCat(df_dict, value_col, bin_col, bin_titles):
	"""Description of function."""
	for type in df_dict:
    subset = []
    for i in [-1, 0, 1]:
        subset.append(df_dict[type][value_col][df_dict[type][bin_col] == i])
    plt.hist(subset, 30)
    plt.legend(bin_titles)
    plt.title(type)
    plt.show()	
	