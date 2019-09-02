all:
	gcc -O2 -ftree-vectorize add.c -fopt-info-vec
basic:
	gcc -O0 add.c
haswell:
	gcc -O2 -ftree-vectorize -march=haswell add.c -fopt-info-vec
FMV:
	gcc -O2 -ftree-vectorize fmv.c
clean:
	rm -rf a.out

