define _GNU_SOURCE
#include <math.h>
#include <stdio.h>

int main(int argc, const char * argv[]){
    double value = 1;

    double _cosine;
    double _sine;

	sincos(value, &_sine, &_cosine);

    printf("The sine of %f is %f\n", value,_sine);
    printf("The cosine of %f is %f\n", value,_cosine);

    return 0;
}
