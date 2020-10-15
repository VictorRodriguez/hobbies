FROM centos:latest
RUN yum install -y numactl git
RUN yum -y install python3
RUN yum -y install python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install intel-tensorflow
RUN git clone https://github.com/IntelAI/models.git
RUN git clone https://github.com/tensorflow/models.git tensorflow-models
RUN yum install -y wget
RUN cd models/benchmarks && wget https://storage.googleapis.com/intel-optimized-tensorflow/models/resnet50_int8_pretrained_model.pb
RUN cd models/benchmarks && wget https://storage.googleapis.com/intel-optimized-tensorflow/models/resnet50_fp32_pretrained_model.pb

CMD cd models/benchmarks && DNNL_VERBOSE=1 python3 launch_benchmark.py \
    -v \
    --disable-tcmalloc=True \
    --model-name resnet50 \
    --precision int8 \
    --mode inference \
    --framework tensorflow \
    --benchmark-only \
    --batch-size 1 \
    --socket-id 0 \
    --in-graph ./resnet50_int8_pretrained_model.pb \
    -- warmup_steps=50 steps=500
