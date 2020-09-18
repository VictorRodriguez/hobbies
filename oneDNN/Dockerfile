FROM centos:latest

# Build req
RUN dnf --enablerepo=PowerTools install doxygen -y
RUN yum install cmake git -y
RUN yum groupinstall 'Development Tools' -y

# Clone
RUN git clone https://github.com/oneapi-src/oneDNN.git

# Build
RUN mkdir oneDNN/build
RUN cd oneDNN/build && cmake ../ ; exit 0
RUN cd oneDNN/build && make

# Make Test
RUN cd oneDNN/build && make test

# Install
RUN cd oneDNN/build && make install

# Build/Run examples
RUN cd oneDNN/examples && mkdir build
RUN cd oneDNN/examples/build && cmake ../
RUN cd /oneDNN/build/examples/ && make

COPY run-examples.sh /
CMD /run-examples.sh
