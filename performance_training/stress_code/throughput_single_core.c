#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <sched.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

#ifndef DEFAULT_ITERS
#define DEFAULT_ITERS 1000000000ULL
#endif

#define OPS_PER_ITER 8ULL

static void pin_to_core(int core_id)
{
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(core_id, &set);

    if (sched_setaffinity(0, sizeof(set), &set) != 0) {
        fprintf(stderr, "Warning: failed to pin to core %d: %s\n",
                core_id, strerror(errno));
    }
}

static double seconds_now(void)
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
}

static uint64_t run_integer_workload(uint64_t iters)
{
    uint64_t a = 0x123456789abcdef0ULL;
    uint64_t b = 0xfedcba9876543210ULL;
    uint64_t c = 0x0f0f0f0f0f0f0f0fULL;
    uint64_t d = 0xf0f0f0f0f0f0f0f0ULL;

    for (uint64_t i = 0; i < iters; i++) {
        a += b;
        b ^= c;
        c += d;
        d ^= a;

        a = (a << 7) | (a >> 57);
        b = (b << 13) | (b >> 51);
        c = (c << 17) | (c >> 47);
        d = (d << 29) | (d >> 35);
    }

    return a ^ b ^ c ^ d;
}

int main(int argc, char **argv)
{
    uint64_t iters = DEFAULT_ITERS;
    int core_id = 0;

    if (argc >= 2) {
        iters = strtoull(argv[1], NULL, 10);
    }

    if (argc >= 3) {
        core_id = atoi(argv[2]);
    }

    pin_to_core(core_id);

    printf("Single-core throughput benchmark\n");
    printf("Iterations:        %lu\n", iters);
    printf("Operations/iter:   %lu\n", (uint64_t)OPS_PER_ITER);
    printf("Pinned core:       %d\n", core_id);
    fflush(stdout);

    /*
     * Warm-up phase.
     * Useful on real HW to reduce cold-start effects.
     */
    volatile uint64_t warmup = run_integer_workload(1000000ULL);
    (void)warmup;

    double t0 = seconds_now();

    volatile uint64_t checksum = run_integer_workload(iters);

    double t1 = seconds_now();
    double elapsed = t1 - t0;

    uint64_t total_ops = iters * OPS_PER_ITER;

    double iter_per_sec = (double)iters / elapsed;
    double ops_per_sec  = (double)total_ops / elapsed;
    double giga_ops_sec = ops_per_sec / 1e9;

    printf("\nResults\n");
    printf("Elapsed seconds:   %.9f\n", elapsed);
    printf("Iterations/sec:    %.3f\n", iter_per_sec);
    printf("Operations:        %lu\n", total_ops);
    printf("Operations/sec:    %.3f\n", ops_per_sec);
    printf("GOPS:              %.6f\n", giga_ops_sec);
    printf("Checksum:          %lu\n", checksum);

    return 0;
}
