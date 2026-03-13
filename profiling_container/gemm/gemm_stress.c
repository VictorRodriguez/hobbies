// gemm_stress.c
// Minimal GEMM "microkernel approach" benchmark with ROI markers.
// Computes: C = C + A*B, repeated for iters.
// A is column-major (M x K), B is row-major (K x N), C is row-major (M x N).

#define _GNU_SOURCE
#include <immintrin.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef USE_SNIPER
#include "sim_api.h"
#endif

static volatile double sink_p = 0.0;

static void *aligned_malloc(size_t alignment, size_t size) {
    void *p = NULL;
    if (posix_memalign(&p, alignment, size) != 0) return NULL;
    return p;
}

// -------------------- AVX2 microkernel: MR=4, NR=4 (double) --------------------
__attribute__((noinline))
static void gemm_kernel_4x4_avx2(
    const double *Acol, const double *Brow, double *Crow,
    uint64_t M, uint64_t N, uint64_t K,
    uint64_t i, uint64_t j
) {
    // Load C block (4 rows x 4 cols). Each column is a __m256d (4 doubles).
    __m256d c0 = _mm256_loadu_pd(&Crow[(i + 0) * N + (j + 0)]); // rows i..i+3, col j+0 (not contiguous!)
    // Above would be wrong for row-major; rows are strided by N.
    // Instead, we store C row-major and load 4 elements from ONE ROW contiguous.
    // So for AVX2 we vectorize across columns (NR=4) for a single row at a time.
    //
    // We'll compute 4 rows, each row vectorized across 4 columns.

    __m256d c_r0 = _mm256_loadu_pd(&Crow[(i + 0) * N + j]);
    __m256d c_r1 = _mm256_loadu_pd(&Crow[(i + 1) * N + j]);
    __m256d c_r2 = _mm256_loadu_pd(&Crow[(i + 2) * N + j]);
    __m256d c_r3 = _mm256_loadu_pd(&Crow[(i + 3) * N + j]);

    for (uint64_t k = 0; k < K; k++) {
        // Load B row k, columns j..j+3 (contiguous)
        __m256d b = _mm256_loadu_pd(&Brow[k * N + j]);

        // Load A scalars for 4 rows at column k from Acol (column-major)
        double a0 = Acol[k * M + (i + 0)];
        double a1 = Acol[k * M + (i + 1)];
        double a2 = Acol[k * M + (i + 2)];
        double a3 = Acol[k * M + (i + 3)];

        c_r0 = _mm256_fmadd_pd(_mm256_set1_pd(a0), b, c_r0);
        c_r1 = _mm256_fmadd_pd(_mm256_set1_pd(a1), b, c_r1);
        c_r2 = _mm256_fmadd_pd(_mm256_set1_pd(a2), b, c_r2);
        c_r3 = _mm256_fmadd_pd(_mm256_set1_pd(a3), b, c_r3);
    }

    _mm256_storeu_pd(&Crow[(i + 0) * N + j], c_r0);
    _mm256_storeu_pd(&Crow[(i + 1) * N + j], c_r1);
    _mm256_storeu_pd(&Crow[(i + 2) * N + j], c_r2);
    _mm256_storeu_pd(&Crow[(i + 3) * N + j], c_r3);

    (void)c0; // silence unused warning from earlier note
}

// -------------------- AVX-512 microkernel: MR=8, NR=8 (double) --------------------
#ifdef __AVX512F__
__attribute__((noinline))
static void gemm_kernel_8x8_avx512(
    const double *Acol, const double *Brow, double *Crow,
    uint64_t M, uint64_t N, uint64_t K,
    uint64_t i, uint64_t j
) {
    // C rows i..i+7, columns j..j+7 (row-major, contiguous across columns)
    __m512d c0 = _mm512_loadu_pd(&Crow[(i + 0) * N + j]);
    __m512d c1 = _mm512_loadu_pd(&Crow[(i + 1) * N + j]);
    __m512d c2 = _mm512_loadu_pd(&Crow[(i + 2) * N + j]);
    __m512d c3 = _mm512_loadu_pd(&Crow[(i + 3) * N + j]);
    __m512d c4 = _mm512_loadu_pd(&Crow[(i + 4) * N + j]);
    __m512d c5 = _mm512_loadu_pd(&Crow[(i + 5) * N + j]);
    __m512d c6 = _mm512_loadu_pd(&Crow[(i + 6) * N + j]);
    __m512d c7 = _mm512_loadu_pd(&Crow[(i + 7) * N + j]);

    for (uint64_t k = 0; k < K; k++) {
        // Load 8 columns of B for this k (contiguous)
        __m512d b = _mm512_loadu_pd(&Brow[k * N + j]);

        // Broadcast A(i..i+7, k) scalars
        double a0 = Acol[k * M + (i + 0)];
        double a1 = Acol[k * M + (i + 1)];
        double a2 = Acol[k * M + (i + 2)];
        double a3 = Acol[k * M + (i + 3)];
        double a4 = Acol[k * M + (i + 4)];
        double a5 = Acol[k * M + (i + 5)];
        double a6 = Acol[k * M + (i + 6)];
        double a7 = Acol[k * M + (i + 7)];

        c0 = _mm512_fmadd_pd(_mm512_set1_pd(a0), b, c0);
        c1 = _mm512_fmadd_pd(_mm512_set1_pd(a1), b, c1);
        c2 = _mm512_fmadd_pd(_mm512_set1_pd(a2), b, c2);
        c3 = _mm512_fmadd_pd(_mm512_set1_pd(a3), b, c3);
        c4 = _mm512_fmadd_pd(_mm512_set1_pd(a4), b, c4);
        c5 = _mm512_fmadd_pd(_mm512_set1_pd(a5), b, c5);
        c6 = _mm512_fmadd_pd(_mm512_set1_pd(a6), b, c6);
        c7 = _mm512_fmadd_pd(_mm512_set1_pd(a7), b, c7);
    }

    _mm512_storeu_pd(&Crow[(i + 0) * N + j], c0);
    _mm512_storeu_pd(&Crow[(i + 1) * N + j], c1);
    _mm512_storeu_pd(&Crow[(i + 2) * N + j], c2);
    _mm512_storeu_pd(&Crow[(i + 3) * N + j], c3);
    _mm512_storeu_pd(&Crow[(i + 4) * N + j], c4);
    _mm512_storeu_pd(&Crow[(i + 5) * N + j], c5);
    _mm512_storeu_pd(&Crow[(i + 6) * N + j], c6);
    _mm512_storeu_pd(&Crow[(i + 7) * N + j], c7);
}
#endif

