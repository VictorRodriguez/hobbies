#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]){

    char file_name[25];
    FILE *fp;
    bool infile = false;
    char *line_buf = NULL;
    char *patern = "Errors: 1";
    size_t  line_buf_size = 0;
    ssize_t line_size;
    int line_count = 0;

    if (argc < 2){
        printf("No log file to read\n");
        return(EXIT_FAILURE);
    }

    fp = fopen(argv[1], "r");

    if (fp == NULL) {
        perror("Error while opening the file.\n");
        return(EXIT_FAILURE);
    }

    while ((line_size = getline(&line_buf, &line_buf_size, fp)) != -1){
        line_count++;
        if(strstr(line_buf,patern) != NULL) {
            printf("line[%06d]: chars=%06zd,\
                 buf size=%06zu, contents: %s",\
                 line_count,line_size,line_buf_size,line_buf);
        }
    }
    fclose(fp);

    if (line_buf)
        free(line_buf);

    /*
    while((ch = fgetc(fp)) != EOF)
      printf("%c", ch);
    fclose(fp);
    */
    return EXIT_SUCCESS;
}
