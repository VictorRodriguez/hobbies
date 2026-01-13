#!/bin/bash
set -e

OUT_CSV="workload_sweep_results.csv"
IWPS_CFG="skx1c"

echo "mode,governor,iterations,working_set,stride,cycles,instructions,ipc,eff_freq_ghz,l1_misses,llc_misses" > ${OUT_CSV}

# ---------------------------------------
# Compute-bound (frequency sensitivity)
# ---------------------------------------
for gov in performance powersave; do
  for iters in 1e6 1e7 1e8; do
    OUTDIR="results/freq/${gov}_${iters}"
    mkdir -p ${OUTDIR}

    run-iwps \
      -c ${IWPS_CFG} \
      --roi \
      -d ${OUTDIR} \
      -- ./synthetic_char freq ${iters}

    python3 parse_simout.py \
      --simout ${OUTDIR}/sim.out \
      --mode freq \
      --governor ${gov} \
      --iterations ${iters} \
      --csv ${OUT_CSV}
  done
done

# ---------------------------------------
# Memory-bound (cache sensitivity)
# ---------------------------------------
for ws in 4096 16384 65536; do
  for stride in 1 4 16 64; do
    OUTDIR="results/cache/ws${ws}_s${stride}"
    mkdir -p ${OUTDIR}

    run-iwps \
      -c ${IWPS_CFG} \
      --roi \
      -d ${OUTDIR} \
      -- ./synthetic_char cache 100000000 ${ws} ${stride}

    python3 parse_simout.py \
      --simout ${OUTDIR}/sim.out \
      --mode cache \
      --working-set ${ws} \
      --stride ${stride} \
      --csv ${OUT_CSV}
  done
done

