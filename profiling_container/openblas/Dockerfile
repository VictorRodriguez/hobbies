FROM centos:latest
RUN yum install wget -y
RUN yum group install "Development Tools" -y
RUN mkdir /opt/build
RUN mkdir /opt/openblas
RUN cd /opt/build && wget https://github.com/xianyi/OpenBLAS/archive/v0.3.10.tar.gz
RUN cd /opt/build && tar -xvf v0.3.10.tar.gz

ENV AR=gcc-ar
ENV RANLIB=gcc-ranlib
ENV CFLAGS="$CFLAGS  -fno-semantic-interposition -O3 "
ENV FFLAGS="$CFLAGS -fno-semantic-interposition -O3 -fno-f2c "
ENV CXXFLAGS="$CXXFLAGS -fno-semantic-interposition -O3 "

RUN  cd /opt/build/OpenBLAS-0.3.10/ && sed -i -e "s/\-O2/\-O3/g" Makefile*
RUN cd /opt/build/OpenBLAS-0.3.10/ && \
	export CFLAGS="$CFLAGS -march=haswell" && \
	export FFLAGS="$FFLAGS -march=haswell" && \
	grep -q '^flags .*avx2' /proc/cpuinfo 2>/dev/null || SKIPTESTS=CROSS=1 && \
	make TARGET=HASWELL F_COMPILER=GFORTRAN  SHARED=1 DYNAMIC_THREADS=1 USE_OPENMP=1 NO_AFFINITY=1  NUM_THREADS=128 && \
	make install DESTDIR=/opt/openblas/ PREFIX=/usr OPENBLAS_LIBRARY_DIR=/usr/lib64/haswell
RUN cd /opt/build/OpenBLAS-0.3.10/ && ln -sf libopenblas_haswellp-r0.3.10.so /opt/openblas/usr/lib64/haswell/libblas.so
RUN cd /opt/build/OpenBLAS-0.3.10/ && ln -sf libopenblas_haswellp-r0.3.10.so /opt/openblas/usr/lib64/haswell/libblas.so.3
RUN cd /opt/build/OpenBLAS-0.3.10/ && ln -sf libopenblas_haswellp-r0.3.10.so /opt/openblas/usr/lib64/haswell/liblapack.so
RUN cd /opt/build/OpenBLAS-0.3.10/ && ln -sf libopenblas_haswellp-r0.3.10.so /opt/openblas/usr/lib64/haswell/liblapack.so.3
