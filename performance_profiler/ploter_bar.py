# importing pandas library
import pandas as pd
# import matplotlib library
import matplotlib.pyplot as plt

# plotting graph
def ploter(df,title):
    df.plot(x="test_name", y=["branch_misses", "cache_misses", "l1_dcache_load_misses"], kind="bar")
    plt.xticks(rotation=30, horizontalalignment="center")
    plt.title(title)
    plt.ylabel("Ratio (%)")
    plt.show()

df = pd.read_csv("results.csv")
ploter(df, "SPECspeed®2017 Integer and Floating Point")
df_int = df.loc[df['Kind'] == "INT"]
ploter(df_int, "SPECspeed®2017 Integer")
df_fp = df.loc[df['Kind'] == "FP"]
ploter(df_fp, "SPECspeed®2017 Floating Point")

branch_misses_int_average = df_int["branch_misses"].mean()
cache_misses_int_average = df_int["cache_misses"].mean()
l1_dcache_load_misses_int_average = df_int["l1_dcache_load_misses"].mean()

branch_misses_fp_average = df_fp["branch_misses"].mean()
cache_misses_fp_average = df_fp["cache_misses"].mean()
l1_dcache_load_misses_fp_average = df_fp["l1_dcache_load_misses"].mean()

d = {'branch_misses_avg': [branch_misses_int_average, branch_misses_fp_average],\
    'cache_misses_avg': [cache_misses_int_average, cache_misses_fp_average], \
    'l1_dcache_load_misses_avg': [l1_dcache_load_misses_int_average, l1_dcache_load_misses_fp_average]}
df_average = pd.DataFrame(data=d, index=["Integer",  "Floating Point"])

df_average.plot( y=["branch_misses_avg", "cache_misses_avg", "l1_dcache_load_misses_avg"], kind="bar")
plt.xticks(rotation=30, horizontalalignment="center")
plt.title("Average Ratio (%) for SPECspeed®2017 Integer and Floating Point")
plt.ylabel("Ratio (%)")
plt.show()
