#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]){

    char ch, file_name[25];
    FILE *fp;
    if (argc < 2){
        printf("No log file to read\n");
        return(EXIT_FAILURE);
    }

    fp = fopen(argv[1], "r");

    if (fp == NULL) {
        perror("Error while opening the file.\n");
        return(EXIT_FAILURE);
    }

    while((ch = fgetc(fp)) != EOF)
      printf("%c", ch);
    fclose(fp);
    return EXIT_SUCCESS;
}
