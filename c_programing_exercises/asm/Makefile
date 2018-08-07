all:
	gcc add_asm.c -o add
	gcc sub_asm.c -o sub
	gcc mul_asm.c -o mul
	gcc div_asm.c -o div
	gcc -O3 -march=haswell add_avx2.c -o add_avx2
	gcc -O3 -march=icelake-server add_avx512.c -o add_avx512
	gcc -O3 -march=icelake-server add_d_avx512.c -o add_d_avx512
clean:
	rm -rf add sub mul div add_avx2 add_avx512 add_d_avx512

