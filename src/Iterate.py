import re as re
import collections as col
import pprint as pp
import sys
import os

import matplotlib.pyplot as plt
import pandas as pd

if len(sys.argv) != 3:
    sys.stderr.write("Arguments error. Wrong number of arguments!\n")
    sys.stderr.write("\tpython Evaluate.py data-file\n")
    sys.exit(1)

if not os.path.exists('data/violation_hist'):
	os.mkdir('data/violation_hist')

if not os.path.exists('data/violation_hist_perfect'):
	os.mkdir('data/violation_hist_perfect')

if not os.path.exists('data/top_offenses'):
	os.mkdir('data/top_offenses')

if not os.path.exists('data/violations_scores'):
	os.mkdir('data/violations_scores')

violations_plus_file       = sys.argv[1]
input_geolocated_rest = sys.argv[2]

geolocated_rest_path = os.path.join('data', 'output', input_geolocated_rest)
violations_plus_path   = os.path.join('data', 'SFFoodProgram_Complete_Data', violations_plus_file)

most_recent_inspection_results       = pd.read_csv(geolocated_rest_path) 
df_violations                                      = pd.read_csv(violations_plus_path)

violations_table = most_recent_inspection_results.merge(df_violations, on = ['business_id', 'date'])

# Let's see how the violations are distributed
fig = plt.figure(figsize = (18, 7))
violations_hist = violations_table['description'].value_counts().plot(kind = 'bar')
fig.savefig('data/violation_hist/violation_hist.png', bbox_inches = 0)

# Let us see what violations a restaurant can have and still get a perfect score
fig                      = plt.figure(figsize = (20, 10))
perfect_scores = violations_table[violations_table['Score'] == 100]
violations_hist  = perfect_scores['description'].value_counts().plot(kind = 'bar')
fig.savefig('data/violation_hist_perfect/violation_hist_perfect_score.png', bbox_inches = 0)

# Let us bin health violations using the cities quantizations
descriptions = ['Poor', 'Needs Improvement', 'Adequante', 'Good']
bins              = [-1, 70, 85, 90, 100]

# Copy the scores from our grouped DataFrame, DataFrames manipulate
# in place if we do not explicitly copy them.
scores = violations_table['Score'].copy()
violation_transform = violations_table.copy()

# Built-in pandas function which assigns each data point in
# 'scores' to an interval in 'bins' with labels of 'descriptions'
discretized_scores = pd.cut(scores, bins, labels = descriptions)
violation_transform["Scores"] = discretized_scores

grouped = violation_transform.groupby('Scores')

# Let us find the most common violations for each group

# a function that takes a DataFrame and returns the top violations
def common_offenses(df):
    return pd.DataFrame(df['description'].value_counts(normalize = True) * 100).head(10)

# Compute top offenses and save in a json file
top_offenses = grouped.apply(common_offenses)
top_offenses.to_json('data/top_offenses/top_offenses.json')

f          = plt.figure(figsize = (20, 10))
colors = ['r', 'b', 'y', 'g']
for name, group in grouped:
    group['description'].value_counts().plot(kind = 'bar', alpha = 0.5, color = colors.pop())
f.savefig('data/violations_scores/violations_group_scores.png', bbox_inches = 0)
