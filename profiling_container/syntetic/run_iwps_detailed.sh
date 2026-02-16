#!/usr/bin/env bash
set -euo pipefail

# =================================================
# Configuration
# =================================================
BIN=./synthetic_char
PLATFORM=skx1c

MODES=("freq")

# Parameter sweeps (same as perf script)
#ITERATIONS=(10000000 50000000 200000000)
ITERATIONS=(100000000 500000000 2000000000)
WORKSETS=(1024 16384 262144)
STRIDES=(1 8 64 256)

# Output
RESULTS_DIR=results_iwps
MANIFEST=${RESULTS_DIR}/manifest.csv

# =================================================
# Prepare output
# =================================================
mkdir -p "${RESULTS_DIR}"

echo "mode,freq_ghz,iterations,working_set,stride,outdir" > "${MANIFEST}"

# =================================================
# Helper: choose frequency based on workload
# =================================================
select_frequency() {
  local mode=$1
  local ws=$2

  if [[ "${mode}" == "freq" ]]; then
    # Compute-bound (from perf characterization)
    echo "3.8"
  else
    # Cache / memory-bound
    if (( ws <= 16384 )); then
      # L1/L2 bound region
      echo "0.8"
    else
      # LLC / memory-bound region
      echo "2.5"
    fi
  fi
}

# =================================================
# Sweep loop
# =================================================
for MODE in "${MODES[@]}"; do
  for ITER in "${ITERATIONS[@]}"; do

    if [[ "${MODE}" == "freq" ]]; then
      WS=1
      STR=1
      FREQ=$(select_frequency "${MODE}" "${WS}")

      OUTDIR="${RESULTS_DIR}/${MODE}/iter_${ITER}/freq_${FREQ}GHz"
      mkdir -p "${OUTDIR}"

      CMD=(
        run-iwps
        -c "${PLATFORM}"
        -c "perf_model/core/frequency=${FREQ}"
        --roi
        -d "${OUTDIR}"
        --
        "${BIN}" freq "${ITER}" "${WS}" "${STR}"
      )

      echo "=================================================="
      echo "Run: mode=freq iter=${ITER} freq=${FREQ}GHz"
      echo "CMD: ${CMD[*]}"
      echo "=================================================="

      "${CMD[@]}"

      if [[ ! -f "${OUTDIR}/sim.out" ]]; then
        echo "ERROR: sim.out not found in ${OUTDIR}"
        exit 1
      fi

      echo "freq,${FREQ},${ITER},NA,NA,${OUTDIR}" >> "${MANIFEST}"

    elif [[ "${MODE}" == "cache" ]]; then
      for WS in "${WORKSETS[@]}"; do
        for STR in "${STRIDES[@]}"; do

          FREQ=$(select_frequency "${MODE}" "${WS}")
          OUTDIR="${RESULTS_DIR}/${MODE}/iter_${ITER}/ws_${WS}/stride_${STR}/freq_${FREQ}GHz"
          mkdir -p "${OUTDIR}"

          CMD=(
            run-iwps
            -c "${PLATFORM}"
            -c "perf_model/core/frequency=${FREQ}"
            -d "${OUTDIR}"
            --
            "${BIN}" cache "${ITER}" "${WS}" "${STR}"
          )

          echo "=================================================="
          echo "Run: mode=cache iter=${ITER} ws=${WS} stride=${STR} freq=${FREQ}GHz"
          echo "CMD: ${CMD[*]}"
          echo "=================================================="

          "${CMD[@]}"

          if [[ ! -f "${OUTDIR}/sim.out" ]]; then
            echo "ERROR: sim.out not found in ${OUTDIR}"
            exit 1
          fi

          echo "cache,${FREQ},${ITER},${WS},${STR},${OUTDIR}" >> "${MANIFEST}"

        done
      done
    fi
  done
done

echo "=================================================="
echo "IWPS sweep completed successfully"
echo "Manifest saved to ${MANIFEST}"
echo "=================================================="

