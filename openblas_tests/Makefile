all:
	gcc cblas_ddot.c -o cblas_ddot -lopenblas
	gcc -o test_cblas_open test_cblas_dgemm.c -lopenblas -lpthread

clean:
	rm -rf cblas_ddot
