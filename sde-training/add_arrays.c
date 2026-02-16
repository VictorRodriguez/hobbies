#include <stdio.h>

#define MAX_LOOP 10000000

void add_arrays(float *a, float *b, float *result, int n) {
    for (int i = 0; i < n; i++) {
        result[i] = a[i] + b[i];
    }
}

int main() {
    int n = 1024; // Size of the arrays
    float a[n], b[n], result[n];

    // Initialize arrays
    for (int i = 0; i < n; i++) {
        a[i] = i;
        b[i] = i * 2;
    }

	for (int x = 0 ; x < MAX_LOOP; x++){
		// Perform addition
		add_arrays(a, b, result, n);
	}

    // Print some results
    for (int i = 0; i < 10; i++) {
        printf("%f ", result[i]);
    }
    printf("\n");

    return 0;
}

