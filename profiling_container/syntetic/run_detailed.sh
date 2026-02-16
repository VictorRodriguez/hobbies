#!/usr/bin/env bash

# ----------------------------------------
# Configuration
# ----------------------------------------
BIN=./synthetic_char
MODES=("freq" "cache")
CPU=0

OUT=workload_sweep_results_detailed.csv

# Perf events
EVENTS="cycles,instructions,cpu-clock,branches,branch-misses,L1-dcache-load-misses,LLC-load-misses"

# Governors available under intel_pstate
GOVERNORS=("performance" "powersave")

# Workload parameter sweeps
#ITERATIONS=(100000000 500000000 2000000000)
#ITERATIONS=(10000000 50000000 200000000)
#WORKSETS=(1024 16384 262144)
#WORKSETS=(4194304 16777216 67108864 268435456)
#STRIDES=(1 8 64 256)

# Parameter sweeps (same as perf script)
ITERATIONS=(100000000 500000000 2000000000)
WORKSETS=(4194304 16777216 67108864)
STRIDES=(1 8 64 256)

# ----------------------------------------
# CSV Header
# ----------------------------------------
echo "mode,governor,iterations,working_set,stride,cycles,instructions,cpu_clock_ms,ipc,eff_freq_ghz,L1_misses,LLC_misses" > ${OUT}

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
                    echo "Run: mode=${MODE}, gov=${GOV}, iter=${ITER}"
					perf_cmd=(
						sudo taskset -c "${CPU}"
						perf stat -x, -e "${EVENTS}"
						"${BIN}" "${MODE}" "${ITER}" 1 1
					)

				# Print the full command
				echo "Running command:"
				printf '%q ' "${perf_cmd[@]}"
				echo

				# Run and capture output (perf stat writes to stderr)
				PERF_OUT="$("${perf_cmd[@]}" 2>&1)"

				# Print perf output
				echo "Perf output:"
				echo "${PERF_OUT}"


                    CYCLES=$(echo "${PERF_OUT}" | grep -E "cycles" | head -n1 | cut -d, -f1)
                    INSTR=$(echo "${PERF_OUT}" | grep -E "instructions" | head -n1 | cut -d, -f1)
                    CPUCLK=$(echo "${PERF_OUT}" | grep -E "cpu-clock" | head -n1 | cut -d, -f1)
                    L1=$(echo "${PERF_OUT}" | grep "L1-dcache-load-misses" | head -n1 | cut -d, -f1)
                    LLC=$(echo "${PERF_OUT}" | grep "LLC-load-misses" | head -n1 | cut -d, -f1)

                    IPC=$(awk "BEGIN { printf \"%.4f\", ${INSTR}/${CYCLES} }")
                    EFF_FREQ=$(awk "BEGIN { printf \"%.3f\", ${CYCLES}/(${CPUCLK}*1e6) }")

                    echo "${MODE},${GOV},${ITER},${WS},${STR},${CYCLES},${INSTR},${CPUCLK},${IPC},${EFF_FREQ},${L1},${LLC}" >> ${OUT}

            elif [ "${MODE}" == "cache" ]; then
                for WS in "${WORKSETS[@]}"; do
                    for STR in "${STRIDES[@]}"; do
                            echo "Run: mode=${MODE}, gov=${GOV}, iter=${ITER}, ws=${WS}, stride=${STR}}"

							echo "Run: mode=${MODE}, gov=${GOV}, iter=${ITER}"
							perf_cmd=(
								sudo taskset -c "${CPU}"
								perf stat -x, -e "${EVENTS}"
								"${BIN}" "${MODE}" "${ITER}" "${WS}" "${STR}"
							)

							# Print the full command
							echo "Running command:"
							printf '%q ' "${perf_cmd[@]}"
							echo

							# Run and capture output (perf stat writes to stderr)
							PERF_OUT="$("${perf_cmd[@]}" 2>&1)"

							# Print perf output
							echo "Perf output:"
							echo "${PERF_OUT}"

                            CYCLES=$(echo "${PERF_OUT}" | grep -E "cycles" | head -n1 | cut -d, -f1)
                            INSTR=$(echo "${PERF_OUT}" | grep -E "instructions" | head -n1 | cut -d, -f1)
                            CPUCLK=$(echo "${PERF_OUT}" | grep -E "cpu-clock" | head -n1 | cut -d, -f1)
                            L1=$(echo "${PERF_OUT}" | grep "L1-dcache-load-misses" | head -n1 | cut -d, -f1)
                            LLC=$(echo "${PERF_OUT}" | grep "LLC-load-misses" | head -n1 | cut -d, -f1)

                            IPC=$(awk "BEGIN { printf \"%.4f\", ${INSTR}/${CYCLES} }")
                            EFF_FREQ=$(awk "BEGIN { printf \"%.3f\", ${CYCLES}/(${CPUCLK}*1e6) }")

                            echo "${MODE},${GOV},${ITER},${WS},${STR},${CYCLES},${INSTR},${CPUCLK},${IPC},${EFF_FREQ},${L1},${LLC}" >> ${OUT}
                    done
                done
            fi
        done
    done
done

echo "Sweep completed. Results saved to ${OUT}"

