#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 5

int cmpfunc (const void * a, const void * b) {
   return ( *(char*)a - *(char*)b );
}

int main(int argc, char ** argv){

	char input[SIZE];
	int lenght;

	printf("Please provide a string to sort:\n");
	fgets(input,SIZE,stdin);

	lenght = strlen(input);

	printf("string = %s\n",input);

	qsort(input, lenght, sizeof(char), cmpfunc);

	printf("string after sort= %s\n",input);

	return 0;
}
