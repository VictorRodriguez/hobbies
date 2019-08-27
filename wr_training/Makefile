all:
	export CFLAGS= && gcc -O0 basic_add.c -o basic_add
	gcc -O3 basic_add.c -o basic_add_03
	gcc -O3 -march=haswell basic_add.c -o basic_add_03_haswell

clean:
	rm -rf basic_add basic_add_03 basic_add_03_haswell

