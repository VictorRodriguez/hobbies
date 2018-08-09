all:
	gcc add_asm.c -o add
	gcc sub_asm.c -o sub
	gcc mul_asm.c -o mul
	gcc div_asm.c -o div
	gcc -O3 -march=haswell add_avx2.c -o add_avx2
	gcc -O3 -march=skylake-avx512 add_avx512.c -o add_avx512
	gcc -O3 -march=skylake-avx512 add_d_avx512.c -o add_d_avx512
	gcc -O3 -march=skylake-avx512 add_i_avx512.c -o add_i_avx512
	gcc -O3 -march=icelake-server -mavx5124vnniw 4dpwssd_epi32.c -o 4dpwssd_epi32
clean:
	rm -rf add sub mul div add_avx2 add_avx512 add_d_avx512 add_i_avx512 4dpwssd_epi32

