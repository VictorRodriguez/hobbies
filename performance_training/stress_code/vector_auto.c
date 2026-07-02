#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <immintrin.h>

#define N 1024
#define REPEAT 10000
#define ALIGNMENT 32
#define EPSILON 1e-9

void initialize_arrays(double *a, double *b, double *c_intrin, double *c_regular) {
    for (int i = 0; i < N; i++) {
        a[i] = (double)i;
        b[i] = (double)(i + 1);
        c_intrin[i] = 1.0;
        c_regular[i] = 1.0;
    }
}

void compute_fma_intrinsics(const double *a,
                            const double *b,
                            double *c) {
    const int VECTOR_WIDTH = sizeof(__m256d) / sizeof(double);

    for (int r = 0; r < REPEAT; r++) {
        for (int i = 0; i < N; i += VECTOR_WIDTH) {
            __m256d va = _mm256_load_pd(&a[i]);
            __m256d vb = _mm256_load_pd(&b[i]);
            __m256d vc = _mm256_load_pd(&c[i]);

            /*
             * c[i] = a[i] * b[i] + c[i]
             *
             * This should generate:
             *   vfmadd132pd / vfmadd213pd / vfmadd231pd
             */
            vc = _mm256_fmadd_pd(va, vb, vc);

            _mm256_store_pd(&c[i], vc);
        }
    }
}

void compute_regular_c(const double *a,
                       const double *b,
                       double *c) {
    for (int r = 0; r < REPEAT; r++) {
        for (int i = 0; i < N; i++) {
            c[i] = a[i] * b[i] + c[i];
        }
    }
}

double reduce_sum(const double *c) {
    double sum = 0.0;

    for (int i = 0; i < N; i++) {
        sum += c[i];
    }

    return sum;
}

int validate_results(const double *c_intrin,
                     const double *c_regular) {
    for (int i = 0; i < N; i++) {
        double diff = fabs(c_intrin[i] - c_regular[i]);

        if (diff > EPSILON) {
            printf("Mismatch at index %d\n", i);
            printf("intrinsics = %.17f\n", c_intrin[i]);
            printf("regular C  = %.17f\n", c_regular[i]);
            printf("diff       = %.17f\n", diff);
            return 0;
        }
    }

    return 1;
}

int main(void) {
    double *a = aligned_alloc(ALIGNMENT, N * sizeof(double));
    double *b = aligned_alloc(ALIGNMENT, N * sizeof(double));
    double *c_intrin = aligned_alloc(ALIGNMENT, N * sizeof(double));
    double *c_regular = aligned_alloc(ALIGNMENT, N * sizeof(double));

    if (!a || !b || !c_intrin || !c_regular) {
        printf("Memory allocation failed\n");

        free(a);
        free(b);
        free(c_intrin);
        free(c_regular);

        return 1;
    }

    initialize_arrays(a, b, c_intrin, c_regular);

    compute_fma_intrinsics(a, b, c_intrin);
    compute_regular_c(a, b, c_regular);

    double sum_intrin = reduce_sum(c_intrin);
    double sum_regular = reduce_sum(c_regular);

    printf("sum intrinsics = %.17f\n", sum_intrin);
    printf("sum regular C  = %.17f\n", sum_regular);

    if (validate_results(c_intrin, c_regular)) {
        printf("Validation PASSED: both results match\n");
    } else {
        printf("Validation FAILED: results do not match\n");
    }

    free(a);
    free(b);
    free(c_intrin);
    free(c_regular);

    return 0;
}
