import csv
import os
from random import seed
from random import randint

tests_files = 'tests.csv'

workload = " oneDNN/build/tests/benchdnn/benchdnn --conv --mode=p --engine=cpu --fix-times-per-prb=TIMES --batch=oneDNN/build/tests/benchdnn/inputs/conv/shapes_resnet_50"

perf_counters= " cycle_activity.cycles_l1d_miss,cycle_activity.cycles_mem_any,inst_retired.any,branch-instructions,branch-misses,cache-misses,cache-references,cycles,instructions,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores"

seed(1)

for _ in range(3):
    rand_value = str(randint(100, 1000))
    cmd = workload.replace("TIMES",rand_value)
    cmd_ = "perf stat -o %s.log -e %s" %( rand_value, perf_counters)
    cmd_ = cmd_ + cmd
    print (cmd_)
    os.system(cmd_)
