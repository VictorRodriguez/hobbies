#!/usr/bin/env python3
import argparse
from pathlib import Path
import math

import pandas as pd
import matplotlib.pyplot as plt


def parse_perf_csv(csv_path: str) -> pd.DataFrame:
    rows = []

    with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 4:
                continue

            try:
                time_s = float(parts[0])
            except ValueError:
                continue

            count_raw = parts[1]
            unit = parts[2]
            event = parts[3]

            runtime = parts[4] if len(parts) > 4 else ""
            pct_running = parts[5] if len(parts) > 5 else ""
            metric_value = parts[6] if len(parts) > 6 else ""
            metric_unit = parts[7] if len(parts) > 7 else ""

            if count_raw == "<not counted>":
                count = math.nan
            else:
                try:
                    count = float(count_raw)
                except ValueError:
                    count = math.nan

            rows.append(
                {
                    "time_s": time_s,
                    "event": event,
                    "count": count,
                    "unit": unit,
                    "runtime": runtime,
                    "pct_running": pct_running,
                    "metric_value": pd.to_numeric(metric_value, errors="coerce"),
                    "metric_unit": metric_unit,
                }
            )

    if not rows:
        raise ValueError(f"No parseable perf rows found in {csv_path}")

    return pd.DataFrame(rows)


def build_timeseries(df: pd.DataFrame, interval_ms: float) -> pd.DataFrame:
    pivot = (
        df.pivot_table(index="time_s", columns="event", values="count", aggfunc="first")
        .sort_index()
        .copy()
    )

    expected = [
        "task-clock",
        "cycles",
        "instructions",
        "cache-misses",
        "context-switches",
        "page-faults",
    ]
    for col in expected:
        if col not in pivot.columns:
            pivot[col] = math.nan

    # For ROI detection and plotting, treat <not counted> as zero activity.
    pivot = pivot.fillna(0.0)

    # task-clock is reported in msec
    pivot["cpu_utilized"] = pivot["task-clock"] / interval_ms

    # Derived metrics
    pivot["ipc"] = pivot["instructions"] / pivot["cycles"].replace(0, pd.NA)
    pivot["ghz"] = pivot["cycles"] / (pivot["task-clock"].replace(0, pd.NA) * 1e6)

    # Optional extra metric
    pivot["mpki"] = pivot["cache-misses"] / (
        pivot["instructions"].replace(0, pd.NA) / 1000.0
    )

    return pivot.reset_index()


def detect_roi(ts: pd.DataFrame, cpu_threshold: float = 0.05):
    active = ts["cpu_utilized"] > cpu_threshold
    if not active.any():
        return None, None
    return ts.loc[active, "time_s"].min(), ts.loc[active, "time_s"].max()


def plot_cpu_and_ipc(ts: pd.DataFrame, out_png: str, title: str, roi_start=None, roi_end=None):
    plt.figure(figsize=(10, 6))

    # IPC outside ROI is not meaningful; keep it NaN there
    ipc_plot = ts["ipc"].copy()

    plt.plot(ts["time_s"], ts["cpu_utilized"], label="CPU Utilization")
    plt.plot(ts["time_s"], ipc_plot, label="IPC")

    if roi_start is not None and roi_end is not None:
        plt.axvspan(roi_start, roi_end, alpha=0.2, label="Detected ROI")

    plt.xlabel("Time (s)")
    plt.ylabel("Value")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Parse and plot perf stat interval CSV.")
    parser.add_argument("csv", help="perf CSV file produced by perf stat -I -x,")
    parser.add_argument(
        "--interval-ms",
        type=float,
        required=True,
        help="Sampling interval in milliseconds, e.g. 100 or 1000",
    )
    parser.add_argument(
        "--output",
        default="perf_cpu_ipc.png",
        help="Output PNG filename",
    )
    parser.add_argument(
        "--parsed-csv",
        default="perf_parsed.csv",
        help="Output parsed CSV filename",
    )
    parser.add_argument(
        "--title",
        default="CPU Utilization and IPC over Time",
        help="Plot title",
    )
    parser.add_argument(
        "--cpu-threshold",
        type=float,
        default=0.05,
        help="CPU utilization threshold for ROI detection",
    )

    args = parser.parse_args()

    raw_df = parse_perf_csv(args.csv)
    ts = build_timeseries(raw_df, args.interval_ms)

    roi_start, roi_end = detect_roi(ts, cpu_threshold=args.cpu_threshold)

    plot_cpu_and_ipc(
        ts,
        args.output,
        args.title,
        roi_start=roi_start,
        roi_end=roi_end,
    )

    ts.to_csv(args.parsed_csv, index=False)

    print(f"Wrote plot: {args.output}")
    print(f"Wrote parsed CSV: {args.parsed_csv}")
    if roi_start is not None and roi_end is not None:
        print(f"Detected ROI: {roi_start:.3f}s to {roi_end:.3f}s")
    else:
        print("No ROI detected")


if __name__ == "__main__":
    main()
