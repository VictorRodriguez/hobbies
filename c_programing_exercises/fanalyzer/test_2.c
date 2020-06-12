#include <stdio.h>
#include <stdlib.h>

void test(const char *filename) {
  FILE *f = fopen(filename, "r");
  void *p = malloc(1024);
  /* do stuff */
}

int main(){
	return 0;
}
