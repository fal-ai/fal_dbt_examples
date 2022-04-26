import os
import pycurl
import json
import certifi
from io import BytesIO
import pandas as pd
from sqlalchemy import except_

GITHUB_ACCESS_TOKEN = os.environ['GITHUB_TOKEN']

g_url = 'https://api.github.com/repos/fal-ai/fal/traffic/'
header_list = [f'Authorization: token {GITHUB_ACCESS_TOKEN}']
metrics = {'clones': '', 'views': '', 'popular/paths': '', 'popular/referrers': ''}

for metric in metrics.keys():
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, g_url+metric)
    c.setopt(c.HTTPHEADER, header_list)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.perform()
    c.close()
    metrics[metric] = buffer.getvalue().decode('utf-8')
    metrics[metric] = json.loads(metrics[metric])

fal_views_dates_p = source('fal_github_insights', 'fal_views_dates')
fal_clones_dates_p = source('fal_github_insights', 'fal_clones_dates')

fal_views = pd.DataFrame.from_dict(metrics['views']['views'])
fal_clones = pd.DataFrame.from_dict(metrics['clones']['clones'])
fal_ppaths = pd.DataFrame.from_dict(metrics['popular/paths'])
fal_preferrers = pd.DataFrame.from_dict(metrics['popular/referrers'])

fal_views['timestamp'] = fal_views['timestamp'].transform(lambda x: pd.Timestamp(x))
fal_clones['timestamp'] = fal_clones['timestamp'].transform(lambda x: pd.Timestamp(x))
fal_ppaths = fal_ppaths.drop('title', 1)

fal_views = fal_views.sort_values(by='timestamp')
fal_clones = fal_clones.sort_values(by='timestamp')

fal_views_dates = {'start': [fal_views['timestamp'].min()], 'end': [fal_views['timestamp'].max()]}
fal_clones_dates = {'start': [fal_clones['timestamp'].min()], 'end': [fal_clones['timestamp'].max()]}
fal_views_dates = pd.DataFrame.from_dict(fal_views_dates)
fal_clones_dates = pd.DataFrame.from_dict(fal_clones_dates)

write_to_source(fal_ppaths, 'fal_github_insights', 'fal_ppaths', mode='overwrite')
write_to_source(fal_preferrers, 'fal_github_insights', 'fal_preferrers', mode='overwrite')

write_to_source(fal_views_dates, 'fal_github_insights', 'fal_views_dates', mode='overwrite')
write_to_source(fal_clones_dates, 'fal_github_insights', 'fal_clones_dates', mode='overwrite')
    
if fal_views_dates['start'][0] > fal_views_dates_p['end'][0]:
    write_to_source(fal_views, 'fal_github_insights', 'fal_views')
    write_to_source(fal_clones, 'fal_github_insights', 'fal_clones')
else:
    try:
        i = fal_views.loc[fal_views['timestamp'] == fal_views_dates_p['end']] + 1
        write_to_source(fal_views[i:], 'fal_github_insights', 'fal_views')
    except:
        print('no update')
    try:
        i = fal_clones.loc[fal_clones['timestamp'] == fal_clones_dates_p['end']] + 1
        write_to_source(fal_clones[i:], 'fal_github_insights', 'fal_clones')
    except:
        print('no update')

# append data: fal_views, fal_clones
# update data: fal_ppaths, fal_preferrers