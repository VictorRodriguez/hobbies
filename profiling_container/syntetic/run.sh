#!/usr/bin/env bash

# ----------------------------------------
# Configuration
# ----------------------------------------
BIN=./synthetic_char
CPU=0
OUT=workload_sweep_results.csv
EVENTS=cycles,instructions,cpu-clock,branches,branch-misses

# Governors available under intel_pstate
GOVERNORS=("performance" "powersave")

# Workload parameter sweeps
ITERATIONS=(100000000 500000000 2000000000)
WORKING_SETS=(1024 16384 262144)  # For cache mode
STRIDES=(1 8 64 256)

# ----------------------------------------
# CSV Header
# ----------------------------------------
echo "mode,governor,iterations,working_set,stride,cycles,instructions,cpu_clock_ms,ipc,eff_freq_ghz" > ${OUT}

# ----------------------------------------
# Sweep loop
# ----------------------------------------
for GOV in "${GOVERNORS[@]}"; do
    echo "Setting governor: ${GOV}"
    sudo cpupower frequency-set -g ${GOV} >/dev/null
    sleep 1

    # ----------------------------
    # Frequency-bound kernel
    # ----------------------------
    for ITER in "${ITERATIONS[@]}"; do
        echo "Run freq mode: gov=${GOV}, iter=${ITER}"

        PERF_OUT=$(taskset -c ${CPU} \
            perf stat -x, -e ${EVENTS} \
            ${BIN} freq ${ITER} 1 1 2>&1)

        CYCLES=$(echo "${PERF_OUT}" | grep cycles | cut -d, -f1)
        INSTR=$(echo "${PERF_OUT}" | grep instructions | cut -d, -f1)
        CPUCLK=$(echo "${PERF_OUT}" | grep cpu-clock | cut -d, -f1)

        IPC=$(awk "BEGIN { if(${CYCLES}==0) print 0; else printf \"%.4f\", ${INSTR}/${CYCLES} }")
        EFF_FREQ=$(awk "BEGIN { printf \"%.3f\", ${CYCLES}/(${CPUCLK}*1e6) }")

        echo "freq,${GOV},${ITER},NA,NA,${CYCLES},${INSTR},${CPUCLK},${IPC},${EFF_FREQ}" >> ${OUT}
    done

    # ----------------------------
    # Cache-sensitive kernel
    # ----------------------------
    for WS in "${WORKING_SETS[@]}"; do
        for STRIDE in "${STRIDES[@]}"; do
            for ITER in "${ITERATIONS[@]}"; do
                echo "Run cache mode: gov=${GOV}, iter=${ITER}, ws=${WS}, stride=${STRIDE}"

                PERF_OUT=$(taskset -c ${CPU} \
                    perf stat -x, -e ${EVENTS} \
                    ${BIN} cache ${ITER} ${WS} ${STRIDE} 2>&1)

                CYCLES=$(echo "${PERF_OUT}" | grep cycles | cut -d, -f1)
                INSTR=$(echo "${PERF_OUT}" | grep instructions | cut -d, -f1)
                CPUCLK=$(echo "${PERF_OUT}" | grep cpu-clock | cut -d, -f1)

                IPC=$(awk "BEGIN { if(${CYCLES}==0) print 0; else printf \"%.4f\", ${INSTR}/${CYCLES} }")
                EFF_FREQ=$(awk "BEGIN { printf \"%.3f\", ${CYCLES}/(${CPUCLK}*1e6) }")

                echo "cache,${GOV},${ITER},${WS},${STRIDE},${CYCLES},${INSTR},${CPUCLK},${IPC},${EFF_FREQ}" >> ${OUT}
            done
        done
    done
done

echo "Sweep completed. Results saved to ${OUT}"

