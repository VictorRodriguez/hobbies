#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

// Function that performs CPU intensive work
void* stress_cpu(void* arg) {
    unsigned long long i = 0;
    while (1) {
        i++;
    }
    return NULL;
}

int main() {
    // Get the number of CPU cores
    int num_cores = sysconf(_SC_NPROCESSORS_ONLN);
    printf("Number of cores: %d\n", num_cores);

    pthread_t* threads = (pthread_t*)malloc(num_cores * sizeof(pthread_t));
    if (threads == NULL) {
        perror("Unable to allocate memory for threads");
        return 1;
    }

    // Create threads to stress each core
    for (int i = 0; i < num_cores; i++) {
        if (pthread_create(&threads[i], NULL, stress_cpu, NULL) != 0) {
            perror("Error creating thread");
            free(threads);
            return 1;
        }
    }

    // Join threads (this will actually never happen in this infinite loop scenario)
    for (int i = 0; i < num_cores; i++) {
        pthread_join(threads[i], NULL);
    }

    free(threads);
    return 0;
}

