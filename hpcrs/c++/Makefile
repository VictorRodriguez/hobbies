all:
	icc basic.cpp -o basic && ./basic
full:
	cd /opt/intel/documentation_2020/en/mpi/examples/ && make
	cd /opt/intel/documentation_2020/en/mpi/examples/ && ./async_progress
	cd /opt/intel/documentation_2020/en/mpi/examples/ && ./thread_split
	cd /opt/intel/documentation_2020/en/mpi/examples/ && ./thread_split_omp_for
	cd /opt/intel/documentation_2020/en/mpi/examples/ && ./thread_split_omp_task
	cd /opt/intel/documentation_2020/en/mpi/examples/ && ./thread_split_pthreads
run:
	./basic

