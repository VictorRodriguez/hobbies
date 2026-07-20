#define _GNU_SOURCE
#include <errno.h>
#include <inttypes.h>
#include <sched.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#ifndef DEFAULT_ITERS
#define DEFAULT_ITERS 200000000ULL
#endif

#ifndef ARRAY_SIZE
#define ARRAY_SIZE (1U << 20)
#endif

#ifndef INDIRECT_TARGETS
#define INDIRECT_TARGETS 32
#endif

static volatile uint64_t sink = 0;

typedef uint64_t (*branch_fn_t)(uint64_t);

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

static double now_seconds(void)
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1.0e-9;
}

static inline uint64_t xorshift64(uint64_t *state)
{
    uint64_t x = *state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    *state = x;
    return x;
}

__attribute__((noinline)) static uint64_t target_00(uint64_t x) { return x + 0x01; }
__attribute__((noinline)) static uint64_t target_01(uint64_t x) { return x ^ 0x03; }
__attribute__((noinline)) static uint64_t target_02(uint64_t x) { return x + 0x05; }
__attribute__((noinline)) static uint64_t target_03(uint64_t x) { return x ^ 0x07; }
__attribute__((noinline)) static uint64_t target_04(uint64_t x) { return x + 0x0b; }
__attribute__((noinline)) static uint64_t target_05(uint64_t x) { return x ^ 0x0d; }
__attribute__((noinline)) static uint64_t target_06(uint64_t x) { return x + 0x11; }
__attribute__((noinline)) static uint64_t target_07(uint64_t x) { return x ^ 0x13; }
__attribute__((noinline)) static uint64_t target_08(uint64_t x) { return x + 0x17; }
__attribute__((noinline)) static uint64_t target_09(uint64_t x) { return x ^ 0x1d; }
__attribute__((noinline)) static uint64_t target_10(uint64_t x) { return x + 0x1f; }
__attribute__((noinline)) static uint64_t target_11(uint64_t x) { return x ^ 0x25; }
__attribute__((noinline)) static uint64_t target_12(uint64_t x) { return x + 0x29; }
__attribute__((noinline)) static uint64_t target_13(uint64_t x) { return x ^ 0x2b; }
__attribute__((noinline)) static uint64_t target_14(uint64_t x) { return x + 0x2f; }
__attribute__((noinline)) static uint64_t target_15(uint64_t x) { return x ^ 0x35; }
__attribute__((noinline)) static uint64_t target_16(uint64_t x) { return x + 0x3b; }
__attribute__((noinline)) static uint64_t target_17(uint64_t x) { return x ^ 0x3d; }
__attribute__((noinline)) static uint64_t target_18(uint64_t x) { return x + 0x43; }
__attribute__((noinline)) static uint64_t target_19(uint64_t x) { return x ^ 0x47; }
__attribute__((noinline)) static uint64_t target_20(uint64_t x) { return x + 0x49; }
__attribute__((noinline)) static uint64_t target_21(uint64_t x) { return x ^ 0x4f; }
__attribute__((noinline)) static uint64_t target_22(uint64_t x) { return x + 0x53; }
__attribute__((noinline)) static uint64_t target_23(uint64_t x) { return x ^ 0x59; }
__attribute__((noinline)) static uint64_t target_24(uint64_t x) { return x + 0x61; }
__attribute__((noinline)) static uint64_t target_25(uint64_t x) { return x ^ 0x65; }
__attribute__((noinline)) static uint64_t target_26(uint64_t x) { return x + 0x67; }
__attribute__((noinline)) static uint64_t target_27(uint64_t x) { return x ^ 0x6b; }
__attribute__((noinline)) static uint64_t target_28(uint64_t x) { return x + 0x6d; }
__attribute__((noinline)) static uint64_t target_29(uint64_t x) { return x ^ 0x71; }
__attribute__((noinline)) static uint64_t target_30(uint64_t x) { return x + 0x7f; }
__attribute__((noinline)) static uint64_t target_31(uint64_t x) { return x ^ 0x83; }

