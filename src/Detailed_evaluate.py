import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import os

if len(sys.argv) != 3:
    sys.stderr.write("Arguments error. Wrong number of arguments!\n")
    sys.stderr.write("\tpython Detailed_evaluate.py data-file\n")
    sys.exit(1)

if not os.path.exists('data/det_evaluate'):
	os.mkdir('data/det_evaluate')

# Read the dependencies files "geolocated_rest.csv" and "geolocated_rest_discretized.csv"
input_geolocated_rest                     = sys.argv[1]

geolocated_rest_path                      = os.path.join('data', 'output', input_geolocated_rest)

most_recent_inspection_results     = pd.read_csv(geolocated_rest_path) 

# Let's have a more detailet view of the previous data,
# by using the statistics information stored in the file most_recent_inspections_statistics.json

statistics = sys.argv[2]
statistics_path = os.path.join('data', 'statistics', statistics)

with open(statistics_path, "r") as my_file:
    data = my_file.read()

json_data = json.loads(data)

fig = plt.figure(figsize = (15, 7))

# Pandas built-in histogram function authomatically distributes and counts bin values
h   = most_recent_inspection_results['Score'].hist(bins = 100)

plt.axvline(x = json_data["describe"]["mean"], color = "red", ls = "solid", lw = "3", label = "mean")
plt.axvline(x = json_data["median"], color = "green", ls = "solid", lw = "3", label = "median")
plt.axvline(x = json_data["mode"], color = "orange", ls = "solid", lw = "3", label = "mode")

# 25-th quantile
plt.axvline(x = json_data["describe"]["25%"], color = "maroon", ls = "dashed", lw = "3", label = "25th")
plt.axvspan(40, json_data["describe"]["25%"], facecolor = "maroon", alpha = 0.3)

# 75-th quantile
plt.axvline(x = json_data["describe"]["75%"], color = "black", ls = "dashed", lw = "3", label = "75th")
plt.axvspan(40, json_data["describe"]["75%"], facecolor = "yellow", alpha = 0.3)

# Create x-axis ticks of even number 0-100
plt.xticks(np.arange(40, 104, 2))

# Add legend to graph
plt.legend(loc = 2)

# Add a title to the curret figure, our histogram
h.set_title("Histogram of Inspection Scores")

# Save the detailed hisogram
fig.savefig("data/det_evaluate/Detailed_inspections_scores.png", bbox_inches = 0, transparent = True)
