

# BenchDNN Docker Environment

**BenchDNN** is a benchmarking tool included in **oneDNN** (Intel® oneAPI Deep Neural Network Library) for evaluating the performance of deep learning primitives (e.g., convolutions, inner products) on CPUs. It is useful for profiling, optimization, and comparing different data types, batch sizes, and CPU instruction sets.

---

## Key Features

* **Flexible primitive selection:** Convolutions, inner products, pooling, normalization, RNNs, etc.
* **Supports multiple data types:** `f32` (float32), `s8`/`u8` (quantized), `bf16` (bfloat16).
* **Instruction set tuning:** Test performance across AVX2, AVX512, AMX, or the maximum supported CPU ISA.
* **Batch and shape customization:** Predefined shapes (e.g., ResNet-50 inputs) or custom shapes.
* **Threading support:** Uses OpenMP for CPU parallelism with core binding.

---

## Docker Environment

This repository provides a **Dockerfile** and helper script to run BenchDNN in a containerized, reproducible environment.

### Dockerfile

```dockerfile
FROM rockylinux:8

# Default benchmark options (can be overridden at runtime)
ENV DRIVER="--conv"
ENV DT="u8:s8:f32"
ENV BATCH="inputs/conv/shapes_resnet_50"
ENV EXTRA_ARGS=""
ENV ONEDNN_MAX_CPU_ISA=""

# Install build tools
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
```

---

### Benchmark Script

`scripts/run-benchdnn.sh`:

```bash
#!/bin/bash
set -x

# Optionally enable DMR/AMX/AVX10 support
if [ -n "$ONEDNN_MAX_CPU_ISA" ]; then
    export ONEDNN_MAX_CPU_ISA=$ONEDNN_MAX_CPU_ISA
fi

export DNNL_CPU_RUNTIME=OMP
export OMP_PLACES=cores
export OMP_PROC_BIND=close

# Run the benchmark with flexible options
./benchdnn $DRIVER --dt=$DT --batch=$BATCH $EXTRA_ARGS
```

**Environment variables explained:**

| Variable             | Description                                                    |
| -------------------- | -------------------------------------------------------------- |
| `DRIVER`             | Primitive to benchmark (`--conv`, `--ip`, `--pool`, etc.)      |
| `DT`                 | Data types (`f32`, `s8`, `u8`, `bf16`)                         |
| `BATCH`              | Batch/shape definitions (e.g., `inputs/conv/shapes_resnet_50`) |
| `EXTRA_ARGS`         | Additional BenchDNN CLI options                                |
| `ONEDNN_MAX_CPU_ISA` | Force a specific CPU ISA (AVX2, AVX512, AMX, etc.)             |

---

## Building and Running

1. **Build the Docker image:**

```bash
docker build -t benchdnn:latest .
```

2. **Run the container with default options:**

```bash
docker run --rm -it benchdnn:latest
```

3. **Override benchmark options at runtime:**

```bash
docker run --rm -it \
  -e DRIVER="--ip" \
  -e DT="f32" \
  -e BATCH="inputs/ip/shapes_test" \
  benchdnn:latest
```

---

## Supported Benchmarks

BenchDNN benchmarks various neural network operations:

| Benchmark Type               | Description                                      |
| ---------------------------- | ------------------------------------------------ |
| **Convolution (`--conv`)**   | Forward/backward convolutions for CNNs           |
| **Inner Product (`--ip`)**   | Dense layers, fully-connected operations         |
| **Pooling (`--pool`)**       | Max/average pooling layers                       |
| **Normalization (`--norm`)** | BatchNorm, LayerNorm, etc.                       |
| **RNN / LSTM (`--rnn`)**     | Recurrent layers                                 |
| **Binary/Quantized Ops**     | INT8, UINT8, BF16 performance evaluation         |
| **Custom shapes**            | User-defined batch sizes and input/output shapes |

BenchDNN can report:

* Execution time
* Gflops / Gops performance
* Memory footprint
* Thread scaling / CPU utilization

---


## CPU Dispatcher Control (`ONEDNN_MAX_CPU_ISA`)

OneDNN provides a **CPU dispatcher** mechanism that selects the most optimized kernel for your processor’s instruction set at runtime. By default, oneDNN automatically picks the highest available ISA supported by your CPU.

You can **override this behavior** using the environment variable:

```bash
export ONEDNN_MAX_CPU_ISA=<ISA>
```

Where `<ISA>` can be:

* `SSE4_1` – Intel SSE4.1 instructions
* `AVX2` – Intel AVX2 instructions
* `AVX512_CORE` – Intel AVX-512 instructions
* `AMX` – Advanced Matrix Extensions
* `AVX10` / `DMR` – Experimental / upcoming CPU instruction sets

---

### Why this is useful

1. **Controlled testing of new ISAs:**
   When validating **new CPU features** (e.g., DMR, AMX, or AVX10), you can force BenchDNN to use a specific ISA without depending on CPU auto-detection. This is crucial for **pre-silicon or lab testing**, where hardware might be partially implemented.

2. **Performance regression testing:**
   Comparing benchmarks across different instruction sets helps identify regressions or optimizations.

3. **Reproducibility:**
   Ensures that all benchmark runs use the exact same ISA, making results comparable across different machines or CI/CD environments.

4. **Debugging new kernels:**
   Developers can isolate performance issues in **experimental or partially supported ISAs** without affecting stable kernels.

---

### Example Usage

Run BenchDNN with **AMX instructions**:

```bash
docker run --rm -it \
  -e ONEDNN_MAX_CPU_ISA=AMX \
  benchdnn:latest
```

Run with an **experimental DMR ISA**:

```bash
docker run --rm -it \
  -e ONEDNN_MAX_CPU_ISA=AVX10 \
  benchdnn:latest
```

BenchDNN will **only dispatch kernels compatible with the specified ISA**, allowing precise evaluation of performance and correctness.

---



## Summary

BenchDNN is a **powerful tool for CPU deep learning performance characterization**. Using the provided Docker setup, you can:

* Quickly build and run benchmarks in a clean, reproducible environment
* Test different CPU ISAs and threading strategies
* Evaluate multiple data types and batch sizes
* Integrate benchmarks into CI/CD pipelines or regression tests

