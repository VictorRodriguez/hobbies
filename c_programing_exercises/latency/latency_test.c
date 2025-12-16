#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define CACHELINE 64

volatile uint64_t *array;

int main(int argc, char **argv)
{
    if (argc < 3) {
        printf("Usage: %s <array_size_kb> <iterations>\n", argv[0]);
        return 1;
    }

    size_t size_kb = atoi(argv[1]);
    uint64_t iterations = atoll(argv[2]);

    size_t num_elements = (size_kb * 1024) / sizeof(uint64_t);

    // Aligned allocation
    posix_memalign((void **)&array, CACHELINE, num_elements * sizeof(uint64_t));

    // Initialize pointer chasing (linked list)
    for (size_t i = 0; i < num_elements - 1; i++) {
        array[i] = i + 1;
    }
    array[num_elements - 1] = 0;

    uint64_t idx = 0;

    for (uint64_t i = 0; i < iterations; i++) {
        idx = array[idx];
    }

    // Prevent optimization
    printf("Final index: %lu\n", idx);

    return 0;
}


