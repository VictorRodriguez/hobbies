#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ITERATIONS 1000000000 // Number of iterations to stress the ALU

int main() {
    // Initialize random number generator
    srand(time(NULL));

    // Variables for arithmetic operations
    int a, b, c, d, e, f, g, h, i, j;
    a = rand();
    b = rand();
    c = rand();
    d = rand();
    e = rand();
    f = rand();
    g = rand();
    h = rand();
    i = rand();
    j = rand();

    // Start the stress test
    for (long long int iter = 0; iter < ITERATIONS; iter++) {
        a = b + c;
        b = c - d;
        c = d * e;

        // Ensure divisor is not zero for division and modulus operations
        if (f != -1) {
            d = e / (f + 1); // Avoid division by zero
            e = f % (g + 1); // Avoid division by zero
        }

        f = g & h;
        g = h | i;
        h = i ^ j;
        i = ~j;
        j = a << 1;
        a = b >> 1;
    }

    // Print final values to prevent compiler optimization
    printf("Final values: %d %d %d %d %d %d %d %d %d %d\n", a, b, c, d, e, f, g, h, i, j);

    return 0;
}

