/*
 * =====================================================================================
 *
 *       Filename:  realloc_simple_2.c
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  03/07/2018 01:50:20 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Victor Rodriguez (), vm.rod25@gmail.com
 *   Organization:  http://www.cplusplus.com/reference/cstdlib/realloc/
 *
 * =====================================================================================
 */

/* realloc example: rememb-o-matic */
#include <stdio.h>      /* printf, scanf, puts */
#include <stdlib.h>     /* realloc, free, exit, NULL */

int main ()
{
  int input,n;
  int count = 0;
  int* numbers = NULL;
  int* more_numbers = NULL;

  do {
     printf ("Enter an integer value (0 to end): ");
     scanf ("%d", &input);
     count++;

     more_numbers = (int*) realloc (numbers, count * sizeof(int));

     /*
      * This is just for: 
      * If the function fails to allocate the requested block of memory, a null
      * pointer is returned, and the memory block pointed to by argument ptr is
      * not deallocated (it is still valid, and with its contents unchanged).
      */
     if (more_numbers!=NULL) {
       numbers=more_numbers;
       numbers[count-1]=input;
     }
     else {
       free (numbers);
       puts ("Error (re)allocating memory");
       exit (1);
     }
  } while (input!=0);

  printf ("Numbers entered: ");
  for (n=0;n<count;n++) {
    printf ("%d ",numbers[n]);
  }
  printf ( "\n" );
  free (numbers);

  return 0;
}
