
import sys
import numpy as np
import pandas as pd

import binning_utils
import data_utils
import hai_data_cleanup

def mergeAllTheThings():
    '''Function that creates the final table that will be sent for classification.'''
    data = mergeHAITables(binning_utils.binByLabel) # TODO: experiment with other binning functions
    data = mergeSCIPDataframes(data)
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
    for index, row in data.iterrows():
        for column in data.columns.values:
            assert not np.isnan(data[column][index]), 'Data with Provider ID %i in column %s is NaN: %s.' % (index, column, data[column][index])
            assert np.isreal(data[column][index]), 'Data with Provider ID %i in column %s has non-numeric data: %s.' % (index, column, data[column][index])
    return data

def mergeHAITables(hai_binning_func):
    '''Merges the three hospital acquired infection data frames into one that can be classified.
    The resulting data frame will be indexed by provider ID, have the location data for the
    hospital, and the HAI scores from all three years.

    The columns of the returned table are: ['Bin 2012', 'Bin 2013', 'Bin 2014', 'City', 'State']
    '''
   # Extract out the 2014 score column, keeping the index. This will be the target column.
    hai_2014 = hai_data_cleanup.parseHAIboth('data/2014/Healthcare Associated Infections - Hospital.csv', '2014')
    hai_2014 = hai_binning_func(hai_2014)
    # Removing rows with null target variables
    hai_2014 = hai_2014[hai_2014['Bin'].notnull()]
    # Renaming target column
    hai_2014['Bin 2014'] = hai_2014['Bin']
    hai_2014 = hai_2014.drop('Bin', 1)
    # Making the two string columns into ints so they can be classified.
    # TODO(alex): this should probably by done in hai_data_cleaup...oh well.
    hai_2014['State'] = pd.Categorical.from_array(hai_2014['State']).codes
    hai_2014['City'] = pd.Categorical.from_array(hai_2014['City']).codes

    # Getting the 2012 data, stripping out only the HAI Score, converting the nulls to zeros.
    hai_2012 = hai_data_cleanup.parseHAIboth('data/2012/Healthcare_Associated_Infections.csv', '2012')
    hai_2012 = hai_binning_func(hai_2012)
    # Renaming target column to reflect year
    hai_2012['Bin 2012'] = hai_2012['Bin']
    hai_2012_score = pd.DataFrame(hai_2012['Bin 2012'], index=hai_2012.index)
    # filling in NaNs with zeros
    hai_2012_score = hai_2012_score.fillna(0)

    # Getting the 2012 data, stripping out only the HAI Score, converting the nulls to zeros.
    hai_2013 = hai_data_cleanup.parseHAIboth('data/2013/Healthcare_Associated_Infections.csv', '2013')
    hai_2013 = hai_binning_func(hai_2013)
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
    expected_columns = ['Bin 2012', 'Bin 2013', 'Bin 2014', 'City', 'State']
    assert expected_columns == sorted(final_table.columns.values), sorted(final_table.columns.values)    
    return final_table

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


if __name__ == '__main__':
    print "Head of final dataframe to classify: %s" % mergeAllTheThings().head()
