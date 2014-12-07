# Target column is df['Bin'] for all binning functions
# 1: Worse than average
# 0: Average or above average
# Functions are equipped to handle nans, so it's fine to throw out nans after calling binning
# Input to function should be a single year dataframe output by hai_data_cleanup.parseHAIboth

import numpy as np
import pandas as pd

# This exposes the 23 positives, as given from the original data.
def binByLabel(df):
    '''Uses the pre-supplied bin labels output by parseHAIbyBinLabel function.
    Bin = 1 if Compared to National is worse than average, otherwise 0.
    Returns dataframe with target in df['Bin'].'''
    df2 = df.copy()
    col = 'Compared to National'
    def binning(score):
        if np.isnan(score):
            return np.nan
        elif score == -1:
            return 1
        else: 
            return 0
    df2['Bin'] = df2[col].map(binning)
    df2 = df2.drop(['Score', col], 1)
    return df2

# This results in 97 positives in 2014 when using quantile 0.1. 
def binByScore1(df, upper = 2):
    '''All SIR scores greater than k standard deviations above the mean labeled 
    as positive (Bin=1), otherwise 0. Default = 2 SD above mean.
    Returns dataframe with target in df['Bin'].'''
    df2 = df.copy()
    col = 'Score'
    def binning(z):
            if np.isnan(z):
                return np.nan
            elif z > upper:
                return 1
            else: 
                return 0
    mean = np.mean(df2[col])
    sd = np.std(df2[col])
    z_scores = df2[col].map(lambda score: (score - mean)/sd)
    df2['Bin'] = z_scores.map(binning)
    df2 = df2.drop([col, 'Compared to National'], 1)
    return df2

# This results in 201 positives in 2014 when using quantile 0.1.
def binByScore2(df, quantile = .10):
    '''All SIR scores in the worst k percentile of the data labeled 
    as positive (Bin=1), otherwise 0. Default = highest 10th percentile.
    Returns dataframe with target in df['Bin'].'''
    df2 = df.copy()
    col = 'Score'
    if quantile > 1:
    	quantile = quantile / 100.0
    df2 = df2.sort(col, ascending=False, na_position='last')
    ncases = sum(df2[col].notnull())
    nmissing = sum(df2[col].isnull())
    bin_col = pd.Series([0]*len(df2.index), index=df2.index)
    bin_col.iloc[:int(round(quantile*ncases))] = 1
    bin_col.iloc[int(round(quantile*ncases)):-nmissing] = 0
    bin_col.iloc[-nmissing:] = np.nan
    df2['Bin'] = bin_col
    df2 = df2.drop([col, 'Compared to National'], 1)
    return df2

# This results in 296 positives in 2014.
def binByScore3(df):
    '''All SIR scores greater than 1 labeled as positive (Bin=1), otherwise 0.
    Returns dataframe with target in df['Bin'].'''
    df2 = df.copy()
    col = 'Score'
    def binning(score):
        if np.isnan(score):
            return np.nan
        elif score > 1:
            return 1
        else: 
            return 0
    df2['Bin'] = df2[col].map(binning)
    df2 = df2.drop([col, 'Compared to National'], 1)
    return df2
    
