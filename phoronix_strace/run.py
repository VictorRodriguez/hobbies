import os 
import argparse
import re
import subprocess

log_file = "/tmp/log"
libraries = []
binaries = []
yum_conf = "~/clearlinux/projects/common-internal/conf/yum.conf"

benchmark = ""
benchmarks = []

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

def analize():
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

        for lib in libraries:
            print("Benchmark " + benchmark + " call: " + lib)
            whatprovides(lib)

        for binary in binaries:
            print("Benchmark " + benchmark + " call: " + binary)
            whatprovides(binary)

def main():
    global benchmark
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', dest='run_mode', action='store_true')
    parser.add_argument('--analize', dest='analize_mode', action='store_true')
    parser.add_argument('filename')
    args = parser.parse_args()

    if os.path.isfile(args.filename):
        with open(args.filename) as f:
            content = f.readlines()
            for bench in content:
                if bench not in benchmarks:
                    benchmarks.append(bench)

    if args.run_mode:
        for loca_benchmark in benchmarks:
            if os.path.isfile(log_file):
                os.remove(log_file)
            os.environ['EXECUTE_BINARY_PREPEND'] = "strace -o /tmp/log"
            benchmark = loca_benchmark.strip()
            cmd = "phoronix-test-suite batch-run " + benchmark
            os.system(cmd)
            analize()


    if args.analize_mode:
        analize()
if __name__ == "__main__":
    main()
