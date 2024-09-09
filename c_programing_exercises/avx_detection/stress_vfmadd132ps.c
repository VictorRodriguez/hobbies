#include <stdio.h>
#include <immintrin.h>

void stress_vfmadd132ps(float *a, float *b, float *c, float *result, int size) {
    __m256 ymm0, ymm1, ymm2, ymm3;

    for (int i = 0; i < size; i += 8) {
        // Load values into YMM registers
        ymm0 = _mm256_loadu_ps(&a[i]);
        ymm1 = _mm256_loadu_ps(&b[i]);
        ymm2 = _mm256_loadu_ps(&c[i]);

        // Perform the VFMADD132PS operation
        for (int j = 0; j < 1000000; ++j) {
            ymm3 = _mm256_fmadd_ps(ymm0, ymm1, ymm2);
        }

        // Store the result
        _mm256_storeu_ps(&result[i], ymm3);
    }
}

int main() {
    const int size = 1024;
    float a[size], b[size], c[size], result[size];

    // Initialize arrays with some values
    for (int i = 0; i < size; ++i) {
        a[i] = (float)i;
        b[i] = (float)(i + 1);
        c[i] = (float)(i + 2);
    }

    // Stress the VFMADD132PS instruction
    stress_vfmadd132ps(a, b, c, result, size);

    // Print some of the results
    for (int i = 0; i < 8; ++i) {
        printf("result[%d] = %f\n", i, result[i]);
    }

    return 0;
}

