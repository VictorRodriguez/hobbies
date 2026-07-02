all:
	gcc -g add.c -o add
	gcc -g -std=c99 malloc.c -o malloc
	gcc -g -std=c99 branches.c -o branches --coverage
	gcc -g -O3 -march=native -o roi_demo roi_demo.c
	gcc -O3 -fno-tree-vectorize -fno-unroll-loops throughput_single_core.c -o throughput_single_core

static:
	gcc -static -g -std=c99 add.c -o add
	gcc -static -g -std=c99 malloc.c -o malloc
	gcc -static -g -std=c99 branches.c -o branches --coverage

gnr:
	gcc add.c -o add -O2 -ftree-vectorize -march=graniterapids
	gcc -g -std=c99 malloc.c -o malloc -O2 -ftree-vectorize -march=graniterapids
	gcc -g -std=c99 branches.c -o branches --coverage -O2 -ftree-vectorize -march=graniterapids

icx-static:
	gcc add.c -o add -static -O2 -ftree-vectorize -march=icelake-server
	gcc -g -std=c99 malloc.c -o malloc -static -O2 -ftree-vectorize -march=icelake-server
	gcc -g -std=c99 branches.c -o branches -static --coverage -O2 -ftree-vectorize -march=icelake-server

clean:
	rm -rf add malloc branches
	rm -rf *.gcno *.gcda
	rm -rf *.c.gcov
	rm -rf perf.data*
