# Branch Predictor Stress Benchmark

A configurable single-core C benchmark designed to stress different components of a CPU branch predictor and compare behavior across multiple processor generations using IWPS.

The benchmark provides several deterministic branch patterns, including predictable, alternating, periodic, correlated, pseudo-random, and indirect branches. Each mode can be executed independently so that IWPS statistics can be attributed to a specific predictor behavior.

## Files

- `branch_predictor_stress.c` — benchmark source code
- `Makefile` — static build configuration
- `README.md` — build and execution instructions

## Requirements

- Linux
- GCC or a compatible C compiler
- Static C runtime development libraries

On some Linux distributions, static compilation may require an additional package such as `glibc-static`.

## Build

Build the benchmark with:

```bash
make
```

The resulting executable is:

```text
branch_predictor_stress
```

The Makefile uses optimization options that preserve explicit branch behavior and reduce compiler transformations that could remove or replace branches:

```text
-O2
-fno-if-conversion
-fno-if-conversion2
-fno-tree-vectorize
-fno-unroll-loops
-fno-omit-frame-pointer
-static
```

Equivalent manual build command:

```bash
gcc -O2 -std=c11 \
    -Wall -Wextra -Wpedantic \
    -fno-if-conversion \
    -fno-if-conversion2 \
    -fno-tree-vectorize \
    -fno-unroll-loops \
    -fno-omit-frame-pointer \
    -static \
    branch_predictor_stress.c \
    -o branch_predictor_stress
```

Verify that the executable is static:

```bash
file branch_predictor_stress
ldd branch_predictor_stress
```

A successful static build should report:

```text
not a dynamic executable
```

## Usage

```bash
./branch_predictor_stress [mode] [iterations] [core] [seed]
```

Arguments:

| Argument | Description | Default |
|---|---|---:|
| `mode` | Branch pattern to execute | `mixed` |
| `iterations` | Number of loop iterations | `200000000` |
| `core` | Logical CPU used for affinity | `0` |
| `seed` | Seed used by pseudo-random modes | `1` |

Example:

```bash
./branch_predictor_stress random 100000000 0 1
```

Display help:

```bash
./branch_predictor_stress --help
```

## Benchmark Modes

### `predictable`

A mostly taken conditional branch. This mode serves as the baseline and should produce a relatively low branch-misprediction rate.

```bash
./branch_predictor_stress predictable 100000000 0 1
```

### `alternating`

A branch that alternates between taken and not taken.

```bash
./branch_predictor_stress alternating 100000000 0 1
```

This mode evaluates whether the predictor can learn a simple two-state repeating pattern.

### `periodic`

A repeating branch-outcome sequence with a period of 16 iterations.

```bash
./branch_predictor_stress periodic 100000000 0 1
```

This mode stresses pattern-history capacity beyond simple alternating behavior.

### `correlated`

Two conditional branches whose outcomes depend on a shared history state.

```bash
./branch_predictor_stress correlated 100000000 0 1
```

This mode is intended to exercise global-history and correlation-based prediction.

### `random`

A conditional branch driven by a pseudo-random sequence generated during execution.

```bash
./branch_predictor_stress random 100000000 0 1
```

This mode creates a difficult-to-predict conditional branch. It also includes the instruction overhead of generating the pseudo-random values.

### `array`

A conditional branch driven by a pre-generated array of pseudo-random outcomes.

```bash
./branch_predictor_stress array 100000000 0 1
```

This separates branch execution from most pseudo-random-number generation overhead. The array is reused cyclically during the benchmark.

### `indirect`

An indirect call whose target is selected from 32 possible functions.

```bash
./branch_predictor_stress indirect 100000000 0 1
```

This mode stresses indirect branch target prediction.

### `mixed`

A combined workload containing predictable, correlated, pseudo-random, and indirect branches.

```bash
./branch_predictor_stress mixed 100000000 0 1
```

This mode provides a broader branch-predictor stress workload but is less useful for isolating a specific predictor component.

### `all`

Runs every mode sequentially.

```bash
./branch_predictor_stress all 100000000 0 1
```

For IWPS analysis, running each mode separately is recommended. A separate simulation prevents statistics from different branch patterns from being aggregated into one result.


