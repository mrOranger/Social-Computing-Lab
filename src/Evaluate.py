import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import os

if len(sys.argv) != 3:
    sys.stderr.write("Arguments error. Wrong number of arguments!\n")
    sys.stderr.write("\tpython Evaluate.py data-file\n")
    sys.exit(1)

if not os.path.exists('data/evaluate'):
	os.mkdir('data/evaluate')

# Read the dependencies files "geolocated_rest.csv" and "geolocated_rest_discretized.csv"
input_geolocated_rest                     = sys.argv[1]
input_geolocated_rest_discretized = sys.argv[2]

geolocated_rest_path                      = os.path.join('data', 'output', input_geolocated_rest)
geolocated_rest_discretized_path = os.path.join('data', 'discrete', input_geolocated_rest_discretized)

most_recent_inspection_results     = pd.read_csv(geolocated_rest_path) 
score_transform                                = pd.read_csv(geolocated_rest_discretized_path)

# Create a figure with 2 subplots
fig = plt.figure(figsize = (30, 7))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

# Count each occurrence of descriptions in the 'Score' column,
# add reverse this result so 'Poor' is left most and 'Good' right most
counts = score_transform['Score'].value_counts()[::-1]
plt        = counts.plot(kind = 'bar', ax = ax2)

# Decore the plot and axis with text
ax2.set_title("Restaurant Inspections (%i total) " % sum(counts))
ax2.set_ylabel("Counts")
ax2.set_xlabel("Descriptions")

# Let us add some labels to each bar
for x, y in enumerate(counts):
    plt.text(x + 0.5, y + 200, '%.f' %y, ha = 'left', va = 'top')

# Plot the original raw scores (same graph as earlier)
most_recent_inspection_results['Score'].hist(bins = 100, ax = ax1)

# Create x-axis ticks of even numbers 0-100
ax1.set_xticks(np.arange(40, 100, 2))

# Add a title to the current figure, our histogram
ax1.set_title("Histogram of Inpections Scores")
ax1.set_ylabel("Counts")
ax1.set_xlabel("Score")

# Save the figures in the output folder
fig.savefig("data/evaluate/Scores_Histograms.png", bbox_inches = 0)

