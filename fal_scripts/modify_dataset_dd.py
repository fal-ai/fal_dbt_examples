import pandas as pd

PATH_PREFIX = '/Users/omeroguz/Documents/fal ai/fal_dbt_examples'

df = pd.read_csv(f'{PATH_PREFIX}/data/city_temperature.csv')

df.pop('State')
df.pop('Country')
df.pop('Region')
df.pop('Month')
df.pop('Day')
df.pop('Year')

print(df.head())

df.to_csv(f'{PATH_PREFIX}/data/city_temperature.csv')