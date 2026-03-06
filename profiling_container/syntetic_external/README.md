# Synthetic Workloads for Microarchitectural Characterization

## Overview

This repository provides **minimal synthetic workloads** designed to characterize CPU microarchitectural behavior in a **controlled and deterministic way**.

Unlike complex application benchmarks, these kernels isolate specific architectural phenomena, allowing performance trends to be attributed directly to hardware characteristics such as execution throughput, cache capacity, or memory latency.

The suite currently includes two orthogonal kernels:

| Kernel               | Type          | Targeted Behavior                               |
| -------------------- | ------------- | ----------------------------------------------- |
| **Frequency kernel** | Compute-bound | Core execution throughput and frequency scaling |
| **Cache kernel**     | Memory-bound  | Cache hierarchy and memory latency              |

These workloads are useful for:

* CPU microarchitecture characterization
* Performance modeling research
* Pre-silicon architecture studies
* Cache hierarchy exploration
* Frequency scaling experiments
* Simulator validation

Because the workloads are intentionally simple, they produce **clean and interpretable performance signals**.

---

# Repository Structure

```
.
├── synthetic_char.c
├── Makefile
└── README.md
```

The project builds a single executable:

```
synthetic_char
```

An optimized version is also produced:

```
synthetic_char_o
```

---

# Build Instructions

## Requirements

* GCC or Clang
* Linux environment
* Standard C library

No external simulators or frameworks are required.

## Compile

```bash
make clean
make
```

This produces two binaries:

| Binary             | Description                                            |
| ------------------ | ------------------------------------------------------ |
| `synthetic_char`   | Baseline build                                         |
| `synthetic_char_o` | Optimized build (`-O3`, vectorization, loop unrolling) |

---

# Program Usage

```
./synthetic_char <mode> <iters> <working_set_elems> <stride>
```

### Arguments

| Argument            | Description                            |
| ------------------- | -------------------------------------- |
| `mode`              | `freq`, `freq_p`, or `cache`           |
| `iters`             | Number of loop iterations              |
| `working_set_elems` | Working set size (elements of 8 bytes) |
| `stride`            | Pointer stride for memory accesses     |

---

# Kernel 1 — Frequency Scaling (Compute Bound)

## Objective

Characterize the performance of **pure compute workloads** and observe scaling behavior with core frequency or execution resources.

## Command

```
./synthetic_char freq 100000000 1 1
```

## Kernel Characteristics

* Minimal memory traffic
* Strong arithmetic dependencies
* Instruction footprint fits in L1 instruction cache
* Execution units dominate performance

## Expected Behavior

| Metric              | Expected Trend                      |
| ------------------- | ----------------------------------- |
| Instructions        | Constant                            |
| IPC                 | Approximately constant              |
| Cycles              | Inversely proportional to frequency |
| Cache misses        | Near zero                           |
| Backend utilization | High                                |

This kernel should exhibit **near-linear scaling with frequency**.

---

# Kernel 2 — Parallel Arithmetic Kernel

## Objective

Evaluate throughput of vectorizable arithmetic loops and observe effects of compiler optimization.

## Command

```
./synthetic_char freq_p 100000 1000000 1
```

## Kernel Characteristics

* Dense arithmetic loop over arrays
* High arithmetic intensity
* Potential compiler vectorization
* Low memory pressure

This kernel helps evaluate:

* vectorization efficiency
* instruction throughput
* compiler optimization effects

---

# Kernel 3 — Cache Sensitivity (Memory Bound)

## Objective

Characterize cache hierarchy and memory latency by sweeping the working set size.

## Command

```
./synthetic_char cache 50000000 <working_set_elems> <stride>
```

Example:

```
./synthetic_char cache 50000000 1048576 8
```

## Working Set Reference Sizes

| Cache Level | Elements  | Approx Size |
| ----------- | --------- | ----------- |
| L1          | 4,096     | 32 KB       |
| L2          | 65,536    | 512 KB      |
| LLC         | 1,048,576 | 8 MB        |
| DRAM        | 4,194,304 | 32 MB       |

## Kernel Characteristics

* Pointer-chasing access pattern
* Strict serial dependency
* Prefetchers largely ineffective
* Memory latency dominates execution time

The kernel enforces **Memory Level Parallelism (MLP) ≈ 1**, making it suitable for latency characterization.

## Expected Behavior

| Working Set | Observation            |
| ----------- | ---------------------- |
| Fits in L1  | High IPC               |
| Exceeds L1  | L1 miss rate increases |
| Exceeds L2  | L2 miss rate increases |
| Exceeds LLC | DRAM accesses dominate |

---

# ROI Markers

The program prints:

```
ROI_START
ROI_END
```

These markers allow external tools to isolate the region of interest during profiling.

Example:

```
perf stat ./synthetic_char freq 100000000 1 1
```

Profiling tools can filter events between these markers.

---

# Recommended Performance Metrics

When profiling the kernels, collect:

* Cycles
* Instructions
* IPC
* Cache miss rates
* Memory bandwidth
* Stall cycles

Example with Linux `perf`:

```
perf stat \
  -e cycles,instructions,cache-misses,cache-references \
  ./synthetic_char cache 50000000 1048576 8
```

---

# Relationship to Analytical Performance Models

The kernels map naturally to **CPI decomposition models**:

```
CPI = CPI_compute + CPI_memory
```

Where:

* **Frequency kernel → CPI_compute**
* **Cache kernel → CPI_memory**

This makes the suite useful for:

* analytical performance modeling
* validation of simulator results
* memory subsystem studies

---

# Possible Extensions

The framework can easily be extended to explore additional architectural behaviors:

* Multiple pointer chains to sweep **MLP**
* Mixed compute/memory kernels
* SIMD-specific kernels (AVX / AMX / FMA)
* Instruction mix characterization
* entropy-based workload diversity studies

---

# Summary

This suite provides a **minimal baseline for architectural characterization**.

| Kernel           | Bottleneck              | Use Case                         |
| ---------------- | ----------------------- | -------------------------------- |
| Frequency        | Execution throughput    | DVFS and compute scaling         |
| Parallel compute | SIMD/vector performance | Compiler and ISA studies         |
| Cache            | Memory latency          | Cache hierarchy characterization |

Because the kernels are intentionally simple, architectural effects remain **visible, reproducible, and analytically tractable**.

