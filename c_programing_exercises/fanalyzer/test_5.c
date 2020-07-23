#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>


void handle_sigint(int sig){
	if (sig == SIGINT){
		printf("SIGNAL = SIGINT\n");
		//printf("SIGNAL: %d", sig);
		exit(-1);
	}
}

int main() {
    signal(SIGINT, handle_sigint);
    while (1)
		sleep(1);
    return 0;
}

