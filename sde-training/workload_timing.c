#include <stdio.h>
#include <stdlib.h>
#include "sim_api.h"
#include <time.h>
#include <unistd.h>

// Function to perform a CPU-intensive task
void cpu_intensive_task(int duration_seconds) {
    volatile double result = 0.0;
	time_t start_time = time(NULL);

    // Print the raw numeric value of start_time
    printf("Start time (raw): %ld\n", (long)start_time);

	while (time(NULL) - start_time < duration_seconds) {
		for (int i = 0; i < 1000000; i++) {
			result += i * 0.1;
		}
    	printf("Time (raw): %ld\n", (long)time(NULL));
	}
	printf("\nresult = %d",result);
}

int main(int argc, char *argv[]) {
	srand(time(NULL));

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <seconds>\n", argv[0]);
        return 1;
    }

    int seconds = atoi(argv[1]);
    if (seconds <= 0) {
        fprintf(stderr, "Please provide a positive integer for the number of seconds.\n");
        return 1;
    }

    printf("Starting CPU-intensive task for %d seconds...\n", seconds);
    SimRoiStart();
    cpu_intensive_task(seconds);
    SimRoiEnd();
    printf("CPU-intensive task completed.\n");

    return 0;
}

