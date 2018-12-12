#include <stdio.h>

#if defined AVX512F
#define VECTOR_SIZE_BYTES 64
#elif defined AVX2
#define VECTOR_SIZE_BYTES 32
#else
#define VECTOR_SIZE_BYTES 16
#endif
int main(){
    printf("SIZE_BYTES = %d\n",VECTOR_SIZE_BYTES);
    return 0;
}
