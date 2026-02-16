#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/pidfd.h>
#include <sys/wait.h>

int main(){
	int r = process_mrelease (-1, 0);
	printf("%d",r);
	return 0;
}
