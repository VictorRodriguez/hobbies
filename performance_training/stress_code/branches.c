#include <time.h>
#include <stdlib.h>
#include <stdio.h>


int main(){

	srand(time(NULL));   // Initialization, should only be called once.
	int r = rand();      // Returns a pseudo-random integer between 0 and RAND_MAX.

	int a = r%10;
	int b = r%20;
	int c = 100;
	if (a < 5){
		if(b > 10){
			c++;
		}
	}else{
		c--;
	}

	printf("%d\n",a);
	printf("%d\n",b);
	printf("%d\n",c);

	return 0;
}
