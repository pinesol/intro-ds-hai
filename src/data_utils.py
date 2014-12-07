'''Functions used to parse data that are not specific to a particular file.'''

import numpy as np
import pandas as pd

# DEPRECATED
def parseFile(filename, useful_columns):
    '''Read the given csv file as a dataframe, keeping only the columns in useful_columns.'''
    data = pd.read_table(filename, sep=',')
    data = data[useful_columns]
    return data

def parseFileWithIndex(filename, useful_columns):
    '''Read the given csv file as a dataframe, keeping only the columns in useful_columns.
    
    The first column, which are assumed to be provider ID values, will be used as the dataframe
    index. The values of this column must be converted from strings to integers, because the indexes
    should be the same across different dataframes, and some provider ID values have leading zeroes,
    and some don't. Making the index have integer values allows all tables keyed with provider ID to 
    be easily joined together.
    As a result of this, all non-integer provider IDs are thrown out.

    Args:
      filename: A string filename that points to a CSV file whose header is the first line.
      useful_columns: A list of strings that indicate the columns from the file that should be 
        retained.

    Returns:
      A dataframe that has an integer-valued 'Provider ID' as its index, and only the columns
      listed in useful_columns.
    '''
    # Read in the data, making the first column the index.
    data = pd.read_csv(filename, sep = ',', index_col = 0)
    # Throw out all rows that have a non-integer for a provider ID. This gets rid of the rows with 
    # non-integer provider IDs, e.g. '01014F'.
    data = data[data.index.map(lambda x: (isinstance(x, int) or (isinstance(x, str) and x.isdigit())))]
    # Convert the index to integers now that the non-integer index values have been removed.
    data.index = data.index.astype(int)
    # Make sure the index is called 'Provider ID'.
    data.index.names = ['Provider ID']
    # Filter out non-useful columns
    data = data[useful_columns]
    return data

# TODO this auto converts floats to ints, which is probably wrong.
def factorizeFeatures(features_data):
    '''Makes all string columns into ints, using category numbers if the column int-izable.
    
    This assumes all 'missing data' has been cleared from the dataframe.

    Args:
      features_data: A dataframe that contains only the features that will be used in a sklearn 
        classifier.

    Returns:
      A dataframe that has had it numeric values changed to integers.
    '''
    X = pd.DataFrame()
    for column in list(data.columns):
        try:
            X[column] = data[column].astype(int)
        except ValueError:
            print 'cant int-ify column, assuming categorical', column
            X[column] = pd.Categorical.from_array(data[column]).codes
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

def ImportSCIPData(year_str):
    '''The returned columns are [SCIP_INF_1, SCIP_INF_2, SCIP_INF_3, SCIP_INF_10]'''
    useful_columns = ["Surgery patients who were given an antibiotic at the right time (within one hour before surgery) to help prevent infection",
                      "Surgery patients who were given the right kind of antibiotic to help prevent infection",
                      "Surgery patients whose preventive antibiotics were stopped at the right time (within 24 hours after surgery)",
                      "Patients having surgery who were actively warmed in the operating room or whose body temperature was near normal"]
    df = parseFileWithIndex('data/'+ year_str + '/Process of Care Measures - SCIP.csv', useful_columns)   
    # Rename columns
    new_column_name_map = {useful_columns[0]: 'SCIP_INF_1',
                           useful_columns[1]: 'SCIP_INF_2',
                           useful_columns[2]: 'SCIP_INF_3',
                           useful_columns[3]: 'SCIP_INF_10'}
    df = df.rename(columns=new_column_name_map)
    # There are two possible bad values: 'Not Available' and 'Too few cases'. 
    # Replacing the latter with the former makes it easier to replace all of these values.
    bad_value = 'Not Available'
    df = df.replace(to_replace='Too few cases', value=bad_value)
    # Give 'Not Available' the mean value.
    for column_name in df.columns.values:
        if sum((df[column_name] == bad_value)) > 0:
            column_mean = df[column_name][(df[column_name] != bad_value)].astype(int).mean().round()
            # TODO(alex): This line will add dumy values. Commenting it out for now.
            #df[column_name + "_dummy"] = (df[column_name] != bad_value) * 1
            df[column_name] = df[column_name].replace(to_replace=bad_value, value=column_mean).astype(int)
    return df


