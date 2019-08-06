#!/usr/bin/python

import sys
import numpy as np
from scipy.stats import variation
from numpy import genfromtxt


if len(sys.argv) >= 2:
    csv_file = sys.argv[1]
    my_data = genfromtxt(csv_file, delimiter=',')
else:
    print("Please provide the csv file with the data")
    sys.exit(-1)

print("Standard Deviation: %f" % np.std(my_data))
print("Mean: %f" % np.mean(my_data))
print("Coefficient of variation: %f" % variation(my_data))

