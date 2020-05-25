all:
	gcc omp_hello.c -fopenmp -o omp_hello && ./omp_hello &> debug.log
full:
	gcc omp_mm.c -fopenmp -o omp_mm && ./omp_mm &> debug_full.log
run:
	./omp_hello
	./omp_mm
clean:
	rm -rf omp_mm omp_hello
	rm -rf *.log
