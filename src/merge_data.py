
import sys
import numpy as np
import pandas as pd

import binning_utils
import data_utils
import hai_data_cleanup

def mergeAllTheThings(hai_2014_binning_func, hai_2013_binning_func, hai_2012_binning_func):
    '''Function that creates the final table that will be sent for classification.'''
    data = mergeHAITables(hai_2014_binning_func=hai_2014_binning_func, 
                          hai_2013_binning_func=hai_2013_binning_func, 
                          hai_2012_binning_func=hai_2012_binning_func)
    data = mergeSCIPDataframes(data)
    data = processSpendingData(data) #process and glom on spending DF
    data = processVolumeData(data)
    
    # TODO(alex, jackie, maya): glom on moar feature columns!
    # e.g.
    # data = mergeJackiesVolumeData(data)
    # data = mergeMayasSpendingData(data)
    # Make sure each function: 
    # 1) takes a dataframe as input, and returns a data frame with your columns left-joined in.
    # 2) fills in the nans created after joining.
    # 3) All string data has been turned into integers
    # 4) Has assert statments that check that the columns are what they're supposed to be, and anything else you can think of. 

    # Tests
    # Check that every data entry in the dataframe is numeric (using numpy's isreal function).
    testData(data)
    return data

def testData(data):
    for index, row in data.iterrows():
        for column in data.columns.values:
            assert not np.isnan(data[column][index]), 'Data with Provider ID %i in column %s is NaN: %s.' % (index, column, data[column][index])
            assert np.isreal(data[column][index]), 'Data with Provider ID %i in column %s has non-numeric data: %s.' % (index, column, data[column][index])


def mergeAllTheThingsForProxy(target_binning_func, proxy_binning_function):
    '''Function that creates the final table that will be sent for classification.'''
    data = mergeHAITables(hai_2014_binning_func=target_binning_func, 
                          hai_2013_binning_func=proxy_binning_function, 
                          hai_2012_binning_func=target_binning_func)
    data = mergeSCIPDataframes(data)
    data = processSpendingData(data) #process and glom on spending DF
    data = processVolumeData(data)
    
    # Make sure each function: 
    # 1) takes a dataframe as input, and returns a data frame with your columns left-joined in.
    # 2) fills in the nans created after joining.
    # 3) All string data has been turned into integers
    # 4) Has assert statments that check that the columns are what they're supposed to be, and anything else you can think of. 

    # Tests
    # Check that every data entry in the dataframe is numeric (using numpy's isreal function).
    
    for index, row in data.iterrows():
        for column in data.columns.values:
            assert not np.isnan(data[column][index]), 'Data with Provider ID %i in column %s is NaN: %s.' % (index, column, data[column][index])
            assert np.isreal(data[column][index]), 'Data with Provider ID %i in column %s has non-numeric data: %s.' % (index, column, data[column][index])
    return data


