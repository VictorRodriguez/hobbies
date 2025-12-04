#!/usr/bin/env python3
import subprocess
import re
from collections import Counter
import sys
import os

# === Configuration ===
binary = "./myapp"          # compiled binary
perf_freq = 99              # sampling frequency
perf_data = "perf.data"
perf_output = "perf_output.txt"
top_n = 10                  # number of top instructions to report

# === Step 0: Optional compilation ===
# subprocess.run([
#     "gcc", "-g", "-O0", "-fno-inline", "-fno-omit-frame-pointer", "-o", "myapp", "myapp.c"
# ], check=True)

# === Step 1: Run perf record ===
print("[INFO] Running perf record...")
subprocess.run([
    "perf", "record", "-F", str(perf_freq), "-g", "--call-graph", "fp", binary
], check=True)

# === Step 2: Run perf script ===
print("[INFO] Running perf script...")
with open(perf_output, "w") as f:
    subprocess.run(["perf", "script", "-i", perf_data], stdout=f, check=True)

# === Step 3: Parse perf output ===
print("[INFO] Extracting instruction addresses...")
addresses = []

with open(perf_output) as f:
    for line in f:
        # Only consider lines containing the binary name
        if os.path.basename(binary) in line:
            # Match address + function (e.g., 4011bb heavy_roi+0x0)
            m = re.search(r"([0-9a-f]+)\s+([\w<>~]+)\+0x[0-9a-f]+", line)
            if m:
                addr = m.group(1)
                func = m.group(2)
                addresses.append((func, addr))

if not addresses:
    print("[WARNING] No addresses extracted! Check debug symbols and workload.")
    sys.exit(1)

# === Step 4: Count samples per function+address ===
counter = Counter(addresses)
total_samples = sum(counter.values())

# === Step 5: Report top ROIs ===
print("\n=== Candidate ROI (Most Sampled Instructions) ===")
print(f"{'Function':20} {'Offset':>10} {'Samples':>10} {'% of total':>12}")
print("-" * 60)

for (func, addr), count in counter.most_common(top_n):
    percent = (count / total_samples) * 100
    print(f"{func:20} 0x{addr:>8} {count:>10} {percent:>11.2f}%")

# Optional: Group by function to see total impact
function_counter = Counter()
for (func, _), count in counter.items():
    function_counter[func] += count

print("\n=== ROI Summary by Function ===")
print(f"{'Function':20} {'Total Samples':>15} {'% of total':>12}")
print("-" * 50)
for func, count in function_counter.most_common():
    percent = (count / total_samples) * 100
    print(f"{func:20} {count:>15} {percent:>11.2f}%")

