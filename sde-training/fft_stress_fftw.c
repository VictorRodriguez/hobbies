#define _GNU_SOURCE
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <fftw3.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <iterations>\n", argv[0]);
        return 1;
    }

    int iterations = atoi(argv[1]);
    int n = 1024;

    fftw_complex *in = fftw_malloc(sizeof(fftw_complex) * n);
    fftw_complex *out = fftw_malloc(sizeof(fftw_complex) * n);
    fftw_plan p = fftw_plan_dft_1d(n, in, out, FFTW_FORWARD, FFTW_MEASURE);

    for (int i = 0; i < n; i++) {
        in[i][0] = cos(2 * M_PI * i / n); // real part
        in[i][1] = sin(2 * M_PI * i / n); // imaginary part
    }

    clock_t start = clock();

    for (int i = 0; i < iterations; i++) {
        fftw_execute(p);
    }

    clock_t end = clock();
    printf("Time taken: %f seconds\n", (double)(end - start) / CLOCKS_PER_SEC);

    fftw_destroy_plan(p);
    fftw_free(in);
    fftw_free(out);
    return 0;
}

