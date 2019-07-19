#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <stdlib.h>

#define BILLION 1E9

void ssh_functions (){

	char command[100];
	strcpy(command, "ssh -l vmrod -p 2222 127.0.0.1 'ls'" );
	system(command);
	//strcpy(command, "ssh -l vmrod -p 2222 127.0.0.1 'echo 1 > /proc/sys/kernel/sysrq'");
	//system(command);
	//strcpy(command, "ssh -l vmrod -p 2222 127.0.0.1 'echo c > /proc/sysrq-trigger'");
	//system(command);
}

void test_timer(){
	sleep(10);
}


int main(){

	struct timespec requestStart, requestEnd;
	clock_gettime(CLOCK_REALTIME, &requestStart);
	ssh_functions();
	clock_gettime(CLOCK_REALTIME, &requestEnd);

	double accum = ( requestEnd.tv_sec - requestStart.tv_sec )
	  + ( requestEnd.tv_nsec - requestStart.tv_nsec )
	  / BILLION;

	printf( "cmd took: %lf\n", accum );
}


