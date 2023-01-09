#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#define MAX  100000

void operation(){
	int a[256], b[256], c[256];
	for (int count = 0; count < MAX; count++){
		for (int i = 0; i < 255; i ++){
			c[i] = a[i] + b[i];
		}
	}
}

int main (int argc, char *argv[]) {
	int time_delta = 10;
	if (argc == 2){
		time_delta = atoi(argv[1]);
		printf("\nTime expected = %d\n", time_delta);
		int operation_counter = 0;

		time_t start, end;
		double elapsed;  // seconds
		start = time(NULL);

		int terminate = 1;
		while (terminate) {
			end = time(NULL);
			elapsed = difftime(end, start);
		if (elapsed >= time_delta /* seconds */){
			terminate = 0;
		}
		else {
			operation();
			operation_counter++;
			}
		}
		printf("done..\n");
		printf("Operations = %d\n", operation_counter);
		printf("Time = %d\n",time_delta);
		printf("Throughput: %d opeartions/s \n", operation_counter/time_delta);
	}
	else{
		printf("\nPlease provide time time as arg\n");
	}

	return 0;
}