## Measuring with `perf`

Run one benchmark mode at a time so that the hardware performance counters correspond to a single branch pattern.

Basic command:

```bash
perf stat \
    -e cycles,instructions,branches,branch-misses \
    ./branch_predictor_stress random 100000000 0 1
```

Recommended user-space-only measurement:

```bash
perf stat \
    -e cycles:u,instructions:u,branches:u,branch-misses:u \
    ./branch_predictor_stress random 100000000 0 1
```

The `:u` modifier excludes kernel activity and is preferable when comparing the benchmark across systems.

Repeat the measurement to evaluate run-to-run variability:

```bash
perf stat -r 5 \
    -e cycles,instructions,branches,branch-misses \
    ./branch_predictor_stress correlated 100000000 0 1
```

Run every mode independently:

```bash
for mode in predictable alternating periodic correlated random array indirect mixed; do
    echo
    echo "===== ${mode} ====="

    perf stat \
        -e cycles,instructions,branches,branch-misses \
        ./branch_predictor_stress "$mode" 100000000 0 1
done
```

### Derived Metrics

Calculate IPC as:

```text
IPC = Instructions / Cycles
```

Calculate branch-misprediction rate as:

```text
Branch Misprediction Rate =
    Branch Mispredictions / Retired Branches × 100
```

Calculate branch MPKI as:

```text
Branch MPKI =
    Branch Mispredictions / Instructions × 1000
```

For a fixed iteration count, the following normalized metrics are also useful:

```text
Cycles per Iteration = Cycles / Iterations
Instructions per Iteration = Instructions / Iterations
Branches per Iteration = Branches / Iterations
Branch Misses per Iteration = Branch Mispredictions / Iterations
```

### Example Result

The following result was measured for:

```bash
perf stat \
    -e cycles,instructions,branches,branch-misses \
    ./branch_predictor_stress random 100000000 0 1
```

Raw counters:

```text
Cycles:                1,518,493,715
Instructions:          1,702,317,548
Branches:                250,437,164
Branch mispredictions:    50,009,269
Elapsed time:                  0.4336 s
```

Derived values:

| Metric | Value |
|---|---:|
| IPC | 1.12 |
| Branch-misprediction rate | 19.97% |
| Branch MPKI | 29.38 |
| Cycles per iteration | 15.18 |
| Instructions per iteration | 17.02 |
| Branches per iteration | 2.50 |
| Branch misses per iteration | 0.50 |

The approximately `0.50` branch misses per iteration indicate that the primary pseudo-random conditional branch is behaving as intended: roughly half of its outcomes are mispredicted.

The aggregate branch-misprediction rate is lower than 50% because the generic `branches` counter includes other retired branches, such as the loop-back branch and function-control flow. Most of those additional branches are highly predictable.

The workload-level ratio of cycles to branch misses must not be interpreted as the exact branch-misprediction penalty. Total cycles also include useful instructions, pseudo-random-number generation, correctly predicted branches, loop overhead, and other execution costs.

### Processor-Specific Branch Events

The generic events:

```text
branches
branch-misses
```

combine multiple branch types. To inspect processor-specific events:

```bash
perf list | grep -i branch
```

Depending on the processor and kernel PMU definitions, events may include:

```text
br_inst_retired.conditional
br_misp_retired.conditional
br_inst_retired.indirect
br_misp_retired.indirect
```

An example command is:

```bash
perf stat \
    -e cycles \
    -e instructions \
    -e branches \
    -e branch-misses \
    -e br_inst_retired.conditional \
    -e br_misp_retired.conditional \
    -e br_inst_retired.indirect \
    -e br_misp_retired.indirect \
    ./branch_predictor_stress indirect 100000000 0 1
```

The exact event names vary across processor generations. Run `perf list` on each system before creating a cross-platform campaign.

### Saving Results

Save counters using comma-separated output:

```bash
mkdir -p perf-results

perf stat -x, \
    -e task-clock,cycles,instructions,branches,branch-misses \
    -o perf-results/random.csv \
    ./branch_predictor_stress random 100000000 0 1
```

Generate one file per mode:

