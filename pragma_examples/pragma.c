#include <stdio.h>
#include <emmintrin.h>

#pragma GCC option(pop)
#pragma GCC option(push)
#pragma GCC option("sse4.1")
#include <smmintrin.h>

int sse4_1_min (__m128i a, __m128i b) {
    return _mm_cvtsi128_si32(_mm_min_epi32 (a,b));
}

#pragma GCC option(pop)

int main(){
    printf("min = %d",sse4_1_min(10,4));
    return 0;
}
