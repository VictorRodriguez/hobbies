#!/bin/bash

set -x

cd /oneDNN/build/tests/benchdnn
export DNNL_CPU_RUNTIME=OMP
export OMP_PLACES=cores
export OMP_PROC_BIND=close

DNNL_VERBOSE=1 ./benchdnn --engine=cpu --mode=p $DRIVER --cfg=$CONFIG --batch=$BATCH
