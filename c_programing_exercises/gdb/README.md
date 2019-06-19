# Intro to GDB

GDB is a powerfull tool to debug your c code when things got complicated, it is
really powerfull and the aim of this tutorial is to walk over my personal
learnings:

## Segfault

Lets imagine we have the following code:

```
#include <stdio.h>

int main() {
	char *str;
	/* Stored in read only part of data segment */
	str = "GfG";
	/* Problem:  trying to modify read only memory */
	*(str+1) = 'n';
	return 0;
}

```

if we compile and run, we will get:

```
Segmentation fault (core dumped)
```

How to debug this , very simple:

* compile with the -g option:

```
    gcc -g segfaul.c -o segfault
```

Then run the binary with gdb:

```
gdb ./segfault
```

Be aware that the symbols are loaded:

```
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./segfault...done.
```

Then just run:

```
(gdb) run
Starting program: /home/vmrod/hobbies/c_programing_exercises/gdb/segfault

Program received signal SIGSEGV, Segmentation fault.
0x0000555555554611 in main () at segfaul.c:8
8		*(str+1) = 'n';
```

Which makes sence on the line of code with the error


