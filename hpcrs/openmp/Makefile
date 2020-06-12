all:
	gcc omp_hello.c -fopenmp -o omp_hello && ./omp_hello &> debug.log
full:
	gcc omp_mm.c -fopenmp -o omp_mm 
	./omp_mm > debug_full.log
	gcc example_linear_in_loop.c -fopenmp -o example_linear_in_loop
	./example_linear_in_loop >> debug_full.log
	mpicc omp_dotprod_hybrid.c -fopenmp -o omp_dotprod_hybrid
	mpirun ./omp_dotprod_hybrid >> debug_full.log

run:
	./omp_hello
	./omp_mm
clean:
	rm -rf omp_mm omp_hello omp_dotprod_hybrid example_linear_in_loop
	rm -rf *.log