def mergeHAITables(hai_2014_binning_func, hai_2013_binning_func, hai_2012_binning_func):
    '''Merges the three hospital acquired infection data frames into one that can be classified.
    The resulting data frame will be indexed by provider ID, have the location data for the
    hospital, and the HAI scores from all three years.

    Args:
      hai_2014_binning_func: The binning function from binning_utils.py that will be applied to the 2014 HAI scores.
      hai_2013_binning_func: The binning function from binning_utils.py that will be applied to the 2013 HAI scores.
      hai_2012_binning_func: The binning function from binning_utils.py that will be applied to the 2012 HAI scores.

    The columns of the returned table are:
    ['AK', 'AL', 'AR', 'AZ', 'Bin 2012', 'Bin 2013', 'Bin 2014', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL',
    'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 
    'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 
    'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']
    '''
    # Extract out the 2014 score column, keeping the index. This will be the target column.
    hai_2014 = hai_data_cleanup.parseHAIboth('data/2014/Healthcare Associated Infections - Hospital.csv', '2014')
    hai_2014 = hai_2014_binning_func(hai_2014)
    # Removing rows with null target variables
    hai_2014 = hai_2014[hai_2014['Bin'].notnull()]
    # Renaming target column
    hai_2014['Bin 2014'] = hai_2014['Bin']
    hai_2014 = hai_2014.drop('Bin', 1)

    # Dropping the City column because there's just too many of them to make each one have its own column.
    hai_2014 = hai_2014.drop('City', 1)
    # Making the state column into 50 different columns
    hai_2014 = pd.concat([hai_2014, pd.get_dummies(hai_2014['State'])], axis=1)
    # Drop the State column now that it's no longer needed.
    hai_2014 = hai_2014.drop('State', 1)

	# Note that for 2012 and 2013, we might want to use the actual scores rather than the bins
	
    # Getting the 2012 data, stripping out only the HAI Score, converting the nulls to zeros.
    hai_2012 = hai_data_cleanup.parseHAIboth('data/2012/Healthcare_Associated_Infections.csv', '2012')
    hai_2012 = hai_2012_binning_func(hai_2012)
    # Renaming target column to reflect year
    hai_2012['Bin 2012'] = hai_2012['Bin']
    hai_2012_score = pd.DataFrame(hai_2012['Bin 2012'], index=hai_2012.index)
    # filling in NaNs with zeros
    hai_2012_score = hai_2012_score.fillna(0)

    # Getting the 2013 data, stripping out only the HAI Score, converting the nulls to zeros.
    hai_2013 = hai_data_cleanup.parseHAIboth('data/2013/Healthcare_Associated_Infections.csv', '2013')
    hai_2013 = hai_2013_binning_func(hai_2013)
    # Renaming target column to reflect year
    hai_2013['Bin 2013'] = hai_2013['Bin']
    hai_2013_score = pd.DataFrame(hai_2013['Bin 2013'], index=hai_2013.index)
    # filling in NaNs with zeros
    hai_2013_score = hai_2013_score.fillna(0)

    # Creating the final table, join the 2013 location and HAI score data, with the 2012 and 2014 scores.
    final_table = hai_2014
    final_table = final_table.join(hai_2013_score, how = 'left')
    # filling in missing 2013 HAI scores with zeros
    final_table['Bin 2013'] = final_table['Bin 2013'].fillna(0)
    # joining in the 2012 HAI scores
    final_table = final_table.join(hai_2012_score, how = 'left')
    # filling in missing 2012 HAI scores with zeros
    final_table['Bin 2012'] = final_table['Bin 2012'].fillna(0)
    
    # Tests
    # There should be exactly 2005 rows in the table
    assert 2005 == len(final_table)
    # The of hospitals in the final table should equal the set from 2014
    assert set(hai_2014.index) == set(final_table.index)
    # There shuld be no duplicate provider IDs
    assert sorted(set(final_table.index)) == sorted(final_table.index)
    # Check that the columns are what we expect.
    expected_columns = ['AK', 'AL', 'AR', 'AZ', 'Bin 2012', 'Bin 2013', 'Bin 2014', 'CA', 'CO', 
                        'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 
                        'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 
                        'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 
                        'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']
    assert expected_columns == sorted(final_table.columns.values), sorted(final_table.columns.values)    
    return final_table



############################################################

