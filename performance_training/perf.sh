#!/bin/bash

sudo perf record -F 99 -a -g ./stress_code/add
perf script | ./FlameGraph/stackcollapse-perf.pl > out.perf-folded
./FlameGraph/flamegraph.pl out.perf-folded > perf-kernel.svg