static branch_fn_t targets[INDIRECT_TARGETS] = {
    target_00, target_01, target_02, target_03,
    target_04, target_05, target_06, target_07,
    target_08, target_09, target_10, target_11,
    target_12, target_13, target_14, target_15,
    target_16, target_17, target_18, target_19,
    target_20, target_21, target_22, target_23,
    target_24, target_25, target_26, target_27,
    target_28, target_29, target_30, target_31
};

static uint64_t run_predictable(uint64_t iterations)
{
    uint64_t acc = 1;

    for (uint64_t i = 0; i < iterations; ++i) {
        if ((i & 1023ULL) != 0)
            acc += i ^ 0x9e3779b97f4a7c15ULL;
        else
            acc ^= i + 0xd1b54a32d192ed03ULL;
    }

    return acc;
}

static uint64_t run_alternating(uint64_t iterations)
{
    uint64_t acc = 1;

    for (uint64_t i = 0; i < iterations; ++i) {
        if (i & 1ULL)
            acc += i;
        else
            acc ^= i + 1;
    }

    return acc;
}

static uint64_t run_periodic(uint64_t iterations)
{
    uint64_t acc = 1;

    for (uint64_t i = 0; i < iterations; ++i) {
        uint64_t pattern = i & 15ULL;

        if (pattern == 0 || pattern == 3 || pattern == 7 ||
            pattern == 8 || pattern == 12)
            acc += i ^ 0x55aa55aa55aa55aaULL;
        else
            acc ^= i + 0x123456789abcdefULL;
    }

    return acc;
}

static uint64_t run_correlated(uint64_t iterations)
{
    uint64_t acc = 1;
    uint64_t history = 0x5a;

    for (uint64_t i = 0; i < iterations; ++i) {
        uint64_t b0 = ((history >> 0) ^ (history >> 3) ^ i) & 1ULL;
        uint64_t b1 = ((history >> 1) ^ (history >> 5) ^ (i >> 2)) & 1ULL;

        if (b0)
            acc += i ^ history;
        else
            acc ^= i + history;

        if (b1)
            acc += history * 3 + 1;
        else
            acc ^= history * 5 + 7;

        history = ((history << 1) | (b0 ^ b1)) & 0xffULL;
    }

    return acc;
}

static uint64_t run_random(uint64_t iterations, uint64_t seed)
{
    uint64_t acc = 1;
    uint64_t state = seed ? seed : 1;

    for (uint64_t i = 0; i < iterations; ++i) {
        uint64_t value = xorshift64(&state);

        if (value & 1ULL)
            acc += value ^ i;
        else
            acc ^= value + i;
    }

    return acc;
}

static uint64_t run_array_random(uint64_t iterations, uint64_t seed)
{
    uint8_t *pattern = aligned_alloc(64, ARRAY_SIZE);
    if (!pattern) {
        fprintf(stderr, "aligned_alloc failed\n");
        exit(EXIT_FAILURE);
    }

    uint64_t state = seed ? seed : 1;
    for (size_t i = 0; i < ARRAY_SIZE; ++i)
        pattern[i] = (uint8_t)(xorshift64(&state) & 1ULL);

    uint64_t acc = 1;
    size_t mask = ARRAY_SIZE - 1;

    for (uint64_t i = 0; i < iterations; ++i) {
        if (pattern[i & mask])
            acc += i ^ 0xaaaaaaaaaaaaaaaaULL;
        else
            acc ^= i + 0x5555555555555555ULL;
    }

    free(pattern);
    return acc;
}

static uint64_t run_indirect(uint64_t iterations, uint64_t seed)
{
    uint64_t acc = 1;
    uint64_t state = seed ? seed : 1;

    for (uint64_t i = 0; i < iterations; ++i) {
        uint64_t selector = xorshift64(&state);
        branch_fn_t fn = targets[selector & (INDIRECT_TARGETS - 1)];
        acc = fn(acc + i);
    }

    return acc;
}

static uint64_t run_mixed(uint64_t iterations, uint64_t seed)
{
    uint64_t acc = 1;
    uint64_t state = seed ? seed : 1;
    uint64_t history = 0x35;

    for (uint64_t i = 0; i < iterations; ++i) {
        uint64_t r = xorshift64(&state);

        if ((i & 7ULL) != 0)
            acc += i;
        else
            acc ^= i;

        if ((history ^ i) & 1ULL)
            acc += r & 0xffffULL;
        else
            acc ^= r >> 16;

        if (r & 1ULL)
            acc += 3;
        else
            acc ^= 7;

        acc = targets[(r >> 8) & (INDIRECT_TARGETS - 1)](acc);

        history = ((history << 1) | (r & 1ULL)) & 0xffULL;
    }

    return acc;
}

