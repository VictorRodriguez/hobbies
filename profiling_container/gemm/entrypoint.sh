#!/bin/sh
set -eu

ARCH=${ARCH:-avx2}
ITERS=${ITERS:-10}
M=${M:-256}
N=${N:-256}
K=${K:-256}

case "$ARCH" in
  avx2)
    BIN="/app/gemm_stress_avx2"
    ;;
  avx512)
    BIN="/app/gemm_stress_avx512"
    ;;
  *)
    echo "Error: ARCH must be avx2 or avx512"
    exit 1
    ;;
esac

echo "Running GEMM benchmark"
echo "ISA   : $ARCH"
echo "iters : $ITERS"
echo "M,N,K : $M $N $K"
echo ""

exec "$BIN" "$ITERS" "$M" "$N" "$K"
