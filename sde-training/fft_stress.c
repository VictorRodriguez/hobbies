#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h>
#include <time.h>

#define PI 3.14159265358979323846

#include "sim_api.h"

// Function to perform the FFT
void fft(complex double *X, int n) {
    if (n <= 1) return;

    // Divide
    complex double *even = malloc(n/2 * sizeof(complex double));
    complex double *odd = malloc(n/2 * sizeof(complex double));
    for (int i = 0; i < n/2; i++) {
        even[i] = X[i*2];
        odd[i] = X[i*2 + 1];
    }

    // Conquer
    fft(even, n/2);
    fft(odd, n/2);

    // Combine
    for (int k = 0; k < n/2; k++) {
        complex double t = cexp(-2.0 * I * PI * k / n) * odd[k];
        X[k] = even[k] + t;
        X[k + n/2] = even[k] - t;
    }

    free(even);
    free(odd);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number_of_iterations>\n", argv[0]);
        return 1;
    }

    int iterations = atoi(argv[1]);
    if (iterations <= 0) {
        fprintf(stderr, "The number of iterations must be a positive integer.\n");
        return 1;
    }

    int n = 1024; // Size of the FFT

    // Allocate memory for the input array
    complex double *X = malloc(n * sizeof(complex double));

    // Initialize the input array with some values
    for (int i = 0; i < n; i++) {
        X[i] = cos(2 * PI * i / n) + I * sin(2 * PI * i / n);
    }

    // Measure the time taken for the computation
    clock_t start = clock();


	printf("START\n");
	SimRoiStart();
    // Perform the FFT multiple times
    for (int i = 0; i < iterations; i++) {
        fft(X, n);
    }
	printf("END\n");
  	SimRoiEnd();
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

    printf("Time taken for %d iterations of FFT: %f seconds\n", iterations, time_spent);

    // Free the allocated memory
    free(X);

    return 0;
}

