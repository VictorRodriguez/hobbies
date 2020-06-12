all:
	python  mpi_basic.py &> debug.log
full:
	git clone https://github.com/LLNL/mpiBench.git
	cd mpiBench/ && make
	cd mpiBench/ && ./mpiBench -i 10000000
	rm -rf mpiBench/
