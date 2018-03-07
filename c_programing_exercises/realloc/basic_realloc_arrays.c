/*
 * =====================================================================================
 *
 *       Filename:  main.c
 *
 *    Description:  Basic realloc example
 *
 *        Version:  1.0
 *        Created:  03/03/2018 11:15:21 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Victor Rodriguez (), vm.rod25@gmail.com
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct process{
    char name[50];
    int pid;

};

struct process *allprocs=NULL;
int numproc=0;

void addnode(struct process *p)
{
	numproc++;
    allprocs = realloc(allprocs,numproc*sizeof(struct process));
	allprocs[numproc-1]=*p;
}

void print_list(){
    struct process *p = allprocs;
    for (int i=0 ; i<numproc; i++){
            printf ( "%d\n",p[i].pid );
    }
}

int main ( int argc, char *argv[] ){

    for ( int i = 0 ; i < 10 ; i ++){
        struct process tmp;
        tmp.pid = i;
        addnode(&tmp);
    }

    print_list();

    return 0;
}
