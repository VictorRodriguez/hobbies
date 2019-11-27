nclude <stdio.h>
#include <stdlib.h>
#include <cblas.h>
#include <stdlib.h>
#include <time.h>

int main() {


    //read file into array
    static double a[625] = {1,2,5,6};
    static double b[625] = {3,4,7,8};

    FILE *myFile;
    myFile = fopen("mat_a.txt", "r");

    for (int i = 0; i < 625; i++) {
        fscanf(myFile, "%lf", &a[i]);
    }

    for (int i = 0; i < 625; i++) {
        //printf("a = %.10e\n", a[i]);
    }

    fclose(myFile);

    myFile = fopen("mat_b.txt", "r");

    for (int i = 0; i < 625; i++) {
        fscanf(myFile, "%lf", &b[i]);
    }

    for (int i = 0; i < 625; i++) {
        //printf("b = %.10e\n", b[i]);
    }

    fclose(myFile);

    int N = 25;
    double res;
    for (int i = 0; i < N; i++) {
        for (int j=0; j<N; j++) {
            res = cblas_ddot(N,&a[N*i],1,&b[j],25);
            printf("%.10e\n", res);
        }
        printf("\n");
    }
    return 0;
}
