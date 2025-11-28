FROM rockylinux:8

# Default benchmark options (can be overridden at runtime)
ENV DRIVER="--conv"
ENV DT="u8:s8:f32"
ENV BATCH="inputs/conv/shapes_resnet_50"
ENV EXTRA_ARGS=""
ENV ONEDNN_MAX_CPU_ISA=""

# Prepare repos and install build requirements
RUN dnf install -y dnf-plugins-core && \
    dnf config-manager --set-enabled powertools && \
    dnf install -y doxygen cmake git && \
    dnf groupinstall -y "Development Tools"

# Clone and build oneDNN
RUN git clone https://github.com/oneapi-src/oneDNN.git
RUN mkdir oneDNN/build
RUN cd oneDNN/build && cmake ../ ; exit 0
RUN cd oneDNN/build && make -j

# Add benchmark script
COPY ./scripts/run-benchdnn.sh /

WORKDIR /oneDNN/build/tests/benchdnn

CMD ["/run-benchdnn.sh"]

