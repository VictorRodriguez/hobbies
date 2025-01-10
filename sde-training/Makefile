all:
	gcc -g -march=skylake -O2 -mavx2 -I/home/centos/iwps/include -o fft_stress fft_stress.c -lm
	gcc -g -march=skylake -O2 -mavx2 -I/home/centos/iwps/include -o workload workload.c
	gcc -g -march=skylake -O2 -mavx2 -I/home/centos/iwps/include -o workload_timing workload_timing.c
	gcc -O2 -lm -march=native -pthread -I/home/centos/iwps/include -o fft_stress_threads fft_stress_threads.c

