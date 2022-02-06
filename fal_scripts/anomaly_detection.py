"""Finding anomalies on a dataset using DBSCAN

Dependencies:
 - sklearn
 - slack_sdk

Follow instructions in slack.py for setting up a minimal Slack bot.

This example is built for a model that has two columns: y and ds, where
y is a metric measure and ds is a timestamp.

The metric that we look at is Agent Wait Time in minutes.
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(context.config.script_path, '..')))

from math import floor
import ssl
from anomaly_detection_functions import *

model_df = ref(context.current_model.name).sort_values(by='ds')

column_y = model_df['y'].to_numpy(dtype=np.float).reshape(-1,1)
column_date = model_df['ds'].to_numpy(dtype=datetime.datetime).reshape(-1,1)

window_size = 100

range_min_samples = [2,3,4,5]
min_samples = find_ideal_min_samples(column_y, range_min_samples, window_size)

range_const = int(floor(np.amax(column_y)*0.02))
find_eps_range(column_y, range_const)
range_eps = range(range_const, (range_const*5)+1, range_const)

eps = find_ideal_eps(column_y, min_samples, window_size, range_eps)

anomalies = anomaly_detection(column_y, eps, min_samples, window_size)
fpath = plot_anomalies(column_y, column_date, anomalies)
now = str(datetime.datetime.now())
date = now[:10]
hour = now[11:13]+now[14:16]

print(f'anomalies: {anomalies.size}\ndata: {column_y.size}\npercentage: {(anomalies.size/column_y.size)*100}%')

# This is to get around a bug, usually it is not needed.
ssl._create_default_https_context = ssl._create_unverified_context

message = f'fal.ai anomaly detection.\nFound {anomalies.size} anomalies.\nModel: {context.current_model.name}\nDate: {date}\nTime: {hour}-{TIMEZONE}\neps: {eps}, min_samples: {min_samples}, window_size: {window_size}'
send_slack_file(fpath, message, CHANNEL_ID, SLACK_TOKEN)
