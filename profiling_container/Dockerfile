FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install curl --assume-yes
RUN apt-get install xz-utils --assume-yes
RUN echo "deb-src http://archive.ubuntu.com/ubuntu/ bionic main" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get build-dep python3.6 --assume-yes
RUN curl -O -L https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tar.xz
RUN curl -O -L http://www.phoronix-test-suite.com/benchmark-files/pybench-2018-02-16.tar.gz
RUN tar -xvf Python-3.8.3.tar.xz

#RUN mkdir /build
COPY patches/AVX2-and-AVX512-support.patch /
COPY patches/Build-avx2-and-avx512-versions-of-the-math-library.patch /
RUN cd Python-3.8.3/ && patch -p1 < ../AVX2-and-AVX512-support.patch
RUN cd Python-3.8.3/ && patch -p1 < ../Build-avx2-and-avx512-versions-of-the-math-library.patch

RUN mkdir /build

RUN export LANG=C && \
	export CFLAGS="$CFLAGS -O3" \
	export CFLAGS="$CFLAGS -march=haswell -mfma  " \
	export CXXFLAGS="$CXXFLAGS -march=haswell -mfma" \
	&& echo $CFLAGS \
	&& cd Python-3.8.3/ \
	&& ./configure \
	LDFLAGS="-Wa,-mbranches-within-32B-boundaries" \
	--with-pymalloc \
	--without-cxx-main \
	--enable-ipv6=yes \
	--prefix=/build/ \
	ac_cv_header_bluetooth_bluetooth_h=no \
	ac_cv_header_bluetooth_h=no \
	--with-system-ffi \
	--with-system-expat \
	--with-lto=8 \
	--with-computed-gotos \
	--without-ensurepip \
	--enable-optimizations \
	&& make -j8\
	&& make install
RUN rm -rf /usr/bin/python3
run ln -s /build/bin/python3 /usr/bin/python3
