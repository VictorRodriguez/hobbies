#include <stdio.h>

void foo(){
	char *str;
	/* Stored in read only part of data segment */
	str = "GfG";
	/* Problem:  trying to modify read only memory */
	*(str+1) = 'n';
}
int main() {
    foo();
	return 0;
}
