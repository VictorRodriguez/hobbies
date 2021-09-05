#include<stdio.h>
int main() {
    // a = 5(00000101)
    unsigned char a = 5;

    // The result is 00001010
    printf("a<<1 = %d\n", a<<1);

	// Test for shift-count-negative
    printf("a<<1 = %d\n", a<<-1);

    return 0;
}
