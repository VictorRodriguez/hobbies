#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------------------------
# Configuration
# -------------------------------------------------
HW_FILE = "workload_sweep_results.csv"
IWPS_FILE = "iwps_workload_results.csv"
OUTDIR = Path("plots")
OUTDIR.mkdir(exist_ok=True)

ITER_FIXED = 10000000  # iteration slice for cache analysis

# -------------------------------------------------
# Load data
# -------------------------------------------------
hw = pd.read_csv(HW_FILE)
iwps = pd.read_csv(IWPS_FILE)

# -------------------------------------------------
# 1. IPC vs Working Set (Cache sweep)
# -------------------------------------------------
hw_cache = hw[(hw["mode"] == "cache") & (hw["iterations"] == ITER_FIXED)]
iwps_cache = iwps[(iwps["mode"] == "cache") & (iwps["iterations"] == ITER_FIXED)]

hw_grp = hw_cache.groupby("working_set")["ipc"].mean().reset_index()
iwps_grp = iwps_cache.groupby("working_set")["ipc"].mean().reset_index()

plt.figure()
plt.plot(hw_grp["working_set"], hw_grp["ipc"], marker="o", label="Hardware")
plt.plot(iwps_grp["working_set"], iwps_grp["ipc"], marker="o", label="IWPS")
plt.xscale("log")
plt.xlabel("Working Set (bytes)")
plt.ylabel("IPC")
plt.title("IPC vs Working Set (Cache Sweep)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(OUTDIR / "ipc_vs_working_set.png", dpi=300)
plt.close()

# -------------------------------------------------
# 2. Normalized IPC (HW / IWPS)
# -------------------------------------------------
df_norm = pd.merge(
    hw_grp,
    iwps_grp,
    on="working_set",
    suffixes=("_hw", "_iwps")
)
df_norm["ipc_norm"] = df_norm["ipc_hw"] / df_norm["ipc_iwps"]

plt.figure()
plt.plot(df_norm["working_set"], df_norm["ipc_norm"], marker="o")
plt.xscale("log")
plt.xlabel("Working Set (bytes)")
plt.ylabel("Normalized IPC (HW / IWPS)")
plt.title("Normalized IPC vs Working Set")
plt.grid(True)
plt.tight_layout()
plt.savefig(OUTDIR / "normalized_ipc_vs_working_set.png", dpi=300)
plt.close()

# -------------------------------------------------
# 4. Cache Misses vs Working Set (IWPS)
# -------------------------------------------------
miss_grp = iwps_cache.groupby("working_set")[["l1_misses", "llc_misses"]].mean().reset_index()

plt.figure()
plt.plot(miss_grp["working_set"], miss_grp["l1_misses"], marker="o", label="L1-D Misses")
plt.plot(miss_grp["working_set"], miss_grp["llc_misses"], marker="o", label="LLC Misses")
plt.xscale("log")
plt.xlabel("Working Set (bytes)")
plt.ylabel("Miss Count")
plt.title("Cache Misses vs Working Set (IWPS)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(OUTDIR / "cache_misses_vs_working_set.png", dpi=300)
plt.close()

# -------------------------------------------------
# 5. Effective Frequency vs Working Set
# -------------------------------------------------
hw_freq_grp = hw_cache.groupby("working_set")["eff_freq_ghz"].mean().reset_index()
iwps_freq_grp = iwps_cache.groupby("working_set")["eff_freq_ghz"].mean().reset_index()

plt.figure()
plt.plot(hw_freq_grp["working_set"], hw_freq_grp["eff_freq_ghz"],
         marker="o", label="Hardware")
plt.plot(iwps_freq_grp["working_set"], iwps_freq_grp["eff_freq_ghz"] / 1e9,
         marker="o", label="IWPS")
plt.xscale("log")
plt.xlabel("Working Set (bytes)")
plt.ylabel("Effective Frequency (GHz)")
plt.title("Effective Frequency vs Working Set")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(OUTDIR / "effective_frequency_vs_working_set.png", dpi=300)
plt.close()

print(f"All plots generated under: {OUTDIR.resolve()}")

