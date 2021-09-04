all:
	gcc cblas_ddot.c -o cblas_ddot -lopenblas
	gcc -o test_cblas_dgem test_cblas_dgemm.c -lopenblas -lpthread
	gcc -o test_cblas_dgemm_fortran test_cblas_dgemm_fortran.c -lopenblas

image:
	docker build -t openblas_test .

clean:
	rm -rf cblas_ddot test_cblas_dgem test_cblas_dgemm_fortran
