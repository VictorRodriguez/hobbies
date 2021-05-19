FROM centos:centos8.3.2011

ARG PERF_BOOL

RUN yum -y install epel-release
RUN yum -y install gcc gcc-c++ openssl-devel libffi-devel
RUN yum install -y numactl \
	git \
	python3 \
	python3-pip \
	python3-devel \
	wget

RUN if [ "$PERF_BOOL" = "True" ]; then \
	yum install perf -y; \
  fi

RUN pip3 install tensorflow

RUN git clone -q https://github.com/IntelAI/models.git

RUN cd models/benchmarks \
	&& wget -q https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/resnet50v1_5_int8_pretrained_model.pb
RUN cd models/benchmarks \
	&& wget -q https://zenodo.org/record/2535873/files/resnet50_v1.pb
RUN cd models/benchmarks \
    && wget -q https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/resnet50_v1_5_bfloat16.pb

COPY main_resent50.sh /models/benchmarks/
CMD cd models/benchmarks && ./main_resent50.sh
