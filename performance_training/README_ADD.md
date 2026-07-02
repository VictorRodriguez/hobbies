# C VTune Demo: `add.c`

This demo shows how to use **Intel VTune Profiler** from **VS Code + Windows CMD** to analyze a C workload.

The workload performs repeated integer array additions:

```c
c[i] = a[i] + b[i];
```

inside a nested loop. The goal is to create a CPU-intensive workload that can be profiled with VTune.

---

## 1. Demo Directory

Recommended location:

```cmd
C:\Users\vrodri3\OneDrive - Intel Corporation\Documents\dev\hobbies\performance_training\stress_code
```

Go to the directory:

```cmd
cd "C:\Users\vrodri3\OneDrive - Intel Corporation\Documents\dev\hobbies\performance_training\stress_code"
```

---

## 2. C Source Code

Create this file:

```text
add.c
```

Example code:

```c
#define SIZE 100000

int a[SIZE];
int b[SIZE];
int c[SIZE];

int foo() {
    for (int j = 0; j < SIZE; j++) {
        for (int i = 0; i < SIZE; i++) {
            c[i] = a[i] + b[i];
        }
    }

    return 0;
}

int main() {
    int ret;
    ret = foo();
    return ret;
}
```

---

## 3. Initialize Intel oneAPI / VTune

Run this first in **Windows CMD**:

```cmd
"C:\Program Files (x86)\Intel\oneAPI\setvars.bat"
```

Validate VTune:

```cmd
where vtune
vtune --version
```

Validate the VTune GUI:

```cmd
where vtune-gui
```

---

## 4. Build the C Workload

Compile with debug symbols so VTune can map performance data back to source code.

Recommended build:

```cmd
gcc -O2 -g -fno-omit-frame-pointer -o add.exe add.c
```

Alternative aggressive optimization:

```cmd
gcc -O3 -g -fno-omit-frame-pointer -o add.exe add.c
```

Alternative for simple teaching source mapping:

```cmd
gcc -O0 -g -fno-omit-frame-pointer -o add.exe add.c
```

Recommended for this demo:

```cmd
gcc -O2 -g -fno-omit-frame-pointer -o add.exe add.c
```

---

## 5. Run Normally

```cmd
add.exe
```

The program may not print output. That is expected.

---

## 6. VTune Hotspots Analysis

Hotspots analysis answers:

> Where is the program spending most of its CPU time?

Run:

```cmd
vtune -collect hotspots -result-dir vtune-results\add_hotspots -- add.exe
```

Generate a text summary:

```cmd
vtune -report summary -result-dir vtune-results\add_hotspots
```

Generate a hotspots report:

```cmd
vtune -report hotspots -result-dir vtune-results\add_hotspots
```

Open the result in the VTune GUI:

```cmd
vtune-gui vtune-results\add_hotspots
```

Look for:

```text
foo()
main()
add.c source lines
```

---

## 7. VTune Microarchitecture Exploration

Microarchitecture Exploration answers:

> Why is the CPU spending time there?

Run:

```cmd
vtune -collect uarch-exploration -result-dir vtune-results\add_uarch -- add.exe
```

Generate a summary:

```cmd
vtune -report summary -result-dir vtune-results\add_uarch
```

Open the result in the VTune GUI:

```cmd
vtune-gui vtune-results\add_uarch
```

Useful metrics to discuss:

```text
Retiring
Front-End Bound
Back-End Bound
Memory Bound
Bad Speculation
IPC
CPI
```

---

## 8. VTune Memory Access Analysis

Memory Access analysis is useful because the workload repeatedly reads and writes arrays.

Run:

```cmd
vtune -collect memory-access -result-dir vtune-results\add_memory -- add.exe
```

Generate a summary:

```cmd
vtune -report summary -result-dir vtune-results\add_memory
```

Open the result in the VTune GUI:

```cmd
vtune-gui vtune-results\add_memory
```

Useful metrics to discuss:

```text
Loads
Stores
Cache misses
Memory bandwidth
Memory latency
```

---

## 9. VTune HPC Performance Characterization

HPC Performance Characterization gives a high-level view of CPU efficiency.

Run:

```cmd
vtune -collect hpc-performance -result-dir vtune-results\add_hpc -- add.exe
```

Generate a summary:

```cmd
vtune -report summary -result-dir vtune-results\add_hpc
```

Open the result in the VTune GUI:

```cmd
vtune-gui vtune-results\add_hpc
```

Useful metrics to discuss:

```text
CPU utilization
Vectorization
Memory bandwidth
Elapsed time
```

---

## 10. Export Reports to Text

Export summary:

```cmd
vtune -report summary -result-dir vtune-results\add_hotspots > add_hotspots_summary.txt
```

Export hotspots:

```cmd
vtune -report hotspots -result-dir vtune-results\add_hotspots > add_hotspots_report.txt
```

Export microarchitecture summary:

```cmd
vtune -report summary -result-dir vtune-results\add_uarch > add_uarch_summary.txt
```

---

## 11. Clean Old Results

Delete old results before rerunning the same experiment:

```cmd
rmdir /s /q vtune-results\add_hotspots
rmdir /s /q vtune-results\add_uarch
rmdir /s /q vtune-results\add_memory
rmdir /s /q vtune-results\add_hpc
```

---

## 12. Complete Demo Flow

```cmd
"C:\Program Files (x86)\Intel\oneAPI\setvars.bat"

cd "C:\Users\vrodri3\OneDrive - Intel Corporation\Documents\dev\hobbies\performance_training\stress_code"

gcc -O2 -g -fno-omit-frame-pointer -o add.exe add.c

add.exe

vtune -collect hotspots -result-dir vtune-results\add_hotspots -- add.exe

vtune -report summary -result-dir vtune-results\add_hotspots

vtune-gui vtune-results\add_hotspots
```

Then run Microarchitecture Exploration:

```cmd
vtune -collect uarch-exploration -result-dir vtune-results\add_uarch -- add.exe

vtune-gui vtune-results\add_uarch
```

Then run Memory Access:

```cmd
vtune -collect memory-access -result-dir vtune-results\add_memory -- add.exe

vtune-gui vtune-results\add_memory
```

---

## 13. What to Explain During the Demo

### Hotspots

Hotspots tells us:

```text
Where is the program spending CPU time?
```

Useful views:

```text
Top functions
Top source lines
Call stack
CPU time
```

### Microarchitecture Exploration

Microarchitecture Exploration tells us:

```text
Why is the CPU spending time there?
```

Useful metrics:

```text
Retiring
Front-End Bound
Back-End Bound
Memory Bound
Bad Speculation
IPC
CPI
```

### Memory Access

Memory Access tells us:

```text
Is the workload limited by cache or memory behavior?
```

Useful metrics:

```text
Loads
Stores
Cache misses
Memory bandwidth
Memory latency
```

---

## 14. Expected Behavior

For this workload, we expect:

```text
High CPU usage
Hotspot concentrated in foo()
Large number of repeated array operations
Potential memory/cache pressure due to repeated reads and writes
```

If the compiler optimizes the code too aggressively, rebuild with:

```cmd
gcc -O0 -g -fno-omit-frame-pointer -o add.exe add.c
```

For realistic performance behavior, use:

```cmd
gcc -O2 -g -fno-omit-frame-pointer -o add.exe add.c
```
