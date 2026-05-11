# Java VTune Demo: `AddStress.java`

This demo shows how to use **Intel VTune Profiler** from **VS Code + Windows CMD** to analyze a Java workload.

The workload performs repeated integer array additions:

```java
c[i] = a[i] + b[i];
```

inside a nested loop. The goal is to create a CPU-intensive Java workload that can be profiled with VTune.

---

## 1. Demo Directory

Recommended location:

```cmd
C:\Users\vrodri3\OneDrive - Intel Corporation\Documents\dev\hobbies\performance_training\java_stress
```

Go to the directory:

```cmd
cd "C:\Users\vrodri3\OneDrive - Intel Corporation\Documents\dev\hobbies\performance_training\java_stress"
```

---

## 2. Java Source Code

Create this file:

```text
AddStress.java
```

Example code:

```java
public class AddStress {
    static final int SIZE = 100000;

    static int[] a = new int[SIZE];
    static int[] b = new int[SIZE];
    static int[] c = new int[SIZE];

    static int foo() {
        for (int j = 0; j < SIZE; j++) {
            for (int i = 0; i < SIZE; i++) {
                c[i] = a[i] + b[i];
            }
        }
        return c[SIZE - 1];
    }

    public static void main(String[] args) {
        int ret = foo();
        System.out.println(ret);
    }
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

## 4. Configure the Java JDK

For this machine, the installed JDK is:

```cmd
C:\Program Files\Java\jdk-26.0.1
```

Set the Java environment in the current CMD terminal:

```cmd
set JAVA_HOME=C:\Program Files\Java\jdk-26.0.1
set PATH=%JAVA_HOME%\bin;%PATH%
```

Validate Java:

```cmd
java -version
javac -version
where java
where javac
```

The output should show Java and `javac` from:

```cmd
C:\Program Files\Java\jdk-26.0.1\bin
```

---

## 5. Compile and Run

Compile:

```cmd
javac AddStress.java
```

Run:

```cmd
java AddStress
```

Expected output:

```text
0
```

---

## 6. VTune Hotspots Analysis

Hotspots analysis answers:

> Where is the program spending most of its CPU time?

Run:

```cmd
vtune -collect hotspots -result-dir vtune-results\java_add_hotspots -- java AddStress
```

Generate a text summary:

```cmd
vtune -report summary -result-dir vtune-results\java_add_hotspots
```

Generate a hotspots report:

```cmd
vtune -report hotspots -result-dir vtune-results\java_add_hotspots
```

Open the result in the VTune GUI:

```cmd
vtune-gui vtune-results\java_add_hotspots
```

Look for:

```text
AddStress.foo()
```

or JIT-compiled code related to that method.

---

## 7. VTune Microarchitecture Exploration

Microarchitecture Exploration answers:

> Why is the CPU spending time there?

Run:

```cmd
vtune -collect uarch-exploration -result-dir vtune-results\java_add_uarch -- java AddStress
```

Generate a summary:

```cmd
vtune -report summary -result-dir vtune-results\java_add_uarch
```

Open the result in the VTune GUI:

```cmd
vtune-gui vtune-results\java_add_uarch
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

## 8. Optional: Memory Access Analysis

Use this analysis if you want to inspect cache and memory behavior.

```cmd
vtune -collect memory-access -result-dir vtune-results\java_add_memory -- java AddStress
```

Open the result:

```cmd
vtune-gui vtune-results\java_add_memory
```

Generate a summary:

```cmd
vtune -report summary -result-dir vtune-results\java_add_memory
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

## 9. Clean Old Results

Delete old results before rerunning the same experiment:

```cmd
rmdir /s /q vtune-results\java_add_hotspots
rmdir /s /q vtune-results\java_add_uarch
rmdir /s /q vtune-results\java_add_memory
```

---

## 10. Complete Demo Flow

```cmd
"C:\Program Files (x86)\Intel\oneAPI\setvars.bat"

set JAVA_HOME=C:\Program Files\Java\jdk-26.0.1
set PATH=%JAVA_HOME%\bin;%PATH%

cd "C:\Users\vrodri3\OneDrive - Intel Corporation\Documents\dev\hobbies\performance_training\java_stress"

javac AddStress.java

java AddStress

vtune -collect hotspots -result-dir vtune-results\java_add_hotspots -- java AddStress

vtune -report summary -result-dir vtune-results\java_add_hotspots

vtune-gui vtune-results\java_add_hotspots
```

Then run Microarchitecture Exploration:

```cmd
vtune -collect uarch-exploration -result-dir vtune-results\java_add_uarch -- java AddStress

vtune-gui vtune-results\java_add_uarch
```

---

## 11. What to Explain During the Demo

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

### Java-Specific Note

Java runs through the JVM and JIT compiler. VTune may show:

```text
Java methods
JIT-compiled code
JVM runtime functions
Garbage collection/runtime activity
```

For this demo, the expected hotspot is:

```text
AddStress.foo()
```
