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

/* -------------------------------------------------
 * Compute-bound frequency-scaling kernel
 * ------------------------------------------------- */
volatile double sink;

void freq_kernel(uint64_t iters)
{
    double a = 1.1, b = 2.2, c = 3.3;

    SimRoiStart();
    for (uint64_t i = 0; i < iters; i++) {
        a = a * b + c;
        b = b * c + a;
        c = c * a + b;
    }
    SimRoiEnd();

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
        printf("  mode: freq | cache\n");
        exit(1);
    }

    const char *mode = argv[1];
    uint64_t iters   = strtoull(argv[2], NULL, 10);
    uint64_t ws      = strtoull(argv[3], NULL, 10);
    uint64_t stride  = strtoull(argv[4], NULL, 10);

    if (!strcmp(mode, "freq")) {
        freq_kernel(iters);
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

