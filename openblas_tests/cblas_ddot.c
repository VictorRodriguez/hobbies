/**
* Author:    Victor Manuel Rodriguez
* Created:   January 29th 2020
**/

#include <stdio.h>
#include <stdlib.h>
#include <cblas.h>

#define ROWS 2
#define COLS 2

void print_matrix(double matrix[ROWS][COLS]){
    for (int i=0; i<COLS; i++) {
        for (int j=0; j<COLS; j++) {
            printf("%f ",matrix[i][j]);
    	}
		printf("\n");
	}
	printf("\n");
}

int main() {
    double a[ROWS][COLS] = {1,0,0,1};
    double b[COLS][COLS] = {4,1,2,2};
    double c[COLS][COLS] = {0,0,0,0};
    double *ai, *bj;

	printf("Matrix multiplication of:\n");
	printf("Matrix A:\n");
	print_matrix(a);

	printf("Matrix B:\n");
	print_matrix(b);

	printf("Equal to:\n");
    ai = a[0];
    for (int i=0; i<COLS; i++) {
        bj = b[0];
        for (int j=0; j<COLS; j++) {
            c[i][j] = cblas_ddot(ROWS,ai,COLS,bj,COLS);
            printf("%f ",c[i][j]);
            if (c[i][j] != b[i][j]) {
				printf("cblas_ddot Test: FAIL\n");
                return -1;
            }
            bj += 1;
        }
        printf("\n");
        ai += 1;
    }
        printf("\ncblas_ddot Test: PASS\n");
        return 0;
}

