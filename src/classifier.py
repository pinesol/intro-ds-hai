
import matplotlib
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import KFold
from sklearn.metrics import roc_curve, auc

# Local files, intro-ds-hai/src/ directly must be in the path.
import data_utils
import merge_data


def testLogisticRegression():
    initial_data = merge_data.mergeAllTheThings()
    
    Y = initial_data['Bin 2014']
    X = initial_data.drop('Bin 2014', 1)

    print 'The total number of hospitals is', len(Y) # 2005
    print 'The number of hospitals with a positive label is', sum(Y) # 23!
    # Base rate is 23/2005 ~= 1.1%

    train_ix, test_ix = data_utils.splitTestTrainIndices(initial_data, 'Bin 2014', 
                                                         train_size=0.8)
    X_train, X_test = X.ix[train_ix], X.ix[test_ix]
    Y_train, Y_test = Y.ix[train_ix], Y.ix[test_ix]

    # TODO try this without the fancy split algo, see the difference
    lr_classifier = BestAUCLogisiticRegression(X_train, Y_train)
    
    # Evaluate on the test set
    final_auc = metrics.roc_auc_score(y_true = Y_test, 
                                      y_score=lr_classifier.decision_function(X_test)) # predict_proba?
    print 'logistic regression gets an AUC of:', final_auc
    # Woot AUC 0.73!
    # Once volume data was added, AUC went down to 0.53!!!
    # TODO make roc graph and choose best cutoff by examining it graphically, optimize for recall.
    

def BestAUCLogisiticRegression(X, Y, regularization_type='l2'):
    logistic_regression_params = [10**i for i in range(-3,7)] + [1e30]
    best_c = None
    best_auc = None
    best_classifier = None

    for c in logistic_regression_params:
        classifier = linear_model.LogisticRegression(C=c, penalty=regularization_type) 
        auc = meanAUCCrossValidation(X, Y, classifier)
        if not best_c or best_auc < auc:
            best_c = c
            best_auc = auc
            best_classifier = classifier
    print 'best C for logistic regression', best_c, 'results in AUC', best_auc
    # L2: Best value for C seems to be 100, it gives AUC ~= .70. These means that some regularization is helpful.
    # L1: Best value for C seems to be 10, it gives AUC ~= .68
    return best_classifier
    

def meanAUCCrossValidation(X, Y, classifier, num_folds=5):
    cross_valdation_obj = KFold(n=X.shape[0], n_folds = num_folds, random_state=42)
    aucs = []
    for train_index, test_index in cross_valdation_obj:
        X_train = X.iloc[train_index]
        Y_train = Y.iloc[train_index]
        X_test = X.iloc[test_index]
        Y_test = Y.iloc[test_index]
       
        scores = classifier.fit(X_train, Y_train).predict_proba(X_test)[:,1] # TODO use .decision_function(X_test)? seems to work out the same
        auc = metrics.roc_auc_score(Y_test, scores)
        aucs.append(auc)

    return np.mean(aucs)


# Plan, I update these functions to do the following:
# Vary on different versions of the data (autoregressive, standard binning, different binning, w/general info, w/volume, etc.)
# For each classifier, find best AUC, that's the best classifier+data pair, choose cutoff point best for recall somehow
# Make lots of ROC graphs


# Take best classifier+binning, split out 2014 and 2013 Bin. Train on 2013, test on 2014

# TODO test what is our baseline? 
#  If the positive class happens x% of the time, then the baseline classifier just picks randomly at that rate?
# TODO test autoregressive model
# TODO calculate recall
# TODO test SVM
# TODO add general info data
# TODO test with proxy 
# TODO write agenda for tomorrow

# TODO questions for the professor:
# Should we use L1 or L2 regularization?
# What is correct, decision_function, or predict_proba?
#how many true positives is our auc based off of?

if __name__ == '__main__':
    testLogisticRegression()
