#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h>
#include <pthread.h>
#include <time.h>

#define PI 3.14159265358979323846

#include "sim_api.h"

// Struct for passing arguments to the threaded FFT
typedef struct {
    complex double *X;
    int n;
    int max_threads;
} FFTArgs;

// Function to perform the FFT
void fft(complex double *X, int n, int max_threads);

// Wrapper function for threaded FFT
void* fft_thread(void* arg) {
    FFTArgs *args = (FFTArgs*)arg;
    fft(args->X, args->n, args->max_threads / 2);  // Halve max_threads for each recursion level
    return NULL;
}

// FFT function with threading support
void fft(complex double *X, int n, int max_threads) {
    if (n <= 1) return;

    // Divide
    complex double *even = malloc(n/2 * sizeof(complex double));
    complex double *odd = malloc(n/2 * sizeof(complex double));
    for (int i = 0; i < n/2; i++) {
        even[i] = X[i*2];
        odd[i] = X[i*2 + 1];
    }

    // Conquer with threading if possible
    if (max_threads > 1) {
        pthread_t thread;
        FFTArgs args = {odd, n/2, max_threads};

        // Create a thread to handle the "odd" part
        pthread_create(&thread, NULL, fft_thread, &args);

        // Process "even" part in the current thread
        fft(even, n/2, max_threads / 2);

        // Wait for the "odd" thread to finish
        pthread_join(thread, NULL);
    } else {
        // Process without threads if max_threads limit is reached
        fft(even, n/2, 1);
        fft(odd, n/2, 1);
    }

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
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <number_of_iterations> <max_threads>\n", argv[0]);
        return 1;
    }

    int iterations = atoi(argv[1]);
    int max_threads = atoi(argv[2]);

    if (iterations <= 0 || max_threads <= 0) {
        fprintf(stderr, "The number of iterations and max_threads must be positive integers.\n");
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

    SimRoiStart();
    // Perform the FFT multiple times
    for (int i = 0; i < iterations; i++) {
        fft(X, n, max_threads);
    }
    SimRoiEnd();
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

    printf("Time taken for %d iterations of FFT with %d threads: %f seconds\n", iterations, max_threads, time_spent);

    // Free the allocated memory
    free(X);

    return 0;
}

