#include <signal.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]){

    char file_name[25];
    FILE *fp;
    bool error_flag = false;
    char *line_buf = NULL;
    char *patern = "Errors: 1";
    size_t  line_buf_size = 0;
    ssize_t line_size;
    int line_count = 0;
    pid_t  pid = 0;

    if (argc < 2){
        printf("No log file to read\n");
        return(EXIT_FAILURE);
    }
    if (argc == 3){
        pid = atoi(argv[2]);
        printf("PID to kill:%d\n",pid);
    }

    while(!error_flag){

    line_buf_size = 0;
    line_buf = NULL;

    fp = fopen(argv[1], "r");

    if (fp == NULL) {
        perror("Error while opening the file.\n");
        return(EXIT_FAILURE);
    }

    while ((line_size = getline(&line_buf, &line_buf_size, fp)) != -1){
        line_count++;
        if(strstr(line_buf,patern) != NULL) {
            error_flag = true;
            printf("%s",line_buf);
            if(pid)
                kill(pid, SIGTERM);
            __asm__("ud2");
        }
    }

    fclose(fp);

    if (line_buf)
        free(line_buf);
    }
    return EXIT_SUCCESS;
}
