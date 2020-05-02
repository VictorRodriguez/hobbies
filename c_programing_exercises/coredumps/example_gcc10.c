#include <stdlib.h>

int main(){
	int var = 10;
	int *ptr = &var;
	free(ptr);
	free(ptr);

	return 0;
}
