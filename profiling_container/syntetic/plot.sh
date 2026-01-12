import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV
df = pd.read_csv("workload_sweep_results.csv")

# Set plot style
sns.set(style="whitegrid", context="talk")

# --------------------------------------------
# 1. Compute-bound kernel IPC vs Iterations
# --------------------------------------------
df_freq = df[df['mode'] == 'freq']

plt.figure(figsize=(8,6))
sns.lineplot(
    data=df_freq,
    x='iterations',
    y='ipc',
    hue='governor',
    marker='o'
)
plt.title("Compute-bound Kernel IPC vs Iterations")
plt.xlabel("Iterations")
plt.ylabel("IPC")
plt.xscale('log')
plt.grid(True)
plt.tight_layout()
plt.savefig("freq_ipc_vs_iterations.png")
plt.close()  # Close figure instead of showing

# --------------------------------------------
# 2. Memory-bound IPC vs Working Set
# --------------------------------------------
df_cache = df[df['mode'] == 'cache']

plt.figure(figsize=(8,6))
sns.lineplot(
    data=df_cache,
    x='working_set',
    y='ipc',
    hue='stride',
    style='governor',
    markers=True,
    dashes=False
)
plt.title("Memory-bound Kernel IPC vs Working Set")
plt.xlabel("Working Set Size (elements)")
plt.ylabel("IPC")
plt.xscale('log')
plt.grid(True)
plt.tight_layout()
plt.savefig("cache_ipc_vs_ws.png")
plt.close()

# --------------------------------------------
# 3. Memory-bound Effective Frequency vs Working Set
# --------------------------------------------
plt.figure(figsize=(8,6))
sns.lineplot(
    data=df_cache,
    x='working_set',
    y='eff_freq_ghz',
    hue='stride',
    style='governor',
    markers=True,
    dashes=False
)
plt.title("Memory-bound Kernel Effective Frequency vs Working Set")
plt.xlabel("Working Set Size (elements)")
plt.ylabel("Effective Frequency (GHz)")
plt.xscale('log')
plt.grid(True)
plt.tight_layout()
plt.savefig("cache_efffreq_vs_ws.png")
plt.close()


df_cache = pd.read_csv("workload_sweep_results.csv")
df_cache = df_cache[df_cache['mode'] == 'cache']

# Pivot table for heatmap: working set × stride
heatmap_data = df_cache.pivot_table(
    index='stride',
    columns='working_set',
    values='ipc',
    aggfunc='mean'
)

plt.figure(figsize=(10,6))
sns.heatmap(heatmap_data, annot=True, fmt=".3f", cmap="viridis")
plt.title("Cache-bound IPC vs Working Set and Stride")
plt.xlabel("Working Set Size (elements)")
plt.ylabel("Stride")
plt.tight_layout()
plt.savefig("cache_ipc_heatmap.png")
plt.close()

# Filter compute-bound data
df_freq = df[df['mode'] == 'freq']

# Line plot: IPC vs iterations for each governor
plt.figure(figsize=(8,5))
sns.lineplot(
    data=df_freq,
    x='iterations',
    y='ipc',
    hue='governor',
    marker='o'
)
plt.xscale('log')  # Because iterations vary by orders of magnitude
plt.xlabel("Iterations")
plt.ylabel("IPC")
plt.title("Compute-bound IPC vs Iterations")
plt.grid(True)
plt.savefig("compute_bound_ipc_vs_iterations.png")

