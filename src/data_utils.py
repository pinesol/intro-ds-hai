'''Functions used to parse data that are not specific to a particular file.'''

import pandas as pd

def parseFile(filename, useful_columns):
    '''Read the given csv file as a dataframe, keeping only the columns in useful_columns.'''
    data = pd.read_table(filename, sep=',')
    data = data[useful_columns]
    return data


def parseGeneralInfoCSV(filepath):
    '''Imports "Hospital_Data.csv" or "Hospital General Information.csv" as a dataframe.
    The useful columns seem to have the same name year, so there is no year param.
    '''
    useful_columns = ['Provider ID', 'Hospital Type', 'Hospital Ownership', 'Emergency Services']
    data = data_utils.parseFile(filepath, useful_columns)
    # 'Conflate Government Federal' with 'Government - Federal'
    data['Hospital Ownership'] = data['Hospital Ownership'].replace('Government Federal', 'Government - Federal')
    return data
