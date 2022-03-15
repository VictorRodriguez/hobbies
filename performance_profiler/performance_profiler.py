import csv
import re
import os
from random import seed
from random import randint

tests_files = 'tests.csv'

benchdnn_workload = " oneDNN/build/tests/benchdnn/benchdnn --conv --mode=p --engine=cpu --fix-times-per-prb=TIMES --batch=oneDNN/build/tests/benchdnn/inputs/conv/shapes_resnet_50"

perf_counters= " cycle_activity.cycles_l1d_miss,cycle_activity.cycles_mem_any,inst_retired.any,branch-instructions,branch-misses,cache-misses,cache-references,cycles,instructions,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores"


def runner_benchdnn(range_limit):
    seed(1)
    for _ in range(range_limit):
        rand_value = str(randint(100, 1000))
        cmd = workload.replace("TIMES",rand_value)
        file_name = "benchdnn_" + rand_value
        cmd_ = "perf stat -o %s.log -e %s" %(file_name, perf_counters)
        cmd_ = cmd_ + cmd
        print (cmd_)
        os.system(cmd_)



files_list = []

for files in os.listdir("."):
    if files.endswith(".log"):
        files_list.append(files)
    else:
        continue

print(files_list)

for filename in files_list:
    branch_misses = 0
    cache_misses = 0
    l1_dcache_load_misses = 0
    with open(filename) as file_:
        lines = file_.readlines()
        for line_ in lines:
            line = line_.strip()
            if "branch-misses" in line:
                result = re.search('#(.*)% of', line)
                branch_misses = (result.group(1)).strip()
                print(branch_misses)
            if "cache-misses" in line:
                result = re.search('#(.*)% of', line)
                cache_misses = (result.group(1)).strip()
                print(cache_misses)
            if "L1-dcache-load-misses" in line:
                result = re.search('#(.*)% of', line)
                l1_dcache_load_misses = (result.group(1)).strip()
                print(l1_dcache_load_misses)


