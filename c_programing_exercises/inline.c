#include <stdio.h>


void foo( int * x ){
    *x = *x + 10;
}


int main() {

	int var = 0;

	for(int cnt=0;cnt<100;cnt++){
		foo(&var);
	}

	printf("var is now %d\n",var);
	return 0;
}

