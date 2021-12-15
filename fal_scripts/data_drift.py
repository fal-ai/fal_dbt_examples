PATH_PREFIX = '/Users/omeroguz/Documents/fal ai/fal_dbt_examples'
import sys
sys.path.append(f'{PATH_PREFIX}/fal_scripts')

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

# get our data
model = ref(context.current_model.name).sort_values(by='x')

# we delete the last 140 days to make the total number of days perfectly divisible into years
model['y'] = model['y'].astype(float)
y = model['y'].to_numpy()[:-140]

model['x'] = model['x'].astype(float)
x = model['x'].to_numpy()[:-140]

# slice it into years
n = floor(int(y.shape[0])/365)
y_windowed = np.split(y, n, axis=0)
x_windowed = np.split(x, n, axis=0)

# plot every year with and notate them with red and blue color
fig = plt.figure(figsize=(15,5))
axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])

for i in range(len(y_windowed)):
    if (i % 2) == 0:
        color = 'b.'
    else:
        color = 'r.'
    axes.plot(x_windowed[i], y_windowed[i], color)

plt.savefig(f'{PATH_PREFIX}/fal_scripts/dd_data.png')

# find the years in which data drift from one year to the next occurs
dd_years = []

for i in range(len(y_windowed)-1):
    if data_drift(y_windowed[i], y_windowed[i+1]):
        dd_years.append((i,i+1))
    else:
        continue

print(f'data drift in {dd_years}')

