FROM centos:latest

RUN yum install wget gcc zlib-devel  autogen-libopts -y
RUN wget http://mirror.centos.org/centos/7/os/x86_64/Packages/autogen-5.18-5.el7.x86_64.rpm
RUN rpm -ivh autogen-5.18-5.el7.x86_64.rpm --nodeps
RUN yum group install "Development Tools" -y
COPY build-gcc.sh /
COPY build-binutils.sh /
RUN ./build-gcc.sh
RUN dnf --enablerepo=PowerTools install texinfo -y
RUN ./build-binutils.sh
