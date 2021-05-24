#include <stdio.h>

int main(){

	int value = 0;
	printf("Please enter a int > than 0\n");
	scanf("%d",&value);
	if (value > 0){
		printf("Number is %s \n",
		(value % 2) ? "odd": "even");
	}
	return 0;
}