```bash
mkdir -p perf-results

for mode in predictable alternating periodic correlated random array indirect mixed; do
    perf stat -x, \
        -e task-clock,cycles,instructions,branches,branch-misses \
        -o "perf-results/${mode}.csv" \
        ./branch_predictor_stress "$mode" 100000000 0 1
done
```

For CPU-generation comparisons, retain the same executable, mode, iteration count, seed, affinity, and frequency configuration. Compare branch MPKI, branch-misprediction rate, IPC, and cycles per iteration for the same mode on each platform.

## Recommended Comparison Metrics

Collect the following metrics from each simulation:

- Instructions
- Cycles
- IPC
- Conditional branch instructions
- Indirect branch instructions, when available
- Branch mispredictions
- Branch-misprediction rate
- Branch MPKI
- Execution time or simulated cycles

Branch MPKI is calculated as:

```text
Branch MPKI = Branch Mispredictions / Instructions × 1000
```

Branch-misprediction rate is calculated as:

```text
Misprediction Rate = Branch Mispredictions / Branch Instructions × 100
```

For cross-generation comparisons, the most informative quantities are usually:

1. Branch MPKI reduction
2. Misprediction-rate reduction
3. IPC improvement
4. Cycle reduction at a fixed instruction count
5. Improvement relative to the `predictable` baseline

## Suggested Experiment Matrix

| Predictor behavior | Mode |
|---|---|
| Baseline predictable branch | `predictable` |
| Simple local pattern | `alternating` |
| Longer periodic pattern | `periodic` |
| Global-history correlation | `correlated` |
| Unpredictable conditional branch | `random` |
| Pre-generated random outcome | `array` |
| Indirect target prediction | `indirect` |
| Combined branch behavior | `mixed` |

Run every mode on every processor generation being evaluated.

Example result structure:

| Platform | Mode | Instructions | Cycles | IPC | Branch MPKI | Misprediction Rate |
|---|---|---:|---:|---:|---:|---:|
| EMR | correlated | — | — | — | — | — |
| GNR | correlated | — | — | — | — | — |
| DMR | correlated | — | — | — | — | — |

## Reproducibility Guidelines

To obtain comparable results:

- Use the exact same executable on all platforms.
- Keep the seed constant.
- Keep the iteration count constant.
- Use the same affinity configuration.
- Use one active benchmark thread.
- Use the same core and uncore frequencies when the platform models permit it.
- Use the same IWPS instrumentation and region-of-interest configuration.
- Run each mode in a separate simulation.
- Confirm that the compiler did not eliminate the branches.
- Record the IWPS revision and platform configuration.

The benchmark prints a checksum at the end of every run. The checksum prevents the compiler from treating the loop body as unused and can also be used to verify deterministic execution.

## Inspecting the Generated Assembly

Compiler behavior should be checked before launching a large simulation campaign.

Generate assembly:

```bash
gcc -O2 -std=c11 \
    -fno-if-conversion \
    -fno-if-conversion2 \
    -fno-tree-vectorize \
    -fno-unroll-loops \
    -S branch_predictor_stress.c \
    -o branch_predictor_stress.s
```

Inspect conditional and indirect branches:

```bash
grep -E '\b(j[a-z]+|call|jmp)\b' branch_predictor_stress.s
```

Inspect the final executable:

```bash
objdump -d branch_predictor_stress | less
```

The compiler and target ISA can influence the generated branch structure. For a strict generational comparison, compile once for a common ISA baseline and reuse that binary for all IWPS platforms.

## Cleaning

Remove the executable:

```bash
make clean
```

## Notes

This benchmark does not attempt to reproduce the complete control-flow behavior of a production workload. It is a controlled microbenchmark intended to isolate branch-predictor behavior and identify relative changes between simulated CPU generations.

The `random` mode should not be interpreted only as a predictor-quality test because it includes pseudo-random-number generation in the measured instruction stream. The `array` mode provides a useful complementary test because branch outcomes are generated before the measured loop.

The `indirect` mode uses 32 possible targets. This value can be changed at compile time through the `INDIRECT_TARGETS` definition, but the source currently defines and initializes 32 target functions.
