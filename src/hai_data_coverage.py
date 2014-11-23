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
