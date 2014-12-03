'''Functions to manipulate the "Healthcare Associated Infections - Hospital.csv" file, and those like it.'''

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_curve, auc
# Local file, intro-ds-hai/src/ directly must be in the path.
import data_utils


def convertOldHAIDataframe(old_df, year_str):
    '''Replaces the 'Measure' column with the 'Measure ID' column. year_str can be either '2012' or '2013' for now.'''
    # TODO both maps have other HAI_1 measures, like upper and lower bounds
    # TODO 2013_MEASURE_MAP can be extended to have entries for HAI 1 through HAI 4.
    # Rename the scores and compare rows to correspond to 2014 format
    MEASURE_MAP_2013 = {'Central-Line-Associated Blood Stream Infections (CLABSI)': 'HAI_1_SIR',
    					'CLABSI Compared to National': 'HAI_1_compare'}
    MEASURE_MAP_2012 = {'Central Line Associated Blood Stream Infections (CLABSI)': 'HAI_1_SIR',
    					'CLABSI Upper Confidence Limit': 'HAI_1_compare'}

    def measure_map_func(measure_name):
        if year_str == '2013' and measure_name in MEASURE_MAP_2013:
            return MEASURE_MAP_2013[measure_name] 
        elif year_str == '2012' and measure_name in MEASURE_MAP_2012:
            return MEASURE_MAP_2012[measure_name]
        return None

    old_df['Measure ID'] = old_df['Measure'].map(measure_map_func)
    old_df = old_df.drop('Measure', 1)
    return old_df
    
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
    for marker in missing_marker:
    	df[col_label][df[col_label]==marker] = np.nan
    df[col_label] = df[col_label].astype(float)
    return df

def parseHAIFile(filename, year_str):
    '''year_str can be either '2012', '2013', or '2014' for now.'''
    COLUMNS_2014 = ['Provider ID', 'City', 'State', 'ZIP Code', 'County Name', 'Measure ID', 'Score']
    COLUMNS_2013 = ['Provider ID', 'City', 'State', 'ZIP Code', 'County Name', 'Measure', 'Score']
    COLUMNS_2012 = ['Provider ID', 'City', 'State', 'ZIP Code', 'County Name', 'Measure', 'Score']
    useful_columns_map = {'2014': COLUMNS_2014, '2013': COLUMNS_2013, '2012': COLUMNS_2012}
    
    data = data_utils.parseFile(filename, useful_columns_map[year_str])
    #data = data.set_index(data['Provider ID'])
    #data = data.drop('Provider ID', 1)
    if year_str == '2012' or year_str == '2013':
        data = convertOldHAIDataframe(data, year_str)
    assert 'Measure ID' in data.columns
    assert 'Measure' not in data.columns
    data = data[data['Measure ID'] == 'HAI_1_SIR']
    data = convertToNumeric(data, 'Score', ['Not Available', '-'])
    # Make Provider ID an integer so we can use it as a merge key. 
    # Other tables have padding zeros, so converting to int standardizes them.
    data['Provider ID'] = data['Provider ID'].astype(int)
    return data

def parseHAIbyBinLabel(filename, year_str):
    '''year_str can be either '2012', '2013', or '2014' for now.
    Analog of parseHAIFile, but instead of using Score as target, gives numerical indicator for
    Compared to National. -1 means worse than average, 0 no different, 1 better than average.
    Actual SIR value, confidence intervals, etc. will not be included in returned df'''

    COLUMNS_2014 = ['Provider ID', 'City', 'State', 'ZIP Code', 'County Name', 'Measure ID', 'Compared to National']
    COLUMNS_2013 = ['Provider ID', 'City', 'State', 'ZIP Code', 'County Name', 'Measure', 'Score']
    COLUMNS_2012 = ['Provider ID', 'City', 'State', 'ZIP Code', 'County Name', 'Measure', 'Score']
    useful_columns_map = {'2014': COLUMNS_2014, '2013': COLUMNS_2013, '2012': COLUMNS_2012}
    
    data = data_utils.parseFile(filename, useful_columns_map[year_str])
    #data = data.set_index(data['Provider ID'])
    #data = data.drop('Provider ID', 1)
    if year_str == '2013':
        data = convertOldHAIDataframe(data, year_str)
        data['Compared to National'] = data['Score'] #rename the Score column
        data = data.drop('Score', 1)
    elif year_str == '2012': 
    # 2012 doesn't come with its own labels. Instead, we use the CIs to construct the labels.
    	data = binByCI(data, 'CLABSI Lower Confidence Limit', 'CLABSI Upper Confidence Limit', 'Score')
    	data = convertOldHAIDataframe(data, year_str) 
    	data = data.drop('Score', 1)
    elif year_str == '2014':
    	data = data.replace({'Measure ID': {'HAI_1_SIR':'HAI_1_compare'}})
    assert 'Measure ID' in data.columns
    assert 'Measure' not in data.columns
    assert 'Compared to National' in data.columns
    assert 'Score' not in data.columns
    data = data[data['Measure ID'] == 'HAI_1_compare']
    if year_str !='2012':
    	data = categoricalToIndicator(data, 'Compared to National')
    # Make Provider ID an integer so we can use it as a merge key. 
    # Other tables have padding zeros, so converting to int standardizes them.
    #data['Provider ID'] = data['Provider ID'].astype(int)
    return data
    
def binByCI(data, lowerLabel, upperLabel, valueLabel):
	"""For a dataframe with no bin labels, takes the limits of confidence interval
	and converts them into a numerical indicator, -1, 1, or 0. If the interval
	contains 1, we will call this no different (i.e. 0)"""
	hospitals = np.unique(data['Provider ID'])
	data = convertToNumeric(data, valueLabel, ['Not Available', '-'])
	cp = 'Compared to National'
	data[cp] = np.nan
	for h in hospitals:
		hospital = data.loc[data['Provider ID'] == h]
		lower = hospital.loc[hospital['Measure'] == lowerLabel, valueLabel]
		upper = hospital.loc[hospital['Measure'] == upperLabel, valueLabel]
		lower = lower.get_values()[0]
		upper = upper.get_values()[0]
		if upper < 1:
			data.loc[hospital.index, cp] = 1
		elif lower > 1:
			data.loc[hospital.index, cp] = -1
		elif (lower < 1) & (upper > 1):
			data.loc[hospital.index, cp] = 0
	return data
	
def filterByMeasureID(data, measure_id):
    data = data.loc[data['Measure ID'] == measure_id]
    # Drop the measure id column, since it's the same for all rows now.
    data = data.drop('Measure ID', 1)
    return data

def removeRowsWithMissingTarget(data, target_column):
    MISSING_VALUE = 'Not Available'
    data = data[data[target_column] != MISSING_VALUE]
    return data
