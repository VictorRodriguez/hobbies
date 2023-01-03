#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int main (int argc, char *argv[]) {
	int time_delta = 10;
	if (argc == 2){
		time_delta = atoi(argv[1]);
		printf("\nTime expected = %d\n", time_delta);
		sleep(time_delta);
	}
	else{
		printf("\nPlease provide time time as arg\n");
	}

	return 0;
}
