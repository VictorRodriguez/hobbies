import csv
import re
import os
import pandas as pd
import argparse
from random import seed
from random import randint
import matplotlib.pyplot as plt

tests_files = 'tests.csv'

spec_workload  = "docker run --privileged -e BENCHMARK=_BENCH_ -e PLATFORM1=skylake speccpu-2017-v118-gcc-11.1.0-20210510"

perf_counters= " cycle_activity.cycles_l1d_miss,cycle_activity.cycles_mem_any,inst_retired.any,branch-instructions,branch-misses,cache-misses,cache-references,cycles,instructions,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores"

def process_files(files_list):
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

def runner_(test):
        cmd = spec_workload.replace("_BENCH_",test)
        file_name = test
        cmd_ = "perf stat -o %s.log -a -e %s " %(file_name, perf_counters)
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


int_tests_list=["602.gcc_s ",\
"605.mcf_s", \
"620.omnetpp_s", \
"623.xalancbmk_s",\
"625.x264_s",\
"631.deepsjeng_s",\
"641.leela_s",\
"648.exchange2_s",\
"657.xz_s"
]

float_tests_list = ["603.bwaves_s",\
"607.cactuBSSN_s",\
"619.lbm_s",\
"621.wrf_s" ,\
"627.cam4_s" ,\
"628.pop2_s" ,\
"638.imagick_s" ,\
"644.nab_s" ,\
"649.fotonik3d_s" ,\
"654.roms_s"
]

def run_workloads():
    for test in int_tests_list:
        runner_(test)

    for test in float_tests_list:
        runner_(test)
def process_results():
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

#run_workloads()

process_results()
