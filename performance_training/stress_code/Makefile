all:
	gcc -g -std=c99 -O2 -ftree-vectorize add.c -o add
	gcc -g -std=c99 malloc.c -o malloc
	gcc -g -std=c99 branches.c -o branches --coverage

static:
	gcc -static -g -std=c99 add.c -o add
	gcc -static -g -std=c99 malloc.c -o malloc
	gcc -static -g -std=c99 branches.c -o branches --coverage

icx:
	gcc add.c -o add -O2 -ftree-vectorize -march=icelake-server
	gcc -g -std=c99 malloc.c -o malloc -O2 -ftree-vectorize -march=icelake-server
	gcc -g -std=c99 branches.c -o branches --coverage -O2 -ftree-vectorize -march=icelake-server

icx-static:
	gcc add.c -o add -static -O2 -ftree-vectorize -march=icelake-server
	gcc -g -std=c99 malloc.c -o malloc -static -O2 -ftree-vectorize -march=icelake-server
	gcc -g -std=c99 branches.c -o branches -static --coverage -O2 -ftree-vectorize -march=icelake-server

clean:
	rm -rf add malloc branches
	rm -rf *.gcno *.gcda
	rm -rf *.c.gcov
	rm -rf perf.data*
