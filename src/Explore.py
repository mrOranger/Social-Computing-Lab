import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pandas as pd
import json as json
import sys as sys
import os as os

from scipy.stats import expon

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Wrong number of arguments!\n")
    sys.stderr.write("\tpython Explote.py data-file\n")
    sys.exit(1)

if not os.path.exists('data/figures'):
	os.mkdir('data/figures')

if not os.path.exists('data/statistics'):
	os.mkdir('data/statistics')

input_geolocated_rest = sys.argv[1]
csv_path                        = os.path.join(input_geolocated_rest)

most_recent_inspection_results = pd.read_csv(csv_path) 



# Create and save the histogram using matplotlib
plt.figure(figsize = (15, 7))
h = most_recent_inspection_results['Score'].hist(bins = 100) # Pandas built-in function authomatically generates histrogram
plt.xticks(np.arange(40, 100, 2))
h.set_title("Histogram of Insepction Scores")
plt.savefig('data/figures/Inspections_Scores.png') # Save the histogram in an output file

# Print most important statistics and save in a file
scores = most_recent_inspection_results['Score']
mean   = scores.mean()
median = scores.median()
summary = scores.describe()
mode = sp.stats.mode(scores)
skew = scores.skew()

ninety   = scores.quantile(0.9)
eighty   = scores.quantile(0.8)
seventy = scores.quantile(0.7)
sixty      = scores.quantile(0.6)

my_json = {
    "median": median,
    "mode": int(mode.mode[0]),
    "skew": skew,
    "quantiles": {
        "0.9": ninety,
        "0.8": eighty,
        "0.7": seventy,
        "0.6": sixty
    },
    "describe":{
        "count": scores.describe()["count"],
        "mean": scores.describe()["mean"],
        "std": scores.describe()["std"],
        "min": scores.describe()["min"],
        "25%": scores.describe()["25%"],
        "50%": scores.describe()["50%"],
        "75%": scores.describe()["75%"],
        "max": scores.describe()["max"]
    }
}

with open("data/statistics/most_recent_inspections_statistics.json", "w") as json_file:
    json.dump(my_json, json_file)





