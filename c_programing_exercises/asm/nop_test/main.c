#include <pthread.h>
#include <unistd.h>


//#define LOOPS 1000000000000
#define THREADS 48

void *foo(){

    /* If you want to stress the cores
     *
        for (int x=0; x<LOOPS; x++){
        int a = 0;
        int b = 1;
        int c = 1;
            a = b+c;
    	}
    */
    while(1){
    __asm__("nop");
    }
}

int main(){

    pthread_t tid;
    for (int i = 0; i < THREADS; i++){
        pthread_create(&tid, NULL,foo,NULL);
	}

    sleep(10);
    return 0;

    //pthread_exit(NULL);
	//__asm__("ud2");
}
