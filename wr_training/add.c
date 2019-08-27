#include <stdio.h>

#define MAX 1000000

int a[256], b[256], c[256];

void foo() {
    int i,x;
    for (x=0; x<MAX; x++){
        for (i=0; i<256; i++){
            a[i] = (c[i] * b[i]) + c[i];
        }
     }
}

int main()
{
    foo();
    return 0;
}
