
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn import metrics
from sklearn.cross_validation import train_test_split, KFold
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import auc, roc_curve
from sklearn import metrics

# Local files, intro-ds-hai/src/ directly must be in the path.
import binning_utils
import data_utils
import merge_data

#    print 'The total number of hospitals is', len(Y) # 2005
#    print 'The number of hospitals with a positive label is', sum(Y) # 23!
    # Base rate is 23/2005 ~= 1.1%

# TODO different binning functions
#   print("Best parameters set found on development set:")
#    print(lr_classifier.best_estimator_)
#    print("Detailed classification report:")
#    print("The model is trained on the full development set.")
#    print("The scores are computed on the full evaluation set.")
#    print(metrics.classification_report(Y_test, Y_predicted))

def optimizeLogisticRegression(X_train, Y_train, scorer, regularization_type='l2'):
    '''Creates a logisitic regression trainied on the given data with an optimized C parameter.

    Args:
      X_train: A dataframe on which to train the features
      Y_train: A dataframe on which to evaluate the training data
      scorer: A string or a scoring function used to optimize the C hyperparameter. Use 'roc_auc'
        to optimize via roc_auc, and use the following to optimize via F2 score:
        ftwo_scorer = metrics.make_scorer(metrics.fbeta_score, beta=2) 
    Returns:
      A fitted logistic regression classifier.
    '''
    param_grid = {'C': [10**i for i in range(-3,7)] + [1e30]}
    lr_classifier = GridSearchCV(linear_model.LogisticRegression(penalty=regularization_type), 
                                 param_grid=param_grid, scoring=scorer, cv=5)
    print 'best C param for LR classifier:', lr_classifier.best_params_['C']
    return lr_classifier.fit(X_train, Y_train)

def UnfittedLogisticRegression(scorer, regularization_type='l2'):
    '''Creates a logisitic regression trainied on the given data with an optimized C parameter.

    Args:
      scorer: A string or a scoring function used to optimize the C hyperparameter. Use 'roc_auc'
        to optimize via roc_auc, and use the following to optimize via F2 score:
        ftwo_scorer = metrics.make_scorer(metrics.fbeta_score, beta=2) 
    Returns:
      An unfitted logistic regression classifier.
    '''
    param_grid = {'C': [10**i for i in range(-3,7)] + [1e30]}
    lr_classifier = GridSearchCV(linear_model.LogisticRegression(penalty=regularization_type), 
                                 param_grid=param_grid, scoring=scorer, cv=5)
    return lr_classifier

def GetROCData(data, train_ix, test_ix, classifier):
    X, Y = data_utils.splitTrainAndTarget(data)
    X_train, X_test = X.ix[train_ix], X.ix[test_ix]
    Y_train, Y_test = Y.ix[train_ix], Y.ix[test_ix]
    print '-- Number of positives: Y train', sum(Y_train)
    print '-- Number of positives: Y test', sum(Y_test)
    classifier = classifier.fit(X_train, Y_train)
    if hasattr(classifier, 'support_'):
        print 'number of features:', len(X_train.columns.values)
        print 'Useful features:', [col for col_used, col in zip(classifier.support_, X_train.columns.values) if col_used]
    fpr, tpr, thresholds = metrics.roc_curve(Y_test, classifier.decision_function(X_test))
    print '-- Number of ROC threshold values', len(thresholds)    
    return fpr, tpr, metrics.auc(fpr, tpr)

# Graph AUC curves of all four binning functions
def GraphROCs(label_data, bin_1_data, bin_2_data, bin_3_data, train_ix, test_ix, classifier, filename=None):
    # Train classifiers, and get ROC curve data
    print 'Bin: label'
#    lr_fpr_label, lr_tpr_label, lr_auc_label = GetROCData(label_data, train_ix, test_ix, classifier)
#    print 'Bin: 1'    
#    lr_fpr_1, lr_tpr_1, lr_auc_1 = GetROCData(bin_1_data, train_ix, test_ix, classifier)
#    print 'Bin: 2'    
#    lr_fpr_2, lr_tpr_2, lr_auc_2 = GetROCData(bin_2_data, train_ix, test_ix, classifier)
    print 'Bin: 3'    
    lr_fpr_3, lr_tpr_3, lr_auc_3 = GetROCData(bin_3_data, train_ix, test_ix, classifier)
    
    fig, ax = plt.subplots()
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('ROC')    
    legends = []

