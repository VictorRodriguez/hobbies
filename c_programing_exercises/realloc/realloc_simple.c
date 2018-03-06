/*
 * =====================================================================================
 *
 *       Filename:  realloc_simple.c
 *
 *    Description:  Basic realloc example
 *
 *        Version:  1.0
 *        Created:  03/06/2018 08:53:46 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Victor Rodriguez (), vm.rod25@gmail.com
 *         Source:  http://en.cppreference.com/w/c/memory/realloc
 *
 * =====================================================================================
 */

#include <stdio.h>
#include <stdlib.h>
 
int main(void)
{
    int *pa = malloc(10 * sizeof *pa); // allocate an array of 10 int
    if(pa) {
        printf("%zu bytes allocated. Storing ints: ", 10*sizeof(int));
        for(int n = 0; n < 10; ++n)
            printf("%d ", pa[n] = n);
        printf ( "\n" );
    }

    int *pb = realloc(pa, 1000000 * sizeof *pb); // reallocate array to a larger size
    if(pb) {
        printf("\n%zu bytes allocated, first 10 ints are: ", 1000000*sizeof(int));
        for(int n = 0; n < 10; ++n)
            printf("%d ", pb[n]); // show the array
        free(pb);
    } else { // if realloc failed, the original pointer needs to be freed
        free(pa);
    }
    printf ( "\n" );
}

