"""Finding anomalies on a dataset using DBSCAN

Dependencies:
 - sklearn
 - slack_sdk
 - 

Follow instructions in slack.py for setting up a minimal Slack bot.

This example is built for a model that has two columns: y and ds, where
y is a metric measure and ds is a timestamp.

The metric that we look at is Agent Wait Time in minutes.
"""
import os
from numpy.core.fromnumeric import size
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import silhouette_score
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from math import floor
import ssl

CHANNEL_ID = os.getenv("SLACK_BOT_CHANNEL")
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
PATH_PREFIX = os.getcwd()

def anomaly_detection(X: np.array, eps: float, min_samples: int, window_size: int):
    """Find anomalies on given time-series numerical data.

    Parameters
    ----------
    X: numpy.array
        A numpy array with shape (-1,1) containing time-series
        numerical data. I. e. a column of a multi-feature dataset.
    eps: float
        The epsilon value for DBSCAN. It is one of the two
        hyperparameters that needs fine tuning for good results.
    min_samples: int
        The minimum samples value for DBSCAN. It is one of the two
        hyperparameters that needs fine tuning for good results.
    window_size: int
        The window size for applying sliding windows on the data.
        Applying sliding windows to the data before applying DBSCAN
        improves the performance of the system.

    Returns
    -------
    anomalies: numpy.array
        A numpy array with the indices of the anomalies found on
        the data, the indices are with respect to the input data, X.
    """
    X_windowed = np.lib.stride_tricks.sliding_window_view(x=X, window_shape=window_size, axis=0)
    (size_0, _, _) = X_windowed.shape
    anomalies = []

    for window in range(size_0):
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(X_windowed[window][0][:].reshape(-1,1))
        labels = clustering.labels_
        location = np.where(labels == -1)
        location = location[0]
        size = location.size
        if size != 0:
            if size == 1:
                anomalies.append(location[0] + window)
            else:
                for i in range(size):
                    anomalies.append(location[i] + window)
        else:
            continue
    
    anomalies = np.unique(np.array(anomalies))
    
    return anomalies

def find_ideal_min_samples(X: np.array, range_min_samples: list):
    """Finds the ideal min_samples value from a given range of min_samples.
    Parameters
    ----------
    X: numpy.array
        A numpy array with shape (-1,1) containing time-series
        numerical data. I. e. a column of a multi-feature dataset.
    range_min_samples: list of ints
        A list with possible min_samples candidates.
    Returns
    -------
    ideal_min_sample: int
        The ideal min_sample value for DBSCAN for X.
    """
    X_windowed = np.lib.stride_tricks.sliding_window_view(x=X, window_shape=window_size, axis=0)
    (size_0, _, _) = X_windowed.shape

    min_sample_scores = np.zeros(shape=(1, len(range_min_samples)))

    for window in range(size_0):
        for i in range(len(range_min_samples)):
            clustering = KMeans(n_clusters=range_min_samples[i])
            cluster_labels = clustering.fit_predict(X_windowed[window][0][:].reshape(-1,1))
            silhouette_avg = silhouette_score(X_windowed[window][0][:].reshape(-1,1), cluster_labels)
            min_sample_scores[0][i] = min_sample_scores[0][i]+silhouette_avg
    
    min_sample_scores = min_sample_scores / size_0
    ideal_min_sample = range_min_samples[np.where(min_sample_scores.max)[0][0]]

    return ideal_min_sample
    
def find_eps_range(X: np.array, range_const: int):
    """Creates two matplotlib figures with one being a plot of
    the distance between samples and the other one being a bounded
    version of the first plot. It is used to see if the bounded plot
    resembles an elbow curve. The range constant is arbitrarily chosen
    and fine tuned by hand to find a range with an elbow curve.
    Parameters
    ----------
    X: numpy.array
        A numpy array with shape (-1,1) containing time-series
        numerical data. I. e. a column of a multi-feature dataset.
    range_const: int
        A constant that the epsilon range is constructed. Usually
        2.5% of the maximum value of the dataset makes a good starting
        point.

    Returns
    -------
    None
    """
    dists = np.zeros_like(X)
    for i in range(X.size-1):
        dist = np.linalg.norm(X[i]-X[i+1])
        dists[i] = dist
    dists = np.sort(dists, axis=0)

    plt.plot([i for i in range(dists.size)], dists, 'b.', markersize=4)
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.savefig(f'{PATH_PREFIX}/fal_scripts/anomaly_detection_other/distance_between_samples.jpg')
    plt.clf()

    bounded_dists_i = np.where(dists<=range_const*5)[0]
    plt.plot(bounded_dists_i, [dists[i] for i in bounded_dists_i], 'b.', markersize=4)
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.savefig(f'{PATH_PREFIX}/fal_scripts/anomaly_detection_other/distance_between_samples_bounded.jpg')
    plt.clf()