#    plt.plot(lr_fpr_label, lr_tpr_label)
#    legends.append('LR, Original Labels (AUC = %0.2f)' % (lr_auc_label))
#    plt.plot(lr_fpr_1, lr_tpr_1)
#    legends.append('LR, Binning 1 (AUC = %0.2f)' % (lr_auc_1))
#    plt.plot(lr_fpr_2, lr_tpr_2)
#    legends.append('LR, Binning 2 (AUC = %0.2f)' % (lr_auc_2))
    plt.plot(lr_fpr_3, lr_tpr_3)
    legends.append('LR, Binning 3 (AUC = %0.2f)' % (lr_auc_3))

    # Straight line
    diagonal_fpr = [0,1]
    diagonal_tpr = [0,1]
    plt.plot(diagonal_fpr, diagonal_tpr)
    legends.append('Random Guess (AUC = %0.2f)' % (metrics.auc(diagonal_fpr, diagonal_tpr)))
    
    plt.legend(legends, title='Classifier Type', loc='lower right')
    if filename:
        plt.savefig(filename, bbox_inches='tight')
    plt.show()


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


# 205 columns...too slow!
def testDataset():
    data = merge_data.mergeAllTheThings(binning_utils.binByLabel)
    ftwo_scorer = metrics.make_scorer(metrics.fbeta_score, beta=2) 

    score_to_columns_map = {}
    Y = data['Bin 2014']
    X = data.drop('Bin 2014', 1).sort_index(axis=1) #TODO important to sort columns so that we evaluate each binning function the same way.
    train_ix, test_ix = data_utils.splitTestTrainIndices(data, 'Bin 2014', train_size=0.8) # TODO not needed for other binning funcs
    Y_train, Y_test = Y.ix[train_ix], Y.ix[test_ix]
    X2 = X
    for i, column_name in enumerate(X.columns.values):
        X2_train, X2_test = X2.ix[train_ix], X2.ix[test_ix]
        lr_classifier = optimizeLogisticRegression(X2_train, Y_train, ftwo_scorer)
        ftwo = ftwo_scorer(lr_classifier, X2_test, Y_test)
        #auc = metrics.roc_auc_score(y_true=Y_test, y_score=Y_predicted)
        #recall = metrics.recall_score(y_true=Y_test, y_pred=Y_predicted)
        print 'iteration', (i+1), 'of', len(X.columns.values), '. ftwo score:', ftwo, 'from', len(X2.columns.values), 'columns'
        if ftwo not in score_to_columns_map:
            score_to_columns_map[ftwo] = [len(X2.columns.values)]
        else:
            score_to_columns_map[ftwo].append(len(X2.columns.values))
        if column_name != 'Bin 2012' and column_name != 'Bin 2013' and column_name != 'Bin 2014':
            X2 = X2.drop(column_name, 1)
    for score in sorted(score_to_columns_map):
        print score, score_to_columns_map[score]


def GetROCDataProxy(X_train_test, X_holdout,Y_train_test, Y_holdout,Y_s_train_test, classifier):
    print '-- Number of positives: Y train (Proxy variable)', sum(Y_s_train_test)
    print '-- Number of positives: Y test (Target variable)', sum(Y_holdout)

    classifier.fit(X_train_test, Y_s_train_test)
    if hasattr(classifier, 'support_'):
        print 'number of features:', len(X_train.columns.values)
        print 'Useful features:', [col for col_used, col in zip(classifier.support_, X_train_test.columns.values) if col_used]
    fpr, tpr, thresholds = metrics.roc_curve(Y_holdout, classifier.decision_function(X_holdout))
    print '-- Number of ROC threshold values', len(thresholds)    
    return fpr, tpr, metrics.auc(fpr, tpr)



def GetmetricsData(data, train_ix, test_ix, classifier, meassure):
    X, Y = data_utils.splitTrainAndTarget(data)
    X_train, X_test = X.ix[train_ix], X.ix[test_ix]
    Y_train, Y_test = Y.ix[train_ix], Y.ix[test_ix]
    print '-- Number of positives: Y train', sum(Y_train)
    print '-- Number of positives: Y test', sum(Y_test)
    classifier = classifier.fit(X_train, Y_train)
    if hasattr(classifier, 'support_'):
        print 'number of features:', len(X_train.columns.values)
        print 'Useful features:', [col for col_used, col in zip(classifier.support_, X_train.columns.values) if col_used]
    temp = meassure(Y_test, classifier.predict(X_test))
    #print '-- Number of ROC threshold values', len(thresholds)    
    return temp




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
    #testAllDatasets()
    testDataset()
