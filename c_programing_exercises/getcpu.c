#define _GNU_SOURCE
#include <stdio.h>
#include <sched.h>

int main(){

	unsigned int *cpu;
	unsigned int *node;
	int ret;

	ret = getcpu(cpu,node);

	printf("cpu : %d\n",(int *)cpu);
	printf("node : %d\n",(int *)node);

	return ret;
}
