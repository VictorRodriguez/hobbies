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


# Convert numeric columns, coerce errors (turns '<not counted>' into NaN)
df_cache['LLC_misses'] = pd.to_numeric(df_cache['LLC_misses'], errors='coerce')
df_cache['L1_misses'] = pd.to_numeric(df_cache['L1_misses'], errors='coerce')

# Filter only cache mode if needed
df_cache_cache = df_cache[df_cache['mode'] == 'cache']

# Pivot for heatmaps
heatmap_llc = df_cache_cache.pivot_table(
    index='stride',
    columns='working_set',
    values='LLC_misses',
    aggfunc='mean'
)

heatmap_l1 = df_cache_cache.pivot_table(
    index='stride',
    columns='working_set',
    values='L1_misses',
    aggfunc='mean'
)

# Plot and save LLC heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_llc, annot=True, fmt=".0f", cmap="viridis")
plt.title("LLC Misses Heatmap")
plt.xlabel("Working Set")
plt.ylabel("Stride")
plt.tight_layout()
plt.savefig("heatmap_LLC_misses.png")
plt.close()  # Close figure to free memory

# Plot and save L1 heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_l1, annot=True, fmt=".0f", cmap="magma")
plt.title("L1 Misses Heatmap")
plt.xlabel("Working Set")
plt.ylabel("Stride")
plt.tight_layout()
plt.savefig("heatmap_L1_misses.png")
plt.close()

# Replace '<not counted>' with NaN and convert to numeric
df['LLC_misses'] = pd.to_numeric(df['LLC_misses'], errors='coerce')

# Group by working set and sum LLC misses
misses_by_ws = df.groupby('working_set')['LLC_misses'].sum()

# Plot
plt.figure(figsize=(8,5))
plt.plot(misses_by_ws.index, misses_by_ws.values, marker='o')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Working Set Size (Bytes)')
plt.ylabel('Total LLC Misses')
plt.title('Total LLC Misses vs Working Set Size')
plt.grid(True, which="both", ls="--")

# Save to file
plt.savefig("cache_misses_vs_ws.png", dpi=300, bbox_inches='tight')
plt.close()  # Close the figure so it doesn’t display in interactive environments

