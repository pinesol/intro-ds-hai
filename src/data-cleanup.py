
import matplotlib.pyplot as plt
import os
import pandas as pd

from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_curve, auc


def filterByMeasureID(data, measure_id):
    data = data.loc[data['Measure ID'] == measure_id]
    # Drop the measure id column, since it's the same for all rows now.
    data = data.drop('Measure ID', 1)
    return data

def parseFile(filename, useful_columns):
    data = pd.read_table(filename, sep=',')
    data = data[useful_columns]
    return data

def analyzeMissingValues():
    HAI_FILE = '/Users/pinesol/intro-ds-hai/data/Healthcare Associated Infections - Hospital.csv'
    useful_columns = ['Provider ID', 'City', 'State', 'ZIP Code', 'County Name', 'Measure ID', 'Score']

    data = parseFile(HAI_FILE, useful_columns)

    measure_ids = ['HAI_1_SIR', 'HAI_2_SIR', 'HAI_3_SIR', 'HAI_4_SIR', 'HAI_5_SIR', 'HAI_6_SIR']
    data_availability_by_hai = []
    for measure_id in measure_ids:
        measure_data, missing_data = filterByMeasureID(data, measure_id)
        data_availability_by_hai.append(float(len(missing_data)) / (len(measure_data) + len(missing_data)))

    # Plotting
    fig, ax = plt.subplots()
    ax.set_xlabel('Measure IDs')
    ax.set_ylabel('Data Availibility')
    ax.set_title('HAI SIR Measure availibility')    

    ax.bar(range(1,len(data_availability_by_hai)+1), data_availability_by_hai)
    plt.show()
    # HAI 4 has the most data, with 80% coverage
    # HAI 1 has just under 60% coverage
    # TODO make this into an ipython notebook


def factorizeFeatures(train_data):
    '''Makes all string columns into ints, using category numbers if the column isn't convertable into an int directly.'''
    X = pd.DataFrame()
    for column in list(train_data.columns):
        try:
            X[column] = train_data[column].astype(int)
        except ValueError:
            print 'cant interize column, assuming categorical', column
            X[column] = pd.Categorical.from_array(train_data[column]).codes
    return X

def removeRowsWithMissingTarget(data, target_column):
    MISSING_VALUE = 'Not Available'
    missing_scores_data = data.loc[data[target_column] == MISSING_VALUE]
    data = data.loc[data[target_column] != MISSING_VALUE]
    return data

def fakeBucketTargetScores(target_series):
    # TODO make real bucket function
    return target_series.astype(float).map(lambda score: 0 if score < 1 else 1)

def trainLogisticRegression():
    HAI_FILE = '/Users/pinesol/intro-ds-hai/data/Healthcare Associated Infections - Hospital.csv'
    useful_columns = ['Provider ID', 'City', 'State', 'ZIP Code', 'County Name', 'Measure ID', 'Score']
    target_column = 'Score'

    data = parseFile(HAI_FILE, useful_columns)
    data = filterByMeasureID(data, 'HAI_1_SIR')
    data = removeRowsWithMissingTarget(data, target_column)
    
    Y = fakeBucketTargetScores(data['Score'])
    X = factorizeFeatures(data.drop('Score', 1))
    # TODO arbitrary test size
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
#    analyzeMissingValues()
    trainLogisticRegression()