def mergeHAITables_Proxy(Target_binning_func, Proxy_binning_func):
    '''Merges the three hospital acquired infection data frames into one that can be classified.
    The resulting data frame will be indexed by provider ID, have the location data for the
    hospital, and the HAI scores from all three years.

    Args:
      Target_binning_func: The binning function from binning_utils.py that will be applied to the 2014, 2013 and 2012 HAI scores.
      Proxy_binning_func: a more generous binning function from binning_utils.py that will be applied to the 2014 HAI scores and will be used as a proxy of the target for training.
      

    The columns of the returned table are:
    ['AK', 'AL', 'AR', 'AZ', 'Bin 2012', 'Bin 2013', 'Bin 2014' , 'Bin 2014 Proxy', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL',
    'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 
    'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 
    'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']
    '''
    # Extract out the 2014 score column, keeping the index. This will be the target column.
    hai_2014 = hai_data_cleanup.parseHAIboth('data/2014/Healthcare Associated Infections - Hospital.csv', '2014')
    hai_2014_target = Target_binning_func(hai_2014)
    hai_2014_Proxy = Proxy_binning_func(hai_2014)

    
    # Removing rows with null target variables
    hai_2014 = hai_2014_target[hai_2014_target['Bin'].notnull()].copy()

    hai_2014['Bin 2014 Proxy'] = hai_2014_Proxy['Bin']
    # Renaming target column
    hai_2014['Bin 2014'] = hai_2014['Bin']
    hai_2014 = hai_2014.drop('Bin', 1)

    # Dropping the City column because there's just too many of them to make each one have its own column.
    hai_2014 = hai_2014.drop('City', 1)
    # Making the state column into 50 different columns
    hai_2014 = pd.concat([hai_2014, pd.get_dummies(hai_2014['State'])], axis=1)
    # Drop the State column now that it's no longer needed.
    hai_2014 = hai_2014.drop('State', 1)

    # Getting the 2012 data, stripping out only the HAI Score, converting the nulls to zeros.
    hai_2012 = hai_data_cleanup.parseHAIboth('data/2012/Healthcare_Associated_Infections.csv', '2012')
    hai_2012 = Target_binning_func(hai_2012)
    # Renaming target column to reflect year
    hai_2012['Bin 2012'] = hai_2012['Bin']
    hai_2012_score = pd.DataFrame(hai_2012['Bin 2012'], index=hai_2012.index)
    # filling in NaNs with zeros
    hai_2012_score = hai_2012_score.fillna(0)

    # Getting the 2012 data, stripping out only the HAI Score, converting the nulls to zeros.
    hai_2013 = hai_data_cleanup.parseHAIboth('data/2013/Healthcare_Associated_Infections.csv', '2013')
    hai_2013 = Target_binning_func(hai_2013)
    # Renaming target column to reflect year
    hai_2013['Bin 2013'] = hai_2013['Bin']
    hai_2013_score = pd.DataFrame(hai_2013['Bin 2013'], index=hai_2013.index)
    # filling in NaNs with zeros
    hai_2013_score = hai_2013_score.fillna(0)

    # Creating the final table, join the 2013 location and HAI score data, with the 2012 and 2014 scores.
    final_table = hai_2014
    final_table = final_table.join(hai_2013_score, how = 'left')
    # filling in missing 2013 HAI scores with zeros
    final_table['Bin 2013'] = final_table['Bin 2013'].fillna(0)
    # joining in the 2012 HAI scores
    final_table = final_table.join(hai_2012_score, how = 'left')
    # filling in missing 2012 HAI scores with zeros
    final_table['Bin 2012'] = final_table['Bin 2012'].fillna(0)
    
    # Tests
    # There should be exactly 2005 rows in the table
    assert 2005 == len(final_table)

    
    # The of hospitals in the final table should equal the set from 2014
    assert set(hai_2014.index) == set(final_table.index)
    # There shuld be no duplicate provider IDs
    assert sorted(set(final_table.index)) == sorted(final_table.index)
    # Check that the columns are what we expect.
    
    
    expected_columns = ['AK', 'AL', 'AR', 'AZ', 'Bin 2012', 'Bin 2013', 'Bin 2014', 'Bin 2014 Proxy', 'CA', 'CO', 
                        'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 
                        'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 
                        'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 
                        'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']
    assert expected_columns == sorted(final_table.columns.values), sorted(final_table.columns.values)

    return final_table

    ########################################################################


def createAllDatasets(hai_2014_binning_func, hai_2013_binning_func, hai_2012_binning_func):
    '''Returns the following two datasets: "autoregressive" (only HAI data), and "all_data".
    '''
    dataset_dict = {}
    hai_data = mergeHAITables(hai_2014_binning_func=hai_2014_binning_func,
                              hai_2013_binning_func=hai_2013_binning_func, 
                              hai_2012_binning_func=hai_2012_binning_func)
    autoregressive = pd.concat([hai_data['Bin 2014'], hai_data['Bin 2013'], hai_data['Bin 2012']], axis=1)
    
    all_data = mergeSCIPDataframes(hai_data)
    all_data = processSpendingData(all_data)
    all_data = processVolumeData(all_data)

    for dataset in dataset_dict.values():
        testData(dataset)
    return autoregressive, all_data


