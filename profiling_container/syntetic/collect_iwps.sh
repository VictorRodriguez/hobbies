#!/usr/bin/env bash

RESULTS_DIR="results_iwps"
CSV_FILE="iwps_workload_results.csv"

echo "mode,iterations,working_set,stride,frequency,cycles,instructions,ipc,eff_freq_ghz,l1_misses,llc_misses" > "${CSV_FILE}"

echo "Scanning IWPS results under ${RESULTS_DIR}"

# Iterate freq and cache directories
for MODE_DIR in "${RESULTS_DIR}"/*; do
    MODE=$(basename "${MODE_DIR}")   # freq or cache

    for ITER_DIR in "${MODE_DIR}"/*; do
        ITER=$(basename "${ITER_DIR}" | sed 's/iter_//')

        # For cache, extra level: ws/stride/freq
        if [[ "${MODE}" == "cache" ]]; then
            for WS_DIR in "${ITER_DIR}"/*; do
                WS=$(basename "${WS_DIR}" | sed 's/ws_//')
                for STR_DIR in "${WS_DIR}"/*; do
                    STR=$(basename "${STR_DIR}" | sed 's/stride_//')
                    for FREQ_DIR in "${STR_DIR}"/*; do
                        FREQUENCY=$(basename "${FREQ_DIR}" | sed 's/freq_//; s/GHz//')
                        SIMOUT="${FREQ_DIR}/sim.out"
                        if [[ ! -f "${SIMOUT}" ]]; then
                            echo "WARNING: ${SIMOUT} does not exist, skipping"
                            continue
                        fi
                        echo "Parsing ${MODE}: iter=${ITER}, ws=${WS}, stride=${STR}, freq=${FREQUENCY} GHz"
                        python3 parse_simout.py \
                            --simout "${SIMOUT}" \
                            --mode "${MODE}" \
                            --iterations "${ITER}" \
                            --working-set "${WS}" \
                            --stride "${STR}" \
                            --frequency "${FREQUENCY}" \
                            --csv "${CSV_FILE}"
                    done
                done
            done

        # For freq mode: iter/freq
        elif [[ "${MODE}" == "freq" ]]; then
            for FREQ_DIR in "${ITER_DIR}"/*; do
                FREQUENCY=$(basename "${FREQ_DIR}" | sed 's/freq_//; s/GHz//')
                SIMOUT="${FREQ_DIR}/sim.out"
                if [[ ! -f "${SIMOUT}" ]]; then
                    echo "WARNING: ${SIMOUT} does not exist, skipping"
                    continue
                fi
                echo "Parsing ${MODE}: iter=${ITER}, freq=${FREQUENCY} GHz"
                python3 parse_simout.py \
                    --simout "${SIMOUT}" \
                    --mode "${MODE}" \
                    --iterations "${ITER}" \
                    --working-set NA \
                    --stride NA \
                    --frequency "${FREQUENCY}" \
                    --csv "${CSV_FILE}"
            done
        fi
    done
done

echo "IWPS results collected in ${CSV_FILE}"

