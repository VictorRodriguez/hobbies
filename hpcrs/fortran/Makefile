all:
	ifort hello_basic.f90 -o hello_basic && ./hello_basic
	gfortran -ffree-form hello_basic.f90 -o hello_basic && ./hello_basic
gfortran:
	gfortran -ffree-form hello_basic.f -o hello_basic
full:
	cd /opt/intel/compilers_and_libraries_2020.1.217/linux/mpi/test && mpif90 test.f
	cd /opt/intel/compilers_and_libraries_2020.1.217/linux/mpi/test && mpirun ./a.out
	mpif90 -fopenmp omp_dotprod_hybrid.f -o omp_dotprod_hybrid
	mpirun ./omp_dotprod_hybrid
run:
	./hello_basic
clean:
	rm -rf hello_basic
	rm -rf omp_dotprod_hybrid