def mergeSCIPDataframes(data):
    '''Merges a list of scrip dataframes into one that has columns from each.
    Assumes missing data has been removed, that all column names are unique, 
    and that all tables have the same index.

    The columns of the returned table are:
    ['SCIP_INF_1_1', 'SCIP_INF_2_1', 'SCIP_INF_3_1', 'SCIP_INF_10_1', 'SCIP_INF_1_2', 'SCIP_INF_2_2', 
    'SCIP_INF_3_2', 'SCIP_INF_10_2']
    '''
    scip_dfs = [data_utils.ImportSCIPData('2012'), data_utils.ImportSCIPData('2013')]

    new_dfs = []
    for i, df in enumerate(scip_dfs):
        new_columns_map = {column_name: column_name+'_'+str(i+1)
                           for column_name in df.columns.values}
        new_df = df.rename(columns=new_columns_map)
        new_dfs.append(new_df)
    merged_scip_dfs = pd.concat(new_dfs, axis=1)
    # Check that the columns are what we expect.
    expected_columns = ['SCIP_INF_10_1', 'SCIP_INF_10_2', 'SCIP_INF_1_1', 'SCIP_INF_1_2',
                        'SCIP_INF_2_1', 'SCIP_INF_2_2', 'SCIP_INF_3_1', 'SCIP_INF_3_2']
    assert expected_columns == sorted(merged_scip_dfs.columns.values), sorted(merged_scip_dfs.columns.values)
    # Merge into final data frame
    merged_final_data = data.join(merged_scip_dfs, how='left')
    # Remove NaNs with column means
    merged_final_data = merged_final_data.fillna(merged_final_data.mean().round())
    return merged_final_data

# TODO(alex): call parseGenerealInfoCSV for all three years and merge them together
def mergeGeneralInfoTables():
    #parseGenerealInfoCSV(filepath, year_str)
    pass 


def processSpendingData(base_DF):
    ''' Function retrieved spending data, cleans it ad merged with base_DF. missing values are populated with mean of yearly spending.'''
    years = ['2012', '2013']
    DFs = []
    for y in years:
        file_path = 'data/%s/Medicare Spending Per Patient.csv' %y
        useful_columns = ['Spending per Hospital Patient with Medicare']
        spending_df = data_utils.parseFileWithIndex(file_path, useful_columns)
        spending_df = hai_data_cleanup.removeRowsWithMissingTarget(spending_df, 'Spending per Hospital Patient with Medicare')
        spending_df['Spending per Hospital Patient with Medicare'] = spending_df['Spending per Hospital Patient with Medicare'].astype(float)

        spending_df.columns = ['Spending_per_patient_%s' %y]
        DFs.append(spending_df)


    spending_total = DFs[0].join(DFs[1], how = 'outer') # merge spending DFs to eachother
    #    print spending_total.head()
    joined_df = base_DF.join(spending_total, how = 'left') #merge spending DF with base. keep only lines with base_df provider ID's

    joined_df.Spending_per_patient_2012.replace(np.nan, joined_df.Spending_per_patient_2012.mean(), inplace=True )
    joined_df.Spending_per_patient_2013.replace(np.nan, joined_df.Spending_per_patient_2013.mean(), inplace=True )
    
    return joined_df

def processVolumeData(aggregated):
	df_2013 = data_utils.parseFileWithIndex('data/2013/Medicare Volume Measures.csv', 
                               ['Diagnosis Related Group', 'Number Of Cases'])
	df_2012 = data_utils.parseFileWithIndex('data/2012/Medicare Payment and Volume Measures.csv', 
                               ['Diagnosis Related Group', 'Number Of Cases'])
    
	mincases = '10'
	missing_marker = '*'
	test_column = 'Chest Pain 2013';
	
	reformatted = []
	for df in [df_2013, df_2012]:
		df['Number Of Cases'][df['Number Of Cases'] == missing_marker] = mincases
		df['Number Of Cases'] = df['Number Of Cases'].str.replace(",", "")
		df['Number Of Cases'] = df['Number Of Cases'].astype(float)
    
		hospitals = pd.unique(df.index)
		cols = pd.unique(df['Diagnosis Related Group'])
    
		df2 = pd.DataFrame(data = 0, index = hospitals, columns = cols)
		for col in cols:
			x = df['Number Of Cases'][df['Diagnosis Related Group'] == col]
			df2[col] = x
		reformatted.append(df2)
		assert 'Number of Cases' not in df2.columns
		assert 'Diagnosis Related Group' not in df2.columns
	
	reformatted[0].columns = reformatted[0].columns.map(lambda x: str(x) + ' 2013')
	volume = reformatted[0].join(reformatted[1], how = 'outer', rsuffix=' 2012')
	assert test_column in volume.columns
	volume[pd.isnull(volume)] = float(mincases) 
	merged_final_data = aggregated.join(volume, how='left')
	merged_final_data = merged_final_data.fillna(float(mincases))
	return merged_final_data
    
    
if __name__ == '__main__':
    print "Head of final dataframe to classify: %s" % mergeAllTheThings().head()
