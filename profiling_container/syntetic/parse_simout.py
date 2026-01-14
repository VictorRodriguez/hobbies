#!/usr/bin/env python3
import argparse
import re
import csv
from pathlib import Path

def extract(pattern, text, default=0):
    m = re.search(pattern, text, re.MULTILINE)
    if not m:
        return default
    val = m.group(1).replace(',', '')
    try:
        return float(val)
    except ValueError:
        return default

parser = argparse.ArgumentParser(description="Parse IWPS sim.out")
parser.add_argument("--simout", required=True, help="Path to sim.out")
parser.add_argument("--mode", required=True, help="freq or cache")
parser.add_argument("--iterations", default="NA", help="Number of iterations")
parser.add_argument("--working-set", default="NA", help="Working set size")
parser.add_argument("--stride", default="NA", help="Stride size")
parser.add_argument("--frequency", default="NA", help="CPU frequency (GHz)")
parser.add_argument("--csv", required=True, help="CSV output file")
args = parser.parse_args()

sim_file = Path(args.simout)

print(sim_file)

if not sim_file.exists():
    print(f"ERROR: {args.simout} does not exist")
    exit(1)

sim_text = sim_file.read_text()

# --- Core metrics ---
instructions = extract(r"^\s*Instructions\s*\|\s*([0-9,]+)", sim_text)
cycles      = extract(r"^\s*Cycles\s*\|\s*([0-9,]+)", sim_text)
ipc         = extract(r"^\s*IPC\s*\|\s*([0-9.]+)", sim_text)
time_ns     = extract(r"^\s*Time \(ns\)\s*\|\s*([0-9,]+)", sim_text)
eff_freq_ghz = (cycles / time_ns * 1e9) if time_ns else 0.0


# --- Cache metrics ---
def extract_cache_misses(cache_name, text):
    pattern = rf"{cache_name}.*?num cache misses\s+\|\s+([0-9,]+)"
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        return 0
    return int(m.group(1).replace(",", ""))

l1_misses = extract_cache_misses("Cache L1-D", sim_text)
llc_misses = extract_cache_misses("Cache L2", sim_text)


row = {
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
    "llc_misses": llc_misses
}

print(row)
# Append to CSV
csv_file = Path(args.csv)
if not csv_file.exists():
    # write header if file does not exist
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writeheader()

with open(csv_file, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=row.keys())
    writer.writerow(row)

