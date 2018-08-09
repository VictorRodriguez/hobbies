#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <immintrin.h>


u_int32_t *arr_a, *arr_b, *arr_c;
int n = 16;

void fill_arrays(){
    arr_a = _mm_malloc(sizeof(u_int32_t) * n, 64);
    arr_b = _mm_malloc(sizeof(u_int32_t) * n, 64);
    arr_c = _mm_malloc(sizeof(u_int32_t) * n, 64);
    for(int i = 0; i < n; i++) {
        arr_a[i] = 1;
        arr_b[i] = 2;
    }
}

void foo(){

    __m512i m_a, m_b, m_c;

    m_a = _mm512_load_epi32(arr_a);
    m_b = _mm512_load_epi32(arr_b);

    m_c = _mm512_add_epi32(m_a, m_b);

    _mm512_store_epi32(arr_c, m_c);

}

int check_result(){

    int ret = 0;
    for (int i=0; i<n; i++){
        if (arr_c[i] == 3)
            continue;
        else
            printf("FAIL, corruption in arithmetic");
            ret =  -1;
            printf("%d\n",arr_c[i]);
            break;
    }
    return ret;
}

int main(int argc, char **argv){
    fill_arrays();
    foo();
    if(check_result()){
        return check_result();
    }
    else{
        printf("Works!\n");
    }
}
