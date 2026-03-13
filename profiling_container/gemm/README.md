# GEMM Stress Benchmark Container

This container runs a **CPU-intensive GEMM microkernel benchmark** designed for architectural testing, simulator workloads, and CPU instruction stress experiments.

The benchmark computes:

```

C = C + A * B

```

using a **microkernel GEMM implementation** with vector instructions.

Two binaries are included:

| Binary | ISA | Kernel |
|------|------|------|
| `gemm_stress_avx2_sniper` | AVX2 + FMA | 4×4 microkernel |
| `gemm_stress_avx512_sniper` | AVX-512 + FMA | 8×8 microkernel |

The container selects which binary to run using an **environment variable**.

---

# Container Contents

```

/app
├── gemm_stress_avx2_sniper
├── gemm_stress_avx512_sniper
└── entrypoint.sh

````

The `entrypoint.sh` script selects the correct binary based on the `ARCH` variable.

---

# Build the Container

From the directory containing the Dockerfile:

```bash
docker build -t gemm-stress .
````

---

# Runtime Configuration

The container accepts two types of inputs:

1. **Environment variables**
2. **Program parameters**

---

# Environment Variables

## ARCH

Selects which instruction set binary to run.

| Value    | Description            |
| -------- | ---------------------- |
| `avx2`   | Runs AVX2 benchmark    |
| `avx512` | Runs AVX-512 benchmark |

Default:

```
avx2
```

Example:

```bash
docker run -e ARCH=avx512 gemm-stress
```

---

# Program Arguments

The benchmark accepts the following parameters:

```
<iters> [M] [N] [K]
```

| Argument | Description                | Default  |
| -------- | -------------------------- | -------- |
| `iters`  | Number of GEMM repetitions | required |
| `M`      | Matrix rows                | 256      |
| `N`      | Matrix columns             | 256      |
| `K`      | Inner dimension            | 256      |

Example computation:

```
C(M×N) = C(M×N) + A(M×K) × B(K×N)
```

---

# Basic Usage

Run the default configuration:

```bash
docker run --rm gemm-stress 10
```

Equivalent to:

```
iters = 10
M = 256
N = 256
K = 256
```

---

# Run AVX2 Version

```bash
docker run --rm \
-e ARCH=avx2 \
gemm-stress 10 256 256 256
```

---

# Run AVX-512 Version

```bash
docker run --rm \
-e ARCH=avx512 \
gemm-stress 10 256 256 256
```

⚠️ **Important:**
AVX-512 execution requires the host CPU to support AVX-512 instructions.

---

# Example Benchmark Runs

### Small test

```bash
docker run --rm gemm-stress 5 128 128 128
```

### Medium compute workload

```bash
docker run --rm -e ARCH=avx2 gemm-stress 20 512 512 512
```

### Heavy compute stress

```bash
docker run --rm -e ARCH=avx512 gemm-stress 50 1024 1024 1024
```

---

# ROI Markers

The benchmark prints:

```
ROI_START
ROI_END
```

These markers allow external tools and simulators (e.g., **Sniper**) to detect the region of interest for measurement.

---

# Example Output

```
ROI_START
ROI_END
checksum=67108864.000000
```

The checksum prevents compiler dead-code elimination and ensures the computation is executed.

---

# Export the Container

Save the container as a compressed image:

```bash
docker save gemm-stress | gzip > gemm-stress.tar.gz
```

Load later:

```bash
gunzip -c gemm-stress.tar.gz | docker load
```

---

# Typical Use Cases

This container is useful for:

* CPU microarchitecture testing
* ISA instruction stress testing
* Sniper simulation workloads
* Performance counter experiments
* HPC benchmarking demonstrations

```

