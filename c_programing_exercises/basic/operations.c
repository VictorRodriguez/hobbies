#include <stdio.h>

int main(){

	float val = 0;
	printf("please enter a value\n");
	scanf("%f",&val);

	printf("value *5 = %f\n",val*=5);
	printf("value */3 = %f\n",val/=3);

	return 0;
}
