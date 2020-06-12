#include <stdio.h>
#include <stdlib.h>

int main(){
	void *ptr;
	free(ptr);
	free(ptr);
	return 0;
}
