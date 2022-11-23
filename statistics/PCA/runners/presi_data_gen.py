#!/bin/python3

import json
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from IPython.display import display
import urllib
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

results_file = 'presilicon_spec_cpu2017.csv'

def read_histogram(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    df.columns = df.columns.str.lower()
    df = df.sort_values(by='count', ascending=False)
    return df


def read_json(CUMULUS_ID):
    url = f'https://cumulus-dashboard.intel.com/services-framework/api/metadata/histogram/{CUMULUS_ID}'
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    data = response.read()
    values = json.loads(data)
    df = pd.json_normalize(values['data'])
    df.columns = df.columns.str.lower()
    return df

def get_cathegory(df_histogram):
    df_intrinsics = pd.read_json('/Users/vrodri3/Downloads/intrinsics.json')
    df_histogram["category"] = ""

    for instruction in df_histogram['mnemonic']:
        if (df_intrinsics['instruction'].eq(instruction.upper())).any():
            category = df_intrinsics.loc[df_intrinsics['instruction'] == instruction.upper(), 'category'].iloc[0]
            category = str(category).strip()
            df_histogram.loc[df_histogram['mnemonic'] == instruction,'category'] = category
        else:
            df_histogram.loc[df_histogram['mnemonic'] == instruction,'category'] = 'None'


    df = df_histogram.groupby(['category']).sum(numeric_only=True)
    df = df.sort_values(by=['count'], ascending=False)

    df['percent'] = (df['count'] / df['count'].sum()) * 100

    print(df)

    return df


def calcualte_values(df_copy):

    df_copy["count"] = pd.to_numeric(df_copy["count"])

    df_arithmetic = pd.read_csv('instructions_kind/arithmetic.csv')
    df_branch = pd.read_csv('instructions_kind/branch.csv')
    df_store = pd.read_csv('instructions_kind/store.csv')

    df_copy["pro"] = df_copy["count"]/df_copy["count"].sum()

    df_a = df_copy[df_copy.mnemonic.isin(df_arithmetic.mnemonic)]
    df_b = df_copy[df_copy.mnemonic.isin(df_branch.mnemonic)]
    df_s = df_copy[df_copy.mnemonic.isin(df_store.mnemonic)]
    df_o = pd.concat([df_copy, df_a, df_b, df_s]).drop_duplicates(keep=False)

    data_prob = [['arithmetic', df_a['pro'].sum()],
                 ['branch', df_b['pro'].sum()],
                 ['store_counter', df_s['pro'].sum()],
                 ['other_counter', df_o['pro'].sum()]]

    df_prob = pd.DataFrame(data_prob, columns=['InstrKind', 'probability'])
    return (df_prob)


def get_pareto(df):

    df["cumpercentage"] = df["count"].cumsum()/df["count"].sum()*100
    df2 = pd.DataFrame(columns=["mnemonic", "count", "cumpercentage"])
    for ind in df.index:
        if (df['cumpercentage'][ind]) <= 80:
            df2 = df2.append(df.iloc[ind])
    display(df2)

    fig, ax = plt.subplots()
    ax.bar(df2["mnemonic"], df2["count"], color="C0")
    ax2 = ax.twinx()
    ax2.plot(df2["mnemonic"], df2["cumpercentage"],
             color="C1", marker="D", ms=7)
    ax2.yaxis.set_major_formatter(PercentFormatter())
    ax.tick_params(axis="y", colors="C0")
    ax2.tick_params(axis="y", colors="C1")
    plt.show()


def plot_sumary(df_sumary):
    df_sumary.plot.pie(y = 'percent')
    plt.show()

def plot(df_sumary):
    my_labels = ['arithmetic', 'branch', 'store', 'other']
    df_sumary.plot(labels=my_labels, y='probability', kind='pie', autopct='%1.1f%%',
                   startangle=15, shadow=True,)
    plt.ylabel('')
    plt.show()
    display(df_sumary)

def plot_stacked_bar(df):
    df.plot.barh(stacked=True)
    plt.show()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--cumulus_uri")
    parser.add_argument("--histogram")
    parser.add_argument('--files',nargs='*')
    args = parser.parse_args()

    if args.files:
        my_labels = ['arithmetic', 'branch', 'store', 'other']
        df_global = pd.DataFrame(columns=my_labels)
        for file_name in args.files:
            test_name = file_name
            df = read_histogram(file_name)
            df_sumary = calcualte_values(df)
            df_global.loc[test_name] = df_sumary['probability'].values.tolist()
        plot_stacked_bar(df_global)
        print(df_global)
        df_global.to_csv(results_file)
        exit(0)

    elif args.histogram:
        df = read_histogram(args.histogram)

        # new methodology using Intel intrinsics numbers
        df_sumary = get_cathegory(df)

        # uncoment this when using old methodology
        #df_sumary = calcualte_values(df)

    elif args.cumulus_uri:
        df = read_json(args.cumulus_uri)
        df_sumary = calcualte_values(df)
    else:
        exit(-1)

    get_pareto(df)
    plot_sumary(df_sumary)


if __name__ == '__main__':
    main()
