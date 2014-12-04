
# NOTE from Alex: Jackie, here's how I'd like the interface for these functions to work: 
# Each one should take dataframe as an argument (and possibly also some optional vars, like you've already done on binByScore2 and binByScore3).
# Each one should just assume that 'Compared To National' and 'Score' are in the table, so the 'col' argument isn't needed.
# The returned data frame shouldn't have the 'Compared To National' and 'Score' columns anymore, it should only have the binned column.
# Could you name the column 'Final Score' (or something else, consistency is the important thing)?
# 
def binByScore1(df):
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

def binByScore2(df, upper = 2):
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
    
def binByScore3(df, quantile = .10):
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
    df2['Bin'][:quantile*ncases] = 1
    df2['Bin'][quantile*ncases:-nmissing] = 0
    df2['Bin'][-nmissing:] = np.nan
    df2 = df2.drop([col, 'Compared to National'], 1)
    return df2

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