#include <stdio.h>
#include <stdlib.h>

int main() {
    int *ptr=(int*)malloc(sizeof(int)*5);
    int i;
    for(i=0;i<5;i++) {
        ptr[i]=i;
    }

    for(i=0;i<5;i++){
        printf("ptr [%d] = %d\n",i,ptr[i]);
    }
    free(ptr);
    return 0;
}
