#include <stdio.h>

void foo2(){
    printf("%p\n", __builtin_return_address(0));
}
void foo(){
    foo2();
}
int main(int argc, char **argv) {
    foo();
    return 0;
}
