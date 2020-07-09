#include <stdio.h>
#include <time.h>
#include <stdlib.h>

void B();
int L(int n);


void B(int n){
    printf("Fibonacci !!!\n");
	int i, t1 = 0, t2 = 1, nextTerm;
	for (i = 1; i <= n; ++i) {
		printf("%d, ", t1);
		nextTerm = t1 + t2;
		t1 = t2;
		t2 = nextTerm;
	}
}

int L(int n){
    // Lucas number
    if (n == 0)
        return 2;
    if (n == 1)
        return 1;

    return L(n - 1) +
           L(n - 2);
}

int main(int argc, char *argv[]){
    int i, n;
    time_t t;
    srand((unsigned) time(&t));
    int rand_num = rand() % 50;
    printf("Rand number = %d\n", rand_num);

    if(argc>=2)
        B(rand_num);
	else
        printf("Lucas number:%d\n",L(rand_num));

    return 0;
}
