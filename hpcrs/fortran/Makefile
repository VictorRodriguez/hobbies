all:
	ifort hello_basic.f90 -o hello_basic && ./hello_basic
	gfortran -ffree-form hello_basic.f90 -o hello_basic && ./hello_basic
gfortran:
	gfortran -ffree-form hello_basic.f -o hello_basic
run:
	./hello_basic
clean:
	rm -rf hello_basic