def splitTestTrainIndicesWithProxy(DF, target_column_name, proxy_column_name, train_size = 0.8):
    """This splits a dataframe into training and testing dataframes, ensuring up the positive target values 
    are distributed between them according to the given ratio. 
    
    This function splits the training and test data according to the train_size value.
    The training data gets 100*train_size percent of the data, and the test data gets 100*(1-train_size)
    percent of the data.
    Additionally, this ensures that the training set has at least 100*train_size percent of the positive target
    values AND 100*train_size percent of the proxy training values.
    Likewise it ensures that the test set has at least 100*(1-train_size) percent of the positive target
    values AND 100*(1-train_size) percent of the proxy test values.
    
    Arguments:
       DF: a pandas dataframe on which to do the analysis.
           DF must contain at the very least the columns: [proxy_column_name, target_column_name] and one feature.

       target_column_name: the name of the column containing the binary target variable.
       
       proxy_column_name: the name of the column containing the binary proxy variable.
       
       train_size: float. the mean fraction of overall positives we want the training DF to contain. default = 0.8.
    Returns:
        (train_ix, test_ix): A tuple of sets. The first set has the index values of DF that should go in the training data.
           The second set is has the index values of DF that should go in the test data.
    Raises:
        Exception: If a training and test sets that conform to the train_size parameter after several attempts, 
          an exception is thrown to prevent an infinite loop.
    """
    super_set = set(DF.index)
    condition_a = condition_b = condition_c = condition_d = False
    
    # calculate the minimum number of positives in the target and proxy 
    min_positives_target_train = np.floor(np.sum(DF[target_column_name])*train_size)
    min_positives_proxy_train = np.floor(np.sum(DF[proxy_column_name])*train_size)
    # The test set must have (1-train_size) positives at least.
    min_positives_target_test = np.floor(np.sum(DF[target_column_name])*(1-train_size))
    min_positives_proxy_test = np.floor(np.sum(DF[proxy_column_name])*(1-train_size))
   
    # The train and test indexes to determine.
    train_ix = None
    test_ix = None
    
    # Have we found enough positive target variables in the training data?
    min_positive_target_train_found = False
    # Have we found enough positive proxy variables in the training data?
    min_positive_proxy_train_found = False
    # Have we found enough positive target variables in the test data?
    min_positive_target_test_found = False
    # Have we found enough positive proxy variables in the test data?
    min_positive_proxy_test_found = False
    
    MAX_ITERATIONS = 100
    iterations = 1
    
    while not (min_positive_target_train_found and min_positive_proxy_train_found and
               min_positive_target_test_found and min_positive_proxy_test_found):
        if iterations > MAX_ITERATIONS:
            raise Exception('Couldn\'t find an acceptable training/test data split!')
        iterations += 1
        
        # Randomly choose a training/test split. The training/test split is 80/20.
        train_ix = np.random.choice(DF.index, size=np.floor(train_size*len(DF.index)), replace=False)
        train_ix = set(train_ix)
        test_ix = super_set-train_ix

        # calculate number of positives in target
        positives_target_train = DF[target_column_name].ix[train_ix].sum()
        positives_target_test = DF[target_column_name].ix[test_ix].sum()
        # calculate number of positives in proxy
        positives_proxy_train = DF[proxy_column_name].ix[train_ix].sum()
        positives_proxy_test = DF[proxy_column_name].ix[test_ix].sum()
        
        # Make sure there is at least the minimum amount of positives in target for train and test.
        min_positive_target_train_found = positives_target_train >= min_positives_target_train
        min_positive_target_test_found = positives_target_test >= min_positives_target_test
        # Make sure there is at least the minimum amount of positives in proxy for train and test.
        min_positive_proxy_train_found = positives_proxy_train >= min_positives_proxy_train
        min_positive_proxy_test_found = positives_proxy_test >= min_positives_proxy_test
        
    # make sure we didn't lose any indices
    assert (train_ix | test_ix) == super_set
    
    #print 'Positives in target training:', positives_target_train
    #print 'Positives in proxy training:', positives_proxy_train
    #print 'Positives in target test:', positives_target_test
    #print 'Positives in proxy test:', positives_proxy_test
    
    return train_ix, test_ix

def splitTestTrainIndices(DF, target_column_name, train_size = 0.8):
    """This splits a dataframe into training and testing dataframes, ensuring up the positive target values 
    are distributed between them according to the given ratio. 
    
    This function is just like splitTestTrainIndicesWithProxy above, except there is no proxy column.

    Arguments:
       DF: a pandas dataframe on which to do the analysis.
           DF must contain at the very least the columns: [target_column_name] and one feature.
       target_column_name: the name of the column containing the binary target variable.
       train_size: float. the mean fraction of overall positives we want the training DF to contain. default = 0.8.
    Returns:
        (train_ix, test_ix): A tuple of sets. The first set has the index values of DF that should go in the training data.
           The second set is has the index values of DF that should go in the test data.
    Raises:
        Exception: If a training and test sets that conform to the train_size parameter after several attempts, 
          an exception is thrown to prevent an infinite loop.
    """
    super_set = set(DF.index)
    condition_a = condition_b = condition_c = condition_d = False
    
    # calculate the minimum number of positives in the target
    min_positives_target_train = np.floor(np.sum(DF[target_column_name])*train_size)
    # The test set must have (1-train_size) positives at least.
    min_positives_target_test = np.floor(np.sum(DF[target_column_name])*(1-train_size))
   
    # The train and test indexes to determine.
    train_ix = None
    test_ix = None
    
    # Have we found enough positive target variables in the training data?
    min_positive_target_train_found = False
    # Have we found enough positive target variables in the test data?
    min_positive_target_test_found = False
    
    MAX_ITERATIONS = 100
    iterations = 1
    
    while not (min_positive_target_train_found and min_positive_target_test_found):
        if iterations > MAX_ITERATIONS:
            raise Exception('Couldn\'t find an acceptable training/test data split!')
        iterations += 1
        
        # Randomly choose a training/test split. The training/test split is 80/20.
        train_ix = np.random.choice(DF.index, size=np.floor(train_size*len(DF.index)), replace=False)
        train_ix = set(train_ix)
        test_ix = super_set-train_ix

        # calculate number of positives in target
        positives_target_train = DF[target_column_name].ix[train_ix].sum()
        positives_target_test = DF[target_column_name].ix[test_ix].sum()
        
        # Make sure there is at least the minimum amount of positives in training.
        min_positive_target_train_found = positives_target_train >= min_positives_target_train
        # Make sure there is at least the minimum amount of positives in test.
        min_positive_target_test_found = positives_target_test >= min_positives_target_test
        
    # make sure we didn't lose any indices
    assert (train_ix | test_ix) == super_set
    
    #print 'Positives in target training:', positives_target_train
    #print 'Positives in target test:', positives_target_test
    
    return train_ix, test_ix
