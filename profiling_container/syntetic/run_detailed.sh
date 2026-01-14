#!/usr/bin/env bash

# ----------------------------------------
# Configuration
# ----------------------------------------
BIN=./synthetic_char
MODES=("freq" "cache")
CPU=0

OUT=workload_sweep_results.csv

# Perf events
EVENTS="cycles,instructions,cpu-clock,branches,branch-misses,L1-dcache-load-misses,LLC-load-misses"

# Governors available under intel_pstate
GOVERNORS=("performance" "powersave")

# Workload parameter sweeps
#ITERATIONS=(100000000 500000000 2000000000)
ITERATIONS=(10000000 50000000 200000000)
WORKSETS=(1024 16384 262144)
STRIDES=(1 8 64 256)
CHAINS=(1 4 8)

# ----------------------------------------
# CSV Header
# ----------------------------------------
echo "mode,governor,iterations,working_set,stride,chains,cycles,instructions,cpu_clock_ms,ipc,eff_freq_ghz,L1_misses,LLC_misses" > ${OUT}

# ----------------------------------------
# Sweep loop
# ----------------------------------------
for MODE in "${MODES[@]}"; do
    for GOV in "${GOVERNORS[@]}"; do
        echo "Setting governor: ${GOV}"
        sudo cpupower frequency-set -g ${GOV} >/dev/null
        sleep 1

        for ITER in "${ITERATIONS[@]}"; do
            if [ "${MODE}" == "freq" ]; then
                WS=NA
                STR=NA
                for CH in "${CHAINS[@]}"; do
                    echo "Run: mode=${MODE}, gov=${GOV}, iter=${ITER}, chains=${CH}"

                    PERF_OUT=$(sudo taskset -c ${CPU} perf stat -x, -e ${EVENTS} \
                        ${BIN} ${MODE} ${ITER} 1 1 2>&1)

                    CYCLES=$(echo "${PERF_OUT}" | grep -E "cycles" | head -n1 | cut -d, -f1)
                    INSTR=$(echo "${PERF_OUT}" | grep -E "instructions" | head -n1 | cut -d, -f1)
                    CPUCLK=$(echo "${PERF_OUT}" | grep -E "cpu-clock" | head -n1 | cut -d, -f1)
                    L1=$(echo "${PERF_OUT}" | grep "L1-dcache-load-misses" | head -n1 | cut -d, -f1)
                    LLC=$(echo "${PERF_OUT}" | grep "LLC-load-misses" | head -n1 | cut -d, -f1)

                    IPC=$(awk "BEGIN { printf \"%.4f\", ${INSTR}/${CYCLES} }")
                    EFF_FREQ=$(awk "BEGIN { printf \"%.3f\", ${CYCLES}/(${CPUCLK}*1e6) }")

                    echo "${MODE},${GOV},${ITER},${WS},${STR},${CH},${CYCLES},${INSTR},${CPUCLK},${IPC},${EFF_FREQ},${L1},${LLC}" >> ${OUT}
                done

            elif [ "${MODE}" == "cache" ]; then
                for WS in "${WORKSETS[@]}"; do
                    for STR in "${STRIDES[@]}"; do
                        for CH in "${CHAINS[@]}"; do
                            echo "Run: mode=${MODE}, gov=${GOV}, iter=${ITER}, ws=${WS}, stride=${STR}, chains=${CH}"

                            PERF_OUT=$(sudo taskset -c ${CPU} perf stat -x, -e ${EVENTS} \
                                ${BIN} ${MODE} ${ITER} ${WS} ${STR} 2>&1)

                            CYCLES=$(echo "${PERF_OUT}" | grep -E "cycles" | head -n1 | cut -d, -f1)
                            INSTR=$(echo "${PERF_OUT}" | grep -E "instructions" | head -n1 | cut -d, -f1)
                            CPUCLK=$(echo "${PERF_OUT}" | grep -E "cpu-clock" | head -n1 | cut -d, -f1)
                            L1=$(echo "${PERF_OUT}" | grep "L1-dcache-load-misses" | head -n1 | cut -d, -f1)
                            LLC=$(echo "${PERF_OUT}" | grep "LLC-load-misses" | head -n1 | cut -d, -f1)

                            IPC=$(awk "BEGIN { printf \"%.4f\", ${INSTR}/${CYCLES} }")
                            EFF_FREQ=$(awk "BEGIN { printf \"%.3f\", ${CYCLES}/(${CPUCLK}*1e6) }")

                            echo "${MODE},${GOV},${ITER},${WS},${STR},${CH},${CYCLES},${INSTR},${CPUCLK},${IPC},${EFF_FREQ},${L1},${LLC}" >> ${OUT}
                        done
                    done
                done
            fi
        done
    done
done

echo "Sweep completed. Results saved to ${OUT}"

