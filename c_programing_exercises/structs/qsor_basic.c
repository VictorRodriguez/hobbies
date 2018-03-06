/*
 * =====================================================================================
 *
 *       Filename:  qsor_basic.c
 *
 *    Description:  Basic example with implemented library function qsort
 *
 *        Version:  1.0
 *        Created:  03/06/2018 08:14:08 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Victor Rodriguez (), vm.rod25@gmail.com
 *      Reference:  https://www.tutorialspoint.com/c_standard_library/c_function_qsort.htm
 *
 * =====================================================================================
 */

#include <stdio.h>
#include <stdlib.h>

int values[] = { 88, 56, 100, 2, 25 };

int cmpfunc (const void * a, const void * b) {
   return ( *(int*)a - *(int*)b );
}

int main () {
   int n;

   printf("Before sorting the list is: \n");
   for( n = 0 ; n < 5; n++ ) {
      printf("%d ", values[n]);
   }
   printf ( "\n" );

    /* void qsort(void *base, size_t nitems, size_t size, int (*compar)(const void *, const void*))
     *
     * base − This is the pointer to the first element of the array to be sorted.
     * nitems − This is the number of elements in the array pointed by base.
     * size − This is the size in bytes of each element in the array.
     * compar − This is the function that compares two elements.
     */

   qsort(values, 5, sizeof(int), cmpfunc);

   printf("\nAfter sorting the list is: \n");
   for( n = 0 ; n < 5; n++ ) {   
      printf("%d ", values[n]);
   }
   printf ( "\n" );

   return(0);
}

