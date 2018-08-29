import os 
import argparse
import re
import subprocess
import json 
import wget # pip install wget
import csv
from jinja2 import Environment, FileSystemLoader # pip install jinja2
from itertools import islice


log_file = "/tmp/log"
libraries = []
binaries = []
yum_conf = "~/clearlinux/projects/common-internal/conf/yum.conf"

benchmark = ""
benchmarks = []
data = {}

def get_commit(release,pkg):
    blame_log = []
    # get info from : 
    # https://cdn.download.clearlinux.org/releases/24660/clear/RELEASENOTES
    filename = "/tmp/RELEASENOTES-" + str(release)
    if not os.path.isfile(filename):
        url = 'https://cdn.download.clearlinux.org/releases/'+ release+'/clear/RELEASENOTES'
        filename = wget.download(url=url,out=filename)
        print()
    else:
        token = "Changes in package " + (pkg)
        with open(filename) as f:
            content = f.readlines()
            for line in content:
                if token in line:
                    blame_log.append(line.strip())
                    blame_log.append(content[content.index(line)+1].strip().split("-")[0])
    tmp = list(set(blame_log))
    str1 = ''.join(tmp)
    return str1

def generate_results_dir():
    newpath = r'results' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        os.system('mv index.html results/index.html')
    else:
        os.system('mv index.html results/index.html')


def print_html_doc(dictionary_data):
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
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
        lib_count = 0
        bin_count = 0
        with open(log_file) as f:
            content = f.readlines()
            for line in content:
                if "openat" in line or "access" in line:
                    if "/usr/lib" in line and lib_count < 10:
                        m = re.search('<(.+?)>', line)
                        if m:
                            lib = m.group(1)
                            add_lib(lib)
                            lib_count +=1
                    if "/usr/bin" in line and bin_count < 10:
                        m = re.search('/usr/bin/(.+?)"',line)
                        if m:
                            binary = "/usr/bin/" + m.group(1)
                            add_binary(binary)
                            bin_count +=1

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
    global log_file
    data_json = None
    bench = None
    data_json_valid = False
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', dest='run_mode', action='store_true')
    parser.add_argument('--analize', dest='analize_mode', action='store_true')
    parser.add_argument('--report', dest='report_mode', action='store_true')
    parser.add_argument('filename')
    args = parser.parse_args()

    if os.path.isfile(args.filename):
        with open(args.filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0]:
                    bench = row[0]
                if bench not in benchmarks:
                    benchmarks.append(bench)

    cmd = "touch data.json"
    os.system(cmd)

    if os.path.isfile("data.json"):
        with open('data.json') as json_file:
            try:
                data_json = json.load(json_file)
                data_json_valid = True
            except ValueError as e:
                print('invalid json: %s' % e)
                data_json_valid = False

    if args.run_mode:
        for loca_benchmark in benchmarks:
            benchmark = loca_benchmark.strip()
            if data_json:
                if benchmark in data_json:
                    print("Benchmark " + benchmark + " info already in data.json")
            else:
                if os.path.isfile(log_file):
                    os.remove(log_file)
                cmd = "mkdir -p /tmp/logs/"
                os.system(cmd)
                cmd = "rm -rf  /tmp/logs/log*"
                os.system(cmd)
                os.environ['EXECUTE_BINARY_PREPEND'] = "strace -ff -o /tmp/logs/log"
                cmd = "phoronix-test-suite batch-run " + benchmark
                os.system(cmd)
                cmd = "mkdir -p results/"
                os.system(cmd)
                cmd = "cat /tmp/logs/log* > results/%s-strace.log" % (benchmark.replace("/","-"))
                os.system(cmd)
                tmp_log_file = "./results/%s-strace.log" % (benchmark.replace("/","-"))
                if os.path.isfile(tmp_log_file):
                    log_file = tmp_log_file
                else:
                    print("log file not generated")
                analize()
        if data:
            merge_dict = {}
            if os.path.isfile('data.json'):
                if data_json_valid:
                    with open('data.json') as json_file:
                        data_json = json.load(json_file)
                        if data_json:
                            merge_dict = {**data, **data_json}
            if not merge_dict: 
                merge_dict = data
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
        regression_flag = False
        changelog_flag = False
        regression = None
        data_json = None
        if os.path.isfile(args.filename) and os.path.isfile("data.json"):
            with open(args.filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    tmp = {}
                    if row[0]:
                        bench = row[0]
                    if row[1]:
                        regression = row[1]
                    if bench and regression:
                        with open('data.json') as json_file:
                            data_json = json.load(json_file)
                            for k, v in data_json.items():
                                for v_2 in v:
                                    if 'regresion' in v_2:
                                        regression_flag = True
                                        pass
                            if not regression_flag:
                                data_json[bench].append({
                                    'regresion': regression,
                                    })
                                regression_flag = True

                            for element in data_json[bench]:
                                for k, v in element.items():
                                    if k == "changelog":
                                        changelog_flag = True
                                        break
                                if not changelog_flag:
                                    blame_log = None
                                    pkg = None
                                    for k, v in element.items():
                                        if k == "provided by":
                                            pkg = element[k]
                                            blame_log = get_commit(regression,pkg)
                                            if pkg in tmp:
                                                pass
                                            if not blame_log:
                                                pass
                                            else:
                                                tmp[pkg] = blame_log
                                        
                            if not changelog_flag:
                                for k,v in tmp.items():
                                    data_json[bench].append({
                                        'changelog': v,
                                        })
                                changelog_flag_flag = True
            if data_json:
                with open('data.json', 'w') as outfile:
                    json.dump(data_json, outfile)
if __name__ == "__main__":
    main()
