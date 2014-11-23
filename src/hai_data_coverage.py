'''Misc. functions relating to the Healthcare Associated Infections - Hospital.csv file.'''

import matplotlib

# Local files, intro-ds-hai/src/ directly must be in the path.
import data_utils
from hai_data_cleanup import *


def analyzeMissingValues():
    HAI_FILE = '/Users/pinesol/intro-ds-hai/data/Healthcare Associated Infections - Hospital.csv'
    useful_columns = ['Provider ID', 'City', 'State', 'ZIP Code', 'County Name', 'Measure ID', 'Score']

    data = data_utils.parseFile(HAI_FILE, useful_columns)

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

def fakeBucketTargetScores(target_series):
    # TODO make real bucket function
    return target_series.astype(float).map(lambda score: 0 if score < 1 else 1)

def trainLogisticRegression():
    HAI_FILE = '/Users/pinesol/intro-ds-hai/data/Healthcare Associated Infections - Hospital.csv'
    useful_columns = ['Provider ID', 'City', 'State', 'ZIP Code', 'County Name', 'Measure ID', 'Score']
    target_column = 'Score'

    data = data_utils.parseFile(HAI_FILE, useful_columns)
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
    trainLogisticRegression()
