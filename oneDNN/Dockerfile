FROM centos:latest
RUN dnf --enablerepo=PowerTools install doxygen -y
RUN yum install cmake git -y
RUN yum groupinstall 'Development Tools' -y
RUN git clone https://github.com/oneapi-src/oneDNN.git
RUN mkdir oneDNN/build
RUN cd oneDNN/build && cmake ../ ; exit 0
RUN cd oneDNN/build && make
RUN cd oneDNN/build && make test
RUN cd oneDNN/build && make install
