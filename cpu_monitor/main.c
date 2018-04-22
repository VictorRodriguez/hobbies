#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define LIMIT 60

int check_limit(int cpu_util){
    if (cpu_util >= LIMIT){
        return 1;
    } else{
        return 0;
    }
}

void print_array(int array[]){
    for(int i = 0; i < 24; i ++){
        //printf("times > LIMIT at %d hour = %d\n",i,array[i]);
        printf("%d\n",array[i]);
    }
}
int main(){

    srand(time(NULL));
    int r;
    int cpu_util_list[24];
    int c_states[24];

    int state = 2;

    for(int i = 0; i < 24; i ++){
        cpu_util_list[i] = 0;
        c_states[i] = 0;
    }

    for (int i = 0 ; i < 1440 ; i ++){
        r = rand() % 100 + 1;
        //printf("second %d -> CPU util %d \n",i,r);
        if (check_limit(r)){
            cpu_util_list[i/60]+=1;
        }
    }

    print_array(cpu_util_list);

    for (int i = 0; i < 24; i++){
        if (cpu_util_list[i] >= 50)
            state = 1;
        if (cpu_util_list[i] >= 40 && cpu_util_list[i] < 50)
            state = 2;
        if (cpu_util_list[i] >= 30 && cpu_util_list[i] < 40)
            state = 3;
        if (cpu_util_list[i] < 10)
            state = 6;

        c_states[i] = state;
        c_states[i+1] = state;
        c_states[i-1] = state;
    }


    print_array(c_states);

    return 0;
}
