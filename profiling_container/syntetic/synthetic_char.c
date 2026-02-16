#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

/* -------------------------------------------------
 * Sniper ROI hooks
 * ------------------------------------------------- */
#ifdef ENABLE_SNIPER
#include "sim_api.h"
#else
#define SimRoiStart()
#define SimRoiEnd()
#endif

/* Prevent compiler from optimizing away loops */
#define COMPILER_BARRIER() asm volatile("" ::: "memory")


#include <stdint.h>
#include <stdlib.h>
#define SIZE_N 1000

volatile double sink_p;

/* -------------------------------------------------
 * Compute-bound frequency-scaling kernel - Parallel
 * ------------------------------------------------- */

void freq_kernel_p(uint64_t iters, uint64_t N)
{
    double *a = malloc(N * sizeof(double));
    double *b = malloc(N * sizeof(double));
    double *c = malloc(N * sizeof(double));

    // Initialize arrays
    for (uint64_t i = 0; i < N; i++) {
        a[i] = 1.1;
        b[i] = 2.2;
        c[i] = 3.3;
    }
	printf("ROI_START\n");
    SimRoiStart();
    for (uint64_t iter = 0; iter < iters; iter++) {
        for (uint64_t i = 0; i < N; i++) {
            a[i] = b[i] * c[i] + a[i];
        }
    }
    SimRoiEnd();
	printf("ROI_END\n");

    // Prevent optimization
    double sum = 0.0;
    for (uint64_t i = 0; i < N; i++)
        sum += a[i];
    sink_p = sum;

    free(a);
    free(b);
    free(c);
}


/* -------------------------------------------------
 * Compute-bound frequency-scaling kernel - Serial
 * ------------------------------------------------- */
volatile double sink;

void freq_kernel(uint64_t iters)
{
    double a = 1.1, b = 2.2, c = 3.3;

	printf("ROI_START\n");
    SimRoiStart();
    for (uint64_t i = 0; i < iters; i++) {
        a = a * b + c;
        b = b * c + a;
        c = c * a + b;
    }
    SimRoiEnd();
	printf("ROI_END\n");

    sink = a + b + c;
}


/* -------------------------------------------------
 * Cache-sensitive pointer chasing kernel
 * ------------------------------------------------- */
void cache_kernel(uint64_t *array, uint64_t iters)
{
    uint64_t idx = 0;

    SimRoiStart();
    for (uint64_t i = 0; i < iters; i++) {
        idx = array[idx];
    }
    SimRoiEnd();

    COMPILER_BARRIER();
}

/* -------------------------------------------------
 * Initialize pointer-chasing array
 * ------------------------------------------------- */
void init_array(uint64_t *array, uint64_t size, uint64_t stride)
{
    for (uint64_t i = 0; i < size; i++) {
        array[i] = (i + stride) % size;
    }
}

/* -------------------------------------------------
 * Main
 * ------------------------------------------------- */
int main(int argc, char **argv)
{
    if (argc < 5) {
        printf("Usage: %s <mode> <iters> <working_set_elems> <stride>\n", argv[0]);
        printf("  mode: freq | freq_p | cache\n");
        exit(1);
    }

    const char *mode = argv[1];
    uint64_t iters   = strtoull(argv[2], NULL, 10);
    uint64_t ws      = strtoull(argv[3], NULL, 10);
    uint64_t stride  = strtoull(argv[4], NULL, 10);

    if (!strcmp(mode, "freq")) {
        freq_kernel(iters);
    }
    else if (!strcmp(mode, "freq_p")) {
        freq_kernel_p(iters,SIZE_N);
    }
    else if (!strcmp(mode, "cache")) {
        uint64_t *array = aligned_alloc(64, ws * sizeof(uint64_t));
        if (!array) {
            perror("aligned_alloc");
            exit(1);
        }

        init_array(array, ws, stride);
        cache_kernel(array, iters);

        free(array);
    }
    else {
        printf("Unknown mode: %s\n", mode);
        exit(1);
    }

    return 0;
}

