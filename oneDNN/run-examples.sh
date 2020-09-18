#!/bin/bash

set -x

cd /oneDNN/build/examples/

./primitives-shuffle-cpp
./cnn-inference-f32-cpp
./primitives-lrn-cpp
./performance-profiling-cpp
./primitives-layer-normalization-cpp
./memory-format-propagation-cpp
./primitives-softmax-cpp
./primitives-binary-cpp
./primitives-pooling-cpp
./primitives-eltwise-cpp
./primitives-reorder-cpp
./primitives-reduction-cpp
./cnn-inference-f32-c
./cpu-tutorials-matmul-matmul-quantization-cpp
./cpu-tutorials-matmul-sgemm-and-matmul-cpp
./cnn-inference-int8-cpp
./primitives-lstm-cpp
./cpu-cnn-training-f32-c
./primitives-matmul-cpp
./cpu-rnn-inference-int8-cpp
./primitives-concat-cpp
./primitives-convolution-cpp
./rnn-training-f32-cpp
./primitives-resampling-cpp
./primitives-batch-normalization-cpp
./cnn-training-bf16-cpp
./getting-started-cpp
./primitives-sum-cpp
./primitives-logsoftmax-cpp
./cpu-rnn-inference-f32-cpp
./tutorials-matmul-inference-int8-matmul-cpp
./primitives-inner-product-cpp
./cnn-training-f32-cpp

