import pandas as pd
import scipy as sp
from scipy import stats
import yaml as yaml
import sys as sys
import os as os

params = yaml.safe_load(open('params.yaml'))['transform']

if len(sys.argv) != 3:
    sys.stderr.write("Arguments arror. Wrong number of arguments!\n")
    sys.stderr.write("\tpython Transform.py data-file\n")
    sys.exit(1)

column_sort_index = params['column_sort_index'] # Take column's name to sort by parameter

# Store relevant file paths in variables since we may use them frequently

input_dataset_business     = sys.argv[1]
input_dataset_inspections = sys.argv[2]

businesses  = os.path.join('data', 'SFBusinesses', input_dataset_business)
inspections = os.path.join('data', 'SFBusinesses', input_dataset_inspections)

# Load each file in a Pandas DataFrame, pandas authomatically convers the first line into a header for the columns
df_businesses  = pd.read_csv(businesses)
df_inspections = pd.read_csv(inspections)

# Join the two DataFrames on the 'business_id' column
big_table = df_businesses.merge(df_inspections, on = 'business_id')

# The joined DataFrame columns in our case is the concatention of the df_busines and df_inspections
print("Business: \t {} \n".format(str(df_businesses.columns)))
print("Inspections: \t {} \n".format(str(df_inspections.columns)))
print("Big Tabe: \t {} \n".format(str(big_table.columns)))

# Let us first group our data by business so we can find its more recent score for inspections
grouped_business = big_table.groupby('business_id')

# A function that takes a DataFrame and returns the row with the newest date
def most_recent(df, column = 'date'):
    return df.sort_values(by = column)[-1:]

# Inut to most_recent is the DataFrame of each group, in this case
# all of the rows and columns for each business (grouped on business_id)
most_recent_inspection_results = grouped_business.apply(most_recent)

if not os.path.exists('data/output'):
	os.mkdir('data/output')

# Filter our records without lat/long for mapping
r                      = most_recent_inspection_results
zero_filtered = r[(r['latitude'] != 0) & (r['latitude'] != 0)]
filtered           = zero_filtered.dropna(subset = ['latitude', 'longitude'])[['business_id','name', 'address', 'Score', 'date', 'latitude', 'longitude']]
filtered.to_csv('data/output/geolocated_rest.csv', index=False)
