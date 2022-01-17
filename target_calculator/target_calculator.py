import argparse
import sys

import matplotlib.pyplot as plt
import pandas as pd

import seaborn as sns
import statsmodels.api as sm


def plot(x, y, independent, y_pred, image_name):
    # plotting the data points
    plt.figure(figsize=(12, 8), tight_layout=True)
    sns.scatterplot(x=x[independent], y=y)

    # plotting the line
    sns.lineplot(x=x[independent], y=y_pred, color='red')

    plt.xlim(0)
    plt.ylim(0)
    plt.savefig(image_name)


def calculate_slope_intercept(x, y, independent):
    lm = sm.OLS(y, x).fit()  # fitting the model
    slope = lm.params[1]
    intercept = lm.params[0]
    y_pred = slope * x[independent] + intercept
    print(("Ecuation :  %s*x + %s") % (slope, intercept))
    return y_pred


def parse_args(args):

    parser = argparse.ArgumentParser()
    parser.add_argument('--dependent')
    parser.add_argument('--independent')
    parser.add_argument('--data_file_name')
    parser.add_argument('--image_name', default='linear_regression')
    args = parser.parse_args()
    return (args)


def main():

    args = parse_args(sys.argv[1:])
    if args.data_file_name:
        df_ = pd.read_csv(args.data_file_name)
    else:
        print('Error: Please provide a filename: --data_file_name')
    if args.dependent and args.independent:
        y = df_[args.dependent]
        x = df_[args.independent]
        x = sm.add_constant(x)  # adding a constant
        y_pred = calculate_slope_intercept(x, y, args.independent)
        print(y_pred[100])
        plot(x, y, args.independent, y_pred, args.image_name)
    else:
        print('Error: Please provide --dependent and --independent values')


if __name__ == '__main__':
    main()
