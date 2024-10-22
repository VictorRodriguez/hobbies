#include <stdio.h>
#include <stdlib.h>
#include "sim_api.h"

// Function to perform a CPU-intensive task
void cpu_intensive_task(int loops) {
    volatile double result = 0.0;
    for (int j = 0; j < 100; j++) {
        for (int i = 0; i < loops; i++) {
            result += i * 0.1;
        }
    }
    printf("\nresult = %d",result);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number_of_loops>\n", argv[0]);
        return 1;
    }

    int loops = atoi(argv[1]);
    if (loops <= 0) {
        fprintf(stderr, "Please provide a positive integer for the number of loops.\n");
        return 1;
    }

    printf("Starting CPU-intensive task for %d loops...\n", loops);
    SimRoiStart();
    cpu_intensive_task(loops);
	SimRoiEnd();
    printf("CPU-intensive task completed.\n");

    return 0;
}
