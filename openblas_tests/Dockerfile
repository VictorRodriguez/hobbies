FROM clearlinux:latest

RUN swupd bundle-add make
RUN swupd bundle-add c-basic
RUN swupd bundle-add  openblas
RUN swupd bundle-add strace

COPY Makefile /
COPY *.c /

RUN make
