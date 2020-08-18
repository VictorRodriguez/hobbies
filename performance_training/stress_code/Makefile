all:
	gcc -g -std=c99 add.c -o add
	gcc -g -std=c99 malloc.c -o malloc
	gcc -g -std=c99 branches.c -o branches --coverage
clean:
	rm -rf add malloc branches
	rm -rf *.gcno *.gcda
	rm -rf *.c.gcov
