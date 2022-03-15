import csv
import re
import os
import pandas as pd
import argparse
from random import seed
from random import randint
import matplotlib.pyplot as plt

tests_files = 'tests.csv'

benchdnn_workload = " oneDNN/build/tests/benchdnn/benchdnn --conv --mode=p --engine=cpu --fix-times-per-prb=TIMES --batch=oneDNN/build/tests/benchdnn/inputs/conv/shapes_resnet_50"

perf_counters= " cycle_activity.cycles_l1d_miss,cycle_activity.cycles_mem_any,inst_retired.any,branch-instructions,branch-misses,cache-misses,cache-references,cycles,instructions,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores"

memtier_workload = " memtier_benchmark -t TIMES -R --ratio=1:1"

def process_files(file_list):
    output = pd.DataFrame()
    for filename in files_list:

        metrics_dict = {
            "test_name": "",
            "branch_misses": 0,
            "cache_misses": 0,
            "l1_dcache_load_misses": 0
        }

        with open(filename) as file_:
            lines = file_.readlines()
            for line_ in lines:
                test_name = filename.replace(".log","")
                metrics_dict["test_name"] = test_name
                line = line_.strip()
                if "branch-misses" in line:
                    result = re.search('#(.*)% of', line)
                    metrics_dict["branch_misses"] = float((result.group(1)).strip())
                if "cache-misses" in line:
                    result = re.search('#(.*)% of', line)
                    metrics_dict["cache_misses"] = float((result.group(1)).strip())
                if "L1-dcache-load-misses" in line:
                    result = re.search('#(.*)% of', line)
                    metrics_dict["l1_dcache_load_misses"] = float((result.group(1)).strip())

            print(metrics_dict)
            output = output.append(metrics_dict, ignore_index=True)
    return output

def runner_benchdnn(benchmark,range_limit):
    seed(1)

    for _ in range(range_limit):
        if "benchdnn" in benchmark:
            rand_value = str(randint(100, 1000))
            file_name = "benchdnn_" + rand_value
            cmd = benchdnn_workload.replace("TIMES",rand_value)
        elif "memtier" in benchmark:
            rand_value = str(randint(4, 50))
            file_name = "memtier_" + rand_value
            cmd = memtier_workload.replace("TIMES",rand_value)
        else:
            exit(-1)
        cmd_ = "perf stat -o %s.log -e %s" %(file_name, perf_counters)
        cmd_ = cmd_ + cmd
        print (cmd_)
        os.system(cmd_)


def plot(df, image_file_name):
    df.plot.bar(x="test_name", y=["branch_misses", "cache_misses", "l1_dcache_load_misses"], rot=0)
    plt.title('Workload characterization')
    plt.ylabel('% percentage')
    plt.xlabel('Workloads')
    plt.xticks(rotation='vertical')
    plt.savefig(image_file_name, bbox_inches='tight')

parser = argparse.ArgumentParser()
parser.add_argument('--run')
parser.add_argument('--benchmark')
args = parser.parse_args()

if args.run:
    runner_benchdnn(args.benchmark,int(args.run))
else:

    files_list = []

    for files in os.listdir("."):
        if files.endswith(".log"):
            files_list.append(files)
        else:
            continue
    df = process_files(files_list)
    df_sorted = (df.sort_values(by=['test_name']))
    df_sorted.to_csv('results.csv',index=False)
    plot(df_sorted, "image_file_name.png")
