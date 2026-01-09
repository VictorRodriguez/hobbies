#!/usr/bin/env bash

# ----------------------------------------
# Configuration
# ----------------------------------------
BIN=./synthetic_char
MODE=freq
CPU=0

OUT=workload_sweep_results.csv

EVENTS=cycles,instructions,cpu-clock,branches,branch-misses

# Governors available under intel_pstate
GOVERNORS=("performance" "powersave")

# Workload parameter sweeps
ITERATIONS=(100000000 500000000 2000000000)
STRIDES=(1 8 64 256)
CHAINS=(1 4 8)

# ----------------------------------------
# CSV Header
# ----------------------------------------
echo "governor,iterations,stride,chains,cycles,instructions,cpu_clock_ms,ipc,eff_freq_ghz" > ${OUT}

# ----------------------------------------
# Sweep loop
# ----------------------------------------
for GOV in "${GOVERNORS[@]}"; do
    echo "Setting governor: ${GOV}"
    sudo cpupower frequency-set -g ${GOV} >/dev/null
    sleep 1

    for ITER in "${ITERATIONS[@]}"; do
        for STRIDE in "${STRIDES[@]}"; do
            for CHAIN in "${CHAINS[@]}"; do

                echo "Run: gov=${GOV}, iter=${ITER}, stride=${STRIDE}, chains=${CHAIN}"

                PERF_OUT=$(taskset -c ${CPU} \
                    perf stat -x, -e ${EVENTS} \
                    ${BIN} ${MODE} ${ITER} ${STRIDE} ${CHAIN} 2>&1)

                CYCLES=$(echo "${PERF_OUT}" | grep cycles | cut -d, -f1)
                INSTR=$(echo "${PERF_OUT}" | grep instructions | cut -d, -f1)
                CPUCLK=$(echo "${PERF_OUT}" | grep cpu-clock | cut -d, -f1)

                IPC=$(awk "BEGIN { printf \"%.4f\", ${INSTR}/${CYCLES} }")
                EFF_FREQ=$(awk "BEGIN { printf \"%.3f\", ${CYCLES}/(${CPUCLK}*1e6) }")

                echo "${GOV},${ITER},${STRIDE},${CHAIN},${CYCLES},${INSTR},${CPUCLK},${IPC},${EFF_FREQ}" >> ${OUT}

            done
        done
    done
done

echo "Sweep completed. Results saved to ${OUT}"

