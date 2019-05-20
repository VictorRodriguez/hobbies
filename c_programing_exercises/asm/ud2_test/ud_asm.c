#include <stdio.h>
#include <unistd.h>

int main() {

	/* usleep() takes microseconds, so you will have to
	multiply the input by 1000 in order to sleep in
	milliseconds
	*/
	usleep(1000);

    /* Perform ilegal insruction */
    __asm__("ud2");

    return 0;
}
