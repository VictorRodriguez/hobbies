FROM ubuntu:24.04

WORKDIR /app

COPY gemm_stress_avx2_sniper /app/gemm_stress_avx2_sniper
COPY gemm_stress_avx512_sniper /app/gemm_stress_avx512_sniper
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["100", "256", "256", "256"]
