#include <immintrin.h>
#include <math.h>
#include <stdio.h>
#include <time.h>

// Performs one FFT butterfly stage using AVX-512 (8 doubles)
void fft_butterfly_avx512(double *real, double *imag, int n) {
    const double PI = acos(-1.0);

    for (int k = 0; k < n; k += 8) {
        // Load 8 real and imaginary parts
        __m512d r0 = _mm512_loadu_pd(&real[k]);
        __m512d i0 = _mm512_loadu_pd(&imag[k]);

        // Compute twiddle factors (Wn^k = exp(-2πi * k / n))
        double wr[8], wi[8];
        for (int j = 0; j < 8; ++j) {
            wr[j] = cos(-2.0 * PI * (k + j) / n);
            wi[j] = sin(-2.0 * PI * (k + j) / n);
        }
        __m512d w_real = _mm512_loadu_pd(wr);
        __m512d w_imag = _mm512_loadu_pd(wi);

        // Complex multiplication: (r0 + i0*i) * (wr + wi*i)
        // real = r0 * wr - i0 * wi
        __m512d re_part = _mm512_fmsub_pd(r0, w_real, _mm512_mul_pd(i0, w_imag));
        // imag = r0 * wi + i0 * wr
        __m512d im_part = _mm512_fmadd_pd(r0, w_imag, _mm512_mul_pd(i0, w_real));

        // Store results back
        _mm512_storeu_pd(&real[k], re_part);
        _mm512_storeu_pd(&imag[k], im_part);
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
        fft_butterfly_avx512(real, imag, n);
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
