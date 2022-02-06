import os
import sys
PATH_PREFIX = os.path.abspath(os.path.join(context.config.script_path, '..'))
sys.path.append(PATH_PREFIX)

from anomaly_detection_functions import plot_anomalies, find_ideal_min_samples, anomaly_detection, find_eps_range, find_ideal_eps

import numpy as np
from scipy.stats import ks_2samp
import matplotlib.pyplot as plt
from math import floor

def data_drift(data_1, data_2):
    test = ks_2samp(data_1, data_2)
    p_value = 0.05

    result = 0
    if test[1] < p_value:
        result = 1
    else:
        result = 0

    return result

# Here, we get our data using fal.
model = ref(context.current_model.name).sort_values(by='x')

# Then, we delete the last 140 days to make the total number of days
# perfectly divisible into years.
model['y'] = model['y'].astype(float)
y = model['y'].to_numpy()[:-140]

model['x'] = model['x'].astype(float)
x = model['x'].to_numpy()[:-140]

# After that, we slice the data into years to detect the data drift
# in temperature data.
n = floor(int(y.shape[0])/365)
y_windowed = np.split(y, n, axis=0)
x_windowed = np.split(x, n, axis=0)

# Here, we plot every year with changing colors to visualize the data.
fig = plt.figure(figsize=(15,5))
axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])

for i in range(len(y_windowed)):
    if (i % 2) == 0:
        color = 'b.'
    else:
        color = 'r.'
    axes.plot(x_windowed[i], y_windowed[i], color)

plt.savefig(f'{PATH_PREFIX}/dd_data.png')

# Here, we find where data drift happens and store their indexes.
dd_years = []

for i in range(len(y_windowed)-1):
    if data_drift(y_windowed[i], y_windowed[i+1]):
        dd_years.append((i,i+1))
    else:
        continue

print(f'Data drift found in years with indexes {dd_years}.')

# Here, we create a small function to find anomalies in our data to compare
# with data drift, using functions from the anomaly detection example.
def find_anomalies(dd_y, dd_x):
    window_size = 100

    range_min_samples = [2,3,4,5]
    min_samples = find_ideal_min_samples(dd_y, range_min_samples, window_size)
    print(f'found min_samples, {min_samples}')

    # We can see anomalous activity in the distance_between_samples.jpg in the 
    # form of absurdly large distances. There is a gap starting at around 30
    # distance units. We must set our upper bound to this value, and as our
    # value for the upper bound is calculated as range_const * 5, we can do
    # some quick algebra to find the range_const.
    range_const = int(floor(np.amax(dd_y)*0.075))
    find_eps_range(dd_y, range_const)
    range_eps = range(range_const, (range_const*5)+1, range_const)
    print('eps range graph found')

    eps = find_ideal_eps(dd_y, min_samples, window_size, range_eps)
    print(f'ideal eps found, {eps}')

    anomalies = anomaly_detection(dd_y, eps, min_samples, window_size)
    print('anomaly detection done')

    fpath = plot_anomalies(dd_y, dd_x, anomalies)
    print(f'anomalies plotted at {fpath}')

# Here, we apply our function on a set of data with data drift.
dd_y = np.concatenate((y_windowed[3], y_windowed[4])).reshape(-1,1)
dd_x = np.concatenate((x_windowed[3], x_windowed[4])).reshape(-1,1)

find_anomalies(dd_y, dd_x)

# And here, we apply our function on a set of data without data drift.
dd_y = np.concatenate((y_windowed[0], y_windowed[1])).reshape(-1,1)
dd_x = np.concatenate((x_windowed[0], x_windowed[1])).reshape(-1,1)

find_anomalies(dd_y, dd_x)