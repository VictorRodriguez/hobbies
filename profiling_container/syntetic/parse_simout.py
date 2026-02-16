#!/usr/bin/env python3
import argparse
import re
import csv
from pathlib import Path

def extract(pattern, text, default=0.0):
    """General extractor for simple numeric metrics from sim.out."""
    m = re.search(pattern, text, re.MULTILINE)
    if not m:
        return default
    val = m.group(1).replace(',', '').replace('%', '')
    try:
        return float(val)
    except ValueError:
        return default

def extract_metric_after_header(header, label, text):
    """
    Finds a metric value after a given header and label using DOTALL regex.
    Returns 0.0 if not found.
    """
    pattern = rf"{re.escape(header)}.*?{re.escape(label)}\s*\|\s*([0-9,.]+)"
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        return 0.0
    return float(m.group(1).replace(",", ""))

# -----------------------
# Argument Parsing
# -----------------------
parser = argparse.ArgumentParser(description="Parse IWPS sim.out")
parser.add_argument("--platform", default="NA", help="CPU platform (clx, icx, spr, gnr)")
parser.add_argument("--simout", required=True, help="Path to sim.out file")
parser.add_argument("--mode", required=True, help="freq or cache")
parser.add_argument("--iterations", default="NA")
parser.add_argument("--working-set", default="NA")
parser.add_argument("--stride", default="NA")
parser.add_argument("--frequency", default="NA")
parser.add_argument("--csv", required=True)
args = parser.parse_args()

sim_file = Path(args.simout)
if not sim_file.exists():
    print(f"ERROR: sim.out file not found: {args.simout}")
    exit(1)

sim_text = sim_file.read_text()

# -----------------------
# Core metrics extraction
# -----------------------
instructions = extract(r"^\s*Instructions\s*\|\s*([0-9,]+)", sim_text)
cycles       = extract(r"^\s*Cycles\s*\|\s*([0-9,]+)", sim_text)
ipc          = extract(r"^\s*IPC\s*\|\s*([0-9.]+)", sim_text)
time_ns      = extract(r"^\s*Time \(ns\)\s*\|\s*([0-9,.]+)", sim_text)
eff_freq_ghz = (cycles / time_ns) if time_ns > 0 else 0.0

# -----------------------
# Cache / TLB / DRAM metrics
# -----------------------
l1_misses        = extract_metric_after_header("Cache L1-D", "num cache misses", sim_text)
llc_misses       = extract_metric_after_header("LLC", "num cache misses", sim_text)
llc_miss_rate    = extract_metric_after_header("LLC", "miss rate", sim_text) / 100.0
l2_tlb_miss_rate = extract_metric_after_header("L2 TLB", "miss rate", sim_text) / 100.0
dram_util        = extract_metric_after_header("DDR", "average dram bandwidth utilization", sim_text) / 100.0

# -----------------------
# Row dictionary
# -----------------------
row = {
    "platform": args.platform,
    "mode": args.mode,
    "iterations": args.iterations,
    "working_set": args.working_set,
    "stride": args.stride,
    "frequency": args.frequency,
    "cycles": cycles,
    "instructions": instructions,
    "ipc": ipc,
    "eff_freq_ghz": eff_freq_ghz,
    "l1_misses": l1_misses,
    "llc_misses": llc_misses,
    "llc_miss_rate": llc_miss_rate,
    "l2_tlb_miss_rate": l2_tlb_miss_rate,
    "dram_util": dram_util
}

print(row)

# -----------------------
# Append to CSV
# -----------------------
csv_file = Path(args.csv)
file_exists = csv_file.exists()
with open(csv_file, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=row.keys())
    if not file_exists:
        writer.writeheader()
    writer.writerow(row)

