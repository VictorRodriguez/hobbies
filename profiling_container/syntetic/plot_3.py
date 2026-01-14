#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUTDIR = Path("plots")
OUTDIR.mkdir(exist_ok=True)

# -------------------------------------------------
# Load and tag data
# -------------------------------------------------
hw = pd.read_csv("workload_sweep_results.csv")
iwps = pd.read_csv("iwps_workload_results.csv")

hw["source"] = "HW"
iwps["source"] = "IWPS"

# Normalize column names
for df in (hw, iwps):
    df.columns = [c.strip().lower().replace("-", "_") for c in df.columns]

# -------------------------------------------------
# Keys that define *the same experiment*
# -------------------------------------------------
JOIN_KEYS = [
    "mode",
    "iterations",
    "working_set",
    "stride"
]

# Governor only exists in HW → ignore if missing
JOIN_KEYS = [k for k in JOIN_KEYS if k in hw.columns and k in iwps.columns]

# -------------------------------------------------
# Inner join: only comparable experiments survive
# -------------------------------------------------
merged = hw.merge(
    iwps,
    on=JOIN_KEYS,
    suffixes=("_hw", "_iwps")
)

if merged.empty:
    raise RuntimeError("No matching HW ↔ IWPS experiments found")

# -------------------------------------------------
# 1) IPC comparison scatter
# -------------------------------------------------
plt.figure(figsize=(6, 6))
plt.scatter(
    merged["ipc_hw"],
    merged["ipc_iwps"]
)

max_ipc = max(merged["ipc_hw"].max(), merged["ipc_iwps"].max())
plt.plot([0, max_ipc], [0, max_ipc], linestyle="--")

plt.xlabel("IPC (HW)")
plt.ylabel("IPC (IWPS)")
plt.title("IPC: HW vs IWPS")
plt.grid(True)

plt.savefig(OUTDIR / "ipc_hw_vs_iwps.png", dpi=300, bbox_inches="tight")
plt.close()

# -------------------------------------------------
# 2) IPC ratio vs iterations
# -------------------------------------------------
merged["ipc_ratio"] = merged["ipc_iwps"] / merged["ipc_hw"]

plt.figure(figsize=(7, 5))
plt.scatter(
    merged["iterations"],
    merged["ipc_ratio"]
)

plt.axhline(1.0, linestyle="--")
plt.xscale("log")
plt.xlabel("Iterations")
plt.ylabel("IPC ratio (IWPS / HW)")
plt.title("IPC Fidelity vs Iterations")
plt.grid(True)

plt.savefig(OUTDIR / "ipc_ratio_vs_iterations.png", dpi=300, bbox_inches="tight")
plt.close()

# -------------------------------------------------
# 3) Effective frequency error
# -------------------------------------------------
if "eff_freq_ghz_hw" in merged.columns:
    merged["freq_error_pct"] = (
        (merged["eff_freq_ghz_iwps"] - merged["eff_freq_ghz_hw"])
        / merged["eff_freq_ghz_hw"]
        * 100.0
    )

    plt.figure(figsize=(7, 5))
    plt.scatter(
        merged["iterations"],
        merged["freq_error_pct"]
    )

    plt.axhline(0.0, linestyle="--")
    plt.xscale("log")
    plt.xlabel("Iterations")
    plt.ylabel("Effective Frequency Error (%)")
    plt.title("IWPS Frequency Error vs HW")
    plt.grid(True)

    plt.savefig(
        OUTDIR / "eff_freq_error_vs_iterations.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

print("HW vs IWPS comparison plots generated")

