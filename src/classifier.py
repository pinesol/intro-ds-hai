
import matplotlib
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn import metrics
from sklearn.cross_validation import train_test_split, KFold
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import auc, roc_curve

# Local files, intro-ds-hai/src/ directly must be in the path.
import binning_utils
import data_utils
import merge_data


def testLogisticRegression():
    data = merge_data.mergeAllTheThings(binning_utils.binByLabel)
    
    Y = data['Bin 2014']
    X = data.drop('Bin 2014', 1)

    print 'The total number of hospitals is', len(Y) # 2005
    print 'The number of hospitals with a positive label is', sum(Y) # 23!
    # Base rate is 23/2005 ~= 1.1%

    train_ix, test_ix = data_utils.splitTestTrainIndices(data, 'Bin 2014', train_size=0.8)
    X_train, X_test = X.ix[train_ix], X.ix[test_ix]
    Y_train, Y_test = Y.ix[train_ix], Y.ix[test_ix]

    ftwo_scorer = metrics.make_scorer(metrics.fbeta_score, beta=2) 
    lr_classifier = optimizeLogisiticRegression(X_train, Y_train, ftwo_scorer)

    print("Best parameters set found on development set:")
    print(lr_classifier.best_estimator_)
    print("Detailed classification report:")
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print(metrics.classification_report(Y_test, lr_classifier.predict(X_test)))
    # Evaluate on the test set
    final_auc = metrics.roc_auc_score(y_true=Y_test, 
                                      y_score=lr_classifier.decision_function(X_test))
    print 'logistic regression gets an AUC of:', final_auc
    final_ftwo = ftwo_scorer(lr_classifier, X_test, Y_test)
    print 'logistic regression gets a final f2 score of:', final_ftwo
    

def BestAUCLogisiticRegression(X_train, Y_train, regularization_type='l2'):
    logistic_regression_params = [10**i for i in range(-3,7)] + [1e30]
    best_c = None
    best_auc = None

    for c in logistic_regression_params:
        classifier = linear_model.LogisticRegression(C=c, penalty=regularization_type) 
        auc = meanAUCCrossValidation(X_train, Y_train, classifier)
        if not best_c or best_auc < auc:
            best_c = c
            best_auc = auc
    print 'best C for logistic regression', best_c, 'results in AUC', best_auc
    # L2: Best value for C seems to be 100, it gives AUC ~= .70. These means that some regularization is helpful.
    # L1: Best value for C seems to be 10, it gives AUC ~= .68
    classifier = linear_model.LogisticRegression(C=best_c, penalty=regularization_type)
    return classifier.fit(X_train, Y_train)
    
# Deprecated, use optimizeLogisiticRegression below
def meanAUCCrossValidation(X, Y, classifier, num_folds=5):
    cross_valdation_obj = KFold(n=X.shape[0], n_folds = num_folds, random_state=42)
    aucs = []
    for train_index, test_index in cross_valdation_obj:
        X_train = X.iloc[train_index]
        Y_train = Y.iloc[train_index]
        X_test = X.iloc[test_index]
        Y_test = Y.iloc[test_index]
       
        scores = classifier.fit(X_train, Y_train).decision_function(X_test)
        auc = metrics.roc_auc_score(Y_test, scores)
        aucs.append(auc)

    return np.mean(aucs)

# Deprecated, use optimizeLogisiticRegression below
def optimizeLogisiticRegression(X_train, Y_train, scorer, regularization_type='l2'):
    '''Creates a logisitic regression trainied on the given data with an optimized C parameter.

    Args:
      X_train: A dataframe on which to train the features
      Y_train: A dataframe on which to evaluate the training data
      scorer: A string or a scoring function used to optimize the C hyperparameter. Use 'mean_auc'
        to optimized via mean_auc, and use the following to optimize via F2 score:
        ftwo_scorer = metrics.make_scorer(metrics.fbeta_score, beta=2) 
    Returns:
      A fitted logistic regression classifier.
    '''
    param_grid = {'C': [10**i for i in range(-3,7)] + [1e30]}
    lr_classifier = GridSearchCV(linear_model.LogisticRegression(penalty=regularization_type), 
                                 param_grid=param_grid, scoring=scorer)
    return lr_classifier.fit(X_train, Y_train)


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
