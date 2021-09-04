FROM clearlinux:latest

COPY Makefile .
COPY *.c .

RUN swupd bundle-add make
RUN swupd bundle-add c-basic
RUN swupd bundle-add  openblas
RUN swupd bundle-add strace
RUN make
