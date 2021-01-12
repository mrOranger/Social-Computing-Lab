import pandas as pd
import json
import sys 
import os

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Wrong number of arguments!\n")
    sys.stderr.write("\tpython Discretize.py data-file\n")
    sys.exit(1)

if not os.path.exists('data/discrete'):
	os.mkdir('data/discrete')

# Read the dependency file "geolocated_rest.csv"
input_geolocated_rest                  = sys.argv[1]
csv_path                                       = os.path.join('data', 'output', input_geolocated_rest)
most_recent_inspection_results = pd.read_csv(csv_path) 

# First we need to discretize the numerical values, this can be
# through of as converting a continous variable into a categorical one.
descriptions = ['Poor', 'Needs Improvement', 'Adequate', 'Good']
bins              = [-1, 70, 85, 90, 100]

# Copy the scores from our grouped DataFrame, DataFrames manipulate
# in place if we do not explicitly copy them.
scores                   = most_recent_inspection_results['Score']
score_transform = most_recent_inspection_results

# Built-in pandas function which assigns each data point in
# 'scores' to an interval in bins with labels of 'descriptions'
discretized_scores = pd.cut(scores, bins, labels = descriptions)

# Transform the original DataFrame's "Score" column with the new description
score_transform['Score'] = discretized_scores
score_transform.to_csv('data/discrete/geolocated_rest_discretized.csv', index = False)
