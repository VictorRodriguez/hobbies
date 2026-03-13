#!/bin/sh
set -eu

ARCH="${ARCH:-avx2}"

case "$ARCH" in
  avx2)
    exec /app/gemm_stress_avx2_sniper "$@"
    ;;
  avx512)
    exec /app/gemm_stress_avx512_sniper "$@"
    ;;
  *)
    echo "Error: ARCH must be 'avx2' or 'avx512'" >&2
    exit 1
    ;;
esac
