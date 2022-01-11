FROM centos:latest

ENV DRIVER="--conv"
ENV CONFIG="u8s8f32"
ENV BATCH="inputs/conv/shapes_resnet_50"

# Build req
RUN yum install dnf-plugins-core -y
RUN yum config-manager --set-enabled powertools
RUN dnf install doxygen -y
RUN yum install cmake git -y
RUN yum groupinstall 'Development Tools' -y

# Clone
RUN git clone https://github.com/oneapi-src/oneDNN.git

# Build
RUN mkdir oneDNN/build
RUN cd oneDNN/build && cmake ../ ; exit 0
RUN cd oneDNN/build && make -j

# Run benchmark
COPY ./scripts/run-benchdnn.sh /
CMD /run-benchdnn.sh
