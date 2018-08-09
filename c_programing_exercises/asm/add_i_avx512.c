#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <immintrin.h>


int a[256] = {0}; 
int b[256] = {0};
int c[256] = {0};

void foo(){
    __m512i result,B,C;
        for (int i=0; i<256; i+=16){
            B =  _mm512_load_epi32(&b[i]);
            C =  _mm512_load_epi32(&c[i]);
            result = _mm512_add_epi32(B,C);
            for ( int j=0;j<16;j++){
                a[i+j] = result[j];
            }
        }
}

void fill_arrays(){
    for (int i=0; i<256; i++){
        b[i] = 1.0;
        c[i] = 2.0;

    }
}

int check_arrays(){
    int ret = 0;
    for (int i=0; i<256; i++){
        if (a[i] == 3)
            continue;
        else
            printf("FAIL, corruption in arithmetic");
            ret =  -1;
            break;
    }
    return ret;
}


int main(int argc, char **argv){

    // initialize arrays
    fill_arrays();
    foo();
    if (check_arrays())
        return -1;
    printf("Works!!\n");
    return 0;
}
