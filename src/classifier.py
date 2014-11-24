

import matplotlib
import pandas as pd
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_curve, auc

# Local files, intro-ds-hai/src/ directly must be in the path.
import data_utils
import hai_data_cleanup


def fakeBucketTargetScores(target_series):
    # TODO make real bucket function
    return target_series.astype(float).map(lambda score: 0 if score < 1 else 1)

def trainLogisticRegression():
    HAI_FILE = '/Users/pinesol/intro-ds-hai/data/2014/Healthcare Associated Infections - Hospital.csv'
    year_str = '2014'
    data = hai_data_cleanup.parseHAIFile(HAI_FILE, year_str)
    data = hai_data_cleanup.filterByMeasureID(data, 'HAI_1_SIR')
    target_column = 'Score'
    data = hai_data_cleanup.removeRowsWithMissingTarget(data, target_column)

    # Merge General Info into the data
    GENERAL_FILE = '/Users/pinesol/intro-ds-hai/data/2014/Hospital General Information.csv'
    general_data = data_utils.parseGeneralInfoCSV(GENERAL_FILE, year_str)
    data = data_utils.mergeGeneralInfoIntoHAIFrame(data, general_data)
    
    Y = fakeBucketTargetScores(data['Score'])
    X = data_utils.factorizeFeatures(data.drop('Score', 1))
    # arbitrary test size
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

    #The above returns numpy arrays. I'd prefer to store them as data frames.
    X_train = pd.DataFrame(X_train, columns = X.columns.values)
    X_test = pd.DataFrame(X_test, columns = X.columns.values)
    Y_train = pd.Series(Y_train)
    Y_test = pd.Series(Y_test) 
    assert len(X_train) == len(Y_train)
    assert len(X_test) == len(Y_test)

    lr_classifier = linear_model.LogisticRegression(C=1e30).fit(X_train, Y_train)
    lr_scores = lr_classifier.decision_function(X_test)
    fpr, tpr, thresholds = roc_curve(Y_test, lr_scores)
    print 'logistic regression AUC:', auc(fpr, tpr)


if __name__ == '__main__':
    trainLogisticRegression()
