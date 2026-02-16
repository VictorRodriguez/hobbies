#include <immintrin.h>
#include <math.h>
#include <stdio.h>
#include <time.h>

// Performs one FFT butterfly stage using AVX2 (4 doubles)
void fft_butterfly_avx2(double *real, double *imag, int n) {
    const double PI = acos(-1.0);

    for (int k = 0; k < n; k += 4) {
        // Load 4 real and imaginary parts
        __m256d r0 = _mm256_loadu_pd(&real[k]);
        __m256d i0 = _mm256_loadu_pd(&imag[k]);

        // Compute twiddle factors (Wn^k = exp(-2πi * k / n))
        double wr[4], wi[4];
        for (int j = 0; j < 4; ++j) {
            wr[j] = cos(-2.0 * PI * (k + j) / n);
            wi[j] = sin(-2.0 * PI * (k + j) / n);
        }
        __m256d w_real = _mm256_loadu_pd(wr);
        __m256d w_imag = _mm256_loadu_pd(wi);

        // Complex multiplication: (r0 + i0*i) * (wr + wi*i)
        // real = r0 * wr - i0 * wi
        __m256d re_part = _mm256_sub_pd(_mm256_mul_pd(r0, w_real), _mm256_mul_pd(i0, w_imag));
        // imag = r0 * wi + i0 * wr
        __m256d im_part = _mm256_add_pd(_mm256_mul_pd(r0, w_imag), _mm256_mul_pd(i0, w_real));

        // Store results back
        _mm256_storeu_pd(&real[k], re_part);
        _mm256_storeu_pd(&imag[k], im_part);
    }
}

int main() {
    const int n = 16;
    const int iterations = 1000000;

    double real[16], imag[16];

    for (int i = 0; i < n; ++i) {
        real[i] = cos(2 * M_PI * i / n);
        imag[i] = sin(2 * M_PI * i / n);
    }

    clock_t start = clock();

    for (int i = 0; i < iterations; i++) {
        fft_butterfly_avx2(real, imag, n);
    }

    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

    printf("Time for %d iterations: %f seconds\n", iterations, time_spent);

    // Print some outputs for verification
    for (int i = 0; i < n; ++i) {
        printf("out[%d] = %.6f + %.6fi\n", i, real[i], imag[i]);
    }

    return 0;
}

