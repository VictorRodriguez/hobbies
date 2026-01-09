# Synthetic Workloads for Sniper Characterization

## Overview

This project provides **minimal, orthogonal synthetic workloads** designed to characterize CPU microarchitecture using the **Sniper simulator**.

The workloads are intentionally simple and deterministic so that observed performance trends can be directly attributed to architectural parameters rather than application complexity.

Two kernels are provided:

1. **Frequency-scaling kernel** (compute-bound)
2. **Cache-size sensitivity kernel** (memory-bound, low MLP)

These workloads are suitable for:

* Microarchitectural characterization
* Pre-silicon validation
* Analytical performance modeling
* Frequency and cache sweep experiments

---

## Build Instructions

### Prerequisites

* GCC or Clang
* Sniper simulator
* `SNIPER_ROOT` environment variable set

Example:

```bash
export SNIPER_ROOT=/path/to/sniper
```

### Compile

```bash
make clean
make
```

This builds the binary:

```
synthetic_char
```

---

## Program Usage

```bash
./synthetic_char <mode> <iters> <working_set_elems> <stride>
```

### Arguments

| Argument            | Description                                    |
| ------------------- | ---------------------------------------------- |
| `mode`              | `freq` or `cache`                              |
| `iters`             | Number of loop iterations                      |
| `working_set_elems` | Size of working set in elements (8 bytes each) |
| `stride`            | Pointer stride (in elements)                   |

---

## 1. Frequency-Scaling Experiment

### Objective

Characterize sensitivity to **core frequency** in a purely compute-bound scenario.

### Command

```bash
./synthetic_char freq 100000000 1 1
```

### Characteristics

* No memory accesses in the ROI
* Instruction footprint fits in L1 I-cache
* Strong data dependencies
* Backend execution limited

### Expected Behavior

| Metric           | Expected Trend                      |
| ---------------- | ----------------------------------- |
| Instructions     | Constant                            |
| IPC              | ~Constant                           |
| Cycles           | Inversely proportional to frequency |
| L1/L2/LLC misses | ~0                                  |
| Backend stalls   | High                                |

This kernel should exhibit **near-linear performance scaling** with frequency.

---

## 2. Cache-Size Sensitivity Experiment

### Objective

Characterize cache capacity effects by sweeping the working set size.

### Command

```bash
./synthetic_char cache 50000000 <working_set_elems> <stride>
```

### Working Set Examples

| Cache Level | Elements  | Approx. Size |
| ----------- | --------- | ------------ |
| L1          | 4,096     | 32 KB        |
| L2          | 65,536    | 512 KB       |
| LLC         | 1,048,576 | 8 MB         |
| DRAM        | 4,194,304 | 32 MB        |

Example:

```bash
./synthetic_char cache 50000000 1048576 8
```

### Characteristics

* Pointer-chasing memory access pattern
* Enforced serial dependencies
* Prefetchers ineffective
* Memory latency dominates

### Expected Behavior

| Working Set | Observation                          |
| ----------- | ------------------------------------ |
| Fits in L1  | High IPC                             |
| Exceeds L1  | L1 miss rate increases               |
| Exceeds L2  | L2 miss rate increases               |
| Exceeds LLC | DRAM accesses dominate, IPC very low |

This kernel enforces **MLP ≈ 1**, making it ideal for cache and latency characterization.

---

## Running with Sniper

### Example Sniper Invocation

```bash
run-sniper --roi \
  -c gainestown \
  -- ./synthetic_char cache 50000000 1048576 8
```

The ROI markers (`SimRoiStart` / `SimRoiEnd`) ensure that only kernel execution is measured.

---

## Recommended Sniper Sweeps

### Frequency Sweep

```ini
[perf_model/core]
frequency = 1.0
```

Sweep this value up to 4.0 GHz (or your target range).

### Cache Size Sweep

```ini
[perf_model/l1_dcache]
cache_size = 32kB

[perf_model/l2_cache]
cache_size = 512kB

[perf_model/llc]
cache_size = 8MB
```

---

## Metrics to Collect

* Cycles
* Instructions
* IPC
* L1 / L2 / LLC miss rates
* DRAM accesses
* Backend stall cycles

These metrics are cleanly interpretable due to the intentionally simple workload structure.

---

## Relationship to Analytical Models

The workloads map directly to CPI decomposition:

* **Compute CPI** from the frequency kernel
* **Memory CPI** from the cache kernel
* **Effective memory latency ≈ raw latency / MLP**

This makes them suitable for:

* Analytical CPI models
* Validation of memory subsystem models
* Instruction-level characterization

---

## Extensions (Optional)

* Add multiple independent pointer chains to sweep **MLP**
* Combine frequency and cache sweeps to form a 2D characterization surface
* Extract instruction histograms for entropy-based workload selection

---

## Summary

This suite provides a **minimal characterization baseline**:

| Kernel    | Dominant Bottleneck | Purpose                    |
| --------- | ------------------- | -------------------------- |
| Frequency | Execution units     | DVFS and frequency scaling |
| Cache     | Memory latency      | Cache capacity effects     |

The simplicity of these kernels ensures architectural effects are **visible, measurable, and reproducible**, making them suitable for research, validation, and modeling.

