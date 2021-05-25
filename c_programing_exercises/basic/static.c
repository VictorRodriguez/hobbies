#include <stdio.h>

int *foo (){

	static int values[5];
	for (int x = 0; x < 5;x++){
			values[x]=(x*2)+1;
	}
	return values;
}

int main(){
	int *values_main;
	values_main = foo();
	for (int x = 0; x < 5;x++){
		printf("%d\n",values_main[x]);
	}

	return 0;
}
