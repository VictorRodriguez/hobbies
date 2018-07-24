#include <stdio.h>

int main() {

    int arg1, arg2, add, sub, mul, quo, rem ;

    arg1 = 100000;
    arg2 = 123;

    int i,j;

    for ( i = 0 ; i < 1000000000 ; i++){
        for ( j = 0 ; j < 1000000000 ; j++){
        /* Perform Addition */
        __asm__ ( "subl %%ebx, %%eax;" : "=a" (sub) : "a" (arg1) , "b" (arg2) );
        }
    }

    printf( "%d - %d = %d\n", arg1, arg2, sub );


    return 0 ;
}
