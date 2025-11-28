#!/bin/bash
set -x

# Optionally enable DMR/AMX/AVX10 support if requested
if [ -n "$ONEDNN_MAX_CPU_ISA" ]; then
    export ONEDNN_MAX_CPU_ISA=$ONEDNN_MAX_CPU_ISA
fi

export DNNL_CPU_RUNTIME=OMP
export OMP_PLACES=cores
export OMP_PROC_BIND=close

# Run the benchmark with flexible options
./benchdnn $DRIVER --dt=$DT --batch=$BATCH $EXTRA_ARGS

