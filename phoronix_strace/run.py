import os 
import argparse
import re
import subprocess

log_file = "/tmp/log"
libraries = []
binaries = []
dnf_conf = "/home/clearlinux/projects/common-internal/conf/dnf.conf"

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
    ndf_log = "/tmp/dnf-3.log"
    cmd = "sudo dnf-3 --releasever=clear "
    cmd = cmd + " --config=/home/clearlinux/projects/common-internal/conf/dnf.conf provides "
    cmd = cmd + file_name
    cmd = cmd + " &> /tmp/dnf-3.log"
    os.system(cmd)

    if os.path.isfile(ndf_log):
        with open(ndf_log) as f:
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
            print("Benchmark call: " + lib)
            whatprovides(lib)

        for binary in binaries:
            print("Benchmark call: " + binary)
            whatprovides(binary)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', dest='run_mode', action='store_true')
    parser.add_argument('--analize', dest='analize_mode', action='store_true')
    args = parser.parse_args()

    if args.run_mode:
        if os.path.isfile(log_file):
            os.remove(log_file)
        os.environ['EXECUTE_BINARY_PREPEND'] = "strace -o /tmp/log"

        benchmark="pts/pybench"
        cmd = "phoronix-test-suite batch-run " + benchmark
        os.system(cmd)
        
        analize()

    if args.analize_mode:
        analize()
if __name__ == "__main__":
    main()
