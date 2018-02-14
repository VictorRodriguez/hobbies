#include <stdio.h>
#include <immintrin.h>

int main(){


    int a = 3 ; 
    int b = 5; 
    int c = 0 ; 


    c = a * b ; 

    printf("c = %d", c);

//    if (__builtin_cpu_supports ("ssse3")){
//        printf("I am in SSE system");
//    }
//    if (__builtin_cpu_supports ("avx2")){
//        printf("I am in AVX2 system");
//    }
//    if (__builtin_cpu_supports ("avx512f")){
//        printf("I am in AVX 512 system");
//    }else{
//        printf("no idea");
//    }
return 0;
}
