#include <stdio.h>

#define ROWS 1000
#define COLS 100

int main() {
    int k[ROWS][COLS];

    for (int y = 0; y < COLS; y++) {
        for (int x = 0; x < ROWS; x++) {
            k[x][y] = x * y;
        }
    }

    // Print a value to ensure the computation is not optimized away
    printf("%d\n", k[ROWS-1][COLS-1]);

    return 0;
}

