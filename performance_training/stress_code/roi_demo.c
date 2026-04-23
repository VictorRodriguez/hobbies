#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
#include <unistd.h>

static double now_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

static void busy_wait(double seconds) {
    double start = now_seconds();
    volatile double sink = 0.0;
    while ((now_seconds() - start) < seconds) {
        sink += 1.0;
    }
    if (sink < 0) {
        printf("ignore: %f\n", sink);
    }
}

static void matrix_mul_phase(int n, int repeats) {
    size_t bytes = (size_t)n * (size_t)n * sizeof(double);
    double *A = aligned_alloc(64, bytes);
    double *B = aligned_alloc(64, bytes);
    double *C = aligned_alloc(64, bytes);

    if (!A || !B || !C) {
        fprintf(stderr, "allocation failed\n");
        free(A); free(B); free(C);
        exit(1);
    }

    for (int i = 0; i < n * n; i++) {
        A[i] = (double)((i % 97) + 1) * 0.5;
        B[i] = (double)((i % 89) + 1) * 0.25;
        C[i] = 0.0;
    }

    printf("ROI_START matrix_mul n=%d repeats=%d\n", n, repeats);
    fflush(stdout);

    volatile double checksum = 0.0;
    for (int r = 0; r < repeats; r++) {
        memset(C, 0, bytes);
        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n; k++) {
                double aik = A[(size_t)i * n + k];
                for (int j = 0; j < n; j++) {
                    C[(size_t)i * n + j] += aik * B[(size_t)k * n + j];
                }
            }
        }
        checksum += C[(r * 17) % (n * n)];
    }

    printf("ROI_END checksum=%f\n", checksum);
    fflush(stdout);

    free(A);
    free(B);
    free(C);
}

int main(int argc, char **argv) {
    int n = 384;
    int repeats = 18;
    double idle_before = 5.0;
    double idle_after = 5.0;

    if (argc > 1) idle_before = atof(argv[1]);
    if (argc > 2) n = atoi(argv[2]);
    if (argc > 3) repeats = atoi(argv[3]);
    if (argc > 4) idle_after = atof(argv[4]);

    printf("PID=%d\n", getpid());
    printf("Phase 1: idle_before=%0.2f sec\n", idle_before);
    fflush(stdout);
    sleep((unsigned int)idle_before);

    printf("Phase 2: compute phase begins\n");
    fflush(stdout);
    matrix_mul_phase(n, repeats);

    printf("Phase 3: idle_after=%0.2f sec\n", idle_after);
    fflush(stdout);
    sleep((unsigned int)idle_after);

    printf("Done\n");
    return 0;
}