static void init_mats(double *Acol, double *Brow, double *Crow, uint64_t M, uint64_t N, uint64_t K) {
    // Acol: MxK column-major => Acol[k*M + i]
    for (uint64_t k = 0; k < K; k++)
        for (uint64_t i = 0; i < M; i++)
            Acol[k * M + i] = 1.0 + (double)((i + k) & 7) * 0.001;

    // Brow: KxN row-major => Brow[k*N + j]
    for (uint64_t k = 0; k < K; k++)
        for (uint64_t j = 0; j < N; j++)
            Brow[k * N + j] = 1.0 + (double)((j + k) & 7) * 0.002;

    // Crow: MxN row-major
    for (uint64_t i = 0; i < M; i++)
        for (uint64_t j = 0; j < N; j++)
            Crow[i * N + j] = 0.0;
}

int main(int argc, char **argv) {
    if (argc < 2 || argc > 5) {
        fprintf(stderr, "Usage: %s <iters> [M] [N] [K]\n", argv[0]);
        fprintf(stderr, "Defaults: M=N=K=32 (CPU-bound-ish on 1 core)\n");
        return 1;
    }

    uint64_t iters = strtoull(argv[1], NULL, 10);
    uint64_t M = (argc >= 3) ? strtoull(argv[2], NULL, 10) : 32;
    uint64_t N = (argc >= 4) ? strtoull(argv[3], NULL, 10) : 32;
    uint64_t K = (argc >= 5) ? strtoull(argv[4], NULL, 10) : 32;

    if (iters == 0 || M == 0 || N == 0 || K == 0) {
        fprintf(stderr, "iters/M/N/K must be > 0\n");
        return 1;
    }

    // Require N multiple of 4 due to NR=4
    if (N % 4 != 0) {
        fprintf(stderr, "N must be a multiple of 4 (NR=4)\n");
        return 1;
    }

    // Allocate aligned
    double *Acol = (double*)aligned_malloc(64, sizeof(double) * M * K);
    double *Brow = (double*)aligned_malloc(64, sizeof(double) * K * N);
    double *Crow = (double*)aligned_malloc(64, sizeof(double) * M * N);
    if (!Acol || !Brow || !Crow) {
        fprintf(stderr, "Allocation failed\n");
        return 1;
    }

    init_mats(Acol, Brow, Crow, M, N, K);

    printf("ROI_START\n");
#ifdef USE_SNIPER
    SimRoiStart();
#endif
#ifdef __AVX512F__
    const uint64_t MR = 8;
    const uint64_t NR = 8;
#else
    const uint64_t MR = 4;
    const uint64_t NR = 4;
#endif

    if (N % NR != 0) {
        fprintf(stderr, "N must be a multiple of %llu\n", (unsigned long long)NR);
        return 1;
    }

    for (uint64_t iter = 0; iter < iters; iter++) {
        for (uint64_t i = 0; i + MR <= M; i += MR) {
            for (uint64_t j = 0; j + NR <= N; j += NR) {
#ifdef __AVX512F__
                gemm_kernel_8x8_avx512(Acol, Brow, Crow, M, N, K, i, j);
#else
                gemm_kernel_4x4_avx2(Acol, Brow, Crow, M, N, K, i, j);
#endif
            }
        }
    }

#ifdef USE_SNIPER
    SimRoiEnd();
#endif
    printf("ROI_END\n");

    // Prevent DCE
    double sum = 0.0;
    for (uint64_t i = 0; i < M * N; i++) sum += Crow[i];
    sink_p = sum;
    fprintf(stderr, "checksum=%f\n", sum);

    free(Acol);
    free(Brow);
    free(Crow);
    return 0;
}

