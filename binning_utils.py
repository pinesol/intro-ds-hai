def binByScore1(df, col):
    #cols = df.columns[pd.Series(df.columns).str.contains('Score')]
    df2 = df.copy()
    def binning(score):
        if np.isnan(score):
            return np.nan
        elif score > 1:
            return -1
        else: 
            return 1
    df2 = df2.drop(col, 1)
    df2[col] = df2[col].map(binning)
    return df2

def binByScore2(df, col, lower = -2, upper = 2):
    #cols = df.columns[pd.Series(df.columns).str.contains('Score')]
    df2 = df.copy()
    def binning(z):
            if np.isnan(z):
                return np.nan
            elif z > upper:
                return -1
            elif z < lower:
                return 1
            else: 
                return 0
    mean = np.mean(df2[col])
    sd = np.std(df2[col])
    z_scores = df2[col].map(lambda score: (score - mean)/sd)
    df2 = df2.drop(col, 1)
    df2[col] = z_scores.map(binning)
    return df2
    
def binByScore3(df, col, quantile = .20):
    df2 = df.copy()
    df2 = df2.sort(col, ascending=False)
    ncases = sum(df2[col].notnull())
    nmissing = sum(df2[col].isnull())
    df2[col][:quantile*ncases] = -1
    df2[col][quantile*ncases:-(nmissing+quantile*ncases)] = 0
    df2[col][-(nmissing+quantile*ncases):-nmissing] = 1
    return df2