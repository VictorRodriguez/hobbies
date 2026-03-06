#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

/* Prevent compiler from optimizing away loops */
#define COMPILER_BARRIER() asm volatile("" ::: "memory")

volatile double sink_p = 0.0;
volatile double sink   = 0.0;
volatile uint64_t sink_idx = 0;

/* -------------------------------------------------
 * Compute-bound frequency-scaling kernel - Parallel
 * ------------------------------------------------- */
void freq_kernel_p(uint64_t iters, uint64_t N)
{
    double *a = malloc(N * sizeof(double));
    double *b = malloc(N * sizeof(double));
    double *c = malloc(N * sizeof(double));

    if (!a || !b || !c) {
        perror("malloc");
        free(a);
        free(b);
        free(c);
        exit(EXIT_FAILURE);
    }

    for (uint64_t i = 0; i < N; i++) {
        a[i] = 1.1;
        b[i] = 2.2;
        c[i] = 3.3;
    }

    printf("ROI_START\n");
    for (uint64_t iter = 0; iter < iters; iter++) {
        for (uint64_t i = 0; i < N; i++) {
            a[i] = b[i] * c[i] + a[i];
        }
    }
    printf("ROI_END\n");

    double sum = 0.0;
    for (uint64_t i = 0; i < N; i++) {
        sum += a[i];
    }
    sink_p = sum;

    free(a);
    free(b);
    free(c);
}

/* -------------------------------------------------
 * Compute-bound frequency-scaling kernel - Serial
 * ------------------------------------------------- */
void freq_kernel(uint64_t iters)
{
    double a = 1.1, b = 2.2, c = 3.3;

    printf("ROI_START\n");
    for (uint64_t i = 0; i < iters; i++) {
        a = a * b + c;
        b = b * c + a;
        c = c * a + b;
    }
    printf("ROI_END\n");

    sink = a + b + c;
}

/* -------------------------------------------------
 * Cache-sensitive pointer chasing kernel
 * ------------------------------------------------- */
void cache_kernel(uint64_t *array, uint64_t iters)
{
    uint64_t idx = 0;

    printf("ROI_START\n");
    for (uint64_t i = 0; i < iters; i++) {
        idx = array[idx];
    }
    printf("ROI_END\n");

    COMPILER_BARRIER();
    sink_idx = idx;
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
        return EXIT_FAILURE;
    }

    const char *mode = argv[1];
    uint64_t iters   = strtoull(argv[2], NULL, 10);
    uint64_t ws      = strtoull(argv[3], NULL, 10);
    uint64_t stride  = strtoull(argv[4], NULL, 10);

    if (!strcmp(mode, "freq")) {
        freq_kernel(iters);
    }
    else if (!strcmp(mode, "freq_p")) {
        if (ws == 0) {
            fprintf(stderr, "working_set_elems must be > 0 for freq_p\n");
            return EXIT_FAILURE;
        }
        freq_kernel_p(iters, ws);
    }
    else if (!strcmp(mode, "cache")) {
        if (ws == 0) {
            fprintf(stderr, "working_set_elems must be > 0 for cache\n");
            return EXIT_FAILURE;
        }

        uint64_t *array = NULL;
        if (posix_memalign((void **)&array, 64, ws * sizeof(uint64_t)) != 0) {
            perror("posix_memalign");
            return EXIT_FAILURE;
        }

        init_array(array, ws, stride);
        cache_kernel(array, iters);

        free(array);
    }
    else {
        fprintf(stderr, "Unknown mode: %s\n", mode);
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
