FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install curl --assume-yes
RUN apt-get install xz-utils --assume-yes
RUN apt-get install build-essential --assume-yes
RUN cp /etc/apt/sources.list /etc/apt/sources.list~
RUN sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list
RUN apt-get update
RUN apt-get build-dep python3 --assume-yes
RUN apt-get install zlib1g-dev --assume-yes
RUN curl -O -L https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tar.xz
RUN tar -xvf Python-3.8.3.tar.xz
RUN export LANG=C && export CFLAGS="$CFLAGS -O3" && cd Python-3.8.3/ \
	&& ./configure && make && make install
