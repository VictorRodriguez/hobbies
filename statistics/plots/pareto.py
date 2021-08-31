import pandas as pd

import matplotlib.pyplot as plt

def pareto_plot(df):
    df = df.sort_values(by='Count',ascending=False)
    df['pareto'] = 100 *df.Count.cumsum() / df.Count.sum()
    fig, axes = plt.subplots()
    ax1 = df.plot(use_index=True, y='Count',  kind='bar', ax=axes)
    ax2 = df.plot(use_index=True, y='pareto', marker='D', color="C1", kind='line', ax=axes, secondary_y=True)
    ax2.set_ylim([0,110])
    plt.show()

