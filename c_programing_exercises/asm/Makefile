asm:
	nasm -felf64 hello.asm
	ld hello.o -o hello
	nasm -felf64 loop.asm
	ld loop.o -o loop
all:
	gcc basic_add_asm.c -o basic_add_asm
	gcc basic_sub_asm.c -o basic_sub_asm
	gcc basic_mul_asm.c -o basic_mul_asm
	gcc basic_div_asm.c -o basic_div_asm
	gcc time_foo.c -o time_foo
	gcc -O3 -march=haswell basic_add_avx2.c -o basic_add_avx2
	gcc -O3 -march=haswell stress_add_avx2.c -o stress_add_avx2
	gcc -O3 -march=skylake-avx512 basic_add_avx512.c -o basic_add_avx512
	gcc -O3 -march=skylake-avx512 basic_add_d_avx512.c -o basic_add_d_avx512
	gcc -O3 -march=skylake-avx512 basic_add_i_avx512.c -o basic_add_i_avx512
	gcc -O3 -march=skylake-avx512 stress_add_avx512.c -o stress_add_avx512
	gcc -O3 -march=skylake-avx512 stress_add_d_avx512.c -o stress_add_d_avx512
	gcc -O3 -march=skylake-avx512 stress_add_i_avx512.c -o basic_add_i_avx512
	gcc -O3 -march=icelake-server -mavx5124vnniw 4dpwssd_epi32.c -o 4dpwssd_epi32
clean:
	@find . -type f -executable -exec sh -c "file -i '{}' | grep -q 'x-executable; charset=binary'" \; -print | xargs rm -f


