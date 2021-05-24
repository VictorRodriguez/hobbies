#include <stdio.h>

int main(int argc , char **argv){

	if (argc > 1){
		printf("ok, filename %s\n", argv[1]);
	}else{
		printf("error no filename \n");
	}
	return  0;
}