def find_ideal_eps(X: np.array, min_samples: int, window_size: int, range_eps: list):
    """Finds the ideal min_samples value from a given range of
    min_samples.
    Parameters
    ----------
    X: numpy.array
        A numpy array with shape (-1,1) containing time-series
        numerical data. I. e. a column of a multi-feature dataset.
    min_samples: int
        The minimum samples value for DBSCAN. It is one of the two
        hyperparameters that needs fine tuning for good results.
    window_size: int
        The window size for applying sliding windows on the data.
        Applying sliding windows to the data before applying DBSCAN
        improves the performance of the system.
    range_eps: list of ints
        A list with possible min_samples candidates.

    Returns
    -------
    ideal_eps: float
        The ideal epsilon value for DBSCAN for X.

    """
    X_windowed = np.lib.stride_tricks.sliding_window_view(x=X, window_shape=window_size, axis=0)
    (size_0, _, _) = X_windowed.shape

    eps_scores = np.zeros(shape=(1, len(range_eps)))

    for window in range(size_0):
        for i in range(len(range_eps)):
            clustering = DBSCAN(eps=range_eps[i], min_samples=min_samples).fit(X_windowed[window][0][:].reshape(-1,1))
            labels = clustering.labels_
            if np.unique(labels).size > 1:
                silhouette_avg = silhouette_score(X_windowed[window][0][:].reshape(-1,1), labels)
                eps_scores[0][i] = eps_scores[0][i]+silhouette_avg
    
    eps_scores = eps_scores / size_0

    ideal_eps = range_eps[np.where(eps_scores.max)[0][0]]

    return ideal_eps

def plot_anomalies(column_y: np.array, column_date: np.array, anomalies: np.array):
    """Plots the data and notes the anomalies on a matplotlib figure
    and returns the location of a JPG of the figure.

    Parameters
    ----------
    column_y: np.array
        A numpy array containing one column of values of a time-series
        dataset.
    column_date: np.array
        A numpy array containing the time objects of a time-series
        dataset.
    anomalies:
        A numpy array containing the indices of the anomalous data
        points.

    Returns
    -------
    fname: string
        The path of the matplotlib figure with the data plotted and
        anomailes
        noted.
    """
    fig = plt.figure(figsize=(15,5))
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.plot([column_date[i] for i in range(column_y.size)], column_y, 'b.', markersize=4)
    axes.plot([column_date[i] for i in anomalies], [column_y[i] for i in anomalies], 'r^', markersize=4)
    axes.set_xlabel('Time')
    axes.set_ylabel('Value')
    axes.legend(['Actual', 'Anomaly Found'])
    now = str(datetime.datetime.now())
    now = now[:10]+'-'+now[11:13]+now[14:16]
    fpath = f'{PATH_PREFIX}/fal_scripts/anomaly_detection/{now}-{TIMEZONE}.jpg'
    fig.savefig(fname=fpath)
    plt.clf()

    return fpath

# is the same slack file sending function from forecast_slack.py
def send_slack_file(file_path: str, message_text: str, channel_id: str, slack_token: str):
    """Sends a file and message to Slack.
    Parameters
    ----------
    file_path: string
        The file path of the file that needs to be sent.
    message_text: string
        The messange that needs to be sent along with the text.
    channel_id: string
        Channel ID for the Slack channel that the message needs
        to be sent to.
    slack_token: string
        Slack token for the Slack bot that is going to be used.

    Returns
    -------
    None
    """
    client = WebClient(token=slack_token)

    try:
        client.files_upload(
            channels=channel_id,
            file=file_path,
            title="fal.ai anomaly detection",
            initial_comment=message_text,
        )
    except SlackApiError as e:
        assert e.response["error"]

model_df = ref(context.current_model.name).sort_values(by='ds')

column_y = model_df['y'].to_numpy(dtype=np.float).reshape(-1,1)
column_date = model_df['ds'].to_numpy(dtype=datetime.datetime).reshape(-1,1)

window_size = 100

range_min_samples = [2,3,4,5]
min_samples = find_ideal_min_samples(column_y, range_min_samples)

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
