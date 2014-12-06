
import sys
import pandas as pd

import data_utils
import hai_data_cleanup

def mergeAllTheThings():
    '''Function that creates the final table that will be sent for classification.'''
    data = mergeHAITables()
    data = mergeSCIPDataframes(data)
    # TODO(alex, jackie, maya): glom on moar feature columns!
    # e.g.
    # data = mergeJackiesVolumeData(data) # Make sure to add a function in this file that fills in the nans! Adding asserts is good too!
    # data = mergeMayasSpendingData(data) # Make sure to add a function in this file that fills in the nans! Adding asserts is good too!
    return data

# TODO(alex) make this be able to use the functions in binning_utils.py. You'll have to use parseHaiByBoth.
def mergeHAITables():
    '''Merges all three HAI tables into one table that's ready to be used by a classifier

    The columns are:
    'Compared to National 2014', 'City', 'State', 'Compared to National 2013', 'Compared to National 2012'
    'Compared to National 2014' is the target variable.
    It's index consists of integers, and is named 'Provider ID'.

    This version uses the bucketed scores from hai_data_cleanup._binByCI. This can/should be
    changed going forward. The 'Compared to National' columns are the bucketed HAI scores.

    Returns:
      A dataframe with aforemented columns.
    '''
    # It will be indexed by provider ID, have the location data for the hospital, and the HAI scores from all three years.

    # Extract out the 2014 score column, keeping the index. This will be the target column.
    hai_2014 = hai_data_cleanup.parseHAIbyBinLabel('data/2014/Healthcare Associated Infections - Hospital.csv', '2014')
    # Removing rows with null target variables
    hai_2014 = hai_2014[hai_2014['Compared to National'].notnull()]
    # Renaming target column
    hai_2014['Compared to National 2014'] = hai_2014['Compared to National']
    hai_2014.drop('Compared to National', 1)
    # stripping out everything but the target
    hai_2014_score = pd.DataFrame(hai_2014['Compared to National 2014'], index=hai_2014.index)

    # Getting the 2012 data, stripping out only the HAI Score, converting the nulls to zeros.
    hai_2012 = hai_data_cleanup.parseHAIbyBinLabel('data/2012/Healthcare_Associated_Infections.csv', '2012')
    hai_2012_score = pd.DataFrame(hai_2012['Compared to National'], index=hai_2012.index)
    # Renaming target column
    hai_2012_score['Compared to National 2012'] = hai_2012['Compared to National']
    hai_2012_score = hai_2012_score.drop('Compared to National', 1)
    # filling in NaNs with zeros
    hai_2012_score = hai_2012_score.fillna(0)

    # 2013 HAI will keep its HAI score, and the location data. Also filling in the NaNs with zeros.
    hai_2013 = hai_data_cleanup.parseHAIbyBinLabel('data/2013/Healthcare_Associated_Infections.csv', '2013')
    hai_2013['Compared to National 2013'] = hai_2013['Compared to National']
    hai_2013 = hai_2013.drop('Compared to National', 1)
    hai_2013 = hai_2013.fillna(0) # filling in NaNs with zeros for 2012

    # Creating the final table, join the 2013 location and HAI score data, with the 2012 and 2014 scores.
    final_table = hai_2014_score
    final_table = final_table.join(hai_2013, how = 'left')
    # filling in missing 2013 HAI scores with zeros
    final_table['Compared to National 2013'] = final_table['Compared to National 2013'].fillna(0)
    # joining in the 2012 HAI scores
    final_table = final_table.join(hai_2012_score, how = 'left')
    # filling in missing 2012 HAI scores with zeros
    final_table['Compared to National 2012'] = final_table['Compared to National 2012'].fillna(0)
    
    # Tests
    # There should be exactly 2005 rows in the table
    assert 2005 == len(final_table)
    # The of hospitals in the final table should equal the set from 2014
    assert set(hai_2014_score.index) == set(final_table.index)
    # There shuld be no duplicate provider IDs
    assert sorted(set(hai_2014_score.index)) == sorted(hai_2014_score.index)
    
    return final_table


# TODO fill in NaNs!!
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
    merged_final_data = data.join(merged_scip_dfs, how='left')
    # TODO fill nans

    # TODO add asserts for column names
    # TODO add assert for nans
    return merged_final_data


#TODO(alex): call parseGenerealInfoCSV for all three years and merge them together
def mergeGeneralInfoTables():
    #parseGenerealInfoCSV(filepath, year_str)
    pass 
