'''Functions used to parse data that are not specific to a particular file.'''

import pandas as pd

def parseFile(filename, useful_columns):
    '''Read the given csv file as a dataframe, keeping only the columns in useful_columns.'''
    data = pd.read_table(filename, sep=',')
    data = data[useful_columns]
    return data

def factorizeFeatures(train_data):
    '''Makes all string columns into ints, using category numbers if the column isn't convertable into an int directly.'''
    X = pd.DataFrame()
    for column in list(train_data.columns):
        try:
            X[column] = train_data[column].astype(int)
        except ValueError:
            print 'cant int-ify column, assuming categorical', column
            X[column] = pd.Categorical.from_array(train_data[column]).codes
    return X

def parseGeneralInfoCSV(filepath, year_str):
    '''Imports "Hospital_Data.csv" or "Hospital General Information.csv" as a dataframe.
    
    This function throws out the 'Government Federal' hospitals because they have no HAI
    score and non-integer Provider IDs.

    Returns:
      The returned dataframe has the following columns:
      'Provider ID' (int), 'Hospital Type' (str), 'Hospital Ownership' (str), 
      'Emergency Services' (str). 
    '''
    COLUMNS_OLD = ['Provider Number', 'Hospital Type', 'Hospital Ownership', 'Emergency Services']
    COLUMNS_NEW = ['Provider ID', 'Hospital Type', 'Hospital Ownership', 'Emergency Services']
    useful_columns = COLUMNS_NEW if year_str == '2014' else COLUMNS_OLD
    data = parseFile(filepath, useful_columns)
    # Change 'Provider Number' to 'Provider ID' to match the 2014 version.
    if year_str != '2014':
        data = data.rename(columns={'Provider Number': 'Provider ID'})
    # Throw out 'Government Federal' hospitals -- they have no HAI score and 
    # they have non-integer Provider IDs.
    data = data[data['Hospital Ownership'] != 'Government Federal']
    # Make Provider ID an integer so we can use it as a merge key. 
    # Other tables have padding zeros, so converting to int standardizes them.
    data['Provider ID'] = data['Provider ID'].astype(int)
    return data

def mergeGeneralInfoIntoHAIFrame(hai_df, general_df):
    '''Merges the kind of dataframe returned by parseGeneralInfoCSV into a HAI dataframe.

    Merges on the 'Provider ID' column. All rows in hai_df will be kept.
    '''
    return pd.merge(hai_df, general_df, on='Provider ID', how='left')
