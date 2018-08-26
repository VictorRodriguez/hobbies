import os 
import argparse
import re
import subprocess
import json
from jinja2 import Environment, FileSystemLoader

log_file = "/tmp/log"
libraries = []
binaries = []
yum_conf = "~/clearlinux/projects/common-internal/conf/yum.conf"

benchmark = ""
benchmarks = []
data = {}

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_results_dir():
    newpath = r'results' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        os.system('mv index.html results/index.html')
    else:
        os.system('mv index.html results/index.html')


def print_html_doc(dictionary_data):
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    print(j2_env.get_template('test_template.html').render(data=dictionary_data),file=open("index.html","w"))


def add_binary(binary):
    if os.path.isfile(binary):
        if binary not in binaries:
            binaries.append(binary)

def add_lib(lib):
    if os.path.isfile(lib):
        if lib not in libraries:
            libraries.append(lib)

def whatprovides(file_name):

    pkgs = []
    pkg = ""
    yum_log = "/tmp/yum.log"
    cmd = "sudo dnf-3 --releasever=clear "
    cmd = cmd + " --config=/home/clearlinux/projects/common-internal/conf/dnf.conf provides "
    cmd = cmd + file_name
    cmd = cmd + " &> /tmp/yum.log"
    ret = os.system(cmd)
    if (ret):
        cmd = "repoquery -c "
        cmd = cmd + yum_conf
        cmd = cmd + " --whatprovides " + file_name
        cmd = cmd + " &> /tmp/yum.log"
        ret = os.system(cmd)

    if os.path.isfile(yum_log):
        with open(yum_log) as f:
            content = f.readlines()
            for line in content:
                if ".x86_64" in line: 
                    pkg = line.split("-")[0]
                    if pkg not in pkgs:
                        pkgs.append(pkg)

    for pkg in pkgs:
        print("File : " + file_name + " is provided by : " + pkg)
    return pkg

def analize():
    global data
    if os.path.isfile(log_file):
        global libraries
        libraries = []
        global binaries 
        binaries = []
        with open(log_file) as f:
            content = f.readlines()
            for line in content:
                if "openat" in line or "access" in line:
                    if "/usr/lib" in line:
                        m = re.search('<(.+?)>', line)
                        if m:
                            lib = m.group(1)
                            add_lib(lib)
                    if "/usr/bin" in line:
                        m = re.search('/usr/bin/(.+?)"',line)
                        if m:
                            binary = "/usr/bin/" + m.group(1)
                            add_binary(binary)

        data[benchmark] = []
        for lib in libraries:
            print("Benchmark " + benchmark + " call: " + lib)
            pkg = whatprovides(lib)
            if (pkg):
                data[benchmark].append({
                    'lib': lib,
                    'provided by': pkg
                })

        for binary in binaries:
            print("Benchmark " + benchmark + " call: " + binary)
            pkg = whatprovides(binary)
            if (pkg):
                data[benchmark].append({
                    'binary': binary,
                    'provided by': pkg
                })
        if "strace" not in data[benchmark]:
            strace_log = benchmark.replace("/","-") + "-strace.log"
            data[benchmark].append({
                    'strace':strace_log
                    })

def main():
    global benchmark
    data_json = None
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', dest='run_mode', action='store_true')
    parser.add_argument('--analize', dest='analize_mode', action='store_true')
    parser.add_argument('--report', dest='report_mode', action='store_true')
    parser.add_argument('filename')
    args = parser.parse_args()

    if os.path.isfile(args.filename):
        with open(args.filename) as f:
            content = f.readlines()
            for bench in content:
                if bench not in benchmarks:
                    benchmarks.append(bench)

    if os.path.isfile("data.json"):
        with open('data.json') as json_file:
            data_json = json.load(json_file)

    if args.run_mode:
        for loca_benchmark in benchmarks:
            benchmark = loca_benchmark.strip()
            if benchmark in data_json:
                print("Benchmark " + benchmark + " info already in data.json")
            else:
                if os.path.isfile(log_file):
                    os.remove(log_file)
                os.environ['EXECUTE_BINARY_PREPEND'] = "strace -o /tmp/log"
                cmd = "phoronix-test-suite batch-run " + benchmark
                os.system(cmd)
                cmd = "mkdir -p results/"
                os.system(cmd)
                cmd = "cp /tmp/log results/%s-strace.log" % (benchmark.replace("/","-"))
                os.system(cmd)
                analize()
        if data:
            try:
                with open('data.json') as json_file:
                    data_json = json.load(json_file)
                    if data_json:
                        merge_dict = {**data, **data_json}
            except ValueError:
                    pass
            with open('data.json', 'w') as outfile:
                json.dump(merge_dict, outfile)

    if args.report_mode:
        if os.path.isfile("data.json"):
            with open('data.json') as json_file:
                data_json = json.load(json_file)
                print_html_doc(data_json)
            print("index.html generated")
        if os.path.isfile("index.html"):
            newpath = r'results' 
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                os.system('mv index.html results/index.html')
            else:
                os.system('mv index.html results/index.html')

    if args.analize_mode:
        analize()

if __name__ == "__main__":
    main()
