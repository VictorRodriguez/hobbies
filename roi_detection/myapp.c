#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N  1000000000

// A small function that does almost nothing
void light_work(int *x) {
    for (int i = 0; i < 1000; i++) {
        *x += i % 3;
    }
}

// Heavy “ROI” function: main CPU hotspot
void heavy_roi(int *x) {
    for (int i = 0; i < N; i++) {
        *x += (i & 7);
    }
}


int main() {
    int acc = 0;

    printf("Running synthetic workload…\n");

    // light warm-up
    light_work(&acc);

    // heavy region of interest
    heavy_roi(&acc);

    printf("Result: %d\n", acc);
    return 0;
}

