/*
* Test Name: cblas_dgemm
* Based on : https://github.com/xianyi/OpenBLAS/wiki/User-Manual
* Author: Victor Rodriguez
* Gloal: Review that optimized blas lib works with presition
*/

#include <cblas.h>
#include <stdio.h>

int main(){

  int i=0;
  int alpha = 1;
  double result = 4.0;
  double A[6] = {1.0,1.0,1.0,1.0,1.0,1.0};
  double B[6] = {1.0,1.0,1.0,1.0,1.0,1.0};
  double C[9] = {1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0};

  cblas_dgemm(CblasColMajor,\
	 CblasNoTrans,\
	 CblasTrans,\
	 3,3,2,alpha,A, 3, B, 3,2,C,3);

  for(i=0; i<9; i++){
    printf("%lf ", C[i]);
	if (C[i] != result){
		printf("Error: Aritmetic error\n");
		return -1;
	}
  }
  printf("\n");
  printf("PASS: cblas_dgemm working as expected\n");
}
