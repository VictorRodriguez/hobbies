#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define SIZE 5

void foo(char *input, int size){

	while(*input){
		* input = toupper(*input);
		input++;
	}
}

int main(int argc, char ** argv){

	char input[SIZE];
	int lenght;

	printf("Please provide a string to sort:\n");
	fgets(input,SIZE,stdin);

	lenght = strlen(input);

	printf("string = %s\n",input);

	foo(input,lenght);

	printf("string after sort= %s\n",input);

	return 0;
}