static void print_usage(const char *program)
{
    fprintf(stderr,
        "Usage: %s [mode] [iterations] [core] [seed]\n"
        "\n"
        "Modes:\n"
        "  predictable  Mostly taken conditional branch\n"
        "  alternating  Taken/not-taken alternating pattern\n"
        "  periodic     Repeating 16-element branch pattern\n"
        "  correlated   History-dependent correlated branches\n"
        "  random       Pseudo-random conditional branch\n"
        "  array        Pre-generated random branch outcomes\n"
        "  indirect     Random indirect-call targets\n"
        "  mixed        Conditional, correlated, random, indirect\n"
        "  all          Run every mode sequentially\n"
        "\n"
        "Defaults: mode=mixed iterations=%" PRIu64 " core=0 seed=1\n",
        program, (uint64_t)DEFAULT_ITERS);
}

static uint64_t run_mode(const char *mode, uint64_t iterations, uint64_t seed)
{
    if (strcmp(mode, "predictable") == 0)
        return run_predictable(iterations);
    if (strcmp(mode, "alternating") == 0)
        return run_alternating(iterations);
    if (strcmp(mode, "periodic") == 0)
        return run_periodic(iterations);
    if (strcmp(mode, "correlated") == 0)
        return run_correlated(iterations);
    if (strcmp(mode, "random") == 0)
        return run_random(iterations, seed);
    if (strcmp(mode, "array") == 0)
        return run_array_random(iterations, seed);
    if (strcmp(mode, "indirect") == 0)
        return run_indirect(iterations, seed);
    if (strcmp(mode, "mixed") == 0)
        return run_mixed(iterations, seed);

    fprintf(stderr, "Unknown mode: %s\n", mode);
    exit(EXIT_FAILURE);
}

static void execute_and_report(const char *mode, uint64_t iterations, uint64_t seed)
{
    double start = now_seconds();
    uint64_t result = run_mode(mode, iterations, seed);
    double elapsed = now_seconds() - start;

    sink ^= result;

    printf("%-12s iterations=%" PRIu64
           " elapsed=%.6f s iter/s=%.3f checksum=%" PRIu64 "\n",
           mode,
           iterations,
           elapsed,
           elapsed > 0.0 ? (double)iterations / elapsed : 0.0,
           result);
}

int main(int argc, char **argv)
{
    const char *mode = argc > 1 ? argv[1] : "mixed";
    uint64_t iterations = argc > 2 ? strtoull(argv[2], NULL, 0) : DEFAULT_ITERS;
    int core = argc > 3 ? atoi(argv[3]) : 0;
    uint64_t seed = argc > 4 ? strtoull(argv[4], NULL, 0) : 1;

    if (strcmp(mode, "-h") == 0 || strcmp(mode, "--help") == 0) {
        print_usage(argv[0]);
        return EXIT_SUCCESS;
    }

    if (iterations == 0) {
        fprintf(stderr, "Iterations must be greater than zero\n");
        return EXIT_FAILURE;
    }

    pin_to_core(core);

    printf("Branch predictor stress benchmark\n");
    printf("PID:        %ld\n", (long)getpid());
    printf("Core:       %d\n", core);
    printf("Iterations: %" PRIu64 "\n", iterations);
    printf("Seed:       %" PRIu64 "\n", seed);
    printf("Mode:       %s\n\n", mode);

    if (strcmp(mode, "all") == 0) {
        static const char *modes[] = {
            "predictable",
            "alternating",
            "periodic",
            "correlated",
            "random",
            "array",
            "indirect",
            "mixed"
        };

        for (size_t i = 0; i < sizeof(modes) / sizeof(modes[0]); ++i)
            execute_and_report(modes[i], iterations, seed);
    } else {
        execute_and_report(mode, iterations, seed);
    }

    printf("\nFinal sink: %" PRIu64 "\n", sink);
    return EXIT_SUCCESS;
}

