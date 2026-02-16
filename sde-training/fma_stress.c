#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <immintrin.h>  // For FMA instructions

#define NUM_THREADS 8  // Number of threads to create

// Global variable to hold the number of iterations for FMA operations
long long ITERATIONS = 1000000;  // Default value

void* fma_stress(void* arg) {
    // Initialize values for FMA operations
    __m256d a = _mm256_set1_pd(1.0);
    __m256d b = _mm256_set1_pd(2.0);
    __m256d c = _mm256_set1_pd(3.0);
    __m256d result = _mm256_setzero_pd();

    // Run FMA operations in a loop
    for (long long i = 0; i < ITERATIONS; ++i) {
		for (int x = 0; x < 10000; x++){
        	result = _mm256_fmadd_pd(a, b, c);  // FMA: result = (a * b) + c
		}
    }

    // Prevent compiler optimizations
    double* res = (double*)&result;
    printf("Thread finished with result: %f\n", res[0]);
    return NULL;
}

int main(int argc, char *argv[]) {
    // Check if user provided the number of iterations as an argument
    if (argc > 1) {
        ITERATIONS = atoll(argv[1]);  // Convert argument to long long
    }

    pthread_t threads[NUM_THREADS];
    int i;

    // Create threads to perform FMA operations
    for (i = 0; i < NUM_THREADS; ++i) {
        if (pthread_create(&threads[i], NULL, fma_stress, NULL)) {
            fprintf(stderr, "Error creating thread\n");
            return 1;
        }
    }

    // Wait for threads to complete
    for (i = 0; i < NUM_THREADS; ++i) {
        pthread_join(threads[i], NULL);
    }

    printf("FMA stress test completed with %lld iterations per thread.\n", ITERATIONS);
    return 0;
}

