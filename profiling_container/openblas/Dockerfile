FROM centos:latest
RUN yum install wget -y
RUN yum group install "Development Tools" -y
RUN mkdir /opt/build
RUN cd /opt/build && wget https://github.com/xianyi/OpenBLAS/archive/v0.3.10.tar.gz
RUN cd /opt/build && tar -xvf v0.3.10.tar.gz
RUN cd /opt/build/OpenBLAS-0.3.10/ && \
	grep -q '^flags .*avx2' /proc/cpuinfo 2>/dev/null || SKIPTESTS=CROSS=1 && \
	make TARGET=HASWELL F_COMPILER=GFORTRAN  SHARED=1 DYNAMIC_THREADS=1 USE_OPENMP=1 NO_AFFINITY=1  NUM_THREADS=128
