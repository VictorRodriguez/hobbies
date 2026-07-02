#include <stdio.h>
#include <stdlib.h>

#define N 1000000
#define REPEAT 100

int main(void) {
    double *a = aligned_alloc(64, N * sizeof(double));
    double *b = aligned_alloc(64, N * sizeof(double));
    double *c = aligned_alloc(64, N * sizeof(double));

    if (!a || !b || !c) {
        printf("Memory allocation failed\n");
        return 1;
    }

    for (int i = 0; i < N; i++) {
        a[i] = (double)i;
        b[i] = (double)(i + 1);
        c[i] = 0.0;
    }

    for (int r = 0; r < REPEAT; r++) {
        for (int i = 0; i < N; i++) {
            c[i] = a[i] * b[i] + c[i];
        }
    }

    double sum = 0.0;

    for (int i = 0; i < N; i++) {
        sum += c[i];
    }

    printf("sum = %f\n", sum);

    free(a);
    free(b);
    free(c);

    return 0;
}
