#include <fftw3.h>
#include <stdio.h>
#include <stdlib.h>

#ifdef USE_SNIPER
#include "sim_api.h"
#endif

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <iterations>\n", argv[0]);
        return 1;
    }

    int iterations = atoi(argv[1]);
    if (iterations <= 0) {
        fprintf(stderr, "Iterations must be > 0\n");
        return 1;
    }

    const int N = 1024;

    fftw_complex *in  = (fftw_complex*)fftw_malloc(sizeof(fftw_complex) * N);
    fftw_complex *out = (fftw_complex*)fftw_malloc(sizeof(fftw_complex) * N);
    if (!in || !out) {
        fprintf(stderr, "FFTW allocation failed\n");
        return 1;
    }

    for (int i = 0; i < N; i++) {
        in[i][0] = 1.0;
        in[i][1] = 0.0;
    }

    // Plan outside ROI (planning is expensive; don't pollute measurements)
    fftw_plan plan = fftw_plan_dft_1d(N, in, out, FFTW_FORWARD, FFTW_MEASURE);
    if (!plan) {
        fprintf(stderr, "FFTW plan creation failed\n");
        return 1;
    }

    printf("START\n");
#ifdef USE_SNIPER
    SimRoiStart();
#endif

    for (int i = 0; i < iterations; i++) {
        fftw_execute(plan);
    }

#ifdef USE_SNIPER
    SimRoiEnd();
#endif
    printf("END\n");

    fftw_destroy_plan(plan);
    fftw_free(in);
    fftw_free(out);
    return 0;
}

