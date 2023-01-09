#include <stdlib.h>
#include <stdio.h>

int foo(int a){
	int b = 10;
	return b;
}

int main (int argc, char *argv[]){
	printf("\n return = %d\n",foo(atoi(argv[1])));
	return 0;
}
