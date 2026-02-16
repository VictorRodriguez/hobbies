#include <math.h>
#include <stdio.h>
#include <time.h>

// Performs one FFT butterfly stage on arrays of doubles (no intrinsics)
void fft_butterfly_pure(double *real, double *imag, int n) {
    const double PI = acos(-1.0);

    for (int k = 0; k < n; k += 8) {
        double wr[8], wi[8];
        for (int j = 0; j < 8; ++j) {
            wr[j] = cos(-2.0 * PI * (k + j) / n);
            wi[j] = sin(-2.0 * PI * (k + j) / n);
        }

        // Load the 8 elements manually (scalar)
        double r0[8], i0[8];
        for (int j = 0; j < 8; ++j) {
            r0[j] = real[k + j];
            i0[j] = imag[k + j];
        }

        // Perform complex multiplication (r0 + i0*i) * (wr + wi*i)
        for (int j = 0; j < 8; ++j) {
            double re_part = r0[j] * wr[j] - i0[j] * wi[j];
            double im_part = r0[j] * wi[j] + i0[j] * wr[j];
            real[k + j] = re_part;
            imag[k + j] = im_part;
        }
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
        fft_butterfly_pure(real, imag, n);
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

