#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUTDIR = Path("plots")
OUTDIR.mkdir(exist_ok=True)

# Load datasets
hw = pd.read_csv("workload_sweep_results.csv")
iwps = pd.read_csv("iwps_workload_results.csv")

# Normalize columns
for df in (hw, iwps):
    df.columns = [c.strip().lower().replace("-", "_") for c in df.columns]

# Merge on experiment keys
JOIN_KEYS = ["mode", "iterations", "working_set", "stride"]
# Only keep keys present in both
JOIN_KEYS = [k for k in JOIN_KEYS if k in hw.columns and k in iwps.columns]

merged = hw.merge(
    iwps,
    on=JOIN_KEYS,
    suffixes=("_hw", "_iwps")
)

if merged.empty:
    raise RuntimeError("No matching HW ↔ IWPS experiments found")

# Function to plot a metric over x-axis parameter
def plot_comparison(x, y, ylabel, title, filename, logx=False):
    plt.figure(figsize=(7,5))
    for mode in merged["mode"].unique():
        subset = merged[merged["mode"] == mode]
        subset = subset.sort_values(x)
        plt.plot(subset[x], subset[f"{y}_hw"], marker='o', label=f"{mode} HW")
        plt.plot(subset[x], subset[f"{y}_iwps"], marker='x', linestyle='--', label=f"{mode} IWPS")
    plt.xlabel(x)
    plt.ylabel(ylabel)
    plt.title(title)
    if logx:
        plt.xscale('log')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTDIR / filename, dpi=300)
    plt.close()


# --- Load data ---
hw_file = "workload_sweep_results.csv"
iwps_file = "iwps_workload_results.csv"

hw = pd.read_csv(hw_file)
iwps = pd.read_csv(iwps_file)

##############################################################################

# Data for cache mode
data = {
    "working_set": [1024, 1024, 1024, 1024, 16384, 16384, 16384, 16384, 262144, 262144, 262144, 262144],
    "stride": [1, 8, 64, 256, 1, 8, 64, 256, 1, 8, 64, 256],
    "hw_ipc": [0.8086, 0.8084, 0.8097, 0.8096, 0.5155, 0.5138, 0.5119, 0.5156, 0.3159, 0.3158, 0.3160, 0.3159],
    "iwps_ipc": [1.14, 1.14, 1.14, 1.14, 1.23, 1.23, 1.23, 1.23, 1.20, 1.20, 1.20, 1.20]
}

df = pd.DataFrame(data)

plt.figure(figsize=(10,6))

for stride in df["stride"].unique():
    subset = df[df["stride"] == stride]
    plt.plot(subset["working_set"], subset["hw_ipc"], marker='o', label=f"HW stride {stride}")
    plt.plot(subset["working_set"], subset["iwps_ipc"], marker='x', linestyle='--', label=f"IWPS stride {stride}")

plt.xscale("log")
plt.xlabel("Working Set")
plt.ylabel("IPC")
plt.title("Cache Mode: HW vs IWPS IPC")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("cache_ipc_comparison.png")


##############################################################################

# Filter to freq mode and performance governor
hw_freq = hw[(hw["mode"] == "freq") & (hw["governor"] == "performance")]

# Select relevant columns
hw_freq = hw_freq[["iterations", "ipc"]].sort_values("iterations")
iwps_freq = iwps[iwps["mode"] == "freq"][["iterations", "ipc"]].sort_values("iterations")

# --- Plot ---
plt.figure(figsize=(6,4))
plt.plot(hw_freq["iterations"], hw_freq["ipc"], marker='o', label="HW (performance)")
plt.plot(iwps_freq["iterations"], iwps_freq["ipc"], marker='s', label="IWPS")

plt.xlabel("Iterations")
plt.ylabel("IPC")
plt.title("IPC vs Iterations (freq mode)")
plt.xscale("log")
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()

# --- Save figure ---
plt.savefig("ipc_vs_iterations_freq.png", dpi=300)
print("Plot saved as ipc_vs_iterations_freq.png")


# 2) Cycles vs Iterations
plot_comparison(
    x="iterations",
    y="cycles",
    ylabel="Cycles",
    title="HW vs IWPS: Cycles",
    filename="cycles_vs_iterations.png",
    logx=True
)

# 3) Effective frequency vs Iterations (if present)
if "eff_freq_ghz_hw" in merged.columns:
    plot_comparison(
        x="iterations",
        y="eff_freq_ghz",
        ylabel="Effective Frequency (GHz)",
        title="HW vs IWPS: Effective Frequency",
        filename="eff_freq_vs_iterations.png",
        logx=True
    )

# 4) Optional: IPC vs Working Set (for cache mode)
if "working_set" in merged.columns:
    plot_comparison(
        x="working_set",
        y="ipc",
        ylabel="IPC",
        title="HW vs IWPS: IPC vs Working Set",
        filename="ipc_vs_workingset.png",
        logx=True
    )

print("HW vs IWPS line comparison plots saved in 'plots/'")

