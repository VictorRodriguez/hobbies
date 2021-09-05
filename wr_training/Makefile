all:
	gcc -O2 -ftree-vectorize add.c -fopt-info-vec -o add
basic:
	gcc -O0 add.c -o add
haswell:
	gcc -O2 -ftree-vectorize -march=haswell add.c -fopt-info-vec -o add
FMV:
	gcc -O2 -ftree-vectorize fmv.c -o fmv
image:
	docker build -t wr_training .
clean:
	rm -rf fmv add
