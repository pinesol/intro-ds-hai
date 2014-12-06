
import sys
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
    return data

# TODO(alex): Make this function factorize all its features
def mergeHAITables(hai_binning_func):
    # TODO update comments
    # It will be indexed by provider ID, have the location data for the hospital, and the HAI scores from all three years.

    # Extract out the 2014 score column, keeping the index. This will be the target column.
    hai_2014 = hai_data_cleanup.parseHAIboth('data/2014/Healthcare Associated Infections - Hospital.csv', '2014')
    hai_2014 = hai_binning_func(hai_2014)
    # Removing rows with null target variables
    hai_2014 = hai_2014[hai_2014['Bin'].notnull()]
    # Renaming target column
    hai_2014['Bin 2014'] = hai_2014['Bin']
    hai_2014.drop('Bin', 1)
    # stripping out everything but the target
    hai_2014_score = pd.DataFrame(hai_2014['Bin 2014'], index=hai_2014.index)

    # Getting the 2012 data, stripping out only the HAI Score, converting the nulls to zeros.
    hai_2012 = hai_data_cleanup.parseHAIboth('data/2012/Healthcare_Associated_Infections.csv', '2012')
    hai_2012 = hai_binning_func(hai_2012)
    # Renaming target column to reflect year
    hai_2012['Bin 2012'] = hai_2012['Bin']
    hai_2012 = hai_2012.drop('Bin', 1)
    hai_2012_score = pd.DataFrame(hai_2012['Bin 2012'], index=hai_2012.index)
    # filling in NaNs with zeros
    hai_2012_score = hai_2012_score.fillna(0)

    # 2013 HAI will keep its HAI score, and the location data. Also filling in the NaNs with zeros.
    hai_2013 = hai_data_cleanup.parseHAIboth('data/2013/Healthcare_Associated_Infections.csv', '2013')
    hai_2013 = hai_binning_func(hai_2013)
    # Renaming target column to reflect year
    hai_2013['Bin 2013'] = hai_2013['Bin']
    hai_2013 = hai_2013.drop('Bin', 1)
    hai_2013 = hai_2013.fillna(0) # filling in NaNs with zeros for 2012

    # Creating the final table, join the 2013 location and HAI score data, with the 2012 and 2014 scores.
    final_table = hai_2014_score
    final_table = final_table.join(hai_2013, how = 'left')
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
    assert set(hai_2014_score.index) == set(final_table.index)
    # There shuld be no duplicate provider IDs
    assert sorted(set(hai_2014_score.index)) == sorted(hai_2014_score.index)
    
    return final_table

#TODO(alex): call parseGenerealInfoCSV for all three years and merge them together
def mergeGeneralInfoTables():
    #parseGenerealInfoCSV(filepath, year_str)
    pass 
