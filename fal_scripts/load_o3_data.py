import pandas

cols = ['O3', 'state', 'county', 'month']
df = pandas.read_csv('data/raw_o3_values.csv', usecols=cols)
write_to_source(df, "results", "raw_o3_values")
