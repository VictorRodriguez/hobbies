#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define N 50000000  // 50 million elements

int main() {
    static float data[N];
    double sum = 0.0;

    // Initialize data
    for (int i = 0; i < N; i++)
        data[i] = (float)(i % 100) / 10.0f;

    clock_t start = clock();

    // Stressful computation loop (no unrolling)
    for (int i = 0; i < N; i++) {
        // Do more arithmetic per iteration
        float x = data[i];
        sum += sinf(x) * cosf(x) + sqrtf(x + 1.0f) - logf(x + 2.0f);
    }

    clock_t end = clock();

    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Result = %.6f\n", sum);
    printf("Elapsed time (non-unrolled): %.3f seconds\n", elapsed);

    return 0;
}

