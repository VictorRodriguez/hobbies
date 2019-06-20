#include <sys/types.h> 
#include <stdio.h> 
#include <unistd.h>
#include <errno.h>
#include <sys/wait.h>
#include <stdlib.h>


int main() {
    int var = 0;
	pid_t pid;

	printf("Main Process PID = %d\n", getpid());
	/* fork a child process */
	pid = fork();

	if (pid < 0) {
		/* error occurred */
		fprintf(stderr, "Fork Failed");
		exit (-1) ;
	}
    else if (pid == 0) {
		/* child process */
	    printf("[child] Parent PID = %d\n", getppid());
		printf("[child] Current PID = %d\n", getpid());
        for(int i = 0;i<10;i++){
            var = var +10;
        }
        printf("[child] var = %d\n",var);
	}
	else {
		/* parent process */
		/* parent will wait for the child to complete */
		wait(NULL);
		printf("Child Complete\n");
	}

    printf("var = %d\n",var);
}

