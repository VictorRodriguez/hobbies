import numpy as np
import sys
import csv
import os.path
import statistics
import argparse
from scipy.stats import norm
import matplotlib.pyplot as plt
import json

import calculations


class Metric(object):
    def __init__(self, value):
        self.variable = value
        self.colum_count = 0
        self.list_variables = []

    def add_value(self, value):
        self.list_variables.append(value)

    def set_colum_count(self, value):
        self.colum_count = value

    def get_list(self):
        return self.list_variables

    def get_colum_count(self):
        return self.colum_count


class Calculation(object):
    def __init__(self):
        self.metric = ""
        self.function = ""
        self.list_metrics = []

    def set_metric(self, value):
        self.metric = value

    def set_function(self, value):
        self.function = value

    def set_list(self, value):
        self.list_metrics = value

    def get_list(self):
        return self.list_metrics

    def get_metric(self):
        return self.metric


def plot_data_stdev_mean(data):
    x_axis = np.array(data)
    mean = statistics.mean(x_axis)
    sd = statistics.stdev(x_axis)

    plt.plot(x_axis, norm.pdf(x_axis, mean, sd))
    plt.show()


def plot_data(data, title, ylabel, display):
    plt.bar(list(range(1, len(data)+1)), data, color='maroon',
            width=0.4)
    plt.xlabel("series")
    plt.ylabel(ylabel)
    plt.title(title)
    if (display):
        plt.show()
    else:
        plt.ion()
        plt.savefig(title + '.png')


def get_mean_stdev(data):
    data_mean = statistics.mean(data)
    data_stdev = 100 * \
        statistics.stdev(data)/statistics.mean(data)
    return data_mean, data_stdev


parser = argparse.ArgumentParser()
parser.add_argument('--display',
                    help="display the plots generated",
                    action='store_true', default=False)
parser.add_argument("filename",
                    help="csv file used to generate the plots")
parser.add_argument("--configfile",
                    default='config.json')

args = parser.parse_args()


l = []
c = []

with open(args.configfile) as json_file:
    data = json.load(json_file)
    for p in data['variables']:
        for key, value in p.items():
            obj = Metric(key)
            l.append(obj)

    obj_c = Calculation()
    for p in data['calculations']:
        for key, value in p.items():
            if key == "variable":
                obj_c.set_metric(value)
            if key == "function":
                obj_c.set_function(value)
            c.append(obj_c)


if (os.path.isfile(args.filename)):
    with open(args.filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = 0
        col_count = 0
        for row in csv_reader:
            if row_count == 0:
                for col in row:
                    for i in range(len(l)):
                        if l[i].variable in col:
                            l[i].set_colum_count(col_count)
                    col_count += 1
            else:
                for i in range(len(l)):
                    l[i].add_value(int(float(row[l[i].get_colum_count()])))
            row_count += 1

    for i in range(len(l)):
        mean, stdev = get_mean_stdev(l[i].get_list())
        print("Mean of the {} sample is {} (stdev: {} % )"
              .format(l[i].variable, mean, stdev))

    for i in range(len(c)):
        if c[i].metric == "cpi":
            function_name = c[i].function
            cpi = eval(function_name + "(l)")
            c[i].set_list(cpi)
            mean, stdev = get_mean_stdev(c[i].get_list())
            print("Mean of the {} sample is {} (stdev: {} % )"
                  .format(c[i].get_metric(), mean, stdev))

else:
    print("File %s does not exit" % (fname))


for i in range(len(l)):
    plot_data(l[i].get_list(), l[i].variable, l[i].variable, args.display)

for i in range(len(c)):
    plot_data(c[i].get_list(), c[i].get_metric(),
              c[i].get_metric(), args.display)
